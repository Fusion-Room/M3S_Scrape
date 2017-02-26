from setuptools import setup

# This is the setup file required to generate a mac app wrapper for the crawler script

APP = ['crawler.py']
DATA_FILES = ['chromedriver']
OPTIONS = {'argv_emulation': False}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)