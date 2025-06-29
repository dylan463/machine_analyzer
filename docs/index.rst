Machine Analyzer Documentation
==============================

.. image:: https://img.shields.io/badge/Python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.8+

.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT License

.. image:: https://img.shields.io/badge/Version-1.0.0-orange.svg
   :target: https://github.com/dylan463/machine-analyzer
   :alt: Version 1.0.0

A comprehensive machine energy consumption analysis library for production cycle detection and quality assessment.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide/index
   api_reference/index
   examples/index
   contributing
   changelog

Features
--------

* **Data Loading & Preprocessing**: Support for multiple data formats (CSV, Excel, Parquet) with automatic outlier detection
* **State Detection**: Intelligent detection of machine states (production, standby, idle)
* **Cycle Segmentation**: Automatic identification and segmentation of production cycles
* **Quality Assessment**: Comprehensive quality scoring and grading system (A, B, C, D)
* **Anomaly Detection**: Advanced anomaly detection in production cycles
* **Report Generation**: Multiple report formats (text, CSV) with detailed statistics

Quick Installation
------------------

.. code-block:: bash

   pip install machine-analyzer

For development installation:

.. code-block:: bash

   pip install machine-analyzer[dev]

For documentation:

.. code-block:: bash

   pip install machine-analyzer[docs]

Quick Example
------------

.. code-block:: python

   from machine_analyzer import MachineDataLoader, StateDetector, CycleSegmenter, QualityAnalyzer

   # Load and preprocess data
   loader = MachineDataLoader()
   data = loader.load_data("energy_data.csv",format = "csv")
   processed_data = loader.preprocess_data(data)

   # Detect machine states
   detector = StateDetector(processed_data)
   states = detector.preprocess_states()

   # Segment production cycles
   segmenter = CycleSegmenter(processed_data, states)
   cycles = segmenter.segment_cycles()

   # Analyze quality
   analyzer = QualityAnalyzer(cycles)
   quality_metrics = analyzer.analyze_quality()

   print(f"Detected {len(cycles)} production cycles")
   print(f"Quality score: {quality_metrics.average_score:.2f}")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 