# SBARDS Project - Python Scanner Components
# This package contains the Python components of the SBARDS Project scanner

import sys
import logging

logger = logging.getLogger("SBARDSScanner")

# Define available components
__all__ = [
    'run_scan',
    'Orchestrator',
    'YaraScanner',
    'FileTypeDetector',
    'RuleUpdater',
    'ThreatIntelligence'
]

# Import components with error handling
try:
    from .orchestrator import run_scan, Orchestrator
except ImportError as e:
    logger.warning(f"Failed to import orchestrator: {e}")
    # Create dummy Orchestrator class
    class Orchestrator:
        def __init__(self):
            print("WARNING: Orchestrator module could not be loaded")
        def scan_file(self, *args, **kwargs):
            print("ERROR: Orchestrator module not available")
            return {"error": "Orchestrator module not available"}
        def scan_directory(self, *args, **kwargs):
            print("ERROR: Orchestrator module not available")
            return [{"error": "Orchestrator module not available"}]
        def update_rules(self, *args, **kwargs):
            print("ERROR: Orchestrator module not available")
            return False

try:
    from .yara_wrapper import YaraScanner
except ImportError as e:
    logger.warning(f"Failed to import yara_wrapper: {e}")
    # Create dummy YaraScanner class
    class YaraScanner:
        def __init__(self, *args, **kwargs):
            print("WARNING: YARA module could not be loaded. Install yara-python for full functionality.")
        def scan_file(self, *args, **kwargs):
            return []

try:
    from .file_type_detector import FileTypeDetector
except ImportError as e:
    logger.warning(f"Failed to import file_type_detector: {e}")
    # Create dummy FileTypeDetector class
    class FileTypeDetector:
        def __init__(self):
            print("WARNING: FileTypeDetector module could not be loaded")
        def detect_file_type(self, *args, **kwargs):
            return {"mime_type": "unknown", "category": "unknown"}

try:
    from .rule_updater import RuleUpdater
except ImportError as e:
    logger.warning(f"Failed to import rule_updater: {e}")
    # Create dummy RuleUpdater class
    class RuleUpdater:
        def __init__(self, *args, **kwargs):
            print("WARNING: RuleUpdater module could not be loaded")
        def update_rules(self, *args, **kwargs):
            return False
        def get_all_rule_info(self, *args, **kwargs):
            return []

try:
    from .threat_intel import ThreatIntelligence
except ImportError as e:
    logger.warning(f"Failed to import threat_intel: {e}")
    # Create dummy ThreatIntelligence class
    class ThreatIntelligence:
        def __init__(self):
            print("WARNING: ThreatIntelligence module could not be loaded")
        def check_file(self, *args, **kwargs):
            return {"malicious": 0, "suspicious": 0, "benign": 0, "unknown": 1}
