API Reference
=============

This section contains the complete API reference for Machine Analyzer.

The main modules are:

* **MachineDataLoader**: Load and preprocess energy data from various file formats
* **StateDetector**: Detect machine states (off, standby, production) from energy data
* **CycleSegmenter**: Segment production cycles from state masks
* **QualityAnalyzer**: Analyze cycle quality and detect anomalies
* **ReportGenerator**: Generate analysis reports in text and CSV formats

For detailed API documentation, please refer to the source code or use Python's built-in help system:

.. code-block:: python

   from machine_analyzer import MachineDataLoader, StateDetector, CycleSegmenter, QualityAnalyzer, ReportGenerator
   
   help(MachineDataLoader)
   help(StateDetector)
   help(CycleSegmenter)
   help(QualityAnalyzer)
   help(ReportGenerator)
