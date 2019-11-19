from .region import Region
from .robot import Robot


class App(object):
    @staticmethod
    def open(application: str = None) -> "App":
        raise NotImplementedError("App.open(%r) not implemented" % application)  # FIXME

    @staticmethod
    def focus(application: str = None) -> "App":
        Robot.focus(application)

    @staticmethod
    def close(application: str = None) -> None:
        raise NotImplementedError(
            "App.close(%r) not implemented" % application
        )  # FIXME

    def focusedWindow(self) -> Region:
        raise NotImplementedError("App.focusedWindow() not implemented")  # FIXME

    def window(self, n: int = 0) -> "App":
        raise NotImplementedError("App.window(%r) not implemented" % n)  # FIXME
