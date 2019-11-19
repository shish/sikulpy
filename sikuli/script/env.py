import platform

from .location import Location
from .robot import Robot
from .sikulpy import unofficial


class Env(object):
    @staticmethod
    def addHotkey(key, modifiers, handler):
        raise NotImplementedError(
            "Env.addHotKey(%r, %r, %r) not implemented" % (key, modifiers, handler)
        )  # FIXME

    @staticmethod
    def removeHotkey(key, modifiers):
        raise NotImplementedError(
            "Env.removeHotKey(%r, %r) not implemented" % (key, modifiers)
        )  # FIXME

    @staticmethod
    def getOS() -> str:
        # FIXME: check that this matches sikuli's OS names
        return platform.system()

    @staticmethod
    def getOSVersion() -> str:
        raise NotImplementedError("Env.getOSVersion() not implemented")  # FIXME

    @staticmethod
    def getSikuliVersion() -> str:
        return "sikulpy 0.0"

    @staticmethod
    def getClipboard() -> str:
        return Robot.getClipboard()

    @staticmethod
    @unofficial
    def putClipboard(text: str) -> None:
        return Robot.putClipboard(text)

    @staticmethod
    def isLockOn(key: str) -> bool:
        return Robot.isLockOn(key)

    @staticmethod
    def getMouseLocation() -> Location:
        x, y = Robot.getMouseLocation()
        return Location(x, y)
