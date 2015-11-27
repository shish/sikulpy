from .region import Region
from .rectangle import Rectangle


class Screen(Region):
    def __init__(self, id: int):
        super().__init__(Rectangle(0, 0, 1920, 1080))  # FIXME
        self.id = id

    def getNumberScreens(self) -> int:
        # FIXME
        return 1

    def getBounds(self) -> Rectangle:
        # FIXME
        return None

    def capture(self, rect:Rectangle) -> str:
        # FIXME return filename
        pass

    def selectRegion(self, text=None) -> Region:
        # FIXME: interactive selection, with label
        pass
