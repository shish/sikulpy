# For unofficial extra bits

strict = False


class UnofficialApiException(Exception):
    pass


def unofficial(f):
    if strict:

        def fail(*args, **kwargs):
            raise UnofficialApiException(
                f"{f.__name__}({args!r}, {kwargs!r}) is an unofficial extension "
                "to the Sikuli API and is not supported in strict mode"
            )

        return fail
    else:
        return f
