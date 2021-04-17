import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="autoYT",
    version="1.0.0",
    description="autoYT is lightweight library that automates downloading of youtube videos, subtitles (if available) and playlist.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/umutambyi-gad/autoYT",
    author="Umutambyi Gad",
    author_email="umutambyig@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["autoYT"],
    include_package_data=True,
    install_requires=["pytube"],
)