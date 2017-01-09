"""
http://doc.sikuli.org/screen.html
"""

import tempfile
import warnings

from .region import Region
from .rectangle import Rectangle
from .robot import Robot


class Screen(Region):
    def __init__(self, id_):
        """
        :param int id_:
        """
        x, y, w, h = Robot.screenSize()
        Region.__init__(self, Rectangle(x, y, w, h))
        self.id = id_

    @staticmethod
    def getNumberScreens():
        """
        :rtype: int
        """
        return Robot.getNumberScreens()

    def getBounds(self):
        """
        :rtype: Rectangle
        """
        return self.getRect()

    def capture(self, rect):
        """
        :param Rectangle rect:
        :rtype: str
        """
        if not rect:
            rect = self.getBounds()
        fn = tempfile.mktemp(".png")
        img = Robot.capture(rect.getBounds())
        img.save(fn)
        return fn

    def selectRegion(self, text=None):
        """
        :param str text:
        :rtype: Region
        """
        # interactive selection, with label
        warnings.warn('Screen.selectRegion(%r) not implemented' % text)  # FIXME
