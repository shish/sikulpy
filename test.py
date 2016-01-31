#!/usr/bin/env python3

from sikuli import *
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("sikuli").setLevel(logging.DEBUG)

s = Screen(0)
a = s.find("test.png")
print(a)
s.click()
