from setuptools import setup, find_namespace_packages
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
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src', include=['teslacam', 'teslacam.*']),
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=5.3",
        "azure-storage-blob>=12.1.0",
        "sh>=1.12.14",
        "flask>=1.1.1"
    ],
    scripts=['src/main.py']
)