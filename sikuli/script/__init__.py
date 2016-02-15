import warnings

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
