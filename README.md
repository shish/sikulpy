SikulPy
-------

Sikuli[1] is pretty awesome, but it requires java. Bleh.

This is a project to provide the same API using regular CPython libraries.

The goal is to be able to run any script which works in the Java IDE.

Installation:
```
$ git clone https://github.com/shish/sikulpy
$ cd sikulpy
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -e .
$ sikulpy ~/Documents/sikuli/foo.sikuli
```

[1] http://www.sikulix.com/

Java-Sikuli compatibility
-------------------------
The parts of the Sikuli API that I'm personally using are fairly stable; I'm using it in production on Linux, with development on OSX and occasional testing on Windows.

Parts of the API which are known to be incomplete have tasks filed here: https://github.com/shish/sikulpy/labels/API%20Completion
