from setuptools import setup

setup(
    name='sikulpy',
    version='0.0.0',
    description='An implementation of Sikuli for CPython',
    long_description='',
    author='Shish',
    author_email='webmaster@shishnet.org',
    install_requires=[
        "autopy3",
        "pillow",
        "numpy",
        "mss",
        #"opencv",
    ],
    url='https://github.com/shish/sikulpy',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
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
