import autopy3 as autopy  # EXT
import pyscreenshot  # EXT
import warnings
from time import sleep
import platform
import subprocess

from .image import Image
from .key import Mouse

import logging
log = logging.getLogger(__name__)
PLATFORM = platform.system()


class Robot(object):
    mouseMap = {
        Mouse.LEFT: autopy.mouse.LEFT_BUTTON,
        Mouse.RIGHT: autopy.mouse.RIGHT_BUTTON,
        Mouse.MIDDLE: autopy.mouse.CENTER_BUTTON,
    }

    # mouse
    @staticmethod
    def mouseMove(xy):
        log.info("mouseMove(%r)", xy)
        autopy.mouse.move(int(xy[0]), int(xy[1]))
        sleep(0.1)

    @staticmethod
    def mouseDown(button):
        # log.info("mouseDown(%r)", button)
        autopy.mouse.toggle(True, Robot.mouseMap[button])

    @staticmethod
    def mouseUp(button):
        # log.info("mouseUp(%r)", button)
        autopy.mouse.toggle(False, Robot.mouseMap[button])

    @staticmethod
    def getMouseLocation() -> (int, int):
        warnings.warn('Robot.getMouseLocation() not implemented')  # FIXME

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
    def getClipboard() -> str:
        warnings.warn('Robot.getClipboard() not implemented')  # FIXME
        return ""

    @staticmethod
    def isLockOn(key) -> bool:
        warnings.warn('Robot.isLockOn(%r) not implemented' % key)  # FIXME
        return False

    # screen
    @staticmethod
    def getNumberScreens() -> int:
        warnings.warn('Robot.getNumberScreens() not implemented')  # FIXME
        return 1

    @staticmethod
    def screenSize() -> (int, int, int, int):
        w, h = autopy.screen.get_size()
        return 0, 0, w, h

    @staticmethod
    def capture(bbox: (int, int, int, int)=None) -> Image:
        from time import time
        _start = time()
        bbox2 = (
            bbox[0], bbox[1],
            bbox[0] + bbox[2], bbox[1] + bbox[3]
        )

        data = pyscreenshot.grab(bbox=bbox2)
        if data.size[0] != bbox[2]:
            # log.debug("Captured image is different size than we expected, shrinking")
            data = data.resize((data.size[0]//2, data.size[1]//2))

        log.info("capture(%r) [%.3fs]", bbox, time() - _start)
        return Image(data)

    # window
    @staticmethod
    def focus(application):
        if PLATFORM == "Darwin":
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
""" % application.encode('ascii')
            subprocess.run("osascript", input=script, shell=True)
        #elif PLATFORM == "Linux":
        #    subprocess.run("xdotool --search %s windowactivate" % application, shell=True)
        else:
            warnings.warn('App.focus(%r) not implemented for %r' % (application, PLATFORM))  # FIXME
