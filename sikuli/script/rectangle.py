from .location import Location

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .region import Region


class Rectangle(object):
    def __init__(self, x: float = 0, y: float = 0, w: float = 0, h: float = 0) -> None:
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

    def __eq__(self, b: object) -> bool:
        return (
            isinstance(b, Rectangle)
            and self.x == b.x
            and self.y == b.y
            and self.w == b.w
            and self.h == b.h
        )

    def __ne__(self, b: object) -> bool:
        return not self.__eq__(b)

    # set

    def setX(self, x: float) -> None:
        self.x = x

    def setY(self, y: float) -> None:
        self.y = y

    def setW(self, w: float) -> None:
        self.w = w

    def setH(self, h: float) -> None:
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

    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def getW(self) -> float:
        return self.w

    def getH(self) -> float:
        return self.h

    def getRect(self) -> "Rectangle":
        return Rectangle(self.x, self.y, self.w, self.h)

    def getCenter(self) -> Location:
        return Location(self.x + self.w // 2, self.y + self.h // 2)

    def getTarget(self) -> Location:
        return self.getCenter()

    def getTopLeft(self) -> Location:
        return Location(self.x, self.y)

    def getTopRight(self) -> Location:
        return Location(self.x + self.w, self.y)

    def getBottomLeft(self) -> Location:
        return Location(self.x, self.y + self.h)

    def getBottomRight(self) -> Location:
        return Location(self.x + self.w, self.y + self.h)
