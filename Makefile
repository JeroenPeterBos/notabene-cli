.DEFAULT_GOAL := package
.PHONY: install publish package coverage test lint docs
PROJ_SLUG = notabene
CLI_NAME = notabene
PY_VERSION = 3.8


install: 
	conda env create -f environment.yml

lint:
	flake8 $(PROJ_SLUG)

test: lint
	pytest --cov-report term --cov=$(PROJ_SLUG) tests/

coverage: lint
	pytest --cov-report html:build/coverage/html --cov=$(PROJ_SLUG) tests/
	coverage erase

docs: coverage licenses
	sphinx-build -b html "docs" "build/docs"

package: clean docs
	python setup.py sdist --dist-dir build/dist
	rm -rf *.egg-info

publish: package
	twine upload -r testpypi build/dist/*

clean:
	rm -rf build
	rm -rf *.egg-info
	rm -rf */__pycache__
	coverage erase

licenses:
	pip-licenses
	pip-licenses --with-url --format=rst --output-file docs/licenses.rst
