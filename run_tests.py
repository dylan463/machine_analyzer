#!/usr/bin/env python3
"""
Simple script to run all tests for the machine energy analysis project.
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests using pytest."""
    print("🧪 Running tests for Machine Energy Analysis Project...")
    print("=" * 50)
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "--verbose",
        "tests/test_cycle_segmenter.py",
        "tests/test_quality_analyzer.py",
        "tests/test_report_generator.py",
        "tests/test_machine_data_loader.py",
        "tests/test_state_detector.py",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Print summary
        print("=" * 50)
        if result.returncode == 0:
            print("✅ All tests passed successfully!")
        else:
            print(f"❌ Some tests failed (exit code: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 