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

### Auto completion

`yogit` supports auto-completion. To activate it, you need to setup your shell.

* For Bash, edit your `.bashrc` and add `eval "$(_YOGIT_COMPLETE=source yogit)"`
* For Zsh, edit your `.zshrc` and add `eval "$(_YOGIT_COMPLETE=source_zsh yogit)"`

## Principle

`yogit` is able to:

* Show pull requests
* Show pull request reviews
* Show branches
* Show contributions
* Show organization's information
* Help in writing a daily scrum report and post it on Slack

See documentation below for more details.

## Documentation

### Usage

`yogit --help`

### Account

`yogit account setup`: Setup yogit (include GitHub integration and optionnaly Slack integration to fully enjoy `yogit scrum report` command)

`yogit account usage`: Account API usage

### Pull request

`yogit pr list [--orga TEXT] [--label TEXT]`: List your opened pull requests. If `--orga` is set, results will be expanded to this specific organization. If `--label` is set, results will be filtered by pull request labels, you can set multiple `--label`.

### Review

`yogit review list`: List your reviews on opened pull requests

`yogit review requested [--missed]`: List pull requests where your review is requested. If `--missed` is set, only closed pull requests will be listed.

### Branch

`yogit branch list [--dangling]`: List your branches. If `--dangling` is set, only branches without associated pull request will be listed.

### Contributions

`yogit contrib list [--from TEXT] [--to TEXT]`: List your GitHub contributions within a range of dates.

A contribution is either a pull request or pull request review.

By default this command is listing today's contributions.

`yogit contrib stats`: Show some GitHub statistics.

### Organization

`yogit orga list`: List organizations you belong to.

`yogit orga member list [--orga TEXT]`: List members of one organization you belong to.

`yogit orga member pickone [--orga TEXT]`: Randomly pick one member of one organization you belong to.

### SCRUM

`yogit scrum report [--date TEXT]`: Generate your daily activity report

If Slack integration is setup, report can be published on Slack. Note that report is composed of one or more sections, first section will published as a message, next section will be published as a reply of the first one.

Template of the report can be changed by editing `~/.yogit/scrum_report.yaml`

You might need to install `xcopy` to fully enjoy this command.
