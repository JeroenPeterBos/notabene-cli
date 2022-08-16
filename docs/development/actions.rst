.. toctree::
    :glob:

**************
Github Actions
**************

We make use of Github Actions for the automation in this project.
Currently, we have three workflows:

- Code Quality
- Platform Tests
- Publish PyPI


Code Quality
============

Triggered upon push to ``main`` and pull requests into ``main``.

The code quality pipeline, defined in `.github/workflows/code-quality.yaml` runs some check to verify the quality of the code.
Among others it does linting using `pylint` and `flake8`, formatting using `isort` and `black`, run all of the tests using `pytest` and do a `coverage` analysis.


Platform Tests
==============

Triggered upon push to ``main`` and pull requests into ``main`` with the tag ``platform-test`` applied. (apply this tag to trigger the platform tests)

The platform tests pipeline, defined in `.github/workflows/code-quality.yaml` runs the tests on a wide range of platforms and environments.
The tests are run on linux, windows and macos machines. 
On each of these platforms we run te tests on python ``3.6``, ``3.7``, ``3.8`` and then we use several versions of ``click`` with version larger or equal to ``7.0``.


Publish PyPI
============

Triggered when a new tag is applied to a commit, the tag should have the shape ``v0.0.0``. If the tag version does not the version in the code, the pipeline fails.

The publish PyPI workflow builds the package, tries to upload the package to a test PyPI server and if all succeeds, uploads the package to PyPI.