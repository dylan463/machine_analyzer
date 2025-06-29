# Machine Energy Analyzer - User Documentation

## Overview

The Machine Energy Analyzer is a Python library designed to analyze machine energy consumption data, detect production cycles, assess quality, and generate comprehensive reports. It's built with simplicity in mind, making it accessible for beginners while providing powerful analysis capabilities.

## Features

- **📊 Data Loading**: Support for multiple file formats (CSV, JSON, TXT, Parquet)
- **🔍 State Detection**: Automatic detection of machine states (off, standby, production)
- **⚙️ Cycle Segmentation**: Identification of individual production cycles
- **📈 Quality Analysis**: Assessment of cycle quality and anomaly detection
- **📄 Report Generation**: Comprehensive text and CSV reports
- **🖥️ CLI Interface**: Command-line tool for quick analysis
- **📓 Jupyter Support**: Notebook integration for interactive analysis

## Quick Start

### Installation

```bash
# Install from PyPI (when available)
pip install machine-analyzer

# Or install from source
git clone https://github.com/yourusername/machine-analyzer.git
cd machine-analyzer
pip install -e .
```

### Basic Usage

```python
from machine_analyzer import MachineDataLoader, StateDetector, CycleSegmenter, QualityAnalyzer, ReportGenerator

# 1. Load data
loader = MachineDataLoader()
energy_data = loader.load_data("data/energy.csv")

# 2. Detect states
detector = StateDetector(energy_data, "value")
state_masks = detector.detect_states()

# 3. Segment cycles
segmenter = CycleSegmenter(energy_data, state_masks, "value")
production_cycles = segmenter.segment_cycles()

# 4. Analyze quality
analyzer = QualityAnalyzer(energy_data, production_cycles, "value")
quality_metrics = analyzer.analyze_quality()
anomalous_units = analyzer.get_anomalous_units()

# 5. Generate report
report_gen = ReportGenerator()
report_path = report_gen.generate_simple_report(
    energy_data, production_cycles, quality_metrics, {}, anomalous_units
)
```

### Command Line Interface

```bash
# Basic analysis
machine-analyzer data/energy.csv

# With custom output directory and verbose logging
machine-analyzer data/energy.csv --output reports --verbose
```

## Core Components

### 1. MachineDataLoader

Loads and preprocesses energy consumption data from various file formats.

**Key Methods:**
- `load_data()`: Load data from file
- `preprocess_data()`: Clean and prepare data
- `validate_data()`: Check data quality
- `get_data_info()`: Get data statistics

**Example:**
```python
loader = MachineDataLoader()
data = loader.load_data("energy.csv", timestamp_column="time", energy_column="power")
info = loader.get_data_info()
print(f"Loaded {info['total_records']} records")
```

### 2. StateDetector

Detects machine states based on energy consumption patterns.

**Key Methods:**
- `detect_states()`: Detect off, standby, and production states
- `get_state_masks()`: Get boolean masks for each state
- `get_state_distribution()`: Get state statistics

**Example:**
```python
detector = StateDetector(energy_data, "value")
state_masks = detector.detect_states(window_size="200ms", standby_threshold=5)
distribution = detector.get_state_distribution()
```

### 3. CycleSegmenter

Identifies individual production cycles from state data.

**Key Methods:**
- `segment_cycles()`: Find production cycles
- `get_cycles()`: Get all detected cycles
- `get_cycle_statistics()`: Get cycle statistics
- `get_abnormal_cycles()`: Get abnormal cycles only

**Example:**
```python
segmenter = CycleSegmenter(energy_data, state_masks, "value")
cycles = segmenter.segment_cycles(min_duration="5s", max_duration="300s")
stats = segmenter.get_cycle_statistics()
```

### 4. QualityAnalyzer

Assesses the quality of production cycles and detects anomalies.

**Key Methods:**
- `analyze_quality()`: Analyze all cycles
- `compute_production_count()`: Count production by time period
- `get_anomalous_units()`: Get list of anomalous cycles
- `get_quality_summary()`: Get quality statistics

**Example:**
```python
analyzer = QualityAnalyzer(energy_data, production_cycles, "value")
quality_metrics = analyzer.analyze_quality()
anomalous_units = analyzer.get_anomalous_units()
summary = analyzer.get_quality_summary()
```

