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
    """
    :param Pattern|str ps:
    :rtype: list[Match]
    """
    return desktop.find(ps)


def popup(text, title):
    """
    :param str text:
    :param str title:
    """
    warnings.warn('sikuli.popup(%r, %r) not implemented' % (text, title))  # FIXME


def input_(text, default):
    """
    :param str text:
    :param str default:
    :rtype: str
    """
    warnings.warn('sikuli.input(%r, %r) not implemented' % (text, default))  # FIXME


def load(path):
    """
    :param str path:
    """
    warnings.warn('sikuli.load(%r) not implemented' % (path, ))  # FIXME


def setShowActions(sa):
    """
    :param bool sa:
    """
    warnings.warn('sikuli.setShowActions(%r) not implemented' % (sa, ))  # FIXME


def exit(code):
    """
    :param int code:
    """
    sys.exit(code)


def getImagePath():
    """
    Get a list of paths where Sikuli will search for images.

    :rtype: list[str]
    """
    return Settings.ImagePaths


def addImagePath(path):
    """
    Add a new path to the list of image search paths

    :param str path: a path
    """
    Settings.ImagePaths.append(path)


def removeImagePath(path):
    """
    Remove a path from the list of image search paths

    :param str path: a path
    """
    Settings.ImagePaths.remove(path)


def getBundlePath():
    """
    :rtype: list[str]
    """
    warnings.warn('sikuli.getBundlePath() not implemented')  # FIXME


def setBundlePath(path):
    """
    :param bool path:
    """
    warnings.warn('sikuli.setBundlePath(%r) not implemented' % (path, ))  # FIXME
