"""
http://doc.sikuli.org/region.html
"""

import logging
import typing as t
from enum import Enum
from pprint import pprint
from time import sleep, time

import cv2  # EXT
import numpy as np  # EXT

from .env import Env
from .exc import FindFailed
from .key import KeyModifier
from .location import Location
from .pattern import Pattern
from .rectangle import Rectangle
from .robot import Mouse, Robot
from .settings import Settings
from .sikulpy import unofficial

if t.TYPE_CHECKING:
    from .match import Match
    from .screen import Screen

log = logging.getLogger(__name__)


class Region(Rectangle):
    @t.overload
    def __init__(self, x: Rectangle) -> None: ...
    @t.overload
    def __init__(self, x: float, y: float, w: float, h: float) -> None: ...
    def __init__(
        self,
        x: Rectangle | float,
        y: float | None = None,
        w: float | None = None,
        h: float | None = None,
    ):
        Rectangle.__init__(self)
        if isinstance(x, Rectangle):
            rect = x
        else:
            assert y is not None and w is not None and h is not None
            rect = Rectangle(x, y, w, h)
        self.setRect(rect)

        # Screen.__init__ will set this, so that any regions created
        # from this region will inherit the root screen. Unsure what
        # we're supposed to do if somebody creates a region in the
        # void like `r = Region(0, 0, 10, 10)`...
        self._screen: Screen = None  # type: ignore
        self._last_matches = []

        self.autoWaitTimeout = Settings.autoWaitTimeout
        self._throwException = True

        # FIXME: unofficial
        self._frozen = None
        self._debug = False

    @unofficial
    def freeze(self) -> None:
        self._frozen = Robot.capture(
            (int(self.x), int(self.y), int(self.w), int(self.h))
        )

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

    def getLastMatches(self) -> list["Match"]:
        return self._last_matches

    # extending a region

    def _copy(self) -> "Region":
        r = Region(self)
        r._screen = self._screen
        return r

    def offset(self, location: Location) -> "Region":
        r = self._copy()
        r.x += location.x
        r.y += location.y
        return r

    def inside(self) -> "Region":
        return self

    def nearby(self, range_: float = 50) -> "Region":
        r = self._copy()
        r.x -= range_
        r.y -= range_
        r.w += range_ * 2
        r.h += range_ * 2
        return r

    def above(self, range_: float | None = None) -> "Region":
        if range_ is None:
            range_ = self.y - self._screen.y
        r = self._copy()
        r.h = range_
        r.y -= range_
        return r

    def below(self, range_: float | None = None) -> "Region":
        if range_ is None:
            range_ = self._screen.h - (self.y + self.h)
        r = self._copy()
        r.y += r.h
        r.h = range_
        return r

    def left(self, range_: float | None = None) -> "Region":
        if range_ is None:
            range_ = self.x - self._screen.x
        r = self._copy()
        r.w = range_
        r.x -= range_
        return r

    def right(self, range_: float | None = None) -> "Region":
        if range_ is None:
            range_ = self._screen.w - (self.x + self.w)
        r = self._copy()
        r.x += r.w
        r.w = range_
        return r

    # finding

    def find(self, target: Pattern | str) -> "Match":
        return self.findAll(target)[0]

    def findAll(self, target: Pattern | str) -> list["Match"]:
        if not isinstance(target, Pattern):
            target = Pattern(target)

        region = self._frozen or Robot.capture(
            (int(self.x), int(self.y), int(self.w), int(self.h))
        )
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
            raise FindFailed(f"{target!r} is larger than {self!r}")

        res = cv2.matchTemplate(
            np.array(region_img), np.array(target_img), cv2.TM_CCOEFF_NORMED
        )
        loc = np.where(res >= target.similarity)
        for pt in zip(*loc[::-1]):
            # if there is a better match right next to this one, ignore this one
            x, y = pt
            local_max = np.amax(res[max(y - 2, 0) : y + 2, max(x - 2, 0) : x + 2])
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

        matches = sorted(matches, reverse=True)

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
            raise FindFailed(f"Couldn't find target {target!r}")
        self._last_matches = matches
        return matches

    def wait(self, target: Pattern | str, seconds: float | None = None) -> "Match":
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            x = self.find(target)
            if x:
                return x
            if time() > until:
                break
            sleep(1)

        raise FindFailed()

    def waitVanish(self, target: Pattern | str, seconds: float | None = None) -> bool:
        until = time() + (seconds or self.autoWaitTimeout)
        while True:
            if not self.find(target):
                return True
            if time() > until:
                break
            sleep(1)
        return False

    def exists(
        self, target: Pattern | str, seconds: float | None = None
    ) -> t.Optional["Match"]:
        try:
            return self.wait(target, seconds)
        except FindFailed:
            return None

    # observing

    def onAppear(self, target: Pattern | str, handler):
        raise NotImplementedError(
            f"Region.onAppear({target!r}, {handler!r}) not implemented"
        )  # FIXME

    def onVanish(self, target: Pattern | str, handler):
        raise NotImplementedError(
            f"Region.onVanish({target!r}, {handler!r}) not implemented"
        )  # FIXME

    def onChange(self, target: Pattern | str, handler):
        raise NotImplementedError(
            f"Region.onChange({target!r}, {handler!r}) not implemented"
        )  # FIXME

    def observe(self, seconds: float, background=False):
        raise NotImplementedError(
            f"Region.observe({seconds!r}, {background!r}) not implemented"
        )  # FIXME

    def stopObserver(self) -> None:
        raise NotImplementedError("Region.stopObserver() not implemented")  # FIXME

    # actions

    def _targetOrLast(
        self, target: Pattern | str | None
    ) -> t.Union[Pattern, str, "Match"]:
        if target is None:
            return self.getLastMatch()
        return target

    def _toLocation(self, target: Pattern | str | Rectangle | Location) -> Location:
        if isinstance(target, str):
            target = Pattern(target)
        if isinstance(target, Pattern):
            target = self.find(target)
        if isinstance(target, Rectangle):  # Includes Match and Region
            target = target.getTarget()
        if isinstance(target, Location):
            return target
        raise ValueError(f"Invalid target {target!r}")

    # mouse

    def mouseDown(self, button):
        Robot.mouseDown(button)

    def mouseUp(self, button):
        Robot.mouseUp(button)

    def mouseMove(
        self,
        target: Pattern | str | None,
        _delay: float | None = None,
    ) -> tuple[float, float]:
        if _delay is None:
            _delay = Settings.MoveMouseDelay
        ticks = 10

        p1 = Location(*Robot.getMouseLocation())
        p2 = self._toLocation(self._targetOrLast(target))
        if _delay > 0:
            for tick in range(ticks + 1):
                factor = float(tick) / float(ticks)
                px = p1 + (p2 - p1) * factor
                pxx, pxy = px.getXY()
                Robot.mouseMove((int(pxx), int(pxy)))
                sleep(_delay / ticks)

        ptx, pty = p2.getXY()
        Robot.mouseMove((int(ptx), int(pty)))
        sleep(0.5)
        return (ptx, pty)

    def wheel(self, target: Pattern | str | None, button, steps=1):
        self.mouseMove(target)
        for _ in range(steps):
            self.mouseDown(button)
            sleep(0.1)
            self.mouseUp(button)
            sleep(0.1)

    def click(
        self,
        target: Pattern | str | None = None,
        modifiers: int | None = None,
    ) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(Mouse.LEFT)
        sleep(0.1)
        self.mouseUp(Mouse.LEFT)
        return 1  # no. of clicks

    def doubleClick(
        self,
        target: Pattern | str | None = None,
        modifiers: int | None = None,
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
        self,
        target: Pattern | str | None = None,
        modifiers: int | None = None,
    ) -> int:
        # FIXME: modifiers
        self.mouseMove(target)
        self.mouseDown(Mouse.RIGHT)
        sleep(0.1)
        self.mouseUp(Mouse.RIGHT)
        return 1  # no. of clicks

    def highlight(self, seconds: float | None = None) -> None:
        # FIXME: display rectangle HUD
        pass

    def hover(self, target: Pattern | str | None = None) -> None:
        self.mouseMove(target)

    def dragDrop(
        self,
        target1: Pattern | str,
        target2: Pattern | str,
        modifiers: int | None = None,
    ) -> None:
        self.drag(target1)
        if Settings.DelayBeforeDrag:
            sleep(Settings.DelayBeforeDrag)
        self.dropAt(target2)

    def drag(self, target: Pattern | str | None = None) -> None:
        self.mouseMove(target)
        if Settings.DelayBeforeMouseDown:
            sleep(Settings.DelayBeforeMouseDown)
        self.mouseDown(Mouse.LEFT)

    def dropAt(
        self,
        target: Pattern | str | None = None,
        delay: float | None = None,
    ) -> None:
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
        a: Pattern | str | None = None,
        b: str | None = None,
        modifiers: int | None = None,
    ) -> None:
        target: Pattern | str | None = None
        text: str | None = None

        if a is not None and b is not None:
            target = a
            text = b
        if b is None and isinstance(a, str):
            text = a
            target = None

        if target is not None:
            self.click(target)

        Robot.type(text, modifiers)

    def paste(
        self,
        target: Pattern | str | None = None,
        text: str | None = None,
    ) -> None:
        """
        Paste the text at a click point.

        Parameters:
          PSMRL - a pattern, a string, a match, a region or a location that
                  evaluates to a click point.
          text - the text to paste at the click point.
        """
        assert text is not None
        Env.putClipboard(text)
        self.type(target, "v", KeyModifier.CTRL)

    # OCR

    def text(self) -> str:
        try:
            import pytesseract  # EXT  # type: ignore

            pil = Robot.capture(
                (int(self.x), int(self.y), int(self.w), int(self.h))
            ).img
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
            f"Region.setFindFailedResponse({response}) not implemented"
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

    def getRegionFromPSRM(self, target: Pattern | str) -> "Region":
        raise NotImplementedError(
            f"Region.getRegionFromPSRM({target!r}) not implemented"
        )  # FIXME

    def getLocationFromPSRML(self, target: Pattern | str) -> Location:
        raise NotImplementedError(
            f"Region.getLocationFromPSRML({target}) not implemented"
        )  # FIXME


class SikuliEvent:
    class Type(Enum):
        APPEAR = 0
        VANISH = 1
        CHANGE = 2

    type = Type.APPEAR
    pattern: t.Any | None = None
    match: t.Optional["Match"] = None
    changes: list["Match"] | None = None
