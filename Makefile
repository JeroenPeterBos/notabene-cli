.DEFAULT_GOAL := help
.PHONY: install destroy format lint test tox coverage licenses docs package publish clean
PROJ_SLUG = notabene
PY_VERSION = 3.8
CONDA_BASE_PATH=$$(conda info --base)


$(CONDA_BASE_PATH)/envs/$(PROJ_SLUG)/bin/python:
	conda create -n $(PROJ_SLUG) python=$(PY_VERSION) pip -y
	conda run -n $(PROJ_SLUG) pip install pip-tools

install: $(CONDA_BASE_PATH)/envs/$(PROJ_SLUG)/bin/python  ## Create the environment and install all dependencies
	conda run -n $(PROJ_SLUG) pip-sync

destroy:  ## Remove the conda environment (make sure it is deactivated)
	conda remove -n $(PROJ_SLUG) --all -y 

format:  ## Format all code and sort imports
	isort .
	black .

lint: format  ## Apply the linters to the project
	flake8p $(PROJ_SLUG) tests
	pylint $(PROJ_SLUG) tests

test: format  ## Run all the tests
	pytest --cov=$(PROJ_SLUG) --cov-fail-under=0

tox:  ## Run all test in several environments with varying dependency versions
	tox -p

coverage: test  ## Generate an HTML coverage report
	coverage html

licenses: docs/licenses.rst  ## Generate licenses from the dependencies
docs/licenses.rst:
	pip-licenses --with-url --format=rst --output-file docs/licenses.rst

docs: lint docs/licenses.rst  ## Generate the documentation
	sphinx-build -b html "docs" "build/docs"

package: clean docs ## tox  ## Package this project / create the distributable
	python setup.py sdist --dist-dir build/dist

publish: package  ## Publish this package to PyPI using twine
	twine upload -r testpypi build/dist/*

clean:  ## Clean the project by deleting temporary files and caches
	rm -rf build
	rm -rf *.egg-info
	rm -rf */__pycache__

COMMAND_TEXT_WIDTH=15
help: ## Show this help message
	@printf "\033[1;36mMakefile of the ${PROJ_SLUG} project. The following commands are available:\033[0m\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-${COMMAND_TEXT_WIDTH}s \033[0m %s\n", $$1, $$2}'