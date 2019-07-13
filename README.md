# yogit

[![Build Status](https://travis-ci.org/hasboeuf/yogit.svg?branch=master)](https://travis-ci.org/hasboeuf/yogit)
![License](https://img.shields.io/github/license/mashape/apistatus.svg)
[![PyPI version](https://badge.fury.io/py/yogit.svg)](https://pypi.org/project/yogit/)

Command line utility for git daily work.

## Requirements

* `Python3` and `pip3`
* `yogit` is tested with Python 3.5 and 3.6
* For now it has only been tested on Linux
* For now only GitHub API is supported

## Installation

* `pip3 install yogit`
* `yogit account setup`

`yogit` internal files are stored in `~/.yogit` folder.

## Principle

`yogit` is able to:

* List your pull requests
* List reviews you need to look into
* List your branches
* Get your GitHub contributions of the day

## Usage

`yogit --help`

### Pull request

`yogit pr list`

### Review

`yogit rv requested`

### Branch

`yogit br list`

### SCRUM

`yogit scrum report`

Template of the report can be changed by editing `~/.yogit/scrum_report.yaml`

You might need to install `xcopy` to fully enjoy this command.
