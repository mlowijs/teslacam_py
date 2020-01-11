from setuptools import setup, find_packages

setup(
    name="teslacam_py",
    version="0.1.3",
    description="TeslaCam uploader",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=5.3",
        "azure-storage-blob>=12.1.0",
        "sh>=1.12.14",
        "flask>=1.1.1"
    ],
    entry_points={"console_scripts": ["teslacam = teslacam.__main__:main"]}
)