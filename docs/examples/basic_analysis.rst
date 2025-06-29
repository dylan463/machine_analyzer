Basic Analysis Example
======================

This example demonstrates a complete end-to-end analysis of machine energy data using Machine Analyzer.

Setup
-----

First, ensure you have the required dependencies installed:

.. code-block:: bash

   pip install machine-analyzer[dev]

Import the necessary modules:

.. code-block:: python

   from machine_analyzer import (
       MachineDataLoader, 
       StateDetector, 
       CycleSegmenter, 
       QualityAnalyzer, 
       ReportGenerator
   )
   import pandas as pd
   import numpy as np

Data Preparation
----------------

For this example, we'll create synthetic data that mimics real machine energy consumption patterns:

.. code-block:: python

   # Create synthetic energy data
   np.random.seed(42)
   timestamps = pd.date_range('2023-01-01', periods=10000, freq='1s')
   
   energy_values = []
   for i in range(10000):
       if i % 1000 < 100:  # Production cycles (every 1000 samples, 100 samples of production)
           energy = 25.0 + np.random.normal(0, 2.0)
       elif i % 1000 < 200:  # Standby periods
           energy = 2.0 + np.random.normal(0, 0.5)
       else:  # Off periods
           energy = 0.0 + np.random.normal(0, 0.1)
       energy_values.append(max(0, energy))
   
   # Create DataFrame
   energy_data = pd.DataFrame({
       'value': energy_values
   }, index=timestamps)
   
   # Save to CSV for analysis
   energy_data.to_csv('example_energy_data.csv', index=True)
   
   print(f"Created synthetic data with {len(energy_data)} samples")
   print(f"Time range: {energy_data.index[0]} to {energy_data.index[-1]}")

Step 1: Load Data
-----------------

Load the energy consumption data:

.. code-block:: python

   # Initialize data loader
   loader = MachineDataLoader()
   
   # Load the data
   data = loader.load_data("example_energy_data.csv")
   
   print(f"Loaded {len(data)} data points")
   print(f"Columns: {list(data.columns)}")
   print(f"Data types: {data.dtypes}")

Step 2: Detect Machine States
-----------------------------

Detect the different states of the machine (off, standby, production):

.. code-block:: python

   # Initialize state detector
   detector = StateDetector(data, "value")
   
   # Detect states with custom parameters
   state_masks = detector.detect_states(
       window_size=200,           # Rolling window size
       production_threshold=5.0,  # Energy threshold for production state
       keep_threshold_column=False
   )
   
   # Get state distribution
   state_distribution = detector.get_state_distribution()
   print("State distribution:")
   for state, count in state_distribution.items():
       print(f"  {state}: {count} samples")
   
   # Get processed data with state information
   processed_data = detector.get_processed_data()
   print(f"Processed data shape: {processed_data.shape}")

Step 3: Segment Production Cycles
---------------------------------

Identify and segment individual production cycles:

.. code-block:: python

   # Initialize cycle segmenter
   segmenter = CycleSegmenter(data, state_masks, "value")
   
   # Segment cycles with duration constraints
   production_cycles = segmenter.segment_cycles(
       min_duration="5s",   # Minimum cycle duration
       max_duration="300s"  # Maximum cycle duration
   )
   
   print(f"Detected {len(production_cycles)} production cycles")
   
   # Get cycle statistics
   cycle_statistics = segmenter.get_cycle_statistics()
   print("\nCycle Statistics:")
   print(f"  Total cycles: {cycle_statistics['total_cycles']}")
   print(f"  Average duration: {cycle_statistics['duration_stats']['mean']:.1f} seconds")
   print(f"  Average energy: {cycle_statistics['energy_stats']['mean']:.1f}")
   
   # Get cycles as DataFrame for analysis
   cycles_df = segmenter.get_cycles_dataframe()
   print(f"\nCycles DataFrame shape: {cycles_df.shape}")
   print(cycles_df.head())

Step 4: Analyze Quality
-----------------------

Analyze the quality of production cycles and detect anomalies:

