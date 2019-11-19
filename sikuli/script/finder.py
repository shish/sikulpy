"""
http://doc.sikuli.org/finder.html
"""

from .match import Match


class Finder(object):
    def __init__(self, filename: str):
        self.filename = filename

    def find(self, filename: str, similarity: float = 0.7):
        pass

    def hasNext(self) -> bool:
        pass

    def next(self) -> Match:
        pass
