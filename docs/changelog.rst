Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

Added
~~~~~

- Comprehensive package configuration with pyproject.toml
- Sphinx documentation setup
- Pre-commit hooks configuration
- Enhanced testing framework
- Code quality tools (black, isort, flake8, mypy)
- Development and documentation dependencies

Changed
~~~~~~~

- Updated dependencies to latest stable versions
- Improved project structure and metadata
- Enhanced setup.py with better classifiers and keywords

[1.0.0] - 2025-06-27
--------------------

Added
~~~~~

- Initial release of Machine Analyzer
- Core modules for machine energy analysis:
  - ``machine_data_loader``: Data loading and preprocessing
  - ``state_detector``: Machine state detection
  - ``cycle_segmenter``: Production cycle segmentation
  - ``quality_analyzer``: Quality assessment and anomaly detection
  - ``report_generator``: Report generation
- Comprehensive test suite
- Example usage and notebooks
- Basic documentation

Features
~~~~~~~~

- Automatic outlier detection and removal
- Production cycle identification
- Quality scoring and grading (A, B, C, D)
- Anomaly detection in production cycles
- Multiple report formats (text, CSV)
- Command-line interface for batch processing
- Support for various data formats (CSV, Excel, Parquet)

Technical
~~~~~~~~~

- Python 3.8+ compatibility
- Pandas and NumPy for data processing
- Scikit-learn for machine learning algorithms
- Matplotlib for visualization
- Comprehensive error handling and logging 