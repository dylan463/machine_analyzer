"""
State Detector - Responsible for detecting machine states and managing state masks.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def calculate_iqr_bounds(dataframe: pd.DataFrame, column_name: str, upper_coefficient: float, lower_coefficient: float) -> Tuple[float, float]:
    """
    Calculate IQR-based bounds for outlier detection.
    
    Args:
        dataframe: Input DataFrame
        column_name: Column to analyze
        upper_coefficient: Multiplier for upper bound
        lower_coefficient: Multiplier for lower bound
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    mean_value = dataframe[column_name].mean()
    q1 = dataframe[column_name].quantile(0.25)
    q3 = dataframe[column_name].quantile(0.75)
    iqr = q3 - q1
    return (mean_value - iqr * lower_coefficient, mean_value + iqr * upper_coefficient)


class StateDetector:
    """
    Detects machine states and manages state masks.
    """
    
    def __init__(self, energy_data: pd.DataFrame, energy_column: str):
        """
        Initialize the state detector.
        
        Args:
            energy_data: DataFrame containing energy consumption data
            energy_column: Name of the energy consumption column
        """
        self.energy_data = energy_data.copy()
        self.energy_column = energy_column
        self.state_masks = {}
        self.state_distribution = {}
        self.is_processed = False
        
    def detect_states(self, window_size: int = 20, production_threshold: float = 5, 
                      keep_threshold_column: bool = False) -> Dict[str, pd.Series]:
        """
        Detect machine states based on energy consumption patterns.
        This function replicates the logic from the original loader.py generate_states method.
        
        Args:
            window_size: Rolling window size for calculations
            production_threshold: Maximum energy threshold for production state
            sensitivity_factor: Sensitivity factor for state detection
            keep_threshold_column: Whether to keep the threshold column
            
        Returns:
            Dictionary containing state masks
        """
        if self.energy_data is None:
            raise ValueError("Energy data must be provided before state detection")
        
        # Calculate moving average 
        self.energy_data["moving_median"] = self.energy_data[self.energy_column].rolling(window=window_size,center = True).median()
        
        self.energy_data["dynamic_threshold"] = self.energy_data["moving_median"]
        
        # Forward and backward fill to handle NaN values
        self.energy_data["dynamic_threshold"] = self.energy_data["dynamic_threshold"].bfill().ffill()
        
        # Define states
        off_state = (self.energy_data[self.energy_column] == 0) & (self.energy_data["dynamic_threshold"] == 0)
        on_state = ~off_state
        
        # Set power state
        self.energy_data["power_state"] = "off"
        self.energy_data.loc[on_state, "power_state"] = "on"
        
        # Define standby and production states
        standby_state = (self.energy_data["dynamic_threshold"] < production_threshold)
        standby_state = on_state & standby_state
        production_state = on_state & ~standby_state
        
        # Clean up temporary columns
        if not keep_threshold_column:
            self.energy_data.drop(columns="dynamic_threshold", inplace=True)
        self.energy_data.drop(columns=["moving_median"], inplace=True)
        
        # Set final state classification
        self.energy_data["machine_state"] = "off"
        self.energy_data.loc[on_state, "machine_state"] = "on"
        self.energy_data.loc[standby_state, "machine_state"] = "standby"
        self.energy_data.loc[production_state, "machine_state"] = "production"
        
        # Store state masks in dictionary
        self.state_masks = {
            'off_state': off_state,
            'on_state': on_state,
            'standby_state': standby_state,
            'production_state': production_state
        }
        
        # Calculate state distribution
        self.state_distribution = self.energy_data["machine_state"].value_counts().to_dict()
        
        self.is_processed = True
        logger.info("State detection completed successfully")
        
        return self.state_masks
    
    def calculate_state_limits(self, state_mask: pd.Series, upper_coefficient: float, lower_coefficient: float) -> Tuple[float, float]:
        """
        Calculate energy limits for a specific state using IQR method.
        
        Args:
            state_mask: Boolean mask for the state
            upper_coefficient: Upper bound coefficient
            lower_coefficient: Lower bound coefficient
            
        Returns:
            Tuple of (lower_limit, upper_limit)
        """
        if self.energy_data is None:
            raise ValueError("Energy data must be loaded")
        
        state_data = self.energy_data[state_mask]

        return calculate_iqr_bounds(state_data, self.energy_column, upper_coefficient, lower_coefficient)
    
    def remove_outliers(self, state_mask: pd.Series, energy_limits: Tuple[float, float]) -> None:
        """
        Remove outliers from a specific state based on energy limits.
        
        Args:
            state_mask: Boolean mask for the state
            energy_limits: Tuple of (lower_limit, upper_limit)
        """
        if self.energy_data is None:
            raise ValueError("Energy data must be loaded")
        
        lower_limit, upper_limit = energy_limits
        state_data = self.energy_data.loc[state_mask].copy()
        
        # Mark outliers as NaN
        outlier_mask = (state_data[self.energy_column] <= lower_limit) | (state_data[self.energy_column] >= upper_limit)
        state_data.loc[outlier_mask, self.energy_column] = np.nan
        
        # Interpolate missing values
        state_data[self.energy_column] = state_data[self.energy_column].interpolate(method="time")
        
        # Update original dataframe
        self.energy_data.loc[state_mask] = state_data
    
    def preprocess_states(self, window_size: int = 20, production_threshold: float = 5, 
                         keep_threshold_column: bool = False,
                         iqr_coefficients: Tuple[float, float, float, float] = (0, 0, 0, 0)) -> bool:
        """
        Complete state preprocessing pipeline.
        
        Args:
            window_size: Rolling window size
            production_threshold: Production energy threshold
            keep_threshold_column: Whether to keep threshold column
            iqr_coefficients: Coefficients for (standby_lower, standby_upper, production_lower, production_upper)
            
        Returns:
            True if preprocessing successful, False otherwise
        """
        try:
            # Detect states
            state_masks = self.detect_states(
                window_size=window_size,
                production_threshold=production_threshold,
                keep_threshold_column=keep_threshold_column
            )
            
            # Calculate limits for standby and production states
            standby_limits = self.calculate_state_limits(
                state_mask=state_masks['standby_state'],
                lower_coefficient=iqr_coefficients[0],
                upper_coefficient=iqr_coefficients[1]
            )
            
            production_limits = self.calculate_state_limits(
                state_mask=state_masks['production_state'],
                lower_coefficient=iqr_coefficients[2],
                upper_coefficient=iqr_coefficients[3]
            )
            
            # Remove outliers
            self.remove_outliers(state_masks['standby_state'], standby_limits)
            self.remove_outliers(state_masks['production_state'], production_limits)
            
            logger.info("State preprocessing completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"State preprocessing failed: {e}")
            return False
    
    def get_state_masks(self) -> Dict[str, pd.Series]:
        """
        Get all state masks.
        
        Returns:
            Dictionary containing state masks
        """
        return self.state_masks
    
    def get_state_distribution(self) -> Dict[str, int]:
        """
        Get distribution of machine states.
        
        Returns:
            Dictionary with state counts
        """
        return self.state_distribution
    
    def get_processed_data(self) -> pd.DataFrame:
        """
        Get the processed DataFrame with state information.
        
        Returns:
            DataFrame with state information
        """
        return self.energy_data
    
    def get_state_data(self, state_name: str) -> Optional[pd.DataFrame]:
        """
        Get data for a specific state.
        
        Args:
            state_name: Name of the state ('off', 'on', 'standby', 'production')
            
        Returns:
            DataFrame containing data for the specified state
        """
        if not self.is_processed:
            raise ValueError("States must be detected before accessing state data")
        
        state_mask_key = f"{state_name}_state"
        if state_mask_key in self.state_masks:
            return self.energy_data[self.state_masks[state_mask_key]]
        
        return None 