"""
Command line utility for GitHub daily work.
"""
import setuptools
import yogh

DEPENDENCIES = ["click", "requests", "tabulate"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=yogh.__application__,
    version=yogh.__version__,
    author="Adrien Gavignet",
    author_email="adrien.gavignet@gmail.com",
    license="Proprietary",
    description="Command line utility for GitHub daily work.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="git github utility branch pull requests",
    url="https://github.com/hasboeuf/yogh",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
    zip_safe=True,
    install_requires=DEPENDENCIES,
    entry_points={"console_scripts": ["yogh=yogh.yogh.cli:main"]},
)
