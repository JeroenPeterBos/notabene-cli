.DEFAULT_GOAL := package
.PHONY: install publish package coverage test lint docs
PROJ_SLUG = notabene
CLI_NAME = notabene
PY_VERSION = 3.8


env:
	conda env create -f environment.yml

install: 
	pip install -r requirements.txt

lint:
	flake8p $(PROJ_SLUG)

test: lint
	pytest

coverage: test
	coverage html

docs: test licenses
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

licenses:
	pip-licenses
	pip-licenses --with-url --format=rst --output-file docs/licenses.rst
