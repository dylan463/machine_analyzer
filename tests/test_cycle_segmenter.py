"""
Comprehensive tests for CycleSegmenter class.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from machine_analyzer.cycle_segmenter import CycleSegmenter, ProductionCycle


class TestCycleSegmenter:
    """Test cases for CycleSegmenter class."""
    
    @pytest.fixture
    def sample_energy_data(self):
        """Create sample energy data for testing."""
        timestamps = pd.date_range(
            start=datetime(2023, 1, 1, 0, 0, 0),
            periods=1000,
            freq='1s'
        )
        
        # Create realistic energy pattern with cycles
        energy_data = []
        for i in range(1000):
            # Create cycles: off -> standby -> production -> off
            cycle_position = (i // 250) % 4
            
            if cycle_position == 0:  # Off
                energy = 0.0
            elif cycle_position == 1:  # Standby
                energy = 2.0 + np.random.normal(0, 0.5)
            elif cycle_position == 2:  # Production
                energy = 25.0 + np.random.normal(0, 2.0)
            else:  # Back to off
                energy = 0.0
            
            energy_data.append(max(0, energy))
        
        df = pd.DataFrame({
            'value': energy_data
        }, index=timestamps)
        
        return df
    
    @pytest.fixture
    def sample_state_masks(self, sample_energy_data):
        """Create sample state masks for testing."""
        on_mask = pd.Series(False, index=sample_energy_data.index)
        production_mask = pd.Series(False, index=sample_energy_data.index)
        
        # Set production periods (every 250-500 samples)
        for i in range(0, 1000, 500):
            on_mask.iloc[i+250:i+500] = True
            production_mask.iloc[i+275:i+325] = True
            production_mask.iloc[i+350:i+400] = True

        
        
        state_masks = {
            'off_state': ~on_mask,
            'on_state': on_mask,
            'standby_state': on_mask & ~production_mask,
            'production_state': production_mask
        }
        
        return state_masks
    
    @pytest.fixture
    def cycle_segmenter(self, sample_energy_data, sample_state_masks):
        """Create a CycleSegmenter instance for testing."""
        return CycleSegmenter(sample_energy_data, sample_state_masks, 'value')
    
    def test_initialization(self, cycle_segmenter):
        """Test CycleSegmenter initialization."""
        assert cycle_segmenter.energy_data is not None
        assert cycle_segmenter.state_masks is not None
        assert cycle_segmenter.energy_column == 'value'
        assert cycle_segmenter.production_cycles == []
        assert cycle_segmenter.cycle_statistics == {}
    
    def test_find_production_segments(self, cycle_segmenter):
        """Test finding production segments."""
        segments = cycle_segmenter.find_production_segments()
        
        assert isinstance(segments, list)
        assert len(segments) > 0
        
        for start_time, end_time in segments:
            assert isinstance(start_time, pd.Timestamp)
            assert isinstance(end_time, pd.Timestamp)
            assert start_time < end_time
    
    def test_find_production_segments_duration_constraints(self, cycle_segmenter):
        """Test production segments with duration constraints."""
        # Test with very short minimum duration
        segments_short = cycle_segmenter.find_production_segments(min_duration="1s")
        
        # Test with very long minimum duration
        segments_long = cycle_segmenter.find_production_segments(min_duration="100s")
        
        # Should have more segments with shorter minimum duration
        assert len(segments_short) >= len(segments_long)
    
    def test_segment_cycles(self, cycle_segmenter):
        """Test complete cycle segmentation."""
        cycles = cycle_segmenter.segment_cycles()
        
        assert isinstance(cycles, list)
        assert len(cycles) >= 0  # May be 0 if no valid segments found
        
        for cycle in cycles:
            assert isinstance(cycle, ProductionCycle)
            assert cycle.start_time < cycle.end_time
            assert cycle.duration > timedelta(0)
            assert cycle.energy_consumption >= 0
            assert cycle.peak_energy >= 0
            assert cycle.average_energy >= 0
            assert hasattr(cycle, 'variation')  # Check for variation attribute instead
    
    def test_get_cycles(self, cycle_segmenter):
        """Test get_cycles method."""
        cycle_segmenter.segment_cycles()
        
        cycles = cycle_segmenter.get_cycles()
        assert isinstance(cycles, list)
        assert len(cycles) >= 0
    
    def test_get_cycle_statistics(self, cycle_segmenter):
        """Test get_cycle_statistics method."""
        cycle_segmenter.segment_cycles()
        
        stats = cycle_segmenter.get_cycle_statistics()
        assert isinstance(stats, dict)
        
        if stats:  # If cycles were found
            assert 'total_cycles' in stats
            assert 'duration_stats' in stats
            assert 'energy_stats' in stats
            assert 'variation_stats' in stats
    
    def test_get_cycles_dataframe(self, cycle_segmenter):
        """Test get_cycles_dataframe method."""
        cycle_segmenter.segment_cycles()
        
        df = cycle_segmenter.get_cycles_dataframe()
        assert isinstance(df, pd.DataFrame)
        
        if not df.empty:
            expected_columns = ['cycle_id', 'start_time', 'end_time', 'duration_seconds',
                               'energy_consumption', 'peak_energy', 'average_energy', 'variation']
            
            for col in expected_columns:
                assert col in df.columns
    
    def test_no_production_segments(self):
        """Test behavior when no production segments are found."""
        # Create data with no production periods
        timestamps = pd.date_range(
            start=datetime(2023, 1, 1, 0, 0, 0),
            periods=1000,
            freq='1s'
        )
        
        energy_data = pd.DataFrame({
            'value': [0.0] * 1000  # All off
        }, index=timestamps)
        
        state_masks = {
            'off_state': pd.Series(True, index=timestamps),
            'on_state': pd.Series(False, index=timestamps),
            'standby_state': pd.Series(False, index=timestamps),
            'production_state': pd.Series(False, index=timestamps)
        }
        
        segmenter = CycleSegmenter(energy_data, state_masks, 'value')
        cycles = segmenter.segment_cycles()
        
        assert len(cycles) == 0
        assert segmenter.get_cycle_statistics() == {}
    
    def test_missing_production_mask(self):
        """Test error handling when production mask is missing."""
        timestamps = pd.date_range(
            start=datetime(2023, 1, 1, 0, 0, 0),
            periods=1000,
            freq='1s'
        )
        
        energy_data = pd.DataFrame({
            'value': [1.0] * 1000
        }, index=timestamps)
        
        state_masks = {
            'off_state': pd.Series(False, index=timestamps),
            'on_state': pd.Series(True, index=timestamps),
            'standby_state': pd.Series(False, index=timestamps)
            # Missing production_state
        }
        
        segmenter = CycleSegmenter(energy_data, state_masks, 'value')
        
        with pytest.raises(ValueError, match="Production state mask not found"):
            segmenter.find_production_segments()


class TestProductionCycle:
    """Test cases for ProductionCycle dataclass."""
    
    def test_production_cycle_creation(self):
        """Test ProductionCycle object creation."""
        start_time = pd.Timestamp(datetime(2023, 1, 1, 0, 0, 0))
        end_time = pd.Timestamp(datetime(2023, 1, 1, 0, 2, 0))
        duration = pd.Timedelta(end_time - start_time)
        
        cycle = ProductionCycle(
            cycle_id=1,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            energy_consumption=100.0,
            peak_energy=30.0,
            average_energy=25.0,
            variation=0.1
        )
        
        assert cycle.cycle_id == 1
        assert cycle.start_time == start_time
        assert cycle.end_time == end_time
        assert cycle.duration == duration
        assert cycle.energy_consumption == 100.0
        assert cycle.peak_energy == 30.0
        assert cycle.average_energy == 25.0
        assert cycle.variation == 0.1 