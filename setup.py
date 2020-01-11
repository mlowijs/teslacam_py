from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="teslacam_py",
    version="0.0.1",
    description="TeslaCam uploader",
    long_description=long_description,
    long_description_content_type="text/markdown",
)