Sikuli[1] is pretty awesome, but it requires java. Bleh.

This is a project to provide the same API using regular CPython libraries.

The goal is to be able to run any script which works in the Java IDE.

Incompatibilities:
- Sikuli IDE has an implied "from sikuli import *" at the start; to run with sikulpy, you need to add that explicitly

Dependencies:
- CPython 3.5 ( https://www.python.org/downloads/ )
- Pillow (pip install pillow)
- AutoPy (pip install autopy3)
- PyScreenshot (pip install pyscreenshot)
- NumPy ( http://www.lfd.uci.edu/~gohlke/pythonlibs/ )
- OpenCV ( http://www.lfd.uci.edu/~gohlke/pythonlibs/ )

Windows:
- https://www.python.org/downloads/
- pip install pillow autopy3 pyscreenshot *.whl
- Download NumPy and OpenCV from http://www.lfd.uci.edu/~gohlke/pythonlibs/

[1] http://www.sikulix.com/
