#!/usr/bin/env python3
"""
Load testing script for machine_analyzer package.
"""
import argparse
import time
import psutil
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

from machine_analyzer import (
    MachineDataLoader,
    StateDetector,
    CycleSegmenter,
    QualityAnalyzer,
    ReportGenerator
)


def create_test_dataset(size):
    """Create a test dataset of specified size."""
    np.random.seed(42)
    timestamps = pd.date_range('2023-01-01', periods=size, freq='1S')
    energy_values = np.random.normal(50, 20, size)
    
    # Add production cycles
    for i in range(0, size, size // 10):
        cycle_length = min(100, size // 20)
        energy_values[i:i+cycle_length] = np.random.normal(200, 30, cycle_length)
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'value': energy_values
    })


def run_analysis_pipeline(data):
    """Run the complete analysis pipeline on a dataset."""
    try:
        # Load and preprocess data
        loader = MachineDataLoader()
        processed_data = loader.load_data(data)
        
        # Detect states
        detector = StateDetector(processed_data, "value")
        state_masks = detector.detect_states()
        
        # Segment cycles
        segmenter = CycleSegmenter(processed_data, state_masks, "value")
        production_cycles = segmenter.segment_cycles()
        
        # Analyze quality
        analyzer = QualityAnalyzer(processed_data, production_cycles, "value")
        quality_metrics = analyzer.analyze_quality()
        
        # Generate report
        report_gen = ReportGenerator()
        report_path = report_gen.generate_simple_report(
            processed_data, production_cycles, quality_metrics, {}, []
        )
        
        return {
            'success': True,
            'cycles_found': len(production_cycles),
            'report_path': report_path
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def monitor_system_resources():
    """Monitor system resources during load testing."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_available': memory.available / (1024**3),  # GB
        'memory_used': memory.used / (1024**3)  # GB
    }


def run_concurrent_tests(dataset_size, num_concurrent, use_processes=False):
    """Run concurrent analysis tests."""
    print(f"Running {num_concurrent} concurrent tests with dataset size {dataset_size}")
    print(f"Using {'processes' if use_processes else 'threads'}")
    
    # Create test datasets
    datasets = [create_test_dataset(dataset_size) for _ in range(num_concurrent)]
    
    # Monitor initial system state
    initial_resources = monitor_system_resources()
    print(f"Initial CPU: {initial_resources['cpu_percent']}%")
    print(f"Initial Memory: {initial_resources['memory_percent']}%")
    
    # Run concurrent tests
    start_time = time.time()
    
    if use_processes:
        with ProcessPoolExecutor(max_workers=num_concurrent) as executor:
            results = list(executor.map(run_analysis_pipeline, datasets))
    else:
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            results = list(executor.map(run_analysis_pipeline, datasets))
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Monitor final system state
    final_resources = monitor_system_resources()
    
    # Calculate statistics
    successful_tests = sum(1 for r in results if r['success'])
    failed_tests = len(results) - successful_tests
    
    if successful_tests > 0:
        avg_cycles = sum(r.get('cycles_found', 0) for r in results if r['success']) / successful_tests
    else:
        avg_cycles = 0
    
    # Print results
    print(f"\n=== Load Test Results ===")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Successful tests: {successful_tests}/{len(results)}")
    print(f"Failed tests: {failed_tests}")
    print(f"Average cycles found: {avg_cycles:.1f}")
    print(f"Throughput: {len(results)/total_time:.2f} tests/second")
    print(f"Final CPU: {final_resources['cpu_percent']}%")
    print(f"Final Memory: {final_resources['memory_percent']}%")
    
    return {
        'total_time': total_time,
        'successful_tests': successful_tests,
        'failed_tests': failed_tests,
        'throughput': len(results)/total_time,
        'avg_cycles': avg_cycles,
        'initial_resources': initial_resources,
        'final_resources': final_resources
    }


def run_scalability_test():
    """Run scalability test with different dataset sizes."""
    print("=== Scalability Test ===")
    
    sizes = [1000, 5000, 10000, 20000]
    results = {}
    
    for size in sizes:
        print(f"\nTesting dataset size: {size}")
        data = create_test_dataset(size)
        
        start_time = time.time()
        result = run_analysis_pipeline(data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        results[size] = {
            'execution_time': execution_time,
            'success': result['success'],
            'cycles_found': result.get('cycles_found', 0)
        }
        
        print(f"Execution time: {execution_time:.2f}s")
        print(f"Success: {result['success']}")
        print(f"Cycles found: {result.get('cycles_found', 0)}")
    
    # Print scalability summary
    print(f"\n=== Scalability Summary ===")
    for size in sizes:
        result = results[size]
        print(f"Size {size}: {result['execution_time']:.2f}s "
              f"({result['cycles_found']} cycles)")


def main():
    parser = argparse.ArgumentParser(description='Load testing for machine_analyzer')
    parser.add_argument('--dataset-size', type=int, default=1000,
                       help='Size of test dataset')
    parser.add_argument('--concurrent', type=int, default=4,
                       help='Number of concurrent tests')
    parser.add_argument('--use-processes', action='store_true',
                       help='Use processes instead of threads')
    parser.add_argument('--scalability', action='store_true',
                       help='Run scalability test')
    
    args = parser.parse_args()
    
    if args.scalability:
        run_scalability_test()
    else:
        run_concurrent_tests(args.dataset_size, args.concurrent, args.use_processes)


if __name__ == "__main__":
    main() 