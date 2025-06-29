"""
Machine Energy Analyzer

A comprehensive tool for analyzing machine energy consumption and production cycles.
"""

try:
    from .machine_data_loader import MachineDataLoader
    from .state_detector import StateDetector
    from .cycle_segmenter import CycleSegmenter
    from .quality_analyzer import QualityAnalyzer
    from .report_generator import ReportGenerator
except ImportError:
    # Handle case where package isn't installed yet
    MachineDataLoader = None
    StateDetector = None
    CycleSegmenter = None
    QualityAnalyzer = None
    ReportGenerator = None

__version__ = "1.0.0"
__all__ = [
    "MachineDataLoader",
    "StateDetector", 
    "CycleSegmenter",
    "QualityAnalyzer",
    "ReportGenerator"
] 