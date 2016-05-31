# For unofficial extra bits

strict = False


def unofficial(f):
    if strict:
        def fail(*args, **kwargs):
            raise Exception("%s is unofficial" % f.__name__)
        return fail
    else:
        return f
