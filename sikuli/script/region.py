from time import sleep
from enum import Enum
import logging

#from .match import Match
from .settings import Settings
from .rectangle import Rectangle
from .location import Location

from .exc import FindFailed

log = logging.getLogger(__name__)


class Robot(object):
    def __init__(self):
        pass

    def mouseMove(self, (x, y)):
        log.info("mouseMove((%r, %r))", x, y)

    def mouseDown(self, button):
        log.info("mouseDown(%r)", button)

    def mouseUp(self, button):
        log.info("mouseUp(%r)", button)

    def keyDown(self, key):
        log.info("keyDown(%r)", key)

    def keyUp(self, key):
        log.info("keyUp(%r)", key)


class Region(Rectangle):
    def __init__(self, rect:Rectangle):
        super().__init__()
        self.setRect(rect)

        self._robot = Robot()
        self._screen = None
        self._last_matches = []

        self.autoWaitTimeout = Settings.autoWaitTimeout

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

    def offset(self, l:Location) -> 'Region':
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
            range_ = self.y - self.screen.y
        r = self._copy()
        r.h = range_
        r.y -= range_
        return r

    def below(self, range_=None):
        if not range_:
            range_ = self.screen.h - (self.y + self.h)
        r = self._copy()
        r.y += r.h
        r.h = range_
        return r

    def left(self, range_=None):
        if not range_:
            range_ = self.x - self.screen.x
        r = self._copy()
        r.w = range_
        r.x -= range_
        return r

    def right(self, range_=None):
        if not _range:
            range_ = self.screen.w - (self.x + self.w)
        r = self._copy()
        r.x += r.w
        r.w = range_
        return r

    # finding

    def find(self, target:Pattern) -> 'Match':
        return self.findAll(target)[0]

    def findAll(self, target:Pattern) -> ['Match']:
        matches = []

        # FIXME
        # get screenshot
        # find matches
        # sort by similarity

        if not matches:
            raise FindFailed()
        self._last_matches = matches
        return matches

    def wait(self, target, seconds=0) -> 'Match':
        while seconds >= 0:
            x = self.exists(target)
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
            return self.find(target, seconds)
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
        self.mouseDown(MouseButton.BUTTON_1)
        sleep(0.1)
        self.mouseUp(MouseButton.BUTTON_1)
        return 1  # no. of clicks

    def doubleClick(self, target=None, modifiers=None) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(MouseButton.BUTTON_1)
        sleep(0.1)
        self.mouseUp(MouseButton.BUTTON_1)
        sleep(0.1)
        self.mouseDown(MouseButton.BUTTON_1)
        sleep(0.1)
        self.mouseUp(MouseButton.BUTTON_1)
        return 1  # no. of doubleclicks

    def rightClick(self, target=None, modifiers=None) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(MouseButton.BUTTON_2)
        sleep(0.1)
        self.mouseUp(MouseButton.BUTTON_2)
        return 1  # no. of clicks

    def highlight(self, seconds=None):
        # FIXME: display rectangle HUD
        pass

    def hover(self, target=None):
        self.mouseMove(target)

    def dragDrop(self, target1, target2, modifiers=None):
        self.drag(target1)
        self.dropAt(target2, delay=Settings.DelayAfterDrag + Settings.DelayAfterDrop)  # FIXME: aren't these the same thing?

    def drag(self, target=None):
        self.mouseMove(target)
        self.mouseDown(Mouse.BUTTON_1)

    def dropAt(self, target=None, delay=None):
        self.mouseMove(target)
        if delay:
            sleep(delay)
        self.mouseUp(Mouse.BUTTON_1)

    def type(self, target=None, text=None, modifiers=None):
        target = self._targetOrLast(target)
        # FIXME
        pass

    def paste(self, target=None, text=None, modifiers=None):
        target = self._targetOrLast(target)
        # FIXME
        pass

    # OCR

    def text(self) -> str:
        # FIXME
        pass

    # low-level mouse & keyboard

    def mouseDown(self, button):
        self.robot.mouseDown(button)

    def mouseUp(self, button):
        self.robot.mouseUp(button)

    def mouseMove(self, target):
        loc = self._toLocation(self._targetOrLast(target))
        if Settings.MouseMoveDelay:
            sleep(Settings.MouseMoveDelay)
        self.robot.mouseMove(loc.x, loc.y)

    def wheel(self, target, button, steps=1):
        self.mouseMove(target)
        for n in range(0, steps):
            self.mouseDown(button)
            time.sleep(0.1)
            self.mouseUp(button)
            time.sleep(0.1)

    def keyUp(self, key):
        self.robot.keyUp(key)

    def keyDown(self, key):
        self.roboto.keyDown(key)

    # error handling

    def setFindFailedResponse(self):
        # FIXME
        pass

    def getFindFailedResponse(self):
        # FIXME
        pass

    def setThrowException(self):
        # FIXME
        pass

    def getThrowException(self) -> bool:
        # FIXME
        return True

    # special

    def getRegionFromPSRM(target) -> 'Region':
        # FIXME
        pass

    def getLocationFromPSRML(target) -> Location:
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
