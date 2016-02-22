import warnings

from .region import Region
from .robot import Robot


class App(object):
    @staticmethod
    def open(application=None) -> 'App':
        warnings.warn('App.open(%r) not implemented' % application)  # FIXME

    @staticmethod
    def focus(application=None) -> 'App':
        Robot.focus(application)

    @staticmethod
    def close(application=None):
        warnings.warn('App.close(%r) not implemented' % application)  # FIXME

    def focusedWindow(self) -> Region:
        warnings.warn('App.focusedWindow() not implemented')  # FIXME

    def window(self, n=0) -> 'App':
        warnings.warn('App.window(%r) not implemented' % n)  # FIXME
