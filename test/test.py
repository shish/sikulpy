#!/usr/bin/env python3

import logging

from sikuli import *

logging.basicConfig(level=logging.INFO)
logging.getLogger("sikuli").setLevel(logging.DEBUG)

s = Screen(0)
a = s.find("test.png")
print(a)
s.click()
