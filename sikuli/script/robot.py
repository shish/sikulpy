import warnings
import platform
import subprocess
from enum import Enum
from time import time
from typing import Tuple

from PIL import Image as PILImage  # EXT

import autopy3 as autopy  # EXT
import mss  # EXT
import pyperclip  # EXT

from .image import Image
from .key import Mouse
from .sikulpy import unofficial


import logging

log = logging.getLogger(__name__)


class Platform(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    DARWIN = "Darwin"


PLATFORM = Platform(platform.system())


class Robot(object):
    autopyMouseMap = {
        Mouse.LEFT: autopy.mouse.LEFT_BUTTON,
        Mouse.RIGHT: autopy.mouse.RIGHT_BUTTON,
        Mouse.MIDDLE: autopy.mouse.CENTER_BUTTON,
    }

    @staticmethod
    def mouseMove(xy: Tuple[int, int]):
        log.info("mouseMove(%r)", xy)
        x, y = int(xy[0]), int(xy[1])

        autopy.mouse.move(x, y)

    @staticmethod
    def mouseDown(button):
        # log.info("mouseDown(%r)", button)
        autopy.mouse.toggle(True, Robot.autopyMouseMap[button])

    @staticmethod
    def mouseUp(button):
        # log.info("mouseUp(%r)", button)
        autopy.mouse.toggle(False, Robot.autopyMouseMap[button])

    @staticmethod
    def getMouseLocation() -> Tuple[int, int]:
        return autopy.mouse.get_pos()

    # keyboard
    @staticmethod
    def keyDown(key):
        log.info("keyDown(%r)", key)
        autopy.key.toggle(key, True)

    @staticmethod
    def keyUp(key):
        log.info("keyUp(%r)", key)
        autopy.key.toggle(key, False)

    @staticmethod
    @unofficial
    def type(text, modifiers):
        log.info("type(%r, %r)", text, modifiers)
        if isinstance(text, int):  # individual keycode
            autopy.key.tap(text, modifiers or 0)
        else:
            for letter in text:
                if letter == "\n":
                    autopy.key.tap(autopy.key.K_RETURN, modifiers or 0)
                else:
                    autopy.key.tap(letter, modifiers or 0)

    @staticmethod
    def getClipboard() -> str:
        return pyperclip.paste()

    @staticmethod
    @unofficial
    def putClipboard(text: str) -> None:
        pyperclip.copy(text)

    @staticmethod
    def isLockOn(key) -> bool:
        warnings.warn("Robot.isLockOn(%r) not implemented" % key)  # FIXME
        return False

    # screen
    @staticmethod
    def getNumberScreens() -> int:
        with mss.mss() as sct:
            return len(sct.monitors) - 1

    @staticmethod
    def screenSize() -> Tuple[int, int, int, int]:
        with mss.mss() as sct:
            return 0, 0, sct.monitors[0]["width"], sct.monitors[0]["height"]

    @staticmethod
    def capture(bbox: Tuple[int, int, int, int] = None) -> Image:
        _start = time()

        with mss.mss() as sct:
            sct_img = sct.grab(
                {"left": bbox[0], "top": bbox[1], "width": bbox[2], "height": bbox[3]}
            )
            data = PILImage.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        if bbox:
            if data.size[0] == bbox[2] * 2:
                log.debug("Captured image is double size, shrinking")
                data = data.resize((data.size[0] // 2, data.size[1] // 2))
            elif data.size[0] != bbox[2]:
                log.warning(
                    "Captured image is different size than we expected (%dx%d vs %dx%d)",
                    data.size[0],
                    data.size[1],
                    bbox[2],
                    bbox[3],
                )

        log.info("capture(%r) [%.3fs]", bbox, time() - _start)
        return Image(data)

    # window
    @staticmethod
    def focus(application: str) -> None:
        if PLATFORM == Platform.DARWIN:
            # FIXME: we don't want to hard-code 'Chrome' as the app, and
            # we want 'window title contains X' rather than 'is X'
            script = b"""
set theTitle to "%s"
tell application "System Events"
    tell process "Chrome"
        set frontmost to true
        perform action "AXRaise" of (windows whose title is theTitle)
    end tell
end tell
""" % application.encode(
                "ascii"
            )
            subprocess.run("osascript", input=script, shell=True)
        elif PLATFORM == Platform.LINUX:
            p = subprocess.Popen(
                "xdotool search --name '%s' windowactivate" % application, shell=True
            )
            p.wait()
        else:
            warnings.warn(
                "App.focus(%r) not implemented for %r" % (application, PLATFORM)
            )  # FIXME
