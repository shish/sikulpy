"""
http://doc.sikuli.org/finder.html
"""

from .match import Match


class Finder:
    def __init__(self, filename: str):
        self.filename = filename

    def find(self, filename: str, similarity: float = 0.7):
        raise NotImplementedError(
            f"Finder.find({filename!r}, {similarity!r}) not implemented"
        )  # FIXME

    def hasNext(self) -> bool:
        raise NotImplementedError("Finder.hasNext() not implemented")  # FIXME

    def next(self) -> Match:
        raise NotImplementedError("Finder.next() not implemented")  # FIXME
