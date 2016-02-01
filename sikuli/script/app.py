import warnings

from .region import Region


class App(object):
    def open(self, application=None) -> 'App':
        warnings.warn('App.open(%r) not implemented' % application)  # FIXME

    def focus(self, application=None) -> 'App':
        warnings.warn('App.focus(%r) not implemented' % application)  # FIXME

    def close(self, application=None):
        warnings.warn('App.close(%r) not implemented' % application)  # FIXME

    def focusedWindow(self) -> Region:
        warnings.warn('App.focusedWindow() not implemented')  # FIXME

    def window(self, n=0) -> 'App':
        warnings.warn('App.window(%r) not implemented' % n)  # FIXME

