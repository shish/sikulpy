import warnings
import sys

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


def find(ps):
    return desktop.find(ps)


def popup(text, title):
    warnings.warn('sikuli.popup(%r, %r) not implemented' % (text, title))  # FIXME


def input_(text, default):
    warnings.warn('sikuli.input(%r, %r) not implemented' % (text, default))  # FIXME


def load(path):
    warnings.warn('sikuli.load(%r) not implemented' % (path, ))  # FIXME


def setShowActions(sa: bool):
    warnings.warn('sikuli.setShowActions(%r) not implemented' % (sa, ))  # FIXME


def exit(code: int):
    sys.exit(code)


def getImagePath() -> [str]:
    """
    Get a list of paths where Sikuli will search for images.
    """
    return Settings.ImagePaths


def addImagePath(path: str):
    """
    Add a new path to the list of image search paths
    :param path: a path
    """
    Settings.ImagePaths.append(path)


def removeImagePath(path: str):
    """
    Remove a path from the list of image search paths
    :param path: a path
    """
    Settings.ImagePaths.remove(path)


def getBundlePath() -> [str]:
    warnings.warn('sikuli.getBundlePath() not implemented')  # FIXME


def setBundlePath(path: bool):
    warnings.warn('sikuli.setBundlePath(%r) not implemented' % (path, ))  # FIXME
