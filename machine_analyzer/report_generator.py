"""
Report Generator - Simple report generation for machine energy analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Simple report generator for machine energy analysis.
    """
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize the report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_simple_report(self, 
                             energy_data: pd.DataFrame,
                             production_cycles: List,
                             quality_metrics: List,
                             anomalous_units: List[int]) -> str:
        """
        Generate a simple analysis report.
        
        Args:
            energy_data: Processed energy data
            production_cycles: List of production cycles
            quality_metrics: List of quality metrics
            production_counts: Production counts by time period
            anomalous_units: List of anomalous unit IDs
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"machine_analysis_report_{timestamp}.txt"
        report_path = os.path.join(self.output_dir, report_filename)
        
        # Generate simple text report
        report_content = self._create_simple_report(
            energy_data, production_cycles, quality_metrics, 
            anomalous_units
        )
        
        # Save report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"Generated simple report: {report_path}")
        return report_path
    
    def _create_simple_report(self, energy_data: pd.DataFrame, production_cycles: List,
                            quality_metrics: List,
                            anomalous_units: List[int]) -> str:
        """Create simple text report content."""
        
        report_lines = []
        report_lines.append("=" * 50)
        report_lines.append("MACHINE ENERGY ANALYSIS REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 20)
        total_cycles = len(production_cycles)
        anomalous_count = len(anomalous_units)
        
        # Calculate average quality score
        avg_quality = 0
        if quality_metrics:
            avg_quality = np.mean([metric.quality_score for metric in quality_metrics])
        
        report_lines.append(f"Total Production Cycles: {total_cycles}")
        report_lines.append(f"Anomalous Units: {anomalous_count}")
        report_lines.append(f"Average Quality Score: {avg_quality:.2f}")
        report_lines.append("")
        
        # Production Analysis
        report_lines.append("PRODUCTION ANALYSIS")
        report_lines.append("-" * 20)
        if production_cycles:
            durations = [cycle.duration.total_seconds() for cycle in production_cycles]
            energy_consumptions = [cycle.energy_consumption for cycle in production_cycles]
            
            avg_duration = np.mean(durations)
            avg_energy = np.mean(energy_consumptions)
            total_energy = np.sum(energy_consumptions)
            
            report_lines.append(f"Average Cycle Duration: {avg_duration:.1f} seconds")
            report_lines.append(f"Average Energy per Cycle: {avg_energy:.1f}")
            report_lines.append(f"Total Energy Consumed: {total_energy:.1f}")
            report_lines.append("")
        
        # Quality Assessment
        report_lines.append("QUALITY ASSESSMENT")
        report_lines.append("-" * 20)
        if quality_metrics:
            # Count grades
            grade_counts = {}
            for metric in quality_metrics:
                grade_counts[metric.quality_grade] = grade_counts.get(metric.quality_grade, 0) + 1
            
            report_lines.append("Quality Grade Distribution:")
            for grade, count in grade_counts.items():
                report_lines.append(f"  Grade {grade}: {count} cycles")
            report_lines.append("")
        
        # Anomalous Units
        if anomalous_units:
            report_lines.append("ANOMALOUS UNITS")
            report_lines.append("-" * 20)
            report_lines.append(f"Found {len(anomalous_units)} anomalous units:")
            for unit_id in anomalous_units:
                report_lines.append(f"  Cycle ID: {unit_id}")
            report_lines.append("")
        
        # Energy Statistics
        report_lines.append("ENERGY STATISTICS")
        report_lines.append("-" * 20)
        if not energy_data.empty:
            energy_series = energy_data.iloc[:, 0]
            report_lines.append(f"Total Energy: {energy_series.sum():.1f}")
            report_lines.append(f"Average Energy: {energy_series.mean():.1f}")
            report_lines.append(f"Peak Energy: {energy_series.max():.1f}")
            report_lines.append(f"Minimum Energy: {energy_series.min():.1f}")
            report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS")
        report_lines.append("-" * 20)
        recommendations = []
        
        if anomalous_units:
            anomalous_rate = len(anomalous_units) / len(production_cycles) if production_cycles else 0
            if anomalous_rate > 0.1:
                recommendations.append("High anomalous unit rate detected. Investigate root causes.")
            else:
                recommendations.append("Some anomalous units detected. Monitor production process.")
        
        if quality_metrics:
            avg_quality = np.mean([metric.quality_score for metric in quality_metrics])
            if avg_quality < 0.7:
                recommendations.append("Low average quality score. Review production process.")
        
        if not recommendations:
            recommendations.append("No significant issues detected. Continue monitoring.")
        
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec}")
        
        report_lines.append("")
        report_lines.append("=" * 50)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 50)
        
        return "\n".join(report_lines)
    
    def generate_csv_report(self, production_cycles: List, quality_metrics: List) -> str:
        """
        Generate CSV report with cycle and quality data.
        
        Args:
            production_cycles: List of production cycles
            quality_metrics: List of quality metrics
            
        Returns:
            Path to generated CSV report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"cycle_quality_report_{timestamp}.csv"
        csv_path = os.path.join(self.output_dir, csv_filename)
        
        # Combine cycle data with quality metrics
        report_data = []
        for i, cycle in enumerate(production_cycles):
            quality_metric = quality_metrics[i] if i < len(quality_metrics) else None
            
            cycle_data = {
                'cycle_id': cycle.cycle_id,
                'start_time': cycle.start_time,
                'end_time': cycle.end_time,
                'duration_seconds': cycle.duration.total_seconds(),
                'energy_consumption': cycle.energy_consumption
            }
            
            if quality_metric:
                cycle_data.update({
                    'quality_score': quality_metric.quality_score,
                    'quality_grade': quality_metric.quality_grade,
                    'is_anomalous': quality_metric.is_anomalous,
                    'issues': '; '.join(quality_metric.issues)
                })
            
            report_data.append(cycle_data)
        
        # Create DataFrame and save
        report_df = pd.DataFrame(report_data)
        report_df.to_csv(csv_path, index=False)
        
        logger.info(f"Generated CSV report: {csv_path}")
        return csv_path
    
    def generate_summary_statistics(self, energy_data: pd.DataFrame, 
                                  production_cycles: List, quality_metrics: List,
                                  anomalous_units: List[int]) -> Dict:
        """
        Generate summary statistics for the analysis.
        
        Args:
            energy_data: Processed energy data
            production_cycles: List of production cycles
            quality_metrics: List of quality metrics
            anomalous_units: List of anomalous unit IDs
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            "analysis_timestamp": datetime.now().isoformat(),
            "data_period": {
                "start": energy_data.index.min() if not energy_data.empty else None,
                "end": energy_data.index.max() if not energy_data.empty else None,
                "duration_hours": (energy_data.index.max() - energy_data.index.min()).total_seconds() / 3600 if not energy_data.empty else 0
            },
            "energy_statistics": {
                "total_energy": energy_data.iloc[:, 0].sum() if not energy_data.empty else 0,
                "average_energy": energy_data.iloc[:, 0].mean() if not energy_data.empty else 0,
                "peak_energy": energy_data.iloc[:, 0].max() if not energy_data.empty else 0
            },
            "production_summary": {
                "total_cycles": len(production_cycles),
                "anomalous_units": len(anomalous_units),
                "average_quality_score": np.mean([metric.quality_score for metric in quality_metrics]) if quality_metrics else 0
            }
        }
        
        return summary 