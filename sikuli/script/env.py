import platform

from ..version import VERSION
from .location import Location
from .robot import Robot
from .sikulpy import unofficial


class Env:
    @staticmethod
    def addHotkey(key, modifiers, handler):
        raise NotImplementedError(
            f"Env.addHotKey({key!r}, {modifiers!r}, {handler!r}) not implemented"
        )  # FIXME

    @staticmethod
    def removeHotkey(key, modifiers):
        raise NotImplementedError(
            f"Env.removeHotKey({key!r}, {modifiers!r}) not implemented"
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
        return f"sikulpy {VERSION}"

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
