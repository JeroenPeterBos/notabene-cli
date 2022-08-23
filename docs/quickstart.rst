.. _quickstart:

.. toctree::
    :glob:

**********
Quickstart
**********

The aim of this quickstart is to help you get up to speed with ``notabene``.
You can either introduce ``notabene`` to an existing or a new project.
Below we will describe what is a common workflow for using ``notabene``.


Installing the Library
======================

You can use pip to install ``notabene-cli``.

.. code-block:: sh

    pip install notabene-cli


Preparing your repository
=========================

Create a (possibly empty) ``pyproject.toml`` file in the root of your project.


*For now, it is fine if this file is empty, if you don't have any other tools interacting with it.*
An example of what the directory structure of your repository could look like after adding this file is:

::

    my-project-folder
    ├── config          
    │   └── settings.py
    ├── notebooks          
    │   ├── my-exploratory-data-analysis.ipynb
    │   └── my-deep-learning-research.ipynb
    ├── requirements.txt
    └── pyproject.toml


.. note:: What is this pyproject.toml file?

    The ``pyproject.toml`` file is very common file for configuring tools in python projects.
    By using a single file, cluttering from configuration tools is limited.
    If you would like to know more about this file you can read `the following page from the Python Packaging Authoroty <https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/>`_.

.. note:: How does NotaBene use the pyproject.toml file?

    **NotaBene** uses the ``pyproject.toml`` file to determine the root of your repository.
    All commands will be executed relative to this repository root.
    If you don't want to use this file, then all commands have the ability insert a root to execute the commands from using arguments. However, for you own sake, peace of mind and ease of use I would recommend against that.


NotaBene Templates
==================

Currently, ``notabene`` has a set of commands helping you to create and use notebook templates.


Creating a new template
-----------------------

To create a new template from an existing notebook named ``your-notebook.ipynb``, run:

.. code-block:: console

    notabene template create <your-notebook.ipynb>


Using an existing template
--------------------------

To make use of an existing template to create a new notebook named ``your-notebook.ipynb``, run:

.. code-block:: console

    notabene template use <your-notebook.ipynb>


Quality check all notebooks
---------------------------

Quality check all notebooks to make sure they all respect at least one of your templates.
Will fail if a notebook is found that does not respect any notebooks.
A common use-case is to include this step in your git project as a quality check for merge requests. 
(`GitLab CICD <https://docs.gitlab.com/ee/ci/>`_, `Github Actions <https://docs.github.com/en/actions>`_)

.. code-block:: console

    notabene template check


List the registered notebooks
-----------------------------

Show a list of the templates you registered in this project.

.. code-block:: console

    notabene template list