.. code-block:: python

   # Initialize quality analyzer
   analyzer = QualityAnalyzer(cycle_statistics, production_cycles)
   
   # Analyze quality with custom thresholds
   quality_metrics = analyzer.analyze_quality({
       "variation": 2.0,  # Standard deviations for variation
       "duration": 2.0,   # Standard deviations for duration
       "energy": 2.0      # Standard deviations for energy
   })
   
   # Get anomalous units
   anomalous_units = analyzer.get_anomalous_units()
   
   # Get quality summary
   quality_summary = analyzer.get_quality_summary()
   
   print(f"Quality Analysis Results:")
   print(f"  Total cycles analyzed: {quality_summary['total_cycles']}")
   print(f"  Anomalous cycles: {quality_summary['anomalous_cycles']}")
   print(f"  Average quality score: {quality_summary['average_quality_score']:.2f}")
   print(f"  Quality grade distribution: {quality_summary['quality_grade_distribution']}")

Step 5: Generate Report
-----------------------

Generate a comprehensive analysis report:

.. code-block:: python

   # Initialize report generator
   report_gen = ReportGenerator(output_dir="reports/")
   
   # Generate simple text report
   report_path = report_gen.generate_simple_report(
       data, 
       production_cycles, 
       quality_metrics, 
       anomalous_units
   )
   
   print(f"Report generated: {report_path}")
   
   # Generate CSV report
   csv_report_path = report_gen.generate_csv_report(
       production_cycles, 
       quality_metrics
   )
   
   print(f"CSV report generated: {csv_report_path}")

Complete Example Script
-----------------------

Here's the complete script that you can run:

.. code-block:: python

   from machine_analyzer import (
       MachineDataLoader, 
       StateDetector, 
       CycleSegmenter, 
       QualityAnalyzer, 
       ReportGenerator
   )
   import pandas as pd
   import numpy as np

   def run_basic_analysis():
       """Run complete basic analysis pipeline."""
       
       # Create synthetic data
       np.random.seed(42)
       timestamps = pd.date_range('2023-01-01', periods=10000, freq='1s')
       energy_values = []
       for i in range(10000):
           if i % 1000 < 100:
               energy = 25.0 + np.random.normal(0, 2.0)
           elif i % 1000 < 200:
               energy = 2.0 + np.random.normal(0, 0.5)
           else:
               energy = 0.0 + np.random.normal(0, 0.1)
           energy_values.append(max(0, energy))
       
       energy_data = pd.DataFrame({'value': energy_values}, index=timestamps)
       energy_data.to_csv('example_energy_data.csv', index=True)
       
       # Load data
       loader = MachineDataLoader()
       data = loader.load_data("example_energy_data.csv")
       
       # Detect states
       detector = StateDetector(data, "value")
       state_masks = detector.detect_states(window_size=200, production_threshold=5.0)
       
       # Segment cycles
       segmenter = CycleSegmenter(data, state_masks, "value")
       production_cycles = segmenter.segment_cycles(min_duration="5s", max_duration="300s")
       cycle_statistics = segmenter.get_cycle_statistics()
       
       # Analyze quality
       analyzer = QualityAnalyzer(cycle_statistics, production_cycles)
       quality_metrics = analyzer.analyze_quality()
       anomalous_units = analyzer.get_anomalous_units()
       quality_summary = analyzer.get_quality_summary()
       
       # Generate report
       report_gen = ReportGenerator(output_dir="reports/")
       report_path = report_gen.generate_simple_report(
           data, production_cycles, quality_metrics, anomalous_units
       )
       
       # Print summary
       print("=== ANALYSIS SUMMARY ===")
       print(f"Data points: {len(data)}")
       print(f"Production cycles: {len(production_cycles)}")
       print(f"Anomalous cycles: {len(anomalous_units)}")
       print(f"Average quality score: {quality_summary['average_quality_score']:.2f}")
       print(f"Report saved to: {report_path}")
       
       return {
           'data': data,
           'cycles': production_cycles,
           'quality_metrics': quality_metrics,
           'report_path': report_path
       }

   if __name__ == "__main__":
       results = run_basic_analysis() 