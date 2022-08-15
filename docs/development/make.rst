.. _make:

.. toctree::
    :glob:

.. _using-the-makefile:

Using the `Makefile`
====================

This project includes a `Makefile <https://www.gnu.org/software/make/>`_
that you can use to perform common tasks such as running tests and building
documentation.

Targets
-------

This section contains a brief description of the targets defined in the ``Makefile``.

``make install``
^^^^^^^^^^^^^^^^

Create the environment and install development dependencies


``make destroy``
^^^^^^^^^^^^^^^^

Remove the conda environment. __Deactivate the conda environment before you run this command.__


``make format``
^^^^^^^^^^^^^^^

Format all code and sort all imports.


.. _make_lint:

``make lint``
^^^^^^^^^^^^^

Run `pylint <https://www.pylint.org/>`_ and `flake8 <https://flake8.pycqa.org/en/latest/>` against the project files.


.. _make_test:

``make test``
^^^^^^^^^^^^^

Run the unit tests.


``make tox``
^^^^^^^^^^^^

Run all tests in several conda environments with varying dependencies and python versions.


``make coverage``
^^^^^^^^^^^^^^^^^

Generate an HTML coverage report. The report will be placed under `build/coverage/index.html`.


``make licenses``
^^^^^^^^^^^^^^^^^

Generate a table of licenses from the dependencies to be included in the public documentation.

.. note::

    If project dependencies change, please update this documentation.


.. _make_docs:

``make docs``
^^^^^^^^^^^^^

Build the public documentation.


``make package``
^^^^^^^^^^^^^^^^

Build the package for publishing.


.. _make-publish:

``make publish``
^^^^^^^^^^^^^^^^

Publish the package to PyPI using twine.


``make clean``
^^^^^^^^^^^^^^

Clean the project by deleting temporary files and local caches.

