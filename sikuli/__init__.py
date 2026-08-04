try:
    from .script import *
except ImportError as e:
    print(f"Error importing sikuli: {e}")
from .version import *
