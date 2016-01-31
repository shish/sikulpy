from .region import Region
from .rectangle import Rectangle


class Match(Region):
    def __init__(self, rect: Rectangle, sim: float):
        super().__init__(rect)
        self.score = sim
        self.target = 0

    def getScore(self):
        return self.score

    def getTarget(self):
        return self.target

    def __lt__(self, other):
        return self.score < other.score
