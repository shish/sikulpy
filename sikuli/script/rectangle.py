from .location import Location

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .region import Region


class Rectangle(object):
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self) -> str:
        return "%s(%d, %d, %d, %d)" % (
            self.__class__.__name__,
            self.x,
            self.y,
            self.w,
            self.h,
        )

    def __eq__(self, b: "Rectangle") -> bool:
        return self.x == b.x and self.y == b.y and self.w == b.w and self.h == b.h

    def __ne__(self, b: "Rectangle") -> bool:
        return not self.__eq__(b)

    # set

    def setX(self, x: int) -> None:
        self.x = x

    def setY(self, y: int) -> None:
        self.y = y

    def setW(self, w: int) -> None:
        self.w = w

    def setH(self, h: int) -> None:
        self.h = h

    def moveTo(self, location: Location) -> "Rectangle":
        self.x, self.y = location.x, location.y
        return self

    def setRect(self, rect: "Rectangle") -> None:
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h

    setROI = setRect

    def morphTo(self, reg: "Region") -> "Rectangle":
        self.setRect(reg)
        return self

    # get

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getW(self) -> int:
        return self.w

    def getH(self) -> int:
        return self.h

    def getRect(self) -> "Rectangle":
        return Rectangle(self.x, self.y, self.w, self.h)

    def getCenter(self) -> Location:
        return Location(self.x + self.w // 2, self.y + self.h // 2)

    getTarget = getCenter

    def getTopLeft(self) -> Location:
        return Location(self.x, self.y)

    def getTopRight(self) -> Location:
        return Location(self.x + self.w, self.y)

    def getBottomLeft(self) -> Location:
        return Location(self.x, self.y + self.h)

    def getBottomRight(self) -> Location:
        return Location(self.x + self.w, self.y + self.h)
