Examples
========

This section provides practical examples of how to use Machine Analyzer for different scenarios.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   basic_analysis


Basic Analysis
--------------

Complete end-to-end analysis of machine energy data:

.. code-block:: python

   from machine_analyzer import (
       MachineDataLoader, 
       StateDetector, 
       CycleSegmenter, 
       QualityAnalyzer, 
       ReportGenerator
   )
   import pandas as pd

   # 1. Load energy data
   loader = MachineDataLoader()
   energy_data = loader.load_data("data/energy_consumption.csv")
   
   print(f"Loaded {len(energy_data)} data points")
   print(f"Time range: {energy_data.index[0]} to {energy_data.index[-1]}")

   # 2. Detect machine states
   detector = StateDetector(energy_data, "value")
   state_masks = detector.detect_states(window_size=200, production_threshold=5.0)
   
   # Get state distribution
   state_distribution = detector.get_state_distribution()
   print("State distribution:", state_distribution)

   # 3. Segment production cycles
   segmenter = CycleSegmenter(energy_data, state_masks, "value")
   production_cycles = segmenter.segment_cycles(
       min_duration="5s", 
       max_duration="300s"
   )
   
   print(f"Detected {len(production_cycles)} production cycles")
   
   # Get cycle statistics
   cycle_stats = segmenter.get_cycle_statistics()
   print("Cycle statistics:", cycle_stats)

   # 4. Analyze quality
   analyzer = QualityAnalyzer(cycle_stats, production_cycles)
   quality_metrics = analyzer.analyze_quality()
   anomalous_units = analyzer.get_anomalous_units()
   
   print(f"Found {len(anomalous_units)} anomalous cycles")
   
   # Get quality summary
   quality_summary = analyzer.get_quality_summary()
   print("Quality summary:", quality_summary)

   # 5. Generate report
   report_gen = ReportGenerator(output_dir="reports/")
   report_path = report_gen.generate_simple_report(
       energy_data, 
       production_cycles, 
       quality_metrics, 
       anomalous_units
   )
   
   print(f"Report generated: {report_path}")

Advanced Analysis
-----------------

Custom analysis with specific parameters and data preprocessing:

.. code-block:: python

   import numpy as np
   from datetime import datetime, timedelta

   # Create synthetic data for demonstration
   np.random.seed(42)
   timestamps = pd.date_range('2023-01-01', periods=10000, freq='1s')
   
   # Generate realistic energy consumption pattern
   energy_values = []
   for i in range(10000):
       if i % 1000 < 100:  # Production cycles
           energy = 25.0 + np.random.normal(0, 2.0)
       elif i % 1000 < 200:  # Standby
           energy = 2.0 + np.random.normal(0, 0.5)
       else:  # Off
           energy = 0.0 + np.random.normal(0, 0.1)
       energy_values.append(max(0, energy))
   
   # Create DataFrame
   synthetic_data = pd.DataFrame({
       'value': energy_values
   }, index=timestamps)
   
   # Save to CSV for analysis
   synthetic_data.to_csv('synthetic_energy_data.csv')
   
   # Perform analysis with custom parameters
   loader = MachineDataLoader()
   data = loader.load_data('synthetic_energy_data.csv')
   
   # Custom state detection
   detector = StateDetector(data, "value")
   state_masks = detector.detect_states(
       window_size=500,  # Larger window for smoother detection
       production_threshold=10.0,  # Higher threshold
       keep_threshold_column=True
   )
   
   # Advanced cycle segmentation
   segmenter = CycleSegmenter(data, state_masks, "value")
   cycles = segmenter.segment_cycles(
       min_duration="10s",  # Longer minimum duration
       max_duration="600s"  # Longer maximum duration
   )
   
   # Detailed quality analysis
   cycle_stats = segmenter.get_cycle_statistics()
   analyzer = QualityAnalyzer(cycle_stats, cycles)
   
   # Custom threshold factors
   quality_metrics = analyzer.analyze_quality({
       "variation": 1.5,  # More sensitive to variation
       "duration": 2.5,   # Less sensitive to duration
       "energy": 2.0      # Standard sensitivity for energy
   })
   
   # Export detailed results
   cycles_df = segmenter.get_cycles_dataframe()
   cycles_df.to_csv('detailed_cycles_analysis.csv', index=False)
   
   print(f"Analysis complete. Found {len(cycles)} cycles.")
   print(f"Quality metrics calculated for {len(quality_metrics)} cycles.")

Batch Processing
----------------

Process multiple files in batch:

