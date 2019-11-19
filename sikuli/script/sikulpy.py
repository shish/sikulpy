# For unofficial extra bits

strict = False


def unofficial(f):
    if strict:

        def fail(*args, **kwargs):
            raise Exception("%s(%r, %r) is unofficial" % (f.__name__, args, kwargs))

        return fail
    else:
        return f
