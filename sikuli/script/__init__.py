import sys
from typing import Union, List

from .app import App
from .env import Env
from .finder import Finder
from .location import Location
from .match import Match
from .pattern import Pattern
from .rectangle import Rectangle
from .region import Region
from .screen import Screen
from .settings import Settings
from .key import Key, KeyModifier, Mouse
from .robot import Robot

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
