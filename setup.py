from setuptools import setup
from sikuli.version import VERSION

import sys
py3 = (sys.version_info >= (3, 0))

alldeps = [
    "pyscreenshot",
    "pillow",
    "numpy",
    #"opencv",
]
py3deps = ["autopy3"]
py2deps = ["autopy", "enum"]

setup(
    name='sikulpy',
    version=VERSION,
    description='An implementation of Sikuli for CPython',
    long_description='',
    author='Shish',
    author_email='webmaster@shishnet.org',
    install_requires=alldeps + (py3deps if py3 else py2deps),
    url='https://github.com/shish/sikulpy',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
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
