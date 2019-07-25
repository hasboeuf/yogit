"""
Command line utility for GitHub daily work.
"""
import setuptools
import yogit

DEPENDENCIES = ["click", "halo", "packaging", "PyYAML>=5.1", "pyperclip", "requests", "requests-toolbelt", "tabulate"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=yogit.__application__,
    version=yogit.__version__,
    author="Adrien Gavignet",
    author_email="adrien.gavignet@gmail.com",
    license="MIT",
    description="Command line utility for GitHub daily work.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="git github utility branch pull requests",
    url="https://github.com/hasboeuf/yogit",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests"]),
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
    zip_safe=True,
    install_requires=DEPENDENCIES,
    entry_points={"console_scripts": ["yogit=yogit.yogit.cli:main"]},
)
