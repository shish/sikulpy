"""
http://doc.sikuli.org/match.html
"""

from .location import Location
from .rectangle import Rectangle
from .region import Region


class Match(Region):
    def __init__(self, rect: Rectangle, sim: float, targetOffset: Location):
        Region.__init__(self, rect)
        self._name: str | None = None
        self._score = sim
        self._targetOffset = targetOffset

    def getScore(self) -> float:
        """
        Get the similarity score the image or pattern was found. The value
        is between 0 and 1.
        """
        return self._score

    def getTarget(self) -> Location:
        """
        Get the location object that will be used as the click point.

        Typically, when no offset was specified by Pattern.targetOffset(),
        the click point is the center of the matched region. If an offset
        was given, the click point is the offset relative to the center.
        """
        return self.getCenter() + self._targetOffset

    def __lt__(self, other: "Match") -> bool:
        return self.getScore() < other.getScore()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({(self._name or self.getRect())!r}, {self.getScore():.3f})"
