"""
A setuptools based setup module.

See:
 - https://packaging.python.org/en/latest/distributing.html
 - https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

setup(
    name="pylog",
    version="0.0.1",
    description="Simple Python logging library",
    url="https://github.com/jimlawton/pylog",
    author="Jim Lawton",
    author_email="jim.lawton@gmail.com",
    license="GPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: GPL",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux"
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*'])
)
