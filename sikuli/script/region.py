from time import sleep
from enum import Enum
import logging

from .settings import Settings
from .rectangle import Rectangle
from .location import Location
from .pattern import Pattern
from .env import Env
from .robot import Mouse, Key, Robot

from .exc import FindFailed

log = logging.getLogger(__name__)


class Region(Rectangle):
    def __init__(self, rect: Rectangle):
        super().__init__()
        self.setRect(rect)

        self._screen = None
        self._last_matches = []

        self.autoWaitTimeout = Settings.autoWaitTimeout
        self._throwException = True

    # attributes

    def setAutoWaitTimeout(self, t:float):
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

        img = Robot.capture((self.x, self.y, self.w, self.h))
        log.info("Searching for %r within %r", target, img)
        matches = []

        from .match import Match

        import cv2  # EXT
        import numpy as np  # EXT

        img_rgb = np.array(img.img.convert('RGB'))
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

        #template = cv2.imread(target, 0)
        template = np.array(target.img.img.convert('RGB'))
        template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # FIXME: use specified threshold
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            matches.append(
                Match(
                    Rectangle(int(pt[0]), int(pt[1]), w, h),
                    threshold,  # FIXME: use actual similarity value
                    # FIXME: pass target.targetOffset?
                )
            )

        matches = list(reversed(sorted(matches)))

        if not matches:
            raise FindFailed()
        self._last_matches = matches
        return matches

    def wait(self, target, seconds=None) -> 'Match':
        if seconds is None:
            seconds = self.autoWaitTimeout
        while seconds >= 0:
            x = self.find(target)
            if x:
                return x
            sleep(1)
            seconds -= 1

        raise FindFailed()

    def waitVanish(self, target, seconds=None) -> bool:
        # FIXME
        return False

    def exists(self, target, seconds=None) -> 'Match':
        try:
            return self.wait(target, seconds)
        except FindFailed:
            return None

    # observing

    def onAppear(self, target, handler):
        # FIXME
        pass

    def onVanish(self, target, handler):
        # FIXME
        pass

    def onChange(self, target, handler):
        # FIXME
        pass

    def observe(self, seconds, background=False):
        # FIXME
        pass

    def stopObserver(self):
        # FIXME
        pass

    # actions

    def _targetOrLast(self, target):
        if not target:
            target = self.getLastMatch()
        return target

    def _toLocation(self, target):
        if isinstance(target, str):
            target = Pattern(str)
        if isinstance(target, Pattern):
            target = self.find(target)
        if isinstance(target, Rectangle):  # Includes Match and Region
            target = target.getCenter()
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
        # FIXME
        pass

    def paste(self, target=None, text=None, modifiers=None):
        self.click(target)
        self.type(Env.getClipboard())

    # OCR

    def text(self) -> str:
        # FIXME
        pass

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

    def setFindFailedResponse(self):
        # FIXME
        pass

    def getFindFailedResponse(self):
        # FIXME
        pass

    def setThrowException(self, te: bool):
        self._throwException = te

    def getThrowException(self) -> bool:
        return self._throwException

    # special

    def getRegionFromPSRM(self, target) -> 'Region':
        # FIXME
        pass

    def getLocationFromPSRML(self, target) -> Location:
        # FIXME
        pass


class SikuliEvent(object):
    class Type(Enum):
        APPEAR = 0
        VANISH = 1
        CHANGE = 2

    type = Type.APPEAR
    pattern = None
    match = None
    changes = None
