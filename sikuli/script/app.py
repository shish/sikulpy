import warnings

from .region import Region
from .robot import Robot


class App(object):
    @staticmethod
    def open(application=None):
        """
        :param str application:
        :rtype: App
        """
        warnings.warn('App.open(%r) not implemented' % application)  # FIXME

    @staticmethod
    def focus(application=None):
        """
        :param str application:
        :rtype: App
        """
        Robot.focus(application)

    @staticmethod
    def close(application=None):
        """
        :param str application:
        """
        warnings.warn('App.close(%r) not implemented' % application)  # FIXME

    def focusedWindow(self):
        """
        :rtype: Region
        """
        warnings.warn('App.focusedWindow() not implemented')  # FIXME

    def window(self, n=0):
        """
        :param int n:
        :rtype: App
        """
        warnings.warn('App.window(%r) not implemented' % n)  # FIXME
