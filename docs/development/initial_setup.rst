.. _getting_started_dev:

.. toctree::
    :glob:

*************
Initial Setup
*************

This section provides instructions for setting up your development environment.  If you follow the
steps from top to bottom you should be ready to roll by the end.


Get the Source Code
===================

The source code for the `notabene-cli` project lives at
`github <https://github.com/JeroenPeterBos/notabene-cli>`_.  
You can use `git clone` to get it.

.. code-block:: bash

    git clone https://github.com/JeroenPeterBos/notabene-cli


Create the Virtual Environment
==============================

You can create a virtual environment and install the project's dependencies using :ref:`make <make>`.

.. code-block:: bash

    make install
    conda activate notabene


Try It Out
==========

One way to test out the environment is to run the tests.  You can do this with the `make test`
target.

.. code-block:: bash

    make test

If the tests run and pass, you're ready to roll.


Getting Documentation
=====================

Once the environment is set up, you can generate the documentation for the most recent version of the code.
Afterwards the documentation will be available in `build/docs/index.html`.

.. code-block:: bash

    make docs
