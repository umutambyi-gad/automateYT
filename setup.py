import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

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
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'autoYT = autoYT:main',
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
    ],
    packages=["autoYT"],
    include_package_data=True,
    install_requires=["pytube"],
    keywords=["automate", "youtube", "download", "download_playlist", "download_subtitle", "generate_watch_url_from_playlist",],
)
