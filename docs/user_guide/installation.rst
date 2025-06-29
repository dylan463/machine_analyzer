Installation
============

Requirements
------------

* Python 3.8 or higher
* pip (Python package installer)

Basic Installation
------------------

Install the latest stable version from PyPI:

.. code-block:: bash

   pip install machine-analyzer

Installation Options
--------------------

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For development and contributing to the project:

.. code-block:: bash

   pip install machine-analyzer[dev]

This includes additional development tools:
* pytest (testing framework)
* black (code formatting)
* isort (import sorting)
* flake8 (linting)
* mypy (type checking)
* pre-commit (git hooks)

Documentation Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~

For building documentation locally:

.. code-block:: bash

   pip install machine-analyzer[docs]

This includes:
* sphinx (documentation generator)
* sphinx-rtd-theme (Read the Docs theme)
* myst-parser (Markdown support)
* sphinx-autodoc-typehints (type hints in docs)

Notebook Installation
~~~~~~~~~~~~~~~~~~~~~

For Jupyter notebook support:

.. code-block:: bash

   pip install machine-analyzer[notebooks]

This includes:
* jupyter (notebook interface)
* jupyterlab (modern notebook interface)
* seaborn (statistical visualization)
* plotly (interactive plots)

Full Installation
~~~~~~~~~~~~~~~~~

For all features and tools:

.. code-block:: bash

   pip install machine-analyzer[full]

Installation from Source
------------------------

Clone the repository and install in development mode:

.. code-block:: bash

   git clone https://github.com/dylan463/machine-analyzer.git
   cd machine-analyzer
   pip install -e .
