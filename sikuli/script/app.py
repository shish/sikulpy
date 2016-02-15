import warnings
import platform
import subprocess

from .region import Region

PLATFORM = platform.system()


class App(object):
    @staticmethod
    def open(application=None) -> 'App':
        warnings.warn('App.open(%r) not implemented' % application)  # FIXME

    @staticmethod
    def focus(application=None) -> 'App':
        if PLATFORM == "Darwin":
            # FIXME: we don't want to hard-code 'Chrome' as the app, and
            # we want 'window title contains X' rather than 'is X'
            script = b"""
set theTitle to "%s"
tell application "System Events"
    tell process "Chrome"
        set frontmost to true
        perform action "AXRaise" of (windows whose title is theTitle)
    end tell
end tell
""" % application.encode('ascii')
            subprocess.run("osascript", input=script, shell=True)
        else:
            warnings.warn('App.focus(%r) not implemented for %r' % (application, PLATFORM))  # FIXME

    @staticmethod
    def close(application=None):
        warnings.warn('App.close(%r) not implemented' % application)  # FIXME

    def focusedWindow(self) -> Region:
        warnings.warn('App.focusedWindow() not implemented')  # FIXME

    def window(self, n=0) -> 'App':
        warnings.warn('App.window(%r) not implemented' % n)  # FIXME
