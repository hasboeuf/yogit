# yogit

## Unittests

### CI

Run by Travis CI, have a look to `.travis.yml` if you are curious.

### Local run

`pip3 install -r requirements/tests.txt`
`pytest -vv -s yogit/tests`

## Code sanity

Coding style is handled by `black` (via `ci/blackify`).
Static checks are handled by `pylint` (via `ci/pylintify`).

You must `pip3 install -r requirements/codesanity.txt` to use those scripts.

Note: continuous integration does not check code sanity.

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
python3 setup.py sdist bdist_wheel
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
python3 setup.py sdist bdist_wheel
twine upload dist/*
pip3 install yogit
yogit --help
python3 -c "import yogit"
```
