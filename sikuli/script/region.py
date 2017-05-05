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
from .key import KeyModifier
from .sikulpy import unofficial

from .exc import FindFailed

log = logging.getLogger(__name__)


class Region(Rectangle):
    # Constructor can be Region(Rectangle) or Region(x, y, w, h)
    def __init__(self, rect, b=None, c=None, d=None):
        Rectangle.__init__(self)
        if b is not None:
            rect = Rectangle(rect, b, c, d)
        self.setRect(rect)

        self._screen = None
        self._last_matches = []

        self.autoWaitTimeout = Settings.autoWaitTimeout
        self._throwException = True

        # FIXME: unofficial
        self._frozen = None
        self._debug = False
        self._channel = None

    @unofficial
    def freeze(self):
        self._frozen = Robot.capture((self.x, self.y, self.w, self.h))

    @unofficial
    def thaw(self):
        self._frozen = None

    @unofficial
    def setChannel(self, channel):
        self._channel = channel

    # attributes

    def setAutoWaitTimeout(self, t):
        """
        :param float t:
        """
        self.autoWaitTimeout = t

    def getAutoWaitTimeout(self):
        """
        :rtype: float
        """
        return self.autoWaitTimeout

    def getScreen(self):
        """
        :rtype: Screen
        """
        return self._screen

    def getLastMatch(self):
        """
        :rtype: Match
        """
        return self.getLastMatches()[0]

    def getLastMatches(self):
        """
        :rtype: list[Match]
        """
        return self._last_matches

    # extending a region

    def _copy(self):
        """
        :rtype: Region
        """
        r = Region(self)
        r._screen = self._screen
        return r

    def offset(self, l):
        """
        :param Location l:
        :rtype: Region
        """
        r = self._copy()
        r.x += l.x
        r.y += l.y
        return r

    def inside(self):
        """
        :rtype: Region
        """
        return self

    def nearby(self, range_=50):
        """
        :param int range_:
        :rtype: Region
        """
        r = self._copy()
        r.x -= range_
        r.y -= range_
        r.w += range_ * 2
        r.h += range_ * 2
        return r

    def above(self, range_=None):
        """
        :param int range_:
        :rtype: Region
        """
        if not range_:
            range_ = self.y - self._screen.y
        r = self._copy()
        r.h = range_
        r.y -= range_
        return r

    def below(self, range_=None):
        """
        :param int range_:
        :rtype: Region
        """
        if not range_:
            range_ = self._screen.h - (self.y + self.h)
        r = self._copy()
        r.y += r.h
        r.h = range_
        return r

    def left(self, range_=None):
        """
        :param int range_:
        :rtype: Region
        """
        if not range_:
            range_ = self.x - self._screen.x
        r = self._copy()
        r.w = range_
        r.x -= range_
        return r

    def right(self, range_=None):
        """
        :param int range_:
        :rtype: Region
        """
        if not range_:
            range_ = self._screen.w - (self.x + self.w)
        r = self._copy()
        r.x += r.w
        r.w = range_
        return r

    # finding

    def find(self, target):
        """
        :param Pattern|str target:
        :rtype: Match
        """
        return self.findAll(target)[0]

    def findAll(self, target):
        """
        :param Pattern|str target:
        :rtype: list[Match]
        """
        if not isinstance(target, Pattern):
            target = Pattern(target)

        img = self._frozen or Robot.capture((self.x, self.y, self.w, self.h))
        matches = []

        from .match import Match

        _start = time()
        region_img = np.array(img.img.convert('RGB'))
        target_img = np.array(target.img.img.convert('RGB'))

        if self._channel is None:
            region_img = cv2.cvtColor(region_img, cv2.COLOR_BGR2GRAY)
            target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        else:
            # region_img = region_img[:,:,self._channel]
            # target_img = target_img[:,:,self._channel]
            region_img = cv2.split(region_img)[self._channel]
            target_img = cv2.split(target_img)[self._channel]

        _conv = time()
        rw, rh = region_img.shape[::-1]
        tw, th = target_img.shape[::-1]

        if tw > rw or th > rh:
            raise FindFailed("%r is larger than %r" % (target, self))

        res = cv2.matchTemplate(region_img, target_img, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= target.similarity)
        for pt in zip(*loc[::-1]):
            # if there is a better match right next to this one, ignore this one
            local_max = np.amax(res[
                max(pt[1] - 1, 0):pt[1] + 1,
                max(pt[0] - 1, 0):pt[0] + 1
            ])
            if res[pt[1], pt[0]] < local_max:
                continue

            m = Match(
                Rectangle(self.x + int(pt[0]), self.y + int(pt[1]), tw, th),
                float(res[pt[1], pt[0]]),
                target.getTargetOffset()
            )
            m._name = target.getFilename()
            matches.append(m)

        matches = list(reversed(sorted(matches)))

        if self._debug:
            self._display_matches(region_img, matches)
            # cv2.imwrite('img1.png', region_img)
            # cv2.imwrite('img2.png', target_img)
            # cv2.imwrite('img3.png', res * 255)
            # cv2.imwrite('img.png', img_rgb)

        log.debug(
            "Searching for %r within %r: %d matches [%.3fs: %.3fs conv]",
            target, img, len(matches), time() - _start, _conv - _start
        )
        if not matches:
            raise FindFailed()
        self._last_matches = matches
        return matches

    def _display_matches(self, img, matches):
        """
        :param np.array img: 
        :param list[Match] matches: 
        """
        from pprint import pprint
        pprint(matches)

        for m in matches:
            for n in range(4, 0, -1):
                cv2.rectangle(
                    img,
                    m.getTopLeft().getXY(),
                    m.getBottomRight().getXY(),
                    (0, 0, 0) if n % 2 == 0 else (255, 255, 255),
                    n
                )
            cv2.putText(
                img,
                "%.2f" % m.getScore(),
                m.getBottomLeft().getXY(),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

        try:
            cv2.imshow('region', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:  # cv2 build with --no-gui
            cv2.imwrite('region.png', img)

    def wait(self, target, seconds=None):
        """
        :param Pattern|str target:
        :param float seconds:
        :rtype: Match
        """
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            x = self.find(target)
            if x:
                return x
            if time() > until:
                break
            sleep(1)

        raise FindFailed()

    def waitVanish(self, target, seconds=None):
        """
        :param Pattern|str target:
        :param float seconds:
        :rtype: bool
        """
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            if not self.find(target):
                return True
            if time() > until:
                break
            sleep(1)
        return False

    def exists(self, target, seconds=None):
        """
        :param Pattern|str target:
        :param float seconds:
        :rtype: Match
        """
        try:
            return self.wait(target, seconds)
        except FindFailed:
            return None

    # observing

    def onAppear(self, target, handler):
        warnings.warn('Region.onAppear(%r, %r) not implemented' % (
        target, handler))  # FIXME

    def onVanish(self, target, handler):
        warnings.warn('Region.onVanish(%r, %r) not implemented' % (
        target, handler))  # FIXME

    def onChange(self, target, handler):
        warnings.warn('Region.onChange(%r, %r) not implemented' % (
        target, handler))  # FIXME

    def observe(self, seconds, background=False):
        warnings.warn('Region.observe(%r, %r) not implemented' % (
        seconds, background))  # FIXME

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

    # mouse

    def mouseDown(self, button):
        Robot.mouseDown(button)

    def mouseUp(self, button):
        Robot.mouseUp(button)

    def mouseMove(self, target, _delay=None):
        if _delay is None:
            _delay = Settings.MoveMouseDelay
        ticks = 10

        p1 = Location(*Robot.getMouseLocation())
        p2 = self._toLocation(self._targetOrLast(target))
        if _delay > 0:
            for tick in range(0, ticks + 1):
                factor = float(tick) / float(ticks)
                px = p1 + (p2 - p1) * factor
                Robot.mouseMove(px.getXY())
                sleep(_delay / ticks)

        pt = p2.getXY()
        Robot.mouseMove(pt)
        sleep(0.5)
        return pt

    def wheel(self, target, button, steps=1):
        self.mouseMove(target)
        for n in range(0, steps):
            self.mouseDown(button)
            sleep(0.1)
            self.mouseUp(button)
            sleep(0.1)

    def click(self, target=None, modifiers=None):
        """
        :param Pattern|str target:
        :param int modifiers:
        :rtype: int
        """
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(Mouse.LEFT)
        sleep(0.1)
        self.mouseUp(Mouse.LEFT)
        return 1  # no. of clicks

    def doubleClick(self, target=None, modifiers=None):
        """
        :param Pattern|str target:
        :param int modifiers:
        :rtype: int
        """
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

    def rightClick(self, target=None, modifiers=None):
        """
        :param Pattern|str target:
        :param int modifiers:
        :rtype: int
        """
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
        if Settings.DelayBeforeDrag:
            sleep(Settings.DelayBeforeDrag)
        self.dropAt(target2)

    def drag(self, target=None):
        self.mouseMove(target)
        if Settings.DelayBeforeMouseDown:
            sleep(Settings.DelayBeforeMouseDown)
        self.mouseDown(Mouse.LEFT)

    def dropAt(self, target=None, delay=None):
        self.mouseMove(target)
        if Settings.DelayBeforeDrop:
            sleep(Settings.DelayBeforeDrop)
        self.mouseUp(Mouse.LEFT)

    # keyboard

    def keyUp(self, key):
        Robot.keyUp(key)

    def keyDown(self, key):
        Robot.keyDown(key)

    def type(self, target=None, text=None, modifiers=None):
        if target:
            self.click(target)

        Robot.type(text, modifiers)

    def paste(self, target=None, text=None):
        """
        Paste the text at a click point.

        Parameters:
          PSMRL - a pattern, a string, a match, a region or a location that
                  evaluates to a click point.
          modifiers - one or more key modifiers
        Returns:
          the number 1 if the operation could be performed, otherwise 0
          (integer null), which means, that because of some reason, it
          was not possible or the click could be performed (in case of
          PS may be not Found).

        :param target:
        :param text:
        :return:
        """
        Env.putClipboard(text)
        self.type(target, "v", KeyModifier.CTRL)

    # OCR

    def text(self):
        """
        :rtype: str
        """
        warnings.warn('Region.text() not implemented')  # FIXME

    # error handling

    def setFindFailedResponse(self, response):
        # ABORT / SKIP / PROMPT / RETRY
        warnings.warn(
            'Region.setFindFailedResponse(%r) not implemented' % response)  # FIXME

    def getFindFailedResponse(self):
        warnings.warn('Region.getFindFailedResponse() not implemented')  # FIXME

    def setThrowException(self, te):
        """
        :param bool te:
        """
        self._throwException = te

    def getThrowException(self):
        """
        :rtype: bool
        """
        return self._throwException

    # special

    def getRegionFromPSRM(self, target):
        """
        :param Pattern|str target:
        :rtype: Region
        """
        warnings.warn(
            'Region.getRegionFromPSRM(%r) not implemented' % target)  # FIXME

    def getLocationFromPSRML(self, target):
        """
        :param Pattern|str target:
        :rtype: Location
        """
        warnings.warn(
            'Region.getLocationFromPSRML(%r) not implemented' % target)  # FIXME


class SikuliEvent(object):
    class Type(Enum):
        APPEAR = 0
        VANISH = 1
        CHANGE = 2

    type = Type.APPEAR
    pattern = None  # type: Any
    match = None  # type: Match
    changes = None  # type: List[Match]
