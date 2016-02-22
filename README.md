Sikuli[1] is pretty awesome, but it requires java. Bleh.

This is a project to provide the same API using regular CPython libraries.

The goal is to be able to run any script which works in the Java IDE.

Dependencies:
- CPython 3.5
- Pillow (or PIL)
- AutoPy3
- PyScreenshot
- NumPy
- OpenCV

Windows:
- https://www.python.org/downloads/
- Download NumPy and OpenCV .whl files from http://www.lfd.uci.edu/~gohlke/pythonlibs/
- pip install pillow autopy3 pyscreenshot *.whl

OSX:
```
$ git clone https://github.com/shish/sikulpy
$ cd sikulpy
$ virtualenv-3.5 .env
$ . .env/bin/activate
$ CFLAGS="-I/opt/local/include -L/opt/local/lib" pip install -e ./
$ sikulpy ~/Documents/sikuli/foo.sikuli
```

[1] http://www.sikulix.com/
