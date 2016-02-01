from setuptools import setup
from sikuli import VERSION

setup(name='sikulpy',
      version=VERSION,
      description='An implementation of Sikuli for CPython',
      long_description='',
      author='Shish',
      author_email='webmaster@shishnet.org',
      install_requires=[
          "pyscreenshot",
          "autopy",
          "pillow",
          "numpy",
          #"opencv",
          ],
      url='https://github.com/shish/sikulpy',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3.5",
          "Topic :: Utilities",
          ],
      packages=["sikuli", "sikuli.script"],
      entry_points={
          'console_scripts': ['sikulpy = sikuli.run:main'],
          'gui_script': []
        },
)
