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

desktop = Screen(0)


def find(ps):
    return desktop.find(ps)


def popup(text, title):
    # FIXME
    pass


def input(text, default):
    # FIXME
    pass
