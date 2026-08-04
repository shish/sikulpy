from .region import Region
from .robot import Robot


class App:
    @staticmethod
    def open(application: str | None = None) -> "App":
        raise NotImplementedError(f"App.open({application!r}) not implemented")

    @staticmethod
    def focus(application: str | None = None) -> "App":
        assert application is not None
        Robot.focus(application)
        return App()

    @staticmethod
    def close(application: str | None = None) -> None:
        raise NotImplementedError(
            f"App.close({application!r}) not implemented"
        )  # FIXME

    def focusedWindow(self) -> Region:
        raise NotImplementedError("App.focusedWindow() not implemented")  # FIXME

    def window(self, n: int = 0) -> "App":
        raise NotImplementedError(f"App.window({n!r}) not implemented")
