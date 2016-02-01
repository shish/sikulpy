#!/usr/bin/env python3

import sys
import os
import runpy
from sikuli import *

def run(folder):
    folder = os.path.abspath(folder)
    script = os.path.basename(folder).replace(".sikuli", "")
    print("Running %s from %s" % (script, folder))
    sys.path.append(folder)
    os.chdir(folder)  # for .png filenames
    runpy._run_module_as_main(script)
    #mod = __import__(script)

def main():
    if len(sys.argv) > 1:
        run(sys.argv[1])
