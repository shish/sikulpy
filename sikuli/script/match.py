from .region import Region


class Match(Region):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.target = 0

    def getScore(self):
        return self.score

    def getTarget(self):
        return self.target
