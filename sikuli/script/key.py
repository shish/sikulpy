"""
http://doc.sikuli.org/keys.html
"""

import autopy3 as autopy  # EXT


class Key(object):
    ENTER = '\n'


class KeyModifier(object):
    # these differ based on platform
    CTRL = autopy.key.MOD_CONTROL
    SHIFT = autopy.key.MOD_SHIFT
    ALT = autopy.key.MOD_ALT
    META = autopy.key.MOD_META

    CMD = META
    WIN = META


class Mouse(object):
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3
