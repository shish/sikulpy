"""
http://doc.sikuli.org/location.html
"""

from .sikulpy import unofficial


class Location(object):
    def __init__(self, x, y):
        """
        :param int x:
        :param int y:
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """
        :rtype: str
        """
        return "Location(%r, %r)" % (self.x, self.y)

    def __eq__(self, other):
        """
        :param Location other:
        :rtype: bool
        """
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """
        :param Location other:
        :rtype: Location
        """
        return Location(self.x + other.x, self.y + other.y)

    @unofficial
    def __sub__(self, other):
        """
        :param Location other:
        :rtype: Location
        """
        return Location(self.x - other.x, self.y - other.y)

    @unofficial
    def __mul__(self, factor):
        """
        :param float other:
        :rtype: Location
        """
        return Location(self.x * factor, self.y * factor)

    @unofficial
    def getXY(self):
        """
        :rtype: Tuple(float, float)
        """
        return self.getX(), self.getY()

    def getX(self):
        """
        :rtype: float
        """
        return float(self.x)

    def getY(self):
        """
        :rtype: float
        """
        return float(self.y)

    def setLocation(self, x, y):
        """
        :param int x:
        :param int y:
        """
        self.x = x
        self.y = y

    def offset(self, dx, dy):
        """
        :param int dx:
        :param int dy:
        """
        return Location(self.x + dx, self.y + dy)

    def above(self, dy):
        """
        :param int dy:
        """
        return Location(self.x, self.y - dy)

    def below(self, dy):
        """
        :param int dy:
        """
        return Location(self.x, self.y + dy)

    def left(self, dx):
        """
        :param int dx:
        """
        return Location(self.x - dx, self.y)

    def right(self, dx):
        """
        :param int dx:
        """
        return Location(self.x + dx, self.y)
