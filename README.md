# yogit

[![Build Status](https://dev.azure.com/hasboeuf/yogit/_apis/build/status/hasboeuf.yogit?branchName=master)](https://dev.azure.com/hasboeuf/yogit/_build/latest?definitionId=1&branchName=master)
[![Build Status](https://travis-ci.org/hasboeuf/yogit.svg?branch=master)](https://travis-ci.org/hasboeuf/yogit)
![License](https://img.shields.io/github/license/mashape/apistatus.svg)
[![PyPI version](https://badge.fury.io/py/yogit.svg)](https://pypi.org/project/yogit/)
[![Downloads](https://pepy.tech/badge/yogit)](https://pepy.tech/project/yogit)

Command line utility for git daily work.

## Requirements

* `Python3` and `pip3`
* `yogit` is tested with Python `3.5`, `3.6`, `3.7`
* `yogit` is mostly tested on `Linux` but unittests are passing on `Windows` and `macOS`.
* For now only GitHub API is supported

## Continuous integration

* [Azure Pipelines](https://dev.azure.com/hasboeuf/yogit)
* [TravisCI](https://travis-ci.org/hasboeuf/yogit)

## Installation

* `pip3 install yogit`
* `yogit account setup`

`yogit` internal files are stored in `~/.yogit` folder.

## Principle

`yogit` is able to:

* List pull requests
* List reviews
* List branches
* Get your daily activity report

See below for more details.

## Usage

`yogit --help`

## Account

`yogit account setup`: Setup yogit

`yogit account usage`: Account API usage

### Pull request

`yogit pr list`: List your opened pull requests

Options:

* `--orga TEXT`: Expand results to a specific organization

### Review

`yogit rv list`: List your reviews on opened pull requests

`yogit rv requested`: List pull requests where your review is requested

### Branch

`yogit br list`: List your branches

### SCRUM

`yogit scrum report`: Generate your daily activity report

Template of the report can be changed by editing `~/.yogit/scrum_report.yaml`

You might need to install `xcopy` to fully enjoy this command.
