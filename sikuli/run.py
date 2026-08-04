import argparse
import logging
import os
import runpy
import sys

from sikuli import Settings

log = logging.getLogger(__name__)


def reload(module: str) -> None:
    log.debug(f"Stub reload({module!r})")


def run(folder: str) -> None:
    folder = os.path.abspath(folder)
    module = os.path.basename(folder).replace(".sikuli", "")
    # print("Running %s from %s" % (module, folder))
    sys.path.append(folder)
    sys.path.append(os.path.dirname(folder))  # FIXME: adding parent is unofficial
    Settings.ImagePaths.append(folder)
    try:
        runpy._run_module_as_main(module)  # type: ignore
        # mod = __import__(module)
    except KeyboardInterrupt:
        pass


def main() -> int:
    # FIXME: sikuli CLI compat
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", default=False, action="store_true")
    parser.add_argument("-D", "--debugger", default=False, action="store_true")
    parser.add_argument("-s", "--scale", type=float, default=1.0)
    parser.add_argument("script")
    args = parser.parse_args()

    logging.captureWarnings(True)
    if args.debug:
        logging.basicConfig(
            format="%(asctime)-15s %(filename)s:%(lineno)d %(message)s",
            level=logging.DEBUG,
        )
        logging.getLogger("sikuli").setLevel(logging.DEBUG)
    else:
        logging.getLogger("sikuli").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    if args.debugger:
        try:
            import pudb  # noqa

            pudb.set_interrupt_handler()
        except ImportError:
            pass

    Settings.Scale = args.scale
    run(args.script)
    return 0


if __name__ == "__main__":
    sys.exit(main())
