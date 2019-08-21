# Changelog

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
