"""
http://doc.sikuli.org/screen.html
"""

import tempfile

from .rectangle import Rectangle
from .region import Region
from .robot import Robot


class Screen(Region):
    def __init__(self, id_: int) -> None:
        x, y, w, h = Robot.screenSize()
        Region.__init__(self, Rectangle(x, y, w, h))
        self.id = id_
        self._screen = self

    @staticmethod
    def getNumberScreens() -> int:
        return Robot.getNumberScreens()

    def getBounds(self) -> Rectangle:
        return self.getRect()

    def capture(self, rect: Rectangle | None) -> str:
        if not rect:
            rect = self.getBounds()
        (_fd, fn) = tempfile.mkstemp(".png")
        img = Robot.capture((int(rect.x), int(rect.y), int(rect.w), int(rect.h)))
        img.save(fn)
        return fn

    def selectRegion(self, text: str | None = None) -> Region:
        # interactive selection, with label
        raise NotImplementedError(
            f"Screen.selectRegion({text!r}) not implemented"
        )  # FIXME
