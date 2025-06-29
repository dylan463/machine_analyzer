"""
Quality Analyzer - Simple quality assessment for production cycles.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from dataclasses import dataclass
import logging
from machine_analyzer.cycle_segmenter import ProductionCycle

logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    """Simple quality metrics for a production cycle."""
    cycle_id: int
    quality_score: float
    quality_grade: str
    is_anomalous: bool
    issues: List[str]


class QualityAnalyzer:
    """
    Simple quality analyzer for production cycles.
    """
    
    def __init__(self,cycle_statistics: dict,production_cycles: List[ProductionCycle]):
        """
        Initialize the quality analyzer.
        
        Args:
            cycle_statistics: Dictionary containing cycle statistics
            production_cycles: List of production cycles to analyze
        """
        self.cycle_statistics = cycle_statistics
        self.production_cycles = production_cycles
        self.quality_metrics = []
        self.anomalous_units = []
        
    
    def analyze_quality(self,threshold_factor: dict = {"variation": 2, "duration": 2, "energy": 2}) -> List[QualityMetrics]:
        """
        Analyze quality of all production cycles.
        
        Returns:
            List of QualityMetrics objects
        """
        self.quality_metrics = []
        self.anomalous_units = []
        
        # Check if cycle statistics are available
        if not self.cycle_statistics or not self.production_cycles:
            logger.warning("No cycle statistics or production cycles available for quality analysis")
            return []
        
        for cycle in self.production_cycles:
            # Get cycle energy data
            anomaly_count = 0
            issues = []
            
            try:
                # Check variation
                if 'variation_stats' in self.cycle_statistics and 'mean' in self.cycle_statistics['variation_stats'] and 'std' in self.cycle_statistics['variation_stats']:
                    if cycle.variation > self.cycle_statistics["variation_stats"]["mean"] + threshold_factor["variation"] * self.cycle_statistics["variation_stats"]["std"]:
                        anomaly_count += 1
                        issues.append("Variation is too high")
                
                # Check duration
                if 'duration_stats' in self.cycle_statistics and 'mean' in self.cycle_statistics['duration_stats'] and 'std' in self.cycle_statistics['duration_stats']:
                    if cycle.duration.total_seconds() < self.cycle_statistics["duration_stats"]["mean"] - threshold_factor["duration"] * self.cycle_statistics["duration_stats"]["std"]:
                        anomaly_count += 1
                        issues.append("Duration is too short")
                
                # Check energy consumption
                if 'energy_stats' in self.cycle_statistics and 'mean' in self.cycle_statistics['energy_stats'] and 'std' in self.cycle_statistics['energy_stats']:
                    if cycle.energy_consumption > self.cycle_statistics["energy_stats"]["mean"] + threshold_factor["energy"] * self.cycle_statistics["energy_stats"]["std"]:
                        anomaly_count += 1
                        issues.append("Energy consumption is too high")
                        
            except Exception as e:
                logger.error(f"Error analyzing cycle {cycle.cycle_id}: {e}")
                logger.error(f"Cycle statistics: {self.cycle_statistics}")
                continue
            
            quality_score = 1 - anomaly_count / 3

            quality_grade = "A"
            if quality_score >= 0.8:
                quality_grade = "A"
            elif quality_score >= 0.6:
                quality_grade = "B"
            elif quality_score >= 0.4:
                quality_grade = "C"
            else:
                quality_grade = "D"
            
            quality_metrics = QualityMetrics(
                cycle_id=cycle.cycle_id,
                quality_score=quality_score,
                quality_grade=quality_grade,
                is_anomalous=anomaly_count > 0,
                issues=issues
            )

            self.quality_metrics.append(quality_metrics)
            if anomaly_count > 0:
                self.anomalous_units.append(cycle.cycle_id) 
            
        logger.info(f"Quality analysis completed: {len(self.quality_metrics)} cycles analyzed")
        logger.info(f"Anomalous units detected: {len(self.anomalous_units)}")
        
        return self.quality_metrics
    
    def get_quality_summary(self) -> Dict:
        """
        Get simple summary of quality analysis.
        
        Returns:
            Dictionary with quality summary
        """
        if not self.quality_metrics:
            return {}
        
        
        quality_scores = [metric.quality_score for metric in self.quality_metrics]
        
        # Count grades
        grade_counts = {}
        for metric in self.quality_metrics:
            grade_counts[metric.quality_grade] = grade_counts.get(metric.quality_grade, 0) + 1
        
        return {
            'total_cycles': len(self.quality_metrics),
            'anomalous_cycles': len(self.anomalous_units),
            'average_quality_score': np.mean(quality_scores),
            'quality_grade_distribution': grade_counts,
        }
    
    def get_anomalous_units(self) -> List[int]:
        """
        Get list of anomalous unit IDs.
        
        Returns:
            List of anomalous cycle IDs
        """
        return self.anomalous_units
    
    def get_quality_metrics(self) -> List[QualityMetrics]:
        """
        Get all quality metrics.
        
        Returns:
            List of QualityMetrics objects
        """
        return self.quality_metrics 