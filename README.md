SikulPy
-------

Sikuli[1] is pretty awesome, but it requires java. Bleh.

This is a project to provide the same API using regular CPython libraries.

The goal is to be able to run any script which works in the Java IDE.

Dependencies:
- CPython 3.5 (or 2.7)
- Pillow (or PIL)
- AutoPy3 (or AutoPy)
- PyScreenshot
- NumPy
- OpenCV

Windows:
- https://www.python.org/downloads/
- Download NumPy and OpenCV .whl files from http://www.lfd.uci.edu/~gohlke/pythonlibs/
- `pip install pillow autopy3 pyscreenshot *.whl`

OSX / Linux:
```
$ git clone https://github.com/shish/sikulpy
$ cd sikulpy
$ virtualenv-3.5 .env
$ . .env/bin/activate
$ CFLAGS="-I/opt/local/include -L/opt/local/lib" pip install -e ./
$ sikulpy ~/Documents/sikuli/foo.sikuli
```

[1] http://www.sikulix.com/

Java-Sikuli compatibility
-------------------------
The parts of the Sikuli API that I'm personally using are fairly stable; I'm using it in production on Linux, with development on OSX and occasional testing on Windows.

Off the top of my head (check the source code if you want 100% accuracy):

| Feature                                         | Compatibility |
|-------------------------------------------------|---------------|
| Screen capture (Region.find(), etc)             | Y             |
| Screen monitoring (onAppear(), onVanish(), etc) | N             |
| Mouse control (Region.click(), etc)             | Y             |
| Keyboard control (Region.type(), etc)           | Y             |
| Window control (App.open(), App.close(), etc)   | Partial       |
| User input (hotkey binding, popup(), input())   | N             |
