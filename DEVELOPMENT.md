# yogit

## Local environment

```bash
pip3 install -r requirements/yogit.txt -r requirements/tests.txt -r requirements/codesanity.txt
pip3 install -e .
```

Run unittests: `pytest -vv -s yogit/tests`

Check code coverage: `pytest --cov=yogit yogit/tests`

Coding style: handled by `black` (via `ci/blackify`) and enforced by CI.

Static checks: handled by `pylint` (via `ci/pylintify`).

## Continuous integration

Handled by Travis CI and Azure Pipelines.
Responsible of:

* Passing unittests
* Checking coding style
* Releasing

## Release procedure

* Bump version
* Update CHANGELOG.md
* Push a new tag

### Publish via TravisCI

TravisCI automatically publish `yogit` on PyPI when a tag is pushed.

Password in `.travis.yml` has been encrypted with:

`travis encrypt <password> --add deploy.password`

### Publish manually

* Deploy on Test PyPI

```bash
pip3 uninstall yogit
git clean -d --force --dry-run
git clean -d --force
python3 setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip3 install --index-url https://test.pypi.org/simple/ --no-deps yogit
yogit --help
python3 -c "import yogit"
```

* Deploy on PyPI

```bash
pip3 uninstall yogit
git clean -d --force --dry-run
git clean -d --force
python3 setup.py sdist
twine upload dist/*
pip3 install yogit
yogit --help
python3 -c "import yogit"
```
