import sys
from typing import Union, List

from .app import App  # noqa
from .env import Env  # noqa
from .finder import Finder  # noqa
from .location import Location  # noqa
from .match import Match  # noqa
from .pattern import Pattern  # noqa
from .rectangle import Rectangle  # noqa
from .region import Region  # noqa
from .screen import Screen  # noqa
from .settings import Settings  # noqa
from .key import Key, KeyModifier, Mouse  # noqa
from .robot import Robot  # noqa

desktop = Screen(0)


def find(ps: Union[Pattern, str]) -> Match:
    return desktop.find(ps)


def popup(text: str, title: str) -> None:
    raise NotImplementedError(
        "sikuli.popup(%r, %r) not implemented" % (text, title)
    )  # FIXME


def input_(text: str, default: str) -> str:
    raise NotImplementedError(
        "sikuli.input(%r, %r) not implemented" % (text, default)
    )  # FIXME


def load(path: str):
    raise NotImplementedError("sikuli.load(%r) not implemented" % (path,))  # FIXME


def setShowActions(sa: bool):
    raise NotImplementedError(
        "sikuli.setShowActions(%r) not implemented" % (sa,)
    )  # FIXME


def exit(code: int) -> None:
    sys.exit(code)


def getImagePath() -> List[str]:
    """
    Get a list of paths where Sikuli will search for images.
    """
    return Settings.ImagePaths


def addImagePath(path: str) -> None:
    """
    Add a new path to the list of image search paths
    """
    Settings.ImagePaths.append(path)


def removeImagePath(path: str) -> None:
    """
    Remove a path from the list of image search paths
    """
    Settings.ImagePaths.remove(path)


def getBundlePath() -> List[str]:
    raise NotImplementedError("sikuli.getBundlePath() not implemented")  # FIXME


def setBundlePath(path: bool):
    raise NotImplementedError(
        "sikuli.setBundlePath(%r) not implemented" % (path,)
    )  # FIXME
