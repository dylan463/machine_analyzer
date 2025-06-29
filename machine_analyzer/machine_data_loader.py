"""
Machine Data Loader - Responsible for loading and preprocessing data from various formats.
"""

import pandas as pd
import numpy as np
import json
from typing import Optional, Union, Dict
import logging
import os

logger = logging.getLogger(__name__)


class MachineDataLoader:
    """
    Loads and validates machine energy consumption data from various file formats.
    """
    
    def __init__(self):
        """
        Initialize the data loader.
        """
        self.dataframe = None
        self.energy_column = "value"
        self.timestamp_column = "timestamp"
    
    def load_data(self, data_path: str,format = "csv", timestamp_column: str = "timestamp", 
                  energy_column: str = "value", **kwargs) -> pd.DataFrame:
        """
        Load data from file and set up time index.
        
        Args:
            data_path: Path to the data file
            timestamp_column: Name of the timestamp column
            energy_column: Name of the energy consumption column
            **kwargs: Additional arguments for pandas read functions
        
        Returns:
            Loaded DataFrame with time index
        """
        try:
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"Data file not found: {data_path}")
            
            if format == 'txt':
                raw_data = self._load_txt_data(data_path, **kwargs)
            elif format == 'json':
                raw_data = pd.read_json(data_path, **kwargs)
            elif format == 'csv':
                raw_data = pd.read_csv(data_path, **kwargs)
            elif format == 'parquet':
                raw_data = pd.read_parquet(data_path, **kwargs)
            else:
                raise ValueError(f"Unsupported file format: {format}")
            
            # Convert timestamp column to datetime
            if timestamp_column in raw_data.columns:
                raw_data[timestamp_column] = pd.to_datetime(raw_data[timestamp_column])
            
            # Set timestamp as index and sort
            self.dataframe = raw_data.set_index(timestamp_column).sort_index().copy()
            self.energy_column = energy_column
            self.timestamp_column = timestamp_column
            
            logger.info(f"Successfully loaded data with {len(self.dataframe)} records from {data_path}")
            return self.dataframe
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise
    
    def _load_txt_data(self, data_path: str, **kwargs) -> pd.DataFrame:
        """
        Load data from text file (Datadump.txt format).
        
        Args:
            data_path: Path to the text file
            **kwargs: Additional arguments
            
        Returns:
            DataFrame with loaded data
        """
        try:
            # Try to read as CSV first (common for .txt files with structured data)
            raw_data = pd.read_csv(data_path, **kwargs)
            
            # If successful and has expected columns, return as is
            if len(raw_data.columns) >= 2:
                return raw_data
            
        except Exception:
            pass
        
        # If CSV reading fails, try to parse as space/tab separated
        try:
            raw_data = pd.read_csv(data_path, sep=r'\s+', **kwargs)
            return raw_data
        except Exception:
            pass
        
        # Last resort: read line by line and parse manually
        data_lines = []
        with open(data_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        # Try to parse timestamp and value
                        parts = line.split()
                        if len(parts) >= 2:
                            timestamp_str = ' '.join(parts[:-1])
                            value = float(parts[-1])
                            data_lines.append({
                                'timestamp': timestamp_str,
                                'value': value
                            })
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Could not parse line {line_num}: {line}")
                        continue
        
        if not data_lines:
            raise ValueError("No valid data found in text file")
        
        return pd.DataFrame(data_lines)
    
    def preprocess_data(self, energy_data: Optional[pd.DataFrame] = None, 
                       energy_column: str = "value", frequency: str = "1s") -> pd.DataFrame:
        """
        Preprocess energy data: align timestamps, handle missing data and outliers.
        
        Args:
            energy_data: DataFrame to preprocess (uses self.dataframe if None)
            energy_column: Name of the energy consumption column
            frequency: Resampling frequency
            
        Returns:
            Preprocessed DataFrame
        """
        if energy_data is None:
            energy_data = self.dataframe
        
        if energy_data is None:
            raise ValueError("No data available for preprocessing")
        
        # Make a copy to avoid modifying original
        processed_data = energy_data.copy()
        
        # Ensure we have a DatetimeIndex
        if not isinstance(processed_data.index, pd.DatetimeIndex):
            raise ValueError("DataFrame must have DatetimeIndex for preprocessing")
        
        # Resample to specified frequency
        processed_data = processed_data.resample(frequency).mean()
        
        # Handle outliers and negative values
        energy_series = processed_data[energy_column]
        
        # Remove impossible negative values
        energy_series.loc[energy_series < 0] = np.nan
        
        # Interpolate missing values
        energy_series = energy_series.interpolate(method='time')
        
        # Forward/backward fill any remaining NaN values
        energy_series = energy_series.ffill().bfill()
        
        processed_data[energy_column] = energy_series
        
        logger.info(f"Preprocessed data: {len(processed_data)} records, frequency: {frequency}")
        return processed_data
    
    def validate_data(self, energy_data: Optional[pd.DataFrame] = None, 
                     energy_column: str = "value") -> Dict[str, any]:
        """
        Validate the loaded energy data.
        
        Args:
            energy_data: DataFrame to validate (uses self.dataframe if None)
            energy_column: Name of the energy consumption column
            
        Returns:
            Dictionary with validation results
        """
        if energy_data is None:
            energy_data = self.dataframe
        
        if energy_data is None:
            return {"valid": False, "error": "No data available"}
        
        validation_results = {
            "valid": True,
            "total_records": len(energy_data),
            "missing_values": energy_data[energy_column].isna().sum(),
            "negative_values": (energy_data[energy_column] < 0).sum(),
            "zero_values": (energy_data[energy_column] == 0).sum(),
            "start_time": energy_data.index.min(),
            "end_time": energy_data.index.max(),
            "duration": energy_data.index.max() - energy_data.index.min()
        }
        
        # Check for critical issues
        if validation_results["missing_values"] > len(energy_data) * 0.1:  # More than 10% missing
            validation_results["valid"] = False
            validation_results["error"] = "Too many missing values"
        
        if validation_results["negative_values"] > 0:
            validation_results["warning"] = "Negative energy values detected"
        
        logger.info(f"Data validation completed: {validation_results}")
        return validation_results
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Get the loaded DataFrame.
        
        Returns:
            DataFrame if loaded, None otherwise
        """
        return self.dataframe
    
    def get_energy_series(self) -> Optional[pd.Series]:
        """
        Get the energy consumption series.
        
        Returns:
            Energy consumption series if loaded, None otherwise
        """
        if self.dataframe is not None and self.energy_column in self.dataframe.columns:
            return self.dataframe[self.energy_column]
        return None
    
    def get_timestamps(self) -> Optional[pd.DatetimeIndex]:
        """
        Get the timestamp index.
        
        Returns:
            Timestamp index if loaded, None otherwise
        """
        if self.dataframe is not None:
            return self.dataframe.index
        return None
    
    def get_data_info(self) -> dict:
        """
        Get information about the loaded data.
        
        Returns:
            Dictionary with data information
        """
        if self.dataframe is None:
            return {}
        
        return {
            'total_records': len(self.dataframe),
            'start_time': self.dataframe.index.min(),
            'end_time': self.dataframe.index.max(),
            'duration': self.dataframe.index.max() - self.dataframe.index.min(),
            'energy_min': self.dataframe[self.energy_column].min(),
            'energy_max': self.dataframe[self.energy_column].max(),
            'energy_mean': self.dataframe[self.energy_column].mean(),
            'energy_std': self.dataframe[self.energy_column].std(),
            'missing_values': self.dataframe[self.energy_column].isna().sum()
        } 