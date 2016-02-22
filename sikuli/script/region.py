"""
http://doc.sikuli.org/region.html
"""

import cv2  # EXT
import numpy as np  # EXT

from time import time, sleep
from enum import Enum
import logging
import warnings

from .settings import Settings
from .rectangle import Rectangle
from .location import Location
from .pattern import Pattern
from .env import Env
from .robot import Mouse, Robot

from .exc import FindFailed

log = logging.getLogger(__name__)


class Region(Rectangle):
    # Constructor can be Region(Rectangle) or Region(x, y, w, h)
    def __init__(self, rect, b=None, c=None, d=None):
        if b is not None:
            rect = Rectangle(rect, b, c, d)
        super().__init__()
        self.setRect(rect)

        self._screen = None
        self._last_matches = []

        self.autoWaitTimeout = Settings.autoWaitTimeout
        self._throwException = True

        # FIXME: unofficial
        self.recycle_capture = False
        self._last_capture = None
        self._debug = False

    # attributes

    def setAutoWaitTimeout(self, t: float):
        self.autoWaitTimeout = t

    def getAutoWaitTimeout(self) -> float:
        return self.autoWaitTimeout

    def getScreen(self) -> 'Screen':
        return self._screen

    def getLastMatch(self) -> 'Match':
        return self.getLastMatches()[0]

    def getLastMatches(self) -> ['Match']:
        return self._last_matches

    # extending a region

    def _copy(self):
        r = Region(self)
        r._screen = self._screen
        return r

    def offset(self, l: Location) -> 'Region':
        r = self._copy()
        r.x += l.x
        r.y += l.y
        return r

    def inside(self):
        return self

    def nearby(self, range_=50):
        r = self._copy()
        r.x -= range_
        r.y -= range_
        r.w += range_ * 2
        r.h += range_ * 2
        return r

    def above(self, range_=None):
        if not range_:
            range_ = self.y - self._screen.y
        r = self._copy()
        r.h = range_
        r.y -= range_
        return r

    def below(self, range_=None):
        if not range_:
            range_ = self._screen.h - (self.y + self.h)
        r = self._copy()
        r.y += r.h
        r.h = range_
        return r

    def left(self, range_=None):
        if not range_:
            range_ = self.x - self._screen.x
        r = self._copy()
        r.w = range_
        r.x -= range_
        return r

    def right(self, range_=None):
        if not range_:
            range_ = self._screen.w - (self.x + self.w)
        r = self._copy()
        r.x += r.w
        r.w = range_
        return r

    # finding

    def find(self, target) -> 'Match':
        return self.findAll(target)[0]

    def findAll(self, target) -> ['Match']:
        if not isinstance(target, Pattern):
            target = Pattern(target)

        if self.recycle_capture and self._last_capture:
            log.debug("Recycling capture")
            img = self._last_capture
            self.recycle_capture = False
        else:
            img = Robot.capture((self.x, self.y, self.w, self.h))
            self._last_capture = img
        matches = []

        from .match import Match

        _start = time()
        region_img = np.array(img.img.convert('RGB'))
        region_img = cv2.cvtColor(region_img, cv2.COLOR_BGR2GRAY)

        target_img = np.array(target.img.img.convert('RGB'))
        target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        tw, th = target_img.shape[::-1]

        res = cv2.matchTemplate(region_img, target_img, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= target.similarity)
        for pt in zip(*loc[::-1]):
            # if there is a better match right next to this one, ignore this one
            found_better = False
            for x in [-1, 0, +1]:
                for y in [-1, 0, +1]:
                    try:
                        if res[pt[1]+y, pt[0]+x] > res[pt[1], pt[0]]:
                            found_better = True
                    except IndexError:
                        pass
            if found_better:
                continue

            m = Match(
                Rectangle(self.x + int(pt[0]), self.y + int(pt[1]), tw, th),
                float(res[pt[1], pt[0]]),
                target.getTargetOffset()
            )
            m._name = target.getFilename()
            matches.append(m)

            bl = (0, 0, 0)
            wh = (255, 255, 255)
            cv2.rectangle(region_img, pt, (pt[0] + tw, pt[1] + th), bl, 4)
            cv2.rectangle(region_img, pt, (pt[0] + tw, pt[1] + th), wh, 3)
            cv2.rectangle(region_img, pt, (pt[0] + tw, pt[1] + th), bl, 2)
            cv2.rectangle(region_img, pt, (pt[0] + tw, pt[1] + th), wh, 1)
            cv2.putText(region_img, "%.3f" % m.getScore(), (pt[0], pt[1] + th),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, bl, 2, cv2.LINE_AA)

        matches = list(reversed(sorted(matches)))

        from pprint import pprint
        if self._debug and matches:
            pprint(matches)
            cv2.imshow('region', region_img)
            # cv2.imshow('target', target_img)
            # cv2.imshow('matches', res)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # cv2.imwrite('img1.png', region_img)
        # cv2.imwrite('img2.png', target_img)
        # cv2.imwrite('img3.png', res * 255)
        # cv2.imwrite('img.png', img_rgb)

        log.debug(
            "Searching for %r within %r: %d matches [%.3fs]",
            target, img, len(matches), time() - _start
        )
        if not matches:
            raise FindFailed()
        self._last_matches = matches
        return matches

    def wait(self, target, seconds=None) -> 'Match':
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            x = self.find(target)
            if x:
                return x
            if time() > until:
                break
            sleep(1)

        raise FindFailed()

    def waitVanish(self, target, seconds=None) -> bool:
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            if not self.find(target):
                return True
            if time() > until:
                break
            sleep(1)
        return False

    def exists(self, target, seconds=None) -> 'Match':
        try:
            return self.wait(target, seconds)
        except FindFailed:
            return None

    # observing

    def onAppear(self, target, handler):
        warnings.warn('Region.onAppear(%r, %r) not implemented' % (target, handler))  # FIXME

    def onVanish(self, target, handler):
        warnings.warn('Region.onVanish(%r, %r) not implemented' % (target, handler))  # FIXME

    def onChange(self, target, handler):
        warnings.warn('Region.onChange(%r, %r) not implemented' % (target, handler))  # FIXME

    def observe(self, seconds, background=False):
        warnings.warn('Region.observe(%r, %r) not implemented' % (seconds, background))  # FIXME

    def stopObserver(self):
        warnings.warn('Region.stopObserver() not implemented')  # FIXME

    # actions

    def _targetOrLast(self, target):
        if not target:
            target = self.getLastMatch()
        return target

    def _toLocation(self, target):
        if isinstance(target, str):
            target = Pattern(target)
        if isinstance(target, Pattern):
            target = self.find(target)
        if isinstance(target, Rectangle):  # Includes Match and Region
            target = target.getTarget()
        if isinstance(target, Location):
            return target

    def click(self, target=None, modifiers=None) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        sleep(1)
        self.mouseDown(Mouse.LEFT)
        sleep(0.1)
        self.mouseUp(Mouse.LEFT)
        return 1  # no. of clicks

    def doubleClick(self, target=None, modifiers=None) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(Mouse.LEFT)
        sleep(0.1)
        self.mouseUp(Mouse.LEFT)
        sleep(0.1)
        self.mouseDown(Mouse.LEFT)
        sleep(0.1)
        self.mouseUp(Mouse.LEFT)
        return 1  # no. of double clicks

    def rightClick(self, target=None, modifiers=None) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(Mouse.RIGHT)
        sleep(0.1)
        self.mouseUp(Mouse.RIGHT)
        return 1  # no. of clicks

    def highlight(self, seconds=None):
        # FIXME: display rectangle HUD
        pass

    def hover(self, target=None):
        self.mouseMove(target)

    def dragDrop(self, target1, target2, modifiers=None):
        self.drag(target1)
        # FIXME: aren't these the same thing?
        self.dropAt(target2, delay=Settings.DelayAfterDrag + Settings.DelayBeforeDrop)

    def drag(self, target=None):
        self.mouseMove(target)
        self.mouseDown(Mouse.LEFT)

    def dropAt(self, target=None, delay=None):
        self.mouseMove(target)
        if delay:
            sleep(delay)
        self.mouseUp(Mouse.LEFT)

    def type(self, target=None, text=None, modifiers=None):
        target = self._targetOrLast(target)
        warnings.warn('Region.type(%r, %r, %r) not implemented' % (target, text, modifiers))  # FIXME

    def paste(self, target=None, text=None, modifiers=None):
        self.click(target)
        self.type(Env.getClipboard())

    # OCR

    def text(self) -> str:
        warnings.warn('Region.text() not implemented')  # FIXME

    # low-level mouse & keyboard

    def mouseDown(self, button):
        Robot.mouseDown(button)

    def mouseUp(self, button):
        Robot.mouseUp(button)

    def mouseMove(self, target):
        loc = self._toLocation(self._targetOrLast(target))
        if Settings.MouseMoveDelay:
            sleep(Settings.MouseMoveDelay)
        Robot.mouseMove((loc.x, loc.y))

    def wheel(self, target, button, steps=1):
        self.mouseMove(target)
        for n in range(0, steps):
            self.mouseDown(button)
            sleep(0.1)
            self.mouseUp(button)
            sleep(0.1)

    def keyUp(self, key):
        Robot.keyUp(key)

    def keyDown(self, key):
        Robot.keyDown(key)

    # error handling

    def setFindFailedResponse(self, response):
        # ABORT / SKIP / PROMPT / RETRY
        warnings.warn('Region.setFindFailedResponse(%r) not implemented' % response)  # FIXME

    def getFindFailedResponse(self):
        warnings.warn('Region.getFindFailedResponse() not implemented')  # FIXME

    def setThrowException(self, te: bool):
        self._throwException = te

    def getThrowException(self) -> bool:
        return self._throwException

    # special

    def getRegionFromPSRM(self, target) -> 'Region':
        warnings.warn('Region.getRegionFromPSRM(%r) not implemented' % target)  # FIXME

    def getLocationFromPSRML(self, target) -> Location:
        warnings.warn('Region.getLocationFromPSRML(%r) not implemented' % target)  # FIXME


class SikuliEvent(object):
    class Type(Enum):
        APPEAR = 0
        VANISH = 1
        CHANGE = 2

    type = Type.APPEAR
    pattern = None
    match = None
    changes = None
