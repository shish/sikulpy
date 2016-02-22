from sikuli import *
import sys
import argparse

Settings.ImagePaths = ["."]


def run(img):
    p = Pattern(img).similar(0.7)
    s = Screen(0)
    s._debug = True
    s.exists(p)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('-s', '--scale', type=float, default=1.0)
    parser.add_argument('img')
    args = parser.parse_args()
    if args.debug:
        logging.getLogger("sikuli").setLevel(logging.DEBUG)
    Settings.Scale = args.scale
    run(args.img)
    return 0


if __name__ == "__main__":
    sys.exit(main())
