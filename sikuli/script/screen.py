"""
http://doc.sikuli.org/screen.html
"""

import tempfile
import warnings

from .region import Region
from .rectangle import Rectangle
from .robot import Robot


class Screen(Region):
    def __init__(self, id_: int):
        x, y, w, h = Robot.screenSize()
        super().__init__(Rectangle(x, y, w, h))
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
        img = Robot.capture(rect.getBounds())
        img.save(fn)
        return fn

    def selectRegion(self, text=None) -> Region:
        # interactive selection, with label
        warnings.warn('Screen.selectRegion(%r) not implemented' % text)  # FIXME
