
from .location import Location


class Env(object):
    def addHotkey(key, modifiers, handler):
        # FIXME
        pass

    def removeHotkey(key, modifiers):
        # FIXME
        pass

    def getOS(self):
        # FIXME
        pass

    def getOSVersion(self):
        # FIXME
        pass

    def getSikuliVersion(self):
        return "py-sikuli 0.0"

    def getClipboard(self):
        # FIXME
        pass

    def isLockOn(self, key) -> bool:
        # FIXME
        pass

    def getMouseLocation(self) -> Location:
        # FIXME
        pass
