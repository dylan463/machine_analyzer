import pytest
import pandas as pd
from machine_analyzer.machine_data_loader import MachineDataLoader
import os

def test_load_data_csv(tmp_path):
    # Create a simple CSV file
    data = 'timestamp,value\n2023-01-01 00:00:00,10\n2023-01-01 00:01:00,12\n'
    file_path = tmp_path / 'test.csv'
    file_path.write_text(data)

    loader = MachineDataLoader()
    df = loader.load_data(str(file_path))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'value' in df.columns

    info = loader.get_data_info()
    assert info['total_records'] == 2
    assert info['energy_min'] == 10
    assert info['energy_max'] == 12


def test_get_energy_series_and_timestamps(tmp_path):
    data = 'timestamp,value\n2023-01-01 00:00:00,5\n2023-01-01 00:01:00,7\n'
    file_path = tmp_path / 'test2.csv'
    file_path.write_text(data)

    loader = MachineDataLoader()
    loader.load_data(str(file_path))
    energy_series = loader.get_energy_series()
    timestamps = loader.get_timestamps()
    assert list(energy_series) == [5, 7]
    assert len(timestamps) == 2 