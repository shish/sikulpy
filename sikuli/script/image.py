from PIL import Image as PILImage  # EXT

import logging

log = logging.getLogger(__name__)


class Image(object):
    def __init__(self, base):
        if isinstance(base, PILImage.Image):
            self.img = base
        elif isinstance(base, str):
            self.img = PILImage.open(base)
        else:
            print("Can't make an image from %r" % base)

        self.w = self.img.size[0]
        self.h = self.img.size[1]

    def save(self, fn):
        self.img.save(fn)

    def find(self, other):
        return None

    def __repr__(self):
        return "%s(%rx%r)" % (self.__class__.__name__, self.w, self.h)
