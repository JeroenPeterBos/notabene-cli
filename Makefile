.DEFAULT_GOAL := package
.PHONY: install publish package coverage test lint docs
PROJ_SLUG = notabene
CLI_NAME = notabene
PY_VERSION = 3.8


env:
	conda create -n $(PROJ_SLUG) python=$(PY_VERSION) pip -y
	conda run -n $(PROJ_SLUG) pip install pip-tools
	conda run -n $(PROJ_SLUG) pip-sync

install: 
	pip-sync

format:
	isort .
	black .

lint: format
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
	pip-licenses --with-url --format=rst --output-file docs/licenses.rst
