"""
Cycle Segmenter - Responsible for detecting production cycles using state masks.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProductionCycle:
    """Represents a single production cycle."""
    cycle_id: int
    start_time: pd.Timestamp
    end_time: pd.Timestamp
    duration: pd.Timedelta
    energy_consumption: float
    peak_energy: float
    average_energy: float
    variation: float

class CycleSegmenter:
    """
    Detects and segments production cycles using state masks.
    """
    
    def __init__(self, energy_data: pd.DataFrame, state_masks: Dict[str, pd.Series], 
                 energy_column: str = "value"):
        """
        Initialize the cycle segmenter.
        
        Args:
            energy_data: DataFrame containing energy consumption data
            state_masks: Dictionary containing state masks from StateDetector
            energy_column: Name of the energy consumption column
        """
        self.energy_data = energy_data
        self.state_masks = state_masks
        self.energy_column = energy_column
        self.production_cycles = []
        self.cycle_statistics = {}
        
    def find_production_segments(self, min_duration: str = "5s", max_duration: str = "300s") -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
        """
        Find production segments based on production state mask.
        
        Args:
            min_duration: Minimum duration for a valid cycle
            max_duration: Maximum duration for a valid cycle
            
        Returns:
            List of (start_time, end_time) tuples for production segments
        """
        if 'production_state' not in self.state_masks:
            raise ValueError("Production state mask not found in state_masks")
        
        production_mask = self.state_masks['production_state']

        # Créer un groupe de valeurs consécutives identiques (True/False)
        self.energy_data["groups"] = (production_mask != production_mask.shift()).cumsum()

        # Filtrer uniquement les groupes avec mask=True (production)
        production_groups = self.energy_data[production_mask].groupby("groups")

        min_td = pd.Timedelta(min_duration)
        max_td = pd.Timedelta(max_duration)

        segments = []
        for _, group in production_groups:
            start_time = group.index[0]
            end_time = group.index[-1]
            duration = end_time - start_time
            if min_td <= duration <= max_td:
                segments.append((start_time, end_time))

        return segments

    
    def segment_cycles(self, min_duration: str = "5s", max_duration: str = "300s",
                      ) -> List[ProductionCycle]:
        """
        Segment energy data into production cycles.
        
        Args:
            min_duration: Minimum duration for a valid cycle
            max_duration: Maximum duration for a valid cycle
            
        Returns:
            List of ProductionCycle objects
        """
        # Find production segments
        segments = self.find_production_segments(min_duration, max_duration)
        # Create ProductionCycle objects
        self.production_cycles = []
        
        for cycle_id, (start_time, end_time) in enumerate(segments):
            # Get cycle data
            cycle_mask = (self.energy_data.index >= start_time) & (self.energy_data.index <= end_time)
            cycle_energy = self.energy_data.loc[cycle_mask, self.energy_column]
            
            # Calculate cycle characteristics
            duration = end_time - start_time
            total_energy = cycle_energy.sum()
            peak_energy = cycle_energy.max()
            average_energy = cycle_energy.mean()
            variation = cycle_energy.std() / cycle_energy.mean() if cycle_energy.mean() > 0 else 0

            # Create cycle object
            cycle = ProductionCycle(
                cycle_id=cycle_id,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                energy_consumption=total_energy,
                peak_energy=peak_energy,
                average_energy=average_energy,
                variation=variation
            )
            
            self.production_cycles.append(cycle)
        
        # Calculate statistics
        self._calculate_cycle_statistics()
        
        logger.info(f"Detected {len(self.production_cycles)} production cycles")
        return self.production_cycles
    
    def _calculate_cycle_statistics(self) -> None:
        """Calculate statistics for all detected cycles."""
        if not self.production_cycles:
            self.cycle_statistics = {}
            return
        
        durations = [cycle.duration.total_seconds() for cycle in self.production_cycles]
        energy_consumptions = [cycle.energy_consumption for cycle in self.production_cycles]
        peak_energies = [cycle.peak_energy for cycle in self.production_cycles]
        variations = [cycle.variation for cycle in self.production_cycles]

        self.cycle_statistics = {
            'total_cycles': len(self.production_cycles),
            'duration_stats': {
                'mean': np.mean(durations),
                'std': np.std(durations),
                'min': np.min(durations),
                'max': np.max(durations),
                'median': np.median(durations)
            },
            'energy_stats': {
                'mean': np.mean(energy_consumptions),
                'std': np.std(energy_consumptions),
                'mean_peak': np.mean(peak_energies),
                'std_peak': np.std(peak_energies),
                'total_energy': np.sum(energy_consumptions)
            },
            'variation_stats': {
                'mean': np.mean(variations),
                'std': np.std(variations),
                'min': np.min(variations),
                'max': np.max(variations),
                'median': np.median(variations)
            }
        }
    
    def get_cycles(self) -> List[ProductionCycle]:
        """
        Get all detected production cycles.
        
        Returns:
            List of ProductionCycle objects
        """
        return self.production_cycles
    
    def get_cycle_statistics(self) -> Dict:
        """
        Get statistics for all detected cycles.
        
        Returns:
            Dictionary with cycle statistics
        """
        return self.cycle_statistics
    
    def get_cycles_dataframe(self) -> pd.DataFrame:
        """
        Convert cycles to DataFrame for analysis.
        
        Returns:
            DataFrame with cycle information
        """
        if not self.production_cycles:
            return pd.DataFrame()
        
        cycle_data = []
        for cycle in self.production_cycles:
            cycle_data.append({
                'cycle_id': cycle.cycle_id,
                'start_time': cycle.start_time,
                'end_time': cycle.end_time,
                'duration_seconds': cycle.duration.total_seconds(),
                'energy_consumption': cycle.energy_consumption,
                'peak_energy': cycle.peak_energy,
                'average_energy': cycle.average_energy,
                'variation': cycle.variation
            })
        
        return pd.DataFrame(cycle_data)