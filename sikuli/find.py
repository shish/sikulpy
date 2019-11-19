import sys
import argparse
import logging

from sikuli import Settings, Pattern, Screen

Settings.ImagePaths = ["."]


def run(img: str, similarity: float) -> None:
    p = Pattern(img).similar(similarity)
    s = Screen(0)
    s._debug = True
    s.hover(p)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", default=False, action="store_true")
    parser.add_argument("-s", "--scale", type=float, default=1.0)
    parser.add_argument("-S", "--similarity", type=float, default=0.7)
    parser.add_argument("img")
    args = parser.parse_args()
    if args.debug:
        logging.getLogger("sikuli").setLevel(logging.DEBUG)
    Settings.Scale = args.scale
    run(args.img, args.similarity)
    return 0


if __name__ == "__main__":
    sys.exit(main())
