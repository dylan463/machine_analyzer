Quick Start Guide
=================

This guide will help you get started with Machine Analyzer in just a few minutes.

Basic Usage
-----------

Load and Analyze Data
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from machine_analyzer import MachineDataLoader, StateDetector, CycleSegmenter, QualityAnalyzer

   # Load your energy consumption data
   loader = MachineDataLoader()
   loader.load_data(data_path="../data/Datadump.txt",format="json")
   
   # Preprocess the data (resample and fill the data)
   resampled = loader.preprocess_data(loader.dataframe,frequency="1s")
   
   # Detect machine states and remouve outlier
   detector = StateDetector(resampled)
   detector.preprocess_states(window_size="5s",production_threshold=60)

   # no-outliers data and states positions
   processed = detector.get_processed_data()
   states = detector.get_state_masks()
   
   # Segment production cycles
   segmenter = CycleSegmenter(processed,state_masks)
   segmenter.segment_cycles(min_duration="5s",max_duration=f'240s') # in secondes

   production_cycles = segmenter.get_cycles()
   cycles_stat = segmenter.get_cycle_statistics()
   
   # Analyze quality
   analyser = QualityAnalyzer(cycles_stat,production_cycles)
   analyser.analyze_quality()

   quality_metrics = analyser.get_quality_metrics()
   
   # reporrt generator
   reporter = ReportGenerator("../the/output/folder")
   report = reporter.generate_simple_report(processed, production_cycles, quality_metrics, anomaly)

   print(report)

Data Format
-----------

Your data should be in one of these formats:

**CSV Format:**
.. code-block:: csv

   timestamp,value
   2024-01-01 08:00:00,150.5
   2024-01-01 08:00:01,152.3
   2024-01-01 08:00:02,148.9

**Excel Format:**
Same structure as CSV, but in .xlsx or .xls files.

**Parquet Format:**
Optimized columnar format for large datasets.

Required Columns:
- `timestamp`: DateTime column with timestamps
- `value`: Numeric column with energy consumption values

Command Line Interface
---------------------

For quick analysis from the command line:

.. code-block:: bash

   # Basic analysis
   machine-analyzer analyze data.csv
   
   # With custom parameters
   machine-analyzer analyze data.csv --min-duration 30s --max-duration 2h
   
   # Generate reports
   machine-analyzer analyze data.csv --output-dir reports/
