"""
http://doc.sikuli.org/location.html
"""


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
