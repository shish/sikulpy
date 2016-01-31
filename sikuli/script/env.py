import platform

from .location import Location
from .robot import Robot


class Env(object):
    @staticmethod
    def addHotkey(key, modifiers, handler):
        # FIXME
        pass

    @staticmethod
    def removeHotkey(key, modifiers):
        # FIXME
        pass

    @staticmethod
    def getOS():
        # FIXME: check that this matches sikuli's OS names
        return platform.system()

    @staticmethod
    def getOSVersion():
        # FIXME
        pass

    @staticmethod
    def getSikuliVersion():
        return "py-sikuli 0.0"

    @staticmethod
    def getClipboard():
        return Robot.getClipboard()

    @staticmethod
    def isLockOn(key) -> bool:
        return Robot.isLockOn(key)

    @staticmethod
    def getMouseLocation() -> Location:
        x, y = Robot.getMouseLocation()
        return Location(x, y)
