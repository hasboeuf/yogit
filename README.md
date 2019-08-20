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
* `yogit` is mostly tested on `Linux` but also works on `macOS` and `Windows` (if using [Windows Terminal](https://github.com/microsoft/terminal)).
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

### Contributions

`yogit ct list [--from TEXT] [--to TEXT]`: List your GitHub contributions within a range of dates.

A contribution is either a pull request or pull request review.

By default this command is listing today's contributions.

`yogit ct stats`: Show some GitHub statistics.

### SCRUM

`yogit scrum report [--date TEXT]`: Generate your daily activity report

Template of the report can be changed by editing `~/.yogit/scrum_report.yaml`

You might need to install `xcopy` to fully enjoy this command.
