try:
    from .script import *  # noqa
except ImportError as e:
    print("Error importing sikuli: %s" % e)
from .version import *  # noqa
