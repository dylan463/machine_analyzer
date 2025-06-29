Contributing to Machine Analyzer
================================

Thank you for your interest in contributing to Machine Analyzer! This document provides guidelines and information for contributors.

Getting Started
--------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a virtual environment**:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

4. **Install in development mode**:

   .. code-block:: bash

      pip install -e ".[dev,docs,notebooks]"

5. **Install pre-commit hooks**:

   .. code-block:: bash

      pre-commit install

Development Setup
----------------

Code Style
~~~~~~~~~~

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run these tools before committing:

.. code-block:: bash

   black machine_analyzer tests
   isort machine_analyzer tests
   flake8 machine_analyzer tests
   mypy machine_analyzer

Or use pre-commit to run them automatically:

.. code-block:: bash

   pre-commit run --all-files

Testing
-------

Run the test suite:

.. code-block:: bash

   pytest

Run with coverage:

.. code-block:: bash

   pytest --cov=machine_analyzer --cov-report=html

Run specific test categories:

.. code-block:: bash

   pytest -m "not slow"  # Skip slow tests
   pytest -m unit        # Run only unit tests
   pytest -m integration # Run only integration tests

Documentation
------------

Build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The documentation will be available in `docs/_build/html/`.

Writing Documentation
~~~~~~~~~~~~~~~~~~~~

- Use clear, concise language
- Include code examples
- Follow the existing style
- Use proper RST syntax
- Add type hints to all functions

Making Changes
--------------

1. **Create a feature branch**:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes** following the coding standards
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Run the test suite** to ensure everything works
6. **Commit your changes** with a descriptive message

Commit Messages
~~~~~~~~~~~~~~

Follow conventional commit format:

.. code-block:: bash

   feat: add new feature for cycle detection
   fix: resolve issue with outlier removal
   docs: update installation instructions
   test: add tests for quality analyzer
   refactor: improve state detection algorithm

Pull Request Process
-------------------

1. **Push your branch** to your fork
2. **Create a pull request** on GitHub
3. **Fill out the PR template** with:
   - Description of changes
   - Related issue number
   - Type of change (bug fix, feature, etc.)
   - Testing performed
4. **Wait for review** and address feedback
5. **Merge** when approved

Issue Reporting
--------------

When reporting issues, please include:

- **Description**: Clear description of the problem
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: Python version, OS, package versions
- **Code example**: Minimal code to reproduce the issue

Feature Requests
---------------

When requesting features, please include:

- **Use case**: Why this feature is needed
- **Proposed solution**: How you think it should work
- **Alternatives considered**: Other approaches you've considered
- **Impact**: How this would benefit users

Code of Conduct
---------------

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community
- Show empathy towards other community members

Getting Help
-----------

If you need help with contributing:

1. Check the existing documentation
2. Look at existing issues and pull requests
3. Ask questions in GitHub Discussions
4. Contact the maintainers

Thank you for contributing to Machine Analyzer! 