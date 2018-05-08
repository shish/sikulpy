"""
http://doc.sikuli.org/keys.html
"""

import autopy3  # EXT


class Key(object):
    ENTER = '\n'
    BACKSPACE = chr(autopy3.key.K_BACKSPACE)


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
