Sikuli[1] is pretty awesome, but it requires java. Bleh.

This is a project to provide the same API using regular CPython libraries.

The goal is to be able to run any script which works in the Java IDE.

Incompatibilities:
- Sikuli IDE has an implied "from sikuli import *" at the start; to run with sikulpy, you need to add that explicitly

Dependencies:
- CPython 3.?
- PIL
- NumPy
- OpenCV
- autopy
- pyscreenshot

[1] http://www.sikulix.com/
