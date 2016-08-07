"""
http://doc.sikuli.org/finder.html
"""

from .match import Match


class Finder(object):
    def __init__(self, filename):
        """
        :param str filename:
        """
        self.filename = filename

    def find(self, filename, similarity=0.7):
        """
        :param str filename:
        :param float similarity:
        """
        pass

    def hasNext(self):
        """
        :rtype: bool
        """
        pass

    def next(self) -> Match:
        """
        :rtype: Match
        """
        pass