### 5. ReportGenerator

Generates comprehensive analysis reports.

**Key Methods:**
- `generate_simple_report()`: Generate text report
- `generate_csv_report()`: Generate CSV report
- `generate_summary_statistics()`: Get summary statistics

**Example:**
```python
report_gen = ReportGenerator(output_dir="reports")
report_path = report_gen.generate_simple_report(
    energy_data, production_cycles, quality_metrics, production_counts, anomalous_units
)
csv_path = report_gen.generate_csv_report(production_cycles, quality_metrics)
```

## Data Format

The library expects energy consumption data with the following structure:

### Required Columns:
- **timestamp**: Time of measurement (will be converted to datetime)
- **value**: Energy consumption value (numeric)

### Example CSV:
```csv
timestamp,value
2023-01-01 00:00:00,0.0
2023-01-01 00:00:01,2.5
2023-01-01 00:00:02,25.3
...
```

### Supported File Formats:
- **CSV**: Comma-separated values
- **JSON**: JavaScript Object Notation
- **TXT**: Text files (space/tab separated)
- **Parquet**: Apache Parquet format

## Configuration

### State Detection Parameters

```python
detector.detect_states(
    window_size="200ms",      # Rolling window size
    standby_threshold=5,      # Energy threshold for standby state
    sensitivity_factor=1      # Sensitivity for state changes
)
```

### Cycle Segmentation Parameters

```python
segmenter.segment_cycles(
    min_duration="5s",        # Minimum cycle duration
    max_duration="300s",      # Maximum cycle duration
    detect_abnormal=True      # Enable abnormal cycle detection
)
```

### Quality Analysis Parameters

The quality analyzer automatically determines quality scores based on:
- Energy stability (coefficient of variation)
- Cycle duration consistency
- Presence of anomalies

## Output and Reports

### Text Report
The text report includes:
- Executive summary
- Production analysis
- Quality assessment
- Energy statistics
- Anomalous units list
- Recommendations

### CSV Report
The CSV report contains:
- Cycle information (ID, start/end times, duration)
- Energy consumption data
- Quality metrics
- Anomaly flags

### Example Report Structure
```
==================================================
MACHINE ENERGY ANALYSIS REPORT
==================================================
Generated on: 2023-12-01 10:30:00

EXECUTIVE SUMMARY
--------------------
Total Production Cycles: 150
Total Units Produced: 150
Anomalous Units: 12
Average Quality Score: 0.85

PRODUCTION ANALYSIS
--------------------
Average Cycle Duration: 45.2 seconds
Average Energy per Cycle: 1250.5
Total Energy Consumed: 187575.0
...
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure the package is installed correctly
   ```bash
   pip install -e .
   ```

2. **File Not Found**: Check the data file path
   ```python
   import os
   print(os.path.exists("data/energy.csv"))
   ```

3. **No Production Cycles**: Check state detection parameters
   ```python
   # Try different standby threshold
   state_masks = detector.detect_states(standby_threshold=10)
   ```

4. **Memory Issues**: For large datasets, consider sampling
   ```python
   # Sample data for testing
   sample_data = energy_data.head(10000)
   ```

### Performance Tips

1. **Large Datasets**: Use data sampling for initial testing
2. **Frequent Analysis**: Cache state detection results
3. **Memory Management**: Process data in chunks if needed

## Examples

### Complete Analysis Pipeline

See `examples/machine_energy_analysis.ipynb` for a complete Jupyter notebook example.

### Custom Analysis

```python
# Custom quality thresholds
analyzer = QualityAnalyzer(energy_data, production_cycles, "value")
quality_metrics = analyzer.analyze_quality()

# Filter high-quality cycles
high_quality = [m for m in quality_metrics if m.quality_score > 0.8]
print(f"High quality cycles: {len(high_quality)}")

# Analyze specific time periods
from datetime import datetime, timedelta
start_time = datetime(2023, 1, 1, 8, 0, 0)
end_time = datetime(2023, 1, 1, 17, 0, 0)
period_data = energy_data[start_time:end_time]
```

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support:
- Check the documentation
- Open an issue on GitHub
- Review the examples

---

**Happy analyzing! 🚀** 