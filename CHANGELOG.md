# Changelog

## 1.13.0

* Improve `yogit scrum report`: list contributions before completing the report
* Slack post now handles correctly #channel mentions (member mentions is not working yet)

## 1.12.3

* Fix config file loading: do not raise an error when file does not exist

## 1.12.2

* Fix scrum report template migration of `yogit 1.12.0`. If you encountered the bug, remove `~/.yogit/scrum_report.yaml` to get the default one back

## 1.12.1

* Fix `yogit orga member ...` command: GitHub API became less permissive about param types

## 1.12.0

* Add `--label` filter to `yogit pr list` command
* Add Slack integration: thanks @thomascarpentier for this contribution sponsored by Genymobile for #hacktoberfest. It allows `yogit scrum report` to publish the report on Slack on your behalf. To configure it: `yogit account setup`

## 1.11.0

* Change `yogit review requested` output: print pull request title, don't print repository url anymore
* Add `--missed` option to `yogit review requested` command

## 1.10.0

* Add `yogit br` becomes `yogit branch` command
* Add `yogit rv` becomes `yogit review` command

## 1.9.0

* Add `yogit orga list` command
* Add `--orga` discrimator option to `yogit orga member list`
* Add `--orga` discrimator option to `yogit orga member pickone`
* Improve doc regarding auto completion

## 1.8.0

* Add `yogit orga member list` command
* Add `yogit orga member pickone` command
* Add `--dangling` option to `yogit br list`
* `yogit ct` command is renamed to `yogit contrib`
* Improve update warning wording
* Improve `yogit --version` wording

## 1.7.2

* Fix `yogit` upgrade from `1.6.0`

## 1.7.1

* Shit happens

## 1.7.0

* Add `yogit ct stats` command

## 1.6.0

* Add `yogit ct list` command
* Add `--date` arg to `yogit scrum report` command
* Add indentation ability to `yogit scrum report`
* Print pretty bullet points in generated scrum report
* Improve documentation

## 1.5.1

* Replace `yaspin` by `Halo` dep to handle spinner: better handling of pipes and redirects

## 1.5.0

* Tried `yogit` on Windows Terminal and workaround a spinner issue
* Print count little by little if request is big

## 1.4.1

* Fix missing `packaging` dependency

## 1.4.0

* See if pull requests are conflicted in `yogit pr list`
* Improve `yogit scrum report` UX and make it robust to network access failure
* Shorten PR titles in tabulated results (max 50 chars)

## 1.3.0

* Add update available check

## 1.2.1

* Improve help

## 1.2.0

* Add ability to list your current reviews and see outdated ones with `yogit rv list`
* Dedicated wording when there is no result
* Add "Count: X" statement right after result list
* Show a spinner during request time
* Use bold and emojis to make outputs fancier

## 1.1.1

* Reinforce `scrum report` command (better error handling)

## 1.1.0

* Add abilitiy to list pull requests of an organization `yogit pr list --orga TEXT`

## 1.0.4

* Fix typo in scrum report, thx @genygilles

## 1.0.3

* Fix unauthorized error due to too old PyYAML version

## 1.0.2

* Support pagination for branch listing (fix request timeout)

## 1.0.1

* Be more specific on GitHub required scopes
* Improve code regarding account setup flow
* Fix sort of pull request list

## 1.0.0

* Project bootstrap
