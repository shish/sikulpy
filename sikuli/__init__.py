try:
    from .script import *
except ImportError as e:
    print("Error importing sikuli: %s" % e)
from .version import *
