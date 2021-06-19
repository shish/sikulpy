"""
http://doc.sikuli.org/keys.html
"""

import autopy  # EXT


class Key(object):
    ENTER = autopy.key.Code.RETURN
    UP = autopy.key.Code.UP_ARROW
    DOWN = autopy.key.Code.DOWN_ARROW
    LEFT = autopy.key.Code.LEFT_ARROW
    RIGHT = autopy.key.Code.RIGHT_ARROW
    BACKSPACE = autopy.key.Code.BACKSPACE
    TAB = "\t"


class KeyModifier(object):
    # these differ based on platform
    CTRL = autopy.key.Modifier.CONTROL
    SHIFT = autopy.key.Modifier.SHIFT
    ALT = autopy.key.Modifier.ALT
    META = autopy.key.Modifier.META

    CMD = META
    WIN = META


class Mouse(object):
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3
