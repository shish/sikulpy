
from .location import Location
from .image import Image


class Pattern(object):
    def __init__(self, filename: str):
        self.filename = filename

        self.similarity = 0.7
        self.img = Image(filename)
        self.targetOffset = Location(self.img.w/2, self.img.h/2)

    def __repr__(self) -> str:
        return "Pattern(%r, %r)" % (self.img, self.targetOffset)

    def _copy(self):
        p = Pattern(self.filename)
        p.similarity = self.similarity
        p.targetOffset = self.targetOffset
        return p

    def similar(self, similarity:float):
        p = self._copy()
        p.similarity = similarity
        return p

    def exact(self):
        return self.similar(1.0)

    def targetOffset(self, dx, dy):
        p = self._copy()
        p.targetOffset = p.targetOffset.offset(dx, dy)
        return p

    def getFilename(self):
        return self.filename

    def getTargetOffset(self):
        return self.targetOffset
