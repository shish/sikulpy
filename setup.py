from setuptools import setup
from sikulpy.version import VERSION

setup(
    name='sikulpy',
    version=VERSION,
    description='An implementation of Sikuli for CPython',
    long_description='',
    author='Shish',
    author_email='webmaster@shishnet.org',
    install_requires=[
        "pyscreenshot",
        "autopy3",
        "pillow",
        "numpy",
        #"opencv",
    ],
    dependency_links = [
        "https://github.com/Riamse/autopy3/archive/12587da69a2b196e5a964c66246a80831f333de7.zip#egg=autopy3-0.51",
    ],
    url='https://github.com/shish/sikulpy',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
    ],
    packages=[
        "sikulpy",
        "sikuli",
        "sikuli.script",
    ],
    entry_points={
        'console_scripts': ['sikulpy = sikulpy.run:main'],
        'gui_script': []
    },
)
