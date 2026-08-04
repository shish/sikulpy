import logging
import os
import warnings

from PIL import Image as PILImage  # EXT

from .settings import Settings

log = logging.getLogger(__name__)


def _same_contents(a: str, b: str) -> bool:
    return open(a, "rb").read() == open(b, "rb").read()


class Image:
    def __init__(self, base: PILImage.Image | str) -> None:
        if isinstance(base, PILImage.Image):
            self.img = base
            self._repr = f"Image({base.size[0]!r}x{base.size[1]!r})"
        elif isinstance(base, str):
            full_path = None
            for p in Settings.ImagePaths:
                try_path = os.path.join(p, base)
                if os.path.exists(try_path):
                    if not full_path:
                        full_path = try_path
                    else:
                        if not _same_contents(try_path, full_path):
                            warnings.warn(
                                f"Multiple sources for {base}, using {full_path}"
                            )
                            break
            if not full_path:
                raise ValueError(f"Couldn't find {base!r} in {Settings.ImagePaths!r}")

            i: PILImage.Image = PILImage.open(full_path)
            if Settings.Scale != 1.0:
                # resize to multiple of 1/scale
                # eg scale=0.5, round to a multiple of 2
                i = i.crop(
                    (
                        0,
                        0,
                        int(i.size[0] - (i.size[0] % (1 / Settings.Scale))),
                        int(i.size[1] - (i.size[1] % (1 / Settings.Scale))),
                    )
                )
                i.load()
                i = i.resize(
                    (int(i.size[0] * Settings.Scale), int(i.size[1] * Settings.Scale))
                )
            self.img = i
            self._repr = f"Image({base!r})"
        else:
            raise TypeError(f"Can't make an image from {base!r}")

        self.w = self.img.size[0]
        self.h = self.img.size[1]

    def save(self, fn: str) -> None:
        self.img.save(fn)

    def find(self, other: "Image"):
        raise NotImplementedError("Image.find() not implemented")

    def __repr__(self):
        return self._repr
