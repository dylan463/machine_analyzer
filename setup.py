"""
Setup script for Machine Analyzer package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("docs/README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="machine-analyzer",
    version="1.0.0",
    author="Anthony",
    author_email="dylanhinesang@gmail.com",
    description="A comprehensive machine energy consumption analysis library for production cycle detection and quality assessment",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dylan463/machine-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=1.0.0",
            "sphinx-autodoc-typehints>=1.23.0",
            "sphinx-copybutton>=0.5.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "jupyterlab>=4.0.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ],
        "full": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "jupyter>=1.0.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "machine_analyzer": ["*.txt", "*.json", "*.yaml", "*.yml"],
    },
    entry_points={
        "console_scripts": [
            "machine-analyzer=machine_analyzer.cli:main",
        ],
    },
    keywords=[
        "machine learning", 
        "energy analysis", 
        "time series", 
        "production cycles",
        "quality assessment",
        "anomaly detection",
        "manufacturing",
        "industrial",
        "iot",
        "data analysis"
    ],
    project_urls={
        "Bug Reports": "https://github.com/dylan463/machine-analyzer/issues",
        "Source": "https://github.com/dylan463/machine-analyzer",
        "Documentation": "https://machine-analyzer.readthedocs.io/",
        "Changelog": "https://github.com/dylan463/machine-analyzer/blob/main/CHANGELOG.md",
    },
    zip_safe=False,
) 