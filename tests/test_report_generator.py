"""
Simple tests for ReportGenerator class.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from machine_analyzer.report_generator import ReportGenerator
from machine_analyzer.quality_analyzer import QualityMetrics
from machine_analyzer.cycle_segmenter import ProductionCycle


class TestReportGenerator:
    """Test cases for ReportGenerator class."""
    
    @pytest.fixture
    def sample_energy_data(self):
        """Create sample energy data for testing."""
        dates = pd.date_range('2024-01-01 00:00:00', periods=100, freq='1min')
        energy_values = np.random.normal(100, 10, 100)
        return pd.DataFrame({'value': energy_values}, index=dates)
    
    @pytest.fixture
    def sample_production_cycles(self):
        """Create sample production cycles for testing."""
        cycles = []
        base_time = pd.Timestamp('2024-01-01 00:00:00')
        
        for i in range(5):
            start_time = base_time + pd.Timedelta(minutes=i * 20)
            end_time = start_time + pd.Timedelta(minutes=15)
            duration = pd.Timedelta(minutes=15)
            
            cycles.append(ProductionCycle(
                cycle_id=i + 1,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                energy_consumption=1500 + i * 50,
                peak_energy=120 + i * 2,
                average_energy=110 + i * 3,
                variation=0.2 + i * 0.01
            ))
        
        return cycles
    
    @pytest.fixture
    def sample_quality_metrics(self):
        """Create sample quality metrics for testing."""
        metrics = []
        for i in range(5):
            metrics.append(QualityMetrics(
                cycle_id=i + 1,
                quality_score=0.8 + i * 0.02,
                quality_grade=["A", "B", "C", "D", "A"][i],
                is_anomalous=i > 2,
                issues=[f"Issue {i + 1}"] if i > 2 else []
            ))
        
        return metrics
    
    @pytest.fixture
    def sample_production_counts(self):
        """Create sample production counts for testing."""
        return {
            "2024-01-01": 10,
            "2024-01-02": 15,
            "2024-01-03": 12
        }
    
    def test_initialization(self, tmp_path):
        """Test ReportGenerator initialization."""
        generator = ReportGenerator(str(tmp_path))
        
        assert generator.output_dir == str(tmp_path)
        assert os.path.exists(str(tmp_path))
    
    def test_initialization_create_directory(self, tmp_path):
        """Test ReportGenerator creates output directory if it doesn't exist."""
        new_dir = tmp_path / "new_reports"
        generator = ReportGenerator(str(new_dir))
        
        assert os.path.exists(str(new_dir))
        assert generator.output_dir == str(new_dir)
    
    def test_generate_simple_report(self, sample_energy_data, sample_production_cycles,
                                  sample_quality_metrics, tmp_path):
        """Test simple report generation."""
        generator = ReportGenerator(str(tmp_path))
        
        report_path = generator.generate_simple_report(
            sample_energy_data,
            sample_production_cycles,
            sample_quality_metrics,
            [3]  # anomalous units
        )
        
        assert os.path.exists(report_path)
        assert report_path.endswith('.txt')
        
        # Check file content
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'MACHINE ENERGY ANALYSIS REPORT' in content
            assert 'EXECUTIVE SUMMARY' in content
            assert 'PRODUCTION ANALYSIS' in content
            assert 'QUALITY ASSESSMENT' in content
    
    def test_generate_csv_report(self, sample_production_cycles, sample_quality_metrics, tmp_path):
        """Test CSV report generation."""
        generator = ReportGenerator(str(tmp_path))
        
        csv_path = generator.generate_csv_report(sample_production_cycles, sample_quality_metrics)
        
        assert os.path.exists(csv_path)
        assert csv_path.endswith('.csv')
        
        # Check file content
        df = pd.read_csv(csv_path)
        assert len(df) == len(sample_production_cycles)
        assert 'cycle_id' in df.columns
        assert 'quality_score' in df.columns
        assert 'quality_grade' in df.columns
        # Note: variation is not included in CSV output, only in cycle data
    
    def test_generate_csv_report_empty_data(self, tmp_path):
        """Test CSV report generation with empty data."""
        generator = ReportGenerator(str(tmp_path))
        
        csv_path = generator.generate_csv_report([], [])
        
        assert os.path.exists(csv_path)
        assert csv_path.endswith('.csv')
        
        # Check file content - should be empty but with headers
        try:
            df = pd.read_csv(csv_path)
            assert len(df) == 0
        except pd.errors.EmptyDataError:
            # This is also acceptable for empty CSV files
            pass
    
    def test_generate_summary_statistics(self, sample_energy_data, sample_production_cycles,
                                       sample_quality_metrics):
        """Test summary statistics generation."""
        generator = ReportGenerator()
        
        summary = generator.generate_summary_statistics(
            sample_energy_data,
            sample_production_cycles,
            sample_quality_metrics,
            [3]  # anomalous units
        )
        
        assert isinstance(summary, dict)
        assert 'analysis_timestamp' in summary
        assert 'data_period' in summary
        assert 'energy_statistics' in summary
        assert 'production_summary' in summary
        
        # Check data period
        assert 'start' in summary['data_period']
        assert 'end' in summary['data_period']
        assert 'duration_hours' in summary['data_period']
        
        # Check energy statistics
        assert 'total_energy' in summary['energy_statistics']
        assert 'average_energy' in summary['energy_statistics']
        assert 'peak_energy' in summary['energy_statistics']
        
        # Check production summary
        assert 'total_cycles' in summary['production_summary']
        assert 'anomalous_units' in summary['production_summary']
        assert 'average_quality_score' in summary['production_summary']
    
    def test_generate_summary_statistics_empty_data(self):
        """Test summary statistics with empty data."""
        generator = ReportGenerator()
        
        summary = generator.generate_summary_statistics(
            pd.DataFrame(),
            [],
            [],
            []
        )
        
        assert isinstance(summary, dict)
        assert summary['data_period']['duration_hours'] == 0 