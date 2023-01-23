"""Python setup.py for pyzandro package"""
import io
import os
from setuptools import find_packages, setup

setup(
    name="pyzandro",
    version='0.1.0',
    description="Querying tool for Zandronum servers",
    url="https://github.com/klaufir216/pyzandro/",
    author="klaufir216",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    extras_require={"test": ["pytest"]},
)
