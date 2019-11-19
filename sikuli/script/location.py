"""
http://doc.sikuli.org/location.html
"""

from typing import Tuple

from .sikulpy import unofficial


class Location(object):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return "Location(%r, %r)" % (self.x, self.y)

    def __eq__(self, other: "Location") -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Location") -> "Location":
        return Location(self.x + other.x, self.y + other.y)

    @unofficial
    def __sub__(self, other: "Location") -> "Location":
        return Location(self.x - other.x, self.y - other.y)

    @unofficial
    def __mul__(self, factor: float) -> "Location":
        return Location(self.x * factor, self.y * factor)

    @unofficial
    def getXY(self) -> Tuple[float, float]:
        return self.getX(), self.getY()

    def getX(self) -> float:
        return float(self.x)

    def getY(self) -> float:
        return float(self.y)

    def setLocation(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def offset(self, dx: int, dy: int) -> "Location":
        return Location(self.x + dx, self.y + dy)

    def above(self, dy: int) -> "Location":
        return Location(self.x, self.y - dy)

    def below(self, dy: int) -> "Location":
        return Location(self.x, self.y + dy)

    def left(self, dx: int) -> "Location":
        return Location(self.x - dx, self.y)

    def right(self, dx: int) -> "Location":
        return Location(self.x + dx, self.y)
