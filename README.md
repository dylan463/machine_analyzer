# Machine Energy Analyzer

[![CI](https://github.com/dylan463/machine-analyzer/workflows/CI/badge.svg)](https://github.com/dylan463/machine-analyzer/actions)
[![Security](https://github.com/dylan463/machine-analyzer/workflows/Security%20Checks/badge.svg)](https://github.com/dylan463/machine-analyzer/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python library for analyzing machine energy consumption data, detecting production cycles, assessing quality, and generating detailed reports.

## 🚀 Features

- **📊 Data Loading**: Support for multiple file formats (CSV, JSON, TXT, Parquet)
- **🔍 State Detection**: Automatic detection of machine states (off, standby, production)
- **⚙️ Cycle Segmentation**: Identification of individual production cycles
- **📈 Quality Analysis**: Assessment of cycle quality and anomaly detection
- **📄 Report Generation**: Comprehensive text and CSV reports
- **📓 Jupyter Support**: Notebook integration for interactive analysis

## 📦 Installation

```bash
# Install from source
git clone https://github.com/dylan463/machine-analyzer.git
cd machine-analyzer
pip install -e .
```

## 🏃‍♂️ Quick Start

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

## 🛠️ Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/dylan463/machine-analyzer.git
cd machine-analyzer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=machine_analyzer --cov-report=html

# Run load tests
python tests/load_test.py --dataset-size 5000 --concurrent 4
```

### Code quality checks

```bash
# Format code
black machine_analyzer tests
isort machine_analyzer tests

# Lint code
flake8 machine_analyzer tests
mypy machine_analyzer

# Security checks
bandit -r machine_analyzer/
safety check
```

## 📚 Documentation

- [User Guide](docs/_build/html/user_guide/index.html)
- [API Reference](docs/_build/html/api_reference/index.html)
- [Examples](docs/_build/html/examples/index.html)

To build documentation locally:
```bash
cd docs
make html
```

## 🔧 CI/CD Pipeline

This project uses GitHub Actions for continuous integration:

### Workflows

1. **CI** (`ci.yml`): Main CI pipeline
   - Runs tests on multiple Python versions and OS
   - Code quality checks (linting, type checking)
   - Security scans
   - Documentation building

2. **Security Checks** (`security.yml`): Security-focused checks
   - Bandit security scanning
   - Safety dependency checks
   - pip-audit vulnerability scanning
   - Weekly scheduled runs

### Badges

The project includes several badges that show the current status:

- **CI**: Shows the status of the main CI pipeline
- **Security**: Shows the status of security checks
- **Python**: Shows supported Python versions
- **License**: Shows the project license

## 📊 Project Presentation

See [Project Presentation](A%20Lightweight%20Python%20Package%20for%20Industrial%20Time%20Series.pptx) for a detailed overview of the approach and results.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Ensure all CI checks pass
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Special thanks to the open-source community for the amazing tools and libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/dylan463/machine-analyzer/issues)
- **Email**: dylanhinesang@gmail.com 