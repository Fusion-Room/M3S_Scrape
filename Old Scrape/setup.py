from distutils.core import setup
import py2exe
import sys

# This is the setup file required to generate a windows app wrapper for the crawler script

setup( options = {

    }, console=['crawler.py'])
