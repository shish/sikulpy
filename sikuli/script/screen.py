"""
http://doc.sikuli.org/screen.html
"""

import tempfile

from .region import Region
from .rectangle import Rectangle
from .robot import Robot


class Screen(Region):
    def __init__(self, id_: int) -> None:
        x, y, w, h = Robot.screenSize()
        Region.__init__(self, Rectangle(x, y, w, h))
        self.id = id_

    @staticmethod
    def getNumberScreens() -> int:
        return Robot.getNumberScreens()

    def getBounds(self) -> Rectangle:
        return self.getRect()

    def capture(self, rect: Rectangle) -> str:
        if not rect:
            rect = self.getBounds()
        fn = tempfile.mktemp(".png")
        img = Robot.capture((rect.x, rect.y, rect.w, rect.h))
        img.save(fn)
        return fn

    def selectRegion(self, text: str = None) -> Region:
        # interactive selection, with label
        raise NotImplementedError(
            "Screen.selectRegion(%r) not implemented" % text
        )  # FIXME
