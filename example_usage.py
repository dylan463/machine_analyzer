"""
Simple example demonstrating the machine energy analysis workflow.
This is a beginner-friendly example that shows how to use all the classes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
# Import our classes
from machine_analyzer.machine_data_loader import MachineDataLoader
from machine_analyzer.state_detector import StateDetector
from machine_analyzer.cycle_segmenter import CycleSegmenter
from machine_analyzer.quality_analyzer import QualityAnalyzer
from machine_analyzer.report_generator import ReportGenerator


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_sample_data():
    """Create sample energy consumption data for demonstration."""
    logger.info("Creating sample energy consumption data...")
    
    # Create time series with realistic energy patterns
    start_time = datetime(2024, 1, 1, 8, 0, 0)  # 8 AM start
    end_time = datetime(2024, 1, 1, 12, 0, 0)   # 12 PM end (4 hours)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='1min')
    
    # Create realistic energy consumption patterns
    energy_values = []
    current_time = start_time
    
    while current_time <= end_time:
        # Base energy consumption
        base_energy = 50
        
        # Add production cycle patterns (every 15 minutes)
        cycle_minute = (current_time - start_time).total_seconds() / 60
        cycle_phase = (cycle_minute % 15) / 15  # 0 to 1 over each cycle
        
        if cycle_phase < 0.3:  # Startup phase
            energy = base_energy + 100 * cycle_phase / 0.3
        elif cycle_phase < 0.7:  # Production phase
            energy = base_energy + 100 + np.random.normal(0, 5)
        elif cycle_phase < 0.9:  # Shutdown phase
            energy = base_energy + 100 * (1 - (cycle_phase - 0.7) / 0.2)
        else:  # Idle phase
            energy = base_energy + np.random.normal(0, 2)
        
        # Add some noise and ensure positive values
        energy += np.random.normal(0, 3)
        energy = max(10, energy)
        
        energy_values.append(energy)
        current_time += timedelta(minutes=1)
    
    # Create DataFrame
    energy_data = pd.DataFrame({
        'timestamp': timestamps,
        'value': energy_values
    })
    
    # Set timestamp as index
    energy_data.set_index('timestamp', inplace=True)
    
    logger.info(f"Created sample data with {len(energy_data)} data points")
    return energy_data


def main():
    """Main function demonstrating the complete workflow."""
    logger.info("Starting machine energy analysis workflow...")
    
    # Step 1: Create sample data
    energy_data = create_sample_data()
    
    # Step 2: Load and preprocess data
    logger.info("Step 1: Loading and preprocessing data...")
    data_loader = MachineDataLoader()
    
    # In real scenario, you would load from file:
    # energy_data = data_loader.load_data("data/Datadump.txt")
    
    # Preprocess the data
    processed_data = data_loader.preprocess_data(energy_data, energy_column="value")
    logger.info(f"Processed data shape: {processed_data.shape}")
    
    # Step 3: Detect machine states
    logger.info("Step 2: Detecting machine states...")
    state_detector = StateDetector(processed_data, energy_column="value")
    
    # Detect states using energy consumption patterns
    state_detector.preprocess_states(window_size="5s", production_threshold=60,iqr_coefficients=(3,3,1.5,3))
    state_data = state_detector.get_state_masks()
    logger.info(f"Detected {len(state_data)} unique states")
    
    # Get state masks for production cycles
    production_mask = state_data['production_state']

    processed_data = state_detector.get_processed_data()

    # Step 4: Segment production cycles
    logger.info("Step 3: Segmenting production cycles...")
    cycle_segmenter = CycleSegmenter(processed_data, {'production_state': production_mask}, energy_column="value")
    
    # Segment cycles using the production mask with adjusted parameters
    production_cycles = cycle_segmenter.segment_cycles(min_duration="2s", max_duration="1h")
    cycle_statistics = cycle_segmenter.get_cycle_statistics()
    logger.info(f"Segmented {len(production_cycles)} production cycles")
    
    # Step 5: Quality analysis and counting
    logger.info("Step 4: Performing quality analysis and counting...")
    quality_analyzer = QualityAnalyzer(cycle_statistics, production_cycles)
    
    # Analyze quality of all cycles
    quality_metrics = quality_analyzer.analyze_quality(threshold_factor={"variation": 2, "duration": 2, "energy": 2})
    logger.info(f"Quality analysis completed for {len(quality_metrics)} cycles")
    
    # Get quality summary
    quality_summary = quality_analyzer.get_quality_summary()
    print(f"Quality summary:")
    for key, value in quality_summary.items():
        print(f"   • {key}: {value}")
    
    # Get anomalous units
    anomalous_units = quality_analyzer.get_anomalous_units()
    logger.info(f"Anomalous units detected: {anomalous_units}")
    
    # Step 6: Generate reports
    logger.info("Step 5: Generating reports...")
    report_generator = ReportGenerator(output_dir="reports")
    
    # Generate simple text report
    text_report_path = report_generator.generate_simple_report(
        processed_data,
        production_cycles,
        quality_metrics,
        anomalous_units
    )
    logger.info(f"Text report generated: {text_report_path}")
    
    # Generate CSV report
    csv_report_path = report_generator.generate_csv_report(production_cycles, quality_metrics)
    logger.info(f"CSV report generated: {csv_report_path}")
    
    # Generate summary statistics
    summary_stats = report_generator.generate_summary_statistics(
        processed_data,
        production_cycles,
        quality_metrics,
        anomalous_units
    )
    logger.info("Summary statistics generated")
    
    # Step 7: Display key results
    logger.info("\n" + "="*50)
    logger.info("ANALYSIS RESULTS SUMMARY")
    logger.info("="*50)
    
    print(f"\nProduction Analysis:")
    print(f"   • Total production cycles: {len(production_cycles)}")
    if production_cycles:
        print(f"   • Average cycle duration: {np.mean([c.duration.total_seconds() for c in production_cycles]):.1f} seconds")
    else:
        print(f"   • Average cycle duration: N/A (no cycles detected)")
    
    print(f"\nQuality Assessment:")
    print(f"   • Average quality score: {quality_summary.get('average_quality_score', 0):.2f}")
    print(f"   • Anomalous units: {len(anomalous_units)}")
    print(f"   • Quality grade distribution: {quality_summary.get('quality_grade_distribution', {})}")
    
    print(f"\nEnergy Analysis:")
    print(f"   • Total energy consumed: {energy_data['value'].sum():.1f}")
    if production_cycles:
        print(f"   • Average energy per cycle: {np.mean([c.energy_consumption for c in production_cycles]):.1f}")
    else:
        print(f"   • Average energy per cycle: N/A (no cycles detected)")
    print(f"   • Peak energy consumption: {energy_data['value'].max():.1f}")
    
    if anomalous_units:
        print(f"\nAnomalous Units Detected:")

        for unit_id in anomalous_units:
            metric = next((m for m in quality_metrics if m.cycle_id == unit_id), None)
            if metric:
                print(f"   • Cycle {unit_id}: Quality {metric.quality_grade} (Score: {metric.quality_score:.2f})")
                if metric.issues:
                    print(f"     Issues: {', '.join(metric.issues)}")
    
    print(f"\nReports Generated:")
    print(f"   • Text Report: {text_report_path}")
    print(f"   • CSV Report: {csv_report_path}")
    
    logger.info("Complete analysis workflow finished successfully!")
    
    return {
        'energy_data': energy_data,

        'processed_data': processed_data,
        'state_data': state_data,
        'production_cycles': production_cycles,
        'quality_metrics': quality_metrics,
        'anomalous_units': anomalous_units,
        'quality_summary': quality_summary,

        'text_report_path': text_report_path,
        'csv_report_path': csv_report_path,
        'summary_stats': summary_stats
    }


if __name__ == "__main__":
    try:
        results = main()
        print(f"\nAnalysis completed successfully!")
        print(f"Check the 'reports' directory for generated reports.")
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        print(f"\nAnalysis failed: {e}")
        raise 