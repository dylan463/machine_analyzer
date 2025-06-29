import pytest
import pandas as pd
from machine_analyzer.state_detector import StateDetector

def test_detect_states():
    # Create simple energy data
    data = {
        'timestamp': pd.date_range('2023-01-01', periods=5, freq='s'),
        'value': [0, 2, 10, 2, 0]
    }
    df = pd.DataFrame(data).set_index('timestamp')
    detector = StateDetector(df, 'value')
    state_masks = detector.detect_states(window_size=10,production_threshold=10)
    assert 'production_state' in state_masks
    assert 'standby_state' in state_masks
    assert isinstance(state_masks['production_state'], pd.Series)
    # Check state distribution
    dist = detector.get_state_distribution()
    assert isinstance(dist, dict)
    assert sum(dist.values()) == 5 