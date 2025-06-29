"""
Simple tests for QualityAnalyzer class.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from machine_analyzer.quality_analyzer import QualityAnalyzer, QualityMetrics
from machine_analyzer.cycle_segmenter import ProductionCycle


class TestQualityAnalyzer:
    """Test cases for QualityAnalyzer class."""
    
    @pytest.fixture
    def sample_cycle_statistics(self):
        """Create sample cycle statistics for testing."""
        return {
            'total_cycles': 5,
            'duration_stats': {
                'mean': 900.0,  # 15 minutes in seconds
                'std': 30.0,
                'min': 870.0,
                'max': 930.0,
                'median': 900.0
            },
            'energy_stats': {
                'mean_consumption': 1500.0,
                'std_consumption': 100.0,
                'mean_peak': 120.0,
                'std_peak': 5.0,
                'total_energy': 7500.0
            },
            'variation_stats': {
                'mean': 0.2,
                'std': 0.05,
                'min': 0.15,
                'max': 0.25,
                'median': 0.2
            }
        }
    
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
    
    def test_initialization(self, sample_cycle_statistics, sample_production_cycles):
        """Test QualityAnalyzer initialization."""
        analyzer = QualityAnalyzer(sample_cycle_statistics, sample_production_cycles)
        
        assert analyzer.cycle_statistics == sample_cycle_statistics
        assert analyzer.production_cycles == sample_production_cycles
        assert analyzer.quality_metrics == []
        assert analyzer.anomalous_units == []
    
    def test_analyze_quality(self, sample_cycle_statistics, sample_production_cycles):
        """Test quality analysis."""
        analyzer = QualityAnalyzer(sample_cycle_statistics, sample_production_cycles)
        
        metrics = analyzer.analyze_quality()
        
        assert isinstance(metrics, list)
        assert len(metrics) == len(sample_production_cycles)
        
        for metric in metrics:
            assert isinstance(metric, QualityMetrics)
            assert hasattr(metric, 'cycle_id')
            assert hasattr(metric, 'quality_score')
            assert hasattr(metric, 'quality_grade')
            assert hasattr(metric, 'is_anomalous')
            assert hasattr(metric, 'issues')
            
            # Check quality score is between 0 and 1
            assert 0 <= metric.quality_score <= 1
            
            # Check quality grade is valid
            assert metric.quality_grade in ['A', 'B', 'C', 'D']
    
    def test_analyze_quality_empty_cycles(self, sample_cycle_statistics):
        """Test quality analysis with empty cycles."""
        analyzer = QualityAnalyzer(sample_cycle_statistics, [])
        
        metrics = analyzer.analyze_quality()
        assert metrics == []
    
    def test_analyze_quality_empty_statistics(self, sample_production_cycles):
        """Test quality analysis with empty statistics."""
        analyzer = QualityAnalyzer({}, sample_production_cycles)
        
        metrics = analyzer.analyze_quality()
        assert metrics == []
    
    def test_get_quality_summary(self, sample_cycle_statistics, sample_production_cycles):
        """Test quality summary generation."""
        analyzer = QualityAnalyzer(sample_cycle_statistics, sample_production_cycles)
        analyzer.analyze_quality()
        
        summary = analyzer.get_quality_summary()
        
        assert isinstance(summary, dict)
        assert 'total_cycles' in summary
        assert 'anomalous_cycles' in summary
        assert 'average_quality_score' in summary
        assert 'quality_grade_distribution' in summary
        
        assert summary['total_cycles'] == len(sample_production_cycles)
        assert 0 <= summary['average_quality_score'] <= 1
    
    def test_get_quality_summary_empty(self, sample_cycle_statistics):
        """Test quality summary with no metrics."""
        analyzer = QualityAnalyzer(sample_cycle_statistics, [])
        
        summary = analyzer.get_quality_summary()
        assert summary == {}
    
    def test_get_anomalous_units(self, sample_cycle_statistics, sample_production_cycles):
        """Test getting anomalous units."""
        analyzer = QualityAnalyzer(sample_cycle_statistics, sample_production_cycles)
        analyzer.analyze_quality()
        
        anomalous_units = analyzer.get_anomalous_units()
        
        assert isinstance(anomalous_units, list)
        # All anomalous units should be valid cycle IDs
        for unit_id in anomalous_units:
            assert unit_id in [cycle.cycle_id for cycle in sample_production_cycles]
    
    def test_get_quality_metrics(self, sample_cycle_statistics, sample_production_cycles):
        """Test getting quality metrics."""
        analyzer = QualityAnalyzer(sample_cycle_statistics, sample_production_cycles)
        analyzer.analyze_quality()
        
        metrics = analyzer.get_quality_metrics()
        
        assert isinstance(metrics, list)
        assert len(metrics) == len(sample_production_cycles)
        assert all(isinstance(metric, QualityMetrics) for metric in metrics)


class TestQualityMetrics:
    """Test cases for QualityMetrics dataclass."""
    
    def test_quality_metrics_creation(self):
        """Test QualityMetrics dataclass creation."""
        metrics = QualityMetrics(
            cycle_id=1,
            quality_score=0.85,
            quality_grade="A",
            is_anomalous=False,
            issues=["Minor variation"]
        )
        
        assert metrics.cycle_id == 1
        assert metrics.quality_score == 0.85
        assert metrics.quality_grade == "A"
        assert metrics.is_anomalous == False
        assert metrics.issues == ["Minor variation"] 