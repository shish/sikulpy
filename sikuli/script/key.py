"""
http://doc.sikuli.org/keys.html
"""

import autopy3  # EXT


class Key(object):
    ENTER = int(autopy3.key.K_RETURN)
    UP = int(autopy3.key.K_UP)
    DOWN = int(autopy3.key.K_DOWN)
    LEFT = int(autopy3.key.K_LEFT)
    RIGHT = int(autopy3.key.K_RIGHT)
    BACKSPACE = int(autopy3.key.K_BACKSPACE)
    TAB = "\t"


class KeyModifier(object):
    # these differ based on platform
    CTRL = autopy3.key.MOD_CONTROL
    SHIFT = autopy3.key.MOD_SHIFT
    ALT = autopy3.key.MOD_ALT
    META = autopy3.key.MOD_META

    CMD = META
    WIN = META


class Mouse(object):
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3
