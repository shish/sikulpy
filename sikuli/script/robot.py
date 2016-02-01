import autopy  # EXT
import pyscreenshot  # EXT
import warnings

from .image import Image

import logging
log = logging.getLogger(__name__)


class Key(object):
    A = 1


class KeyModifier(object):
    pass


class Mouse(object):
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3


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
        autopy.mouse.move(xy[0], xy[1])

    @staticmethod
    def mouseDown(button):
        log.info("mouseDown(%r)", button)
        autopy.mouse.toggle(True, Robot.mouseMap[button])

    @staticmethod
    def mouseUp(button):
        log.info("mouseUp(%r)", button)
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
        log.info("capture(%r)", bbox)
        bbox2 = (
            bbox[0], bbox[1],
            bbox[0] + bbox[2], bbox[1] + bbox[3]
        )

        #data = autopy.bitmap.capture_screen(bbox)
        data = pyscreenshot.grab(bbox=bbox2)
        if data.size[0] != bbox[2]:
            log.debug("Captured image is different size than we expected, shrinking")
            data = data.resize((data.size[0]//2, data.size[1]//2))
        #log.info("capture(%r) -> %r", bbox2, data.size)

        return Image(data)