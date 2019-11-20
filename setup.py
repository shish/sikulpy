#!/usr/bin/env python

import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sikulpy',
    version='0.0',
    description='An implementation of Sikuli for CPython',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shish',
    author_email='webmaster@shishnet.org',
    install_requires=[
        "autopy3",
        "pillow",
        "numpy",
        "mss",
        "pyperclip",
        "opencv-python",
    ],
    url='https://github.com/shish/sikulpy',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    packages=[
        "sikuli",
        "sikuli.script",
    ],
    entry_points={
        'console_scripts': [
            'sikulpy = sikuli.run:main',
            'sikulpy-find = sikuli.find:main',
        ],
        'gui_script': []
    },
)
