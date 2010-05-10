from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
setup(
    name = "epic",
    version = "0.3",
    packages = find_packages(),
    scripts = ['StartMain.py'],
)

