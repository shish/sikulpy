
class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return float(self.x)

    def getY(self):
        return float(self.y)

    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def offset(self, dx, dy):
        return Location(self.x + dx, self.y + dy)

    def above(self, dy):
        return Location(self.x, self.y - dy)

    def below(self, dy):
        return Location(self.x, self.y + dy)

    def left(self, dx):
        return Location(self.x - dx, self.y)

    def right(self, dx):
        return Location(self.x + dx, self.y)
