import sys
import pyscreenshot  # EXT
import warnings
import platform
import subprocess

if sys.version_info >= (3, 0):
    import autopy3 as autopy  # EXT
else:
    import autopy  # EXT

from .image import Image
from .key import Mouse
from .sikulpy import unofficial

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
        """
        :param (int, int) xy:
        """
        log.info("mouseMove(%r)", xy)
        autopy.mouse.move(int(xy[0]), int(xy[1]))

    @staticmethod
    def mouseDown(button):
        # log.info("mouseDown(%r)", button)
        autopy.mouse.toggle(True, Robot.mouseMap[button])

    @staticmethod
    def mouseUp(button):
        # log.info("mouseUp(%r)", button)
        autopy.mouse.toggle(False, Robot.mouseMap[button])

    @staticmethod
    def getMouseLocation():
        """
        :rtype: (int, int)
        """
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
        for letter in text:
            autopy.key.tap(letter, modifiers or 0)

    @staticmethod
    def getClipboard():
        """
        :rtype: str
        """
        if PLATFORM == "Linux":
            return subprocess.Popen(
                "xclip -o",
                shell=True,
                stdout=subprocess.PIPE
            ).stdout.read().decode("utf8")
        else:
            warnings.warn('Robot.getClipboard() not implemented')  # FIXME
            return ""

    @staticmethod
    @unofficial
    def putClipboard(text):
        """
        :param str text:
        """
        if PLATFORM == "Linux":
            p = subprocess.run(
                "xclip",
                input=text,
                shell=True,
            )
            p.wait()
        else:
            warnings.warn('Robot.putClipboard() not implemented')  # FIXME

    @staticmethod
    def isLockOn(key):
        """
        :param key:
        :rtype: bool
        """
        warnings.warn('Robot.isLockOn(%r) not implemented' % key)  # FIXME
        return False

    # screen
    @staticmethod
    def getNumberScreens():
        """
        :rtype: int
        """
        if PLATFORM == "Linux":
            return 1  # hax for my personal server to not spam warnings...
        else:
            warnings.warn('Robot.getNumberScreens() not implemented')  # FIXME
        return 1

    @staticmethod
    def screenSize():
        """
        :rtype: (int, int, int, int)
        """
        w, h = autopy.screen.get_size()
        return 0, 0, w, h

    @staticmethod
    def capture(bbox=None):
        """
        :param (int, int, int, int) bbox:
        :rtype: Image
        """
        from time import time
        _start = time()
        bbox2 = (
            bbox[0], bbox[1],
            bbox[0] + bbox[2], bbox[1] + bbox[3]
        )

        data = pyscreenshot.grab(bbox=bbox2, childprocess=False)
        if data.size[0] != bbox[2]:
            # log.debug("Captured image is different size than we expected, shrinking")
            data = data.resize((data.size[0]//2, data.size[1]//2))

        log.info("capture(%r) [%.3fs]", bbox, time() - _start)
        return Image(data)

    # window
    @staticmethod
    def focus(application):
        """
        :param str application:
        """
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
        elif PLATFORM == "Linux":
            # subprocess.run(
            #   "xdotool --search %s windowactivate" % application,
            #   shell=True
            # )
            p = subprocess.Popen(
                "xdotool search --name '%s' windowactivate" % application,
                shell=True
            )
            p.wait()
        else:
            warnings.warn('App.focus(%r) not implemented for %r' % (application, PLATFORM))  # FIXME
