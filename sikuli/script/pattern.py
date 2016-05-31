"""
http://doc.sikuli.org/pattern.html
"""

from .location import Location
from .image import Image
from .settings import Settings


class Pattern(object):
    def __init__(self, filename: str):
        """
        This will initialize a new pattern object without any additional
        attributes. As long as no pattern methods are used additionally,
        it is the same as just using the image file name itself in the
        find operation.

        :param filename: a path to an image file
        :return: a new pattern object
        """
        self.filename = filename

        self.similarity = Settings.MinSimilarity
        self.img = Image(filename)
        self._targetOffset = Location(0, 0)  # relative to center

    def __repr__(self) -> str:
        if self._targetOffset == Location(0, 0):
            return "Pattern(%r)" % self.img
        else:
            return "Pattern(%r, %r)" % (self.img, self._targetOffset)

    def _copy(self):
        p = Pattern(self.filename)
        p.similarity = self.similarity
        p._targetOffset = self._targetOffset
        return p

    def similar(self, similarity: float):
        """
        Return a new Pattern object containing the same attributes (image,
        click point) with the minimum similarity set to the specified value.

        :param similarity: the minimum similarity to use in a find operation.
                           The value should be between 0 and 1.
        :return: a new pattern object
        """
        p = self._copy()
        p.similarity = similarity
        return p

    def exact(self):
        """
        Return a new Pattern object containing the same attributes (image,
        click point) with the minimum similarity set to 1.0, which means
        exact match is required.

        :return: a new pattern object
        """
        return self.similar(1.0)

    def targetOffset(self, dx, dy):
        """
        Return a new Pattern object containing the same attributes (image,
        similarity), but a different definition for the click. By default,
        the click point is the center of the found match. By setting the
        target offset, it is possible to specify a click point other than
        the center. dx and dy will be used to calculate the position
        relative to the center.

        :param dx: x offset from the center
        :param dy: y offset from the center
        :return: a new pattern object
        """
        p = self._copy()
        p._targetOffset = p._targetOffset.offset(
            dx*Settings.Scale,
            dy*Settings.Scale
        )
        return p

    def getFilename(self) -> str:
        """
        Get the filename of the image contained in the Pattern object.

        :return: a filename as a string
        """
        return self.filename

    def getTargetOffset(self) -> Location:
        """
        Get the target offset of the Pattern object.

        :return: a Location object as the target offset
        """
        return self._targetOffset
