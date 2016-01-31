import tempfile

from .region import Region
from .rectangle import Rectangle
from .robot import Robot


class Screen(Region):
    def __init__(self, id_: int):
        x, y, w, h = Robot.screenSize()
        super().__init__(Rectangle(x, y, w, h))
        self.id = id_

    def getNumberScreens(self) -> int:
        return Robot.getNumberScreens()

    def getBounds(self) -> Rectangle:
        return self.getRect()

    def capture(self, rect: Rectangle) -> str:
        fn = tempfile.mktemp(".png")
        img = Robot.capture(rect.getBounds())
        img.save(fn)
        return fn

    def selectRegion(self, text=None) -> Region:
        # FIXME: interactive selection, with label
        pass
