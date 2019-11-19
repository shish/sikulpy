"""
http://doc.sikuli.org/region.html
"""

import cv2  # EXT
import numpy as np  # EXT

from time import time, sleep
from enum import Enum
import logging
import warnings
from pprint import pprint

from .settings import Settings
from .rectangle import Rectangle
from .location import Location
from .pattern import Pattern
from .env import Env
from .robot import Mouse, Robot
from .key import KeyModifier
from .sikulpy import unofficial

from .exc import FindFailed

from typing import Union, List, Tuple, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .screen import Screen
    from .match import Match

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

    @unofficial
    def freeze(self) -> None:
        self._frozen = Robot.capture((self.x, self.y, self.w, self.h))

    @unofficial
    def thaw(self) -> None:
        self._frozen = None

    # attributes

    def setAutoWaitTimeout(self, t: float) -> None:
        self.autoWaitTimeout = t

    def getAutoWaitTimeout(self) -> float:
        return self.autoWaitTimeout

    def getScreen(self) -> "Screen":
        return self._screen

    def getLastMatch(self) -> "Match":
        return self.getLastMatches()[0]

    def getLastMatches(self) -> List["Match"]:
        return self._last_matches

    # extending a region

    def _copy(self) -> "Region":
        r = Region(self)
        r._screen = self._screen
        return r

    def offset(self, l: Location) -> "Region":
        r = self._copy()
        r.x += l.x
        r.y += l.y
        return r

    def inside(self) -> "Region":
        return self

    def nearby(self, range_: int = 50) -> "Region":
        r = self._copy()
        r.x -= range_
        r.y -= range_
        r.w += range_ * 2
        r.h += range_ * 2
        return r

    def above(self, range_: int = None) -> "Region":
        if not range_:
            range_ = self.y - self._screen.y
        r = self._copy()
        r.h = range_
        r.y -= range_
        return r

    def below(self, range_: int = None) -> "Region":
        if not range_:
            range_ = self._screen.h - (self.y + self.h)
        r = self._copy()
        r.y += r.h
        r.h = range_
        return r

    def left(self, range_: int = None) -> "Region":
        if not range_:
            range_ = self.x - self._screen.x
        r = self._copy()
        r.w = range_
        r.x -= range_
        return r

    def right(self, range_: int = None) -> "Region":
        if not range_:
            range_ = self._screen.w - (self.x + self.w)
        r = self._copy()
        r.x += r.w
        r.w = range_
        return r

    # finding

    def find(self, target: Union[Pattern, str]) -> "Match":
        return self.findAll(target)[0]

    def findAll(self, target: Union[Pattern, str]) -> List["Match"]:
        if not isinstance(target, Pattern):
            target = Pattern(target)

        region = self._frozen or Robot.capture((self.x, self.y, self.w, self.h))
        matches = []

        from .match import Match

        _start = time()

        if Settings.Channel is None:
            region_img = region.img.convert("L")
            target_img = target.img.img.convert("L")
        else:
            region_img = region.img.split()[Settings.Channel]
            target_img = target.img.img.split()[Settings.Channel]

        if target_img.width > region_img.width or target_img.height > region_img.height:
            raise FindFailed("%r is larger than %r" % (target, self))

        res = cv2.matchTemplate(
            np.array(region_img), np.array(target_img), cv2.TM_CCOEFF_NORMED
        )
        loc = np.where(res >= target.similarity)
        for pt in zip(*loc[::-1]):
            # if there is a better match right next to this one, ignore this one
            x, y = pt
            local_max = np.amax(
                res[max(y - 2, 0) : y + 2, max(x - 2, 0) : x + 2]  # noqa
            )
            if res[pt[1], pt[0]] < local_max:
                continue

            m = Match(
                Rectangle(
                    self.x + int(pt[0]),
                    self.y + int(pt[1]),
                    target_img.width,
                    target_img.height,
                ),
                float(res[pt[1], pt[0]]),
                target.getTargetOffset(),
            )
            m._screen = self._screen
            m._name = target.getFilename()
            matches.append(m)

        matches = list(reversed(sorted(matches)))

        if self._debug:
            pprint(matches)

        log.debug(
            "Searching for %r within %r: %d matches [%.3fs]",
            target,
            region,
            len(matches),
            time() - _start,
        )
        if not matches:
            raise FindFailed("Couldn't find target %r" % target)
        self._last_matches = matches
        return matches

    def wait(self, target: Union[Pattern, str], seconds: float = None) -> "Match":
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            x = self.find(target)
            if x:
                return x
            if time() > until:
                break
            sleep(1)

        raise FindFailed()

    def waitVanish(self, target: Union[Pattern, str], seconds: float = None) -> bool:
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            if not self.find(target):
                return True
            if time() > until:
                break
            sleep(1)
        return False

    def exists(
        self, target: Union[Pattern, str], seconds: float = None
    ) -> Optional["Match"]:
        try:
            return self.wait(target, seconds)
        except FindFailed:
            return None

    # observing

    def onAppear(self, target: Union[Pattern, str], handler):
        warnings.warn(
            "Region.onAppear(%r, %r) not implemented" % (target, handler)
        )  # FIXME

    def onVanish(self, target: Union[Pattern, str], handler):
        warnings.warn(
            "Region.onVanish(%r, %r) not implemented" % (target, handler)
        )  # FIXME

    def onChange(self, target: Union[Pattern, str], handler):
        warnings.warn(
            "Region.onChange(%r, %r) not implemented" % (target, handler)
        )  # FIXME

    def observe(self, seconds: float, background=False):
        warnings.warn(
            "Region.observe(%r, %r) not implemented" % (seconds, background)
        )  # FIXME

    def stopObserver(self) -> None:
        warnings.warn("Region.stopObserver() not implemented")  # FIXME

    # actions

    def _targetOrLast(self, target: Union[Pattern, str]) -> Union[Pattern, str]:
        if not target:
            target = self.getLastMatch()
        return target

    def _toLocation(self, target: Union[Pattern, str]) -> Location:
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

    def mouseMove(
        self, target: Union[Pattern, str], _delay: float = None
    ) -> Tuple[float, float]:
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

    def wheel(self, target: Union[Pattern, str], button, steps=1):
        self.mouseMove(target)
        for _ in range(0, steps):
            self.mouseDown(button)
            sleep(0.1)
            self.mouseUp(button)
            sleep(0.1)

    def click(self, target: Union[Pattern, str] = None, modifiers: int = None) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(Mouse.LEFT)
        sleep(0.1)
        self.mouseUp(Mouse.LEFT)
        return 1  # no. of clicks

    def doubleClick(
        self, target: Union[Pattern, str] = None, modifiers: int = None
    ) -> int:
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

    def rightClick(
        self, target: Union[Pattern, str] = None, modifiers: int = None
    ) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(Mouse.RIGHT)
        sleep(0.1)
        self.mouseUp(Mouse.RIGHT)
        return 1  # no. of clicks

    def highlight(self, seconds: float = None) -> None:
        # FIXME: display rectangle HUD
        pass

    def hover(self, target: Union[Pattern, str] = None) -> None:
        self.mouseMove(target)

    def dragDrop(
        self,
        target1: Union[Pattern, str],
        target2: Union[Pattern, str],
        modifiers: int = None,
    ) -> None:
        self.drag(target1)
        if Settings.DelayBeforeDrag:
            sleep(Settings.DelayBeforeDrag)
        self.dropAt(target2)

    def drag(self, target: Union[Pattern, str] = None) -> None:
        self.mouseMove(target)
        if Settings.DelayBeforeMouseDown:
            sleep(Settings.DelayBeforeMouseDown)
        self.mouseDown(Mouse.LEFT)

    def dropAt(self, target: Union[Pattern, str] = None, delay: float = None) -> None:
        self.mouseMove(target)
        if delay is not None:
            sleep(delay)
        elif Settings.DelayBeforeDrop:
            sleep(Settings.DelayBeforeDrop)
        self.mouseUp(Mouse.LEFT)

    # keyboard

    def keyUp(self, key):
        Robot.keyUp(key)

    def keyDown(self, key):
        Robot.keyDown(key)

    def type(
        self,
        target: Union[Pattern, str] = None,
        text: str = None,
        modifiers: int = None,
    ) -> None:
        if text is None:
            text = target
            target = None

        if target:
            self.click(target)

        Robot.type(text, modifiers)

    def paste(self, target: Union[Pattern, str] = None, text: str = None) -> None:
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
        """
        Env.putClipboard(text)
        self.type(target, "v", KeyModifier.CTRL)

    # OCR

    def text(self) -> str:
        try:
            import pytesseract  # EXT

            pil = Robot.capture((self.x, self.y, self.w, self.h)).img
            cvimg = cv2.cvtColor(np.array(pil.convert("RGB")), cv2.COLOR_RGB2BGR)
            _, cvimg = cv2.threshold(cvimg, 127, 255, cv2.THRESH_BINARY)
            # cvimg = cv.adaptiveThreshold(
            #     img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            #     cv.THRESH_BINARY, 11, 2)
            # cv2.imshow("row", cvimg)
            # img = PILImage.frombytes("L", (cvimg.shape[0], cvimg.shape[1]), cvimg.tostring())
            return pytesseract.image_to_string(cvimg)
        except ImportError:
            raise NotImplementedError("Region.text() requires pytesseract")

    # error handling

    def setFindFailedResponse(self, response):
        # ABORT / SKIP / PROMPT / RETRY
        raise NotImplementedError(
            "Region.setFindFailedResponse(%r) not implemented" % response
        )  # FIXME

    def getFindFailedResponse(self):
        raise NotImplementedError(
            "Region.getFindFailedResponse() not implemented"
        )  # FIXME

    def setThrowException(self, te: bool) -> None:
        self._throwException = te

    def getThrowException(self) -> bool:
        return self._throwException

    # special

    def getRegionFromPSRM(self, target: Union[Pattern, str]) -> "Region":
        raise NotImplementedError(
            "Region.getRegionFromPSRM(%r) not implemented" % target
        )  # FIXME

    def getLocationFromPSRML(self, target: Union[Pattern, str]) -> Location:
        raise NotImplementedError(
            "Region.getLocationFromPSRML(%r) not implemented" % target
        )  # FIXME


class SikuliEvent(object):
    class Type(Enum):
        APPEAR = 0
        VANISH = 1
        CHANGE = 2

    type = Type.APPEAR
    pattern = None  # type: Any
    match = None  # type: Match
    changes = None  # type: List[Match]
