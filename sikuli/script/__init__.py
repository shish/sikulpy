import sys

from .app import App  # noqa
from .env import Env  # noqa
from .finder import Finder  # noqa
from .key import Key, KeyModifier, Mouse  # noqa
from .location import Location  # noqa
from .match import Match
from .pattern import Pattern
from .rectangle import Rectangle  # noqa
from .region import Region  # noqa
from .robot import Robot  # noqa
from .screen import Screen
from .settings import Settings

desktop = Screen(0)


def find(ps: Pattern | str) -> Match:
    return desktop.find(ps)


def popup(text: str, title: str) -> None:
    raise NotImplementedError(
        f"sikuli.popup({text!r}, {title!r}) not implemented"
    )  # FIXME


def input_(text: str, default: str) -> str:
    raise NotImplementedError(
        f"sikuli.input({text!r}, {default!r}) not implemented"
    )  # FIXME


def load(path: str):
    raise NotImplementedError(f"sikuli.load({path!r}) not implemented")


def setShowActions(sa: bool):
    raise NotImplementedError(f"sikuli.setShowActions({sa!r}) not implemented")  # FIXME


def exit(code: int) -> None:
    sys.exit(code)


def getImagePath() -> list[str]:
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


def getBundlePath() -> list[str]:
    raise NotImplementedError("sikuli.getBundlePath() not implemented")  # FIXME


def setBundlePath(path: bool):
    raise NotImplementedError(
        f"sikuli.setBundlePath({path!r}) not implemented"
    )  # FIXME