.. code-block:: python

   import os
   from pathlib import Path

   def analyze_multiple_files(data_directory, output_directory):
       """Analyze multiple energy data files in batch."""
       
       # Create output directory
       os.makedirs(output_directory, exist_ok=True)
       
       # Get all CSV files
       data_files = list(Path(data_directory).glob("*.csv"))
       
       results = {}
       
       for file_path in data_files:
           print(f"Processing {file_path.name}...")
           
           try:
               # Load and analyze
               loader = MachineDataLoader()
               data = loader.load_data(str(file_path))
               
               detector = StateDetector(data, "value")
               state_masks = detector.detect_states()
               
               segmenter = CycleSegmenter(data, state_masks, "value")
               cycles = segmenter.segment_cycles()
               cycle_stats = segmenter.get_cycle_statistics()
               
               analyzer = QualityAnalyzer(cycle_stats, cycles)
               quality_metrics = analyzer.analyze_quality()
               anomalous_units = analyzer.get_anomalous_units()
               
               # Generate report for this file
               report_gen = ReportGenerator(output_dir=output_directory)
               report_path = report_gen.generate_simple_report(
                   data, cycles, quality_metrics, anomalous_units
               )
               
               # Store results
               results[file_path.name] = {
                   'total_cycles': len(cycles),
                   'anomalous_cycles': len(anomalous_units),
                   'report_path': report_path,
                   'cycle_stats': cycle_stats
               }
               
               print(f"  ✓ {len(cycles)} cycles, {len(anomalous_units)} anomalies")
               
           except Exception as e:
               print(f"  ✗ Error processing {file_path.name}: {e}")
               results[file_path.name] = {'error': str(e)}
       
       # Generate summary report
       summary_path = os.path.join(output_directory, "batch_analysis_summary.txt")
       with open(summary_path, 'w') as f:
           f.write("BATCH ANALYSIS SUMMARY\n")
           f.write("=" * 50 + "\n\n")
           
           for filename, result in results.items():
               f.write(f"File: {filename}\n")
               if 'error' in result:
                   f.write(f"  Status: ERROR - {result['error']}\n")
               else:
                   f.write(f"  Total cycles: {result['total_cycles']}\n")
                   f.write(f"  Anomalous cycles: {result['anomalous_cycles']}\n")
                   f.write(f"  Report: {result['report_path']}\n")
               f.write("\n")
       
       return results

   # Example usage
   results = analyze_multiple_files(
       data_directory="data/",
       output_directory="batch_reports/"
   )

Custom Analysis
---------------

Create custom analysis functions for specific use cases:

.. code-block:: python

   def analyze_energy_efficiency(energy_data, production_cycles):
       """Analyze energy efficiency of production cycles."""
       
       efficiency_metrics = []
       
       for cycle in production_cycles:
           # Calculate energy per unit time
           energy_per_second = cycle.energy_consumption / cycle.duration.total_seconds()
           
           # Calculate peak efficiency (energy at peak vs average)
           efficiency_ratio = cycle.peak_energy / cycle.average_energy
           
           efficiency_metrics.append({
               'cycle_id': cycle.cycle_id,
               'energy_per_second': energy_per_second,
               'efficiency_ratio': efficiency_ratio,
               'duration_seconds': cycle.duration.total_seconds(),
               'total_energy': cycle.energy_consumption
           })
       
       return pd.DataFrame(efficiency_metrics)

   def detect_operational_patterns(energy_data, state_masks):
       """Detect operational patterns and trends."""
       
       # Calculate daily patterns
       energy_data['hour'] = energy_data.index.hour
       energy_data['day_of_week'] = energy_data.index.dayofweek
       
       # Production hours analysis
       production_hours = energy_data[state_masks['production_state']]['hour'].value_counts()
       
       # Energy consumption by day of week
       daily_consumption = energy_data.groupby('day_of_week')['value'].sum()
       
       return {
           'production_hours': production_hours,
           'daily_consumption': daily_consumption,
           'total_production_time': state_masks['production_state'].sum(),
           'total_energy': energy_data['value'].sum()
       }

   # Example usage of custom analysis
   loader = MachineDataLoader()
   data = loader.load_data("data/energy_data.csv")
   
   detector = StateDetector(data, "value")
   state_masks = detector.detect_states()
   
   segmenter = CycleSegmenter(data, state_masks, "value")
   cycles = segmenter.segment_cycles()
   
   # Run custom analyses
   efficiency_df = analyze_energy_efficiency(data, cycles)
   patterns = detect_operational_patterns(data, state_masks)
   
   print("Energy efficiency analysis:")
   print(efficiency_df.head())
   
   print("\nOperational patterns:")
   print(f"Peak production hours: {patterns['production_hours'].head()}")
   print(f"Daily consumption: {patterns['daily_consumption']}")

Troubleshooting
---------------

Common issues and solutions:

.. code-block:: python

   # Issue: No production cycles detected
   if len(production_cycles) == 0:
       print("No production cycles detected. Possible solutions:")
       print("1. Check production_threshold value")
       print("2. Verify data contains production periods")
       print("3. Adjust min_duration and max_duration parameters")
       
       # Try with different parameters
       cycles = segmenter.segment_cycles(
           min_duration="1s",  # Shorter minimum
           max_duration="1000s"  # Longer maximum
       )

   # Issue: Too many anomalous units
   if len(anomalous_units) > len(production_cycles) * 0.5:
       print("Too many anomalies detected. Consider:")
       print("1. Increasing threshold factors")
       print("2. Checking data quality")
       print("3. Adjusting state detection parameters")
       
       # Use more lenient thresholds
       quality_metrics = analyzer.analyze_quality({
           "variation": 3.0,  # Less sensitive
           "duration": 3.0,
           "energy": 3.0
       })

   # Issue: Memory usage with large datasets
   if len(energy_data) > 100000:
       print("Large dataset detected. Consider:")
       print("1. Using data sampling")
       print("2. Processing in chunks")
       print("3. Reducing window_size parameter")
       
       # Sample data for analysis
       sampled_data = energy_data.sample(n=50000, random_state=42)