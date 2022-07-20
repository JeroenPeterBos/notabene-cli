# .DEFAULT_GOAL := package
# .PHONY: install publish package coverage test lint docs
PROJ_SLUG = notabene
PY_VERSION = 3.8
CONDA_BASE_PATH=$$(conda info --base)


$(CONDA_BASE_PATH)/envs/$(PROJ_SLUG)/bin/python:
	conda create -n $(PROJ_SLUG) python=$(PY_VERSION) pip -y
	conda run -n $(PROJ_SLUG) pip install pip-tools

install: $(CONDA_BASE_PATH)/envs/$(PROJ_SLUG)/bin/python
	conda run -n $(PROJ_SLUG) pip-sync

destroy:
	conda remove -n $(PROJ_SLUG) --all -y 

hi:
	echo $(CONDA_BASE_PATH)/envs/$(PROJ_SLUG)/bin/python

format:
	isort .
	black .

lint: format
	flake8p $(PROJ_SLUG) tests
	pylint $(PROJ_SLUG) tests

test: format
	pytest --cov=$(PROJ_SLUG)

coverage: test
	coverage html

docs: test lint licenses
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
