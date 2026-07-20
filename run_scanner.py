#!/usr/bin/env python3
"""
SBARDSProject - Comprehensive Security Scanning System
Main execution script for the scanner

This script provides a unified interface for scanning files and directories
for security threats using the SBARDS scanning engine.
"""

import os
import sys
import json
import argparse
import logging
import time
import threading
import multiprocessing
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add scanner_core to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scanner_core'))

# Check for required packages
missing_packages = []
try:
    # We don't use yara directly, but we check if it's available
    # pylint: disable=unused-import
    import yara
except ImportError:
    missing_packages.append("yara-python")

try:
    # We don't use magic directly, but we check if it's available
    # pylint: disable=unused-import
    import magic
except ImportError:
    missing_packages.append("python-magic")

try:
    # We don't use requests directly, but we check if it's available
    # pylint: disable=unused-import
    import requests
except ImportError:
    missing_packages.append("requests")

# Import scanner components
try:
    from scanner_core.python.orchestrator import Orchestrator
    # We import these for completeness, even if not used directly
    # pylint: disable=unused-import
    from scanner_core.python.rule_updater import RuleUpdater
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"Error importing scanner components: {e}")
    print("This may be due to missing dependencies.")

    if missing_packages:
        print("\nMissing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install the missing packages using:")
        print(f"  pip install {' '.join(missing_packages)}")

# Create dummy classes for missing components
class DummyOrchestrator:
    def __init__(self):
        print("WARNING: Using limited functionality due to missing dependencies")

    def scan_file(self, file_path, verbose=False):
        # Don't print here since we already print in scan_directory
        # verbose parameter is required for API compatibility
        # pylint: disable=unused-argument

        # Basic file analysis even without dependencies
        threats = []
        recommendation = "Unknown (missing dependencies)"
        file_type = "unknown"

        # Determine file type based on extension
        _, ext = os.path.splitext(file_path.lower())

        # Check for suspicious extensions
        suspicious_extensions = ['.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.dll', '.sys', '.sh', '.py']
        if any(file_path.lower().endswith(ext) for ext in suspicious_extensions):
            threats.append(f"Suspicious file extension: {ext}")
            recommendation = "Investigate"

            # For script files, do basic content analysis
            if ext in ['.bat', '.cmd', '.ps1', '.js', '.vbs', '.sh', '.py']:
                file_type = f"{ext[1:]} script"
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()

                        # Check for suspicious patterns
                        suspicious_patterns = [
                            # Windows-specific
                            'powershell', 'cmd.exe', 'system32', 'regedit', 'netsh',
                            'Invoke-WebRequest', 'Invoke-Expression', 'IEX', 'ExecutionPolicy Bypass',
                            'Hidden', 'HKEY_LOCAL_MACHINE', 'HKEY_CURRENT_USER', 'Run',

                            # Unix/Linux-specific
                            'chmod 777', 'chown', 'sudo', 'useradd', 'adduser', '/etc/passwd',
                            '/etc/shadow', '/etc/sudoers', 'iptables', 'systemctl',

                            # General
                            'http://', 'https://', 'wget', 'curl', 'nc ', 'netcat',
                            'eval(', 'base64', 'encrypt', 'decrypt', 'backdoor',
                            'exploit', 'vulnerability', 'hack', 'crack'
                        ]

                        found_patterns = []
                        for pattern in suspicious_patterns:
                            if pattern.lower() in content.lower():
                                found_patterns.append(pattern)

                        if found_patterns:
                            threats.append(f"Found suspicious patterns: {', '.join(found_patterns)}")
                            if len(found_patterns) > 3:
                                recommendation = "Quarantine"
                except Exception as e:
                    threats.append(f"Error analyzing file content: {str(e)}")

        # Check for text files with suspicious content
        elif ext in ['.txt', '.log', '.cfg', '.ini', '.json', '.xml', '.html', '.md']:
            file_type = f"{ext[1:]} file"
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()

                    # Check for suspicious patterns
                    suspicious_patterns = [
                        # Windows-specific
                        'powershell', 'cmd.exe', 'system32', 'regedit', 'netsh',
                        'Invoke-WebRequest', 'Invoke-Expression', 'IEX', 'ExecutionPolicy Bypass',
                        'HKEY_LOCAL_MACHINE', 'HKEY_CURRENT_USER',

                        # Unix/Linux-specific
                        'chmod 777', 'chown', 'sudo', 'useradd', '/etc/passwd',
                        '/etc/shadow', '/etc/sudoers', 'iptables',

                        # General
                        'eval(', 'base64_decode', 'encrypt', 'decrypt',
                        'malicious', 'exploit', 'vulnerability', 'backdoor',
                        'trojan', 'virus', 'ransomware', 'keylogger',
                        'hack', 'crack', 'phishing', 'botnet'
                    ]

                    found_patterns = []
                    for pattern in suspicious_patterns:
                        if pattern.lower() in content.lower():
                            found_patterns.append(pattern)

                    if found_patterns:
                        threats.append(f"Found suspicious patterns: {', '.join(found_patterns)}")
                        if len(found_patterns) > 2:
                            recommendation = "Investigate"
                        else:
                            recommendation = "Monitor"
            except Exception as e:
                threats.append(f"Error analyzing file content: {str(e)}")

        # If no threats found and it's a common safe file type, mark as safe
        if not threats and ext in ['.txt', '.log', '.md']:
            recommendation = "Safe"
            threats = []

        return {
            "file_path": file_path,
            "recommendation": recommendation,
            "threats": threats if threats else ["Cannot fully scan due to missing dependencies"],
            "file_type": file_type
        }

    def scan_directory(self, dir_path, recursive=False, verbose=False):
        print(f"Scanning directory: {dir_path} (recursive: {recursive})")
        files = []

        if not os.path.exists(dir_path):
            print(f"Directory not found: {dir_path}")
            return files

        # Use ThreadPoolExecutor for parallel scanning
        try:
            # Collect all files to scan
            file_paths = []

            if recursive:
                # Recursively walk directory
                for root, dirs, filenames in os.walk(dir_path):
                    # Print subdirectories if verbose
                    if verbose and dirs:
                        print(f"Found subdirectories in {root}: {', '.join(dirs)}")

                    for filename in filenames:
                        file_paths.append(os.path.join(root, filename))
            else:
                # Get files in current directory only
                for item in os.listdir(dir_path):
                    full_path = os.path.join(dir_path, item)
                    if os.path.isfile(full_path):
                        file_paths.append(full_path)

            # Sort for consistent results
            file_paths.sort()

            # Print files to be scanned
            for file_path in file_paths:
                print(f"Scanning file: {file_path}")

            # Determine optimal number of workers
            max_workers = min(32, (multiprocessing.cpu_count() or 1) * 2)

            # Use ThreadPoolExecutor for parallel scanning if we have multiple files
            if len(file_paths) > 1:
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Submit all scan tasks
                    future_to_file = {executor.submit(self.scan_file, file_path, verbose): file_path
                                     for file_path in file_paths}

                    # Process results as they complete
                    for future in as_completed(future_to_file):
                        result = future.result()
                        files.append(result)
            else:
                # For a single file, just scan directly
                for file_path in file_paths:
                    files.append(self.scan_file(file_path, verbose))

        except Exception as e:
            print(f"Error scanning directory: {str(e)}")

        return files

    def update_rules(self):
        print("Cannot update rules due to missing dependencies")
        return False

# Use dummy classes
Orchestrator = DummyOrchestrator
COMPONENTS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'scan_history.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SBARDSScanner')

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='SBARDSProject - Comprehensive Security Scanning System')

    # Target specification
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument('target', nargs='?', help='File or directory to scan')
    target_group.add_argument('--all', action='store_true', help='Scan all files in samples directory')

    # Scan options
    parser.add_argument('--recursive', action='store_true', help='Recursively scan directories')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--no-save', action='store_true', help='Do not save scan results')
    parser.add_argument('--update-rules', action='store_true', help='Update YARA rules before scanning')

    # Output options
    parser.add_argument('--output', help='Output file for scan results (default: output/latest_results.json)')

    return parser.parse_args()

def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    default_config = {
        "paths": {
            "rules_dir": "rules",
            "samples_dir": "samples",
            "output_dir": "output",
            "logs_dir": "logs"
        },
        "scan_options": {
            "max_file_size": 104857600,
            "default_recursive": False,
            "parallel_scan": True,
            "max_workers": 0,
            "timeout_seconds": 300
        }
    }

    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        else:
            logger.warning(f"Configuration file not found at {config_path}, using defaults")
            return default_config
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return default_config

def ensure_directories():
    """Ensure required directories exist"""
    config = load_config()
    paths = config.get("paths", {})

    directories = [
        paths.get("rules_dir", "rules"),
        paths.get("samples_dir", "samples"),
        paths.get("output_dir", "output"),
        paths.get("logs_dir", "logs")
    ]

    # Add quarantine directory if enabled
    actions = config.get("actions", {})
    if actions.get("quarantine_enabled", False):
        directories.append(actions.get("quarantine_dir", "quarantine"))

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    logger.info("Directory structure verified")

def update_rules():
    """Update YARA rules"""
    logger.info("Updating YARA rules...")

    rule_updater = RuleUpdater()
    updated = rule_updater.update_rules()

    if updated:
        logger.info("YARA rules updated successfully")
    else:
        logger.warning("Failed to update YARA rules")

    return updated

def scan_file(orchestrator, file_path, verbose=False):
    """Scan a single file"""
    logger.info(f"Scanning file: {file_path}")

    try:
        result = orchestrator.scan_file(file_path, verbose)

        if result['recommendation'] == 'Quarantine':
            logger.warning(f"Threats detected in {file_path}: {result['threats']}")
        else:
            logger.info(f"Scan completed for {file_path}: {result['recommendation']}")

        return result
    except Exception as e:
        logger.error(f"Error scanning file {file_path}: {str(e)}")
        return {
            'file_path': file_path,
            'status': 'error',
            'error': str(e),
            'recommendation': 'Error'
        }

def scan_directory(orchestrator, dir_path, recursive=False, verbose=False):
    """
    Scan a directory using parallel processing for better performance

    Args:
        orchestrator: The scanner orchestrator instance
        dir_path: Path to the directory to scan
        recursive: Whether to scan subdirectories recursively
        verbose: Whether to print verbose output

    Returns:
        List of scan results for each file
    """
    logger.info(f"Scanning directory: {dir_path} (recursive: {recursive})")

    try:
        # Check if we should use the orchestrator's built-in directory scan
        # or our parallel implementation
        if not hasattr(orchestrator, 'scan_file') or isinstance(orchestrator, DummyOrchestrator):
            # Use orchestrator's built-in method if scan_file is not available
            # or if we're using the dummy orchestrator
            results = orchestrator.scan_directory(dir_path, recursive, verbose)

            # Ensure results is a list
            if not isinstance(results, list):
                results = [results]

            # Debug output
            if verbose:
                print(f"DEBUG: Scan returned {len(results)} results")
                for i, result in enumerate(results):
                    print(f"DEBUG: Result {i+1}: {result.get('file_path')}")
        else:
            # Use our parallel implementation for better performance
            results = []
            file_list = []

            # Collect all files to scan
            if recursive:
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        file_list.append(os.path.join(root, file))
            else:
                for file in os.listdir(dir_path):
                    full_path = os.path.join(dir_path, file)
                    if os.path.isfile(full_path):
                        file_list.append(full_path)

            # Sort for consistent results
            file_list.sort()

            # Get configuration
            config = load_config()
            scan_options = config.get("scan_options", {})

            # Determine optimal number of workers
            config_max_workers = scan_options.get("max_workers", 0)
            if config_max_workers > 0:
                max_workers = config_max_workers
            else:
                max_workers = min(32, (multiprocessing.cpu_count() or 1) * 2)

            # Create a progress display
            total_files = len(file_list)
            processed_files = 0
            lock = threading.Lock()

            def update_progress():
                nonlocal processed_files
                with lock:
                    processed_files += 1
                    if verbose or total_files > 10:
                        percent = (processed_files / total_files) * 100
                        bar_length = 30
                        filled_length = int(bar_length * processed_files // total_files)
                        bar = '█' * filled_length + '░' * (bar_length - filled_length)
                        sys.stdout.write(f'\rProgress: |{bar}| {percent:.1f}% ({processed_files}/{total_files}) ')
                        sys.stdout.flush()

            # Define a worker function for scanning a single file
            def scan_worker(file_path):
                try:
                    result = orchestrator.scan_file(file_path, verbose)
                    update_progress()
                    return result
                except Exception as e:
                    logger.error(f"Error scanning file {file_path}: {str(e)}")
                    update_progress()
                    return {
                        'file_path': file_path,
                        'status': 'error',
                        'error': str(e),
                        'recommendation': 'Error'
                    }

            # Use ThreadPoolExecutor for parallel scanning
            if file_list:
                print(f"Scanning {total_files} files with {max_workers} parallel workers...")
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_file = {executor.submit(scan_worker, file_path): file_path for file_path in file_list}
                    for future in as_completed(future_to_file):
                        result = future.result()
                        results.append(result)

                # Print newline after progress bar
                if verbose or total_files > 10:
                    print()

            # Debug output
            if verbose:
                print(f"DEBUG: Parallel scan completed for {len(results)} files")

        # Calculate threat statistics
        threat_count = sum(1 for r in results if r.get('recommendation') == 'Quarantine')
        logger.info(f"Scan completed for directory {dir_path}: {len(results)} files scanned, {threat_count} threats detected")

        return results
    except Exception as e:
        logger.error(f"Error scanning directory {dir_path}: {str(e)}")
        return [{
            'directory': dir_path,
            'status': 'error',
            'error': str(e),
            'recommendation': 'Error'
        }]

def save_results(results, output_file):
    """
    Save scan results to file with additional metadata

    Args:
        results: Scan results (single result or list of results)
        output_file: Path to the output file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Prepare results with metadata
        timestamp = datetime.now().isoformat()
        hostname = os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'unknown'))

        # Count results by recommendation if results is a list
        stats = {}
        if isinstance(results, list):
            total = len(results)
            threat_count = sum(1 for r in results if r.get('recommendation') == 'Quarantine')
            investigate_count = sum(1 for r in results if r.get('recommendation') == 'Investigate')
            monitor_count = sum(1 for r in results if r.get('recommendation') == 'Monitor')
            safe_count = sum(1 for r in results if r.get('recommendation') == 'Safe')
            error_count = sum(1 for r in results if r.get('recommendation') == 'Error')
            unknown_count = total - (threat_count + investigate_count + monitor_count + safe_count + error_count)

            stats = {
                "total": total,
                "threats": threat_count,
                "investigate": investigate_count,
                "monitor": monitor_count,
                "safe": safe_count,
                "errors": error_count,
                "unknown": unknown_count
            }

        # Create the output data structure
        output_data = {
            "metadata": {
                "timestamp": timestamp,
                "hostname": hostname,
                "scanner_version": "1.0.0",
                "platform": sys.platform
            }
        }

        # Add statistics if available
        if stats:
            output_data["statistics"] = stats

        # Add the results
        if isinstance(results, list):
            output_data["scan_results"] = results
        else:
            output_data["scan_result"] = results

        # Write to file
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        logger.info(f"Scan results saved to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving results to {output_file}: {str(e)}")
        return False

def print_results(results, verbose=False):
    """
    Print scan results to console in a well-formatted way

    Args:
        results: Scan results (single result or list of results)
        verbose: Whether to print detailed results
    """
    # Try to detect if terminal supports colors
    try:
        import colorama
        colorama.init()
        # Define colors
        RED = colorama.Fore.RED
        GREEN = colorama.Fore.GREEN
        YELLOW = colorama.Fore.YELLOW
        BLUE = colorama.Fore.BLUE
        MAGENTA = colorama.Fore.MAGENTA
        CYAN = colorama.Fore.CYAN
        RESET = colorama.Style.RESET_ALL
        BRIGHT = colorama.Style.BRIGHT
        DIM = colorama.Style.DIM

        # Define recommendation colors
        REC_COLORS = {
            'Quarantine': RED,
            'Investigate': YELLOW,
            'Monitor': BLUE,
            'Safe': GREEN,
            'Error': MAGENTA,
            'Unknown': CYAN
        }
    except ImportError:
        # No color support
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = RESET = BRIGHT = DIM = ''
        REC_COLORS = {
            'Quarantine': '',
            'Investigate': '',
            'Monitor': '',
            'Safe': '',
            'Error': '',
            'Unknown': ''
        }

    # Get current terminal width
    try:
        terminal_width = os.get_terminal_size().columns
    except (AttributeError, OSError):
        terminal_width = 80

    # Helper function to create a centered header
    def print_header(text, char='=', color=BRIGHT):
        width = min(terminal_width, 80)
        print(f"\n{color}{text.center(width)}{RESET}")
        print(f"{color}{(char * len(text)).center(width)}{RESET}")

    # Helper function to print a key-value pair
    def print_kv(key, value, color=''):
        print(f"{BRIGHT}{key}:{RESET} {color}{value}{RESET}")

    # Helper function to print a recommendation with color
    def print_recommendation(rec):
        rec_color = REC_COLORS.get(rec, '')
        print(f"{BRIGHT}Recommendation:{RESET} {rec_color}{rec}{RESET}")

    # Print timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{DIM}Scan completed at: {timestamp}{RESET}")

    if isinstance(results, list):
        # Print summary for multiple results
        print_header("Scan Results Summary", '=', BRIGHT + BLUE)

        # Count results by recommendation
        total = len(results)
        threat_count = sum(1 for r in results if r.get('recommendation') == 'Quarantine')
        investigate_count = sum(1 for r in results if r.get('recommendation') == 'Investigate')
        monitor_count = sum(1 for r in results if r.get('recommendation') == 'Monitor')
        safe_count = sum(1 for r in results if r.get('recommendation') == 'Safe')
        error_count = sum(1 for r in results if r.get('recommendation') == 'Error')
        unknown_count = total - (threat_count + investigate_count + monitor_count + safe_count + error_count)

        # Print counts
        print_kv("Total files scanned", total)
        if threat_count > 0:
            print_kv("Threats detected", threat_count, RED)
        if investigate_count > 0:
            print_kv("Files to investigate", investigate_count, YELLOW)
        if monitor_count > 0:
            print_kv("Files to monitor", monitor_count, BLUE)
        print_kv("Safe files", safe_count, GREEN)
        if error_count > 0:
            print_kv("Errors", error_count, MAGENTA)
        if unknown_count > 0:
            print_kv("Unknown status", unknown_count, CYAN)

        # Print threat details if any found
        if threat_count > 0:
            print_header("Threat Details", '-', BRIGHT + RED)
            threat_files = [r for r in results if r.get('recommendation') == 'Quarantine']
            for result in threat_files:
                file_path = result.get('file_path', 'Unknown')
                print(f"\n{BRIGHT}{RED}File:{RESET} {file_path}")
                print_kv("Type", result.get('file_type', 'Unknown'))
                print_recommendation(result.get('recommendation', 'Unknown'))

                if result.get('threats'):
                    print(f"{BRIGHT}Threats:{RESET}")
                    for threat in result['threats']:
                        print(f"  {RED}•{RESET} {threat}")

        # Print detailed results if requested
        if verbose:
            print_header("Detailed Results", '-', BRIGHT)

            # Group results by recommendation for better organization
            results_by_rec = {}
            for result in results:
                rec = result.get('recommendation', 'Unknown')
                if rec not in results_by_rec:
                    results_by_rec[rec] = []
                results_by_rec[rec].append(result)

            # Print results by recommendation group
            for rec in ['Quarantine', 'Investigate', 'Monitor', 'Error', 'Unknown', 'Safe']:
                if rec in results_by_rec and results_by_rec[rec]:
                    rec_color = REC_COLORS.get(rec, '')
                    print(f"\n{BRIGHT}{rec_color}{rec} Files:{RESET}")

                    for result in results_by_rec[rec]:
                        file_path = result.get('file_path', 'Unknown')
                        print(f"\n{BRIGHT}File:{RESET} {file_path}")
                        print_kv("Type", result.get('file_type', 'Unknown'))

                        if result.get('threats'):
                            print(f"{BRIGHT}Threats:{RESET}")
                            for threat in result['threats']:
                                print(f"  {rec_color}•{RESET} {threat}")
    else:
        # Print details for a single result
        print_header("Scan Results", '=', BRIGHT + BLUE)

        file_path = results.get('file_path', 'Unknown')
        recommendation = results.get('recommendation', 'Unknown')
        rec_color = REC_COLORS.get(recommendation, '')

        print_kv("File", file_path)
        print_kv("Type", results.get('file_type', 'Unknown'))
        print_recommendation(recommendation)

        if results.get('threats'):
            print(f"\n{BRIGHT}Threats:{RESET}")
            for threat in results['threats']:
                print(f"  {rec_color}•{RESET} {threat}")

        # Print additional details if available and verbose is enabled
        if verbose and 'details' in results:
            print(f"\n{BRIGHT}Additional Details:{RESET}")
            for key, value in results['details'].items():
                if isinstance(value, dict):
                    print(f"  {BRIGHT}{key}:{RESET}")
                    for k, v in value.items():
                        print(f"    {k}: {v}")
                else:
                    print(f"  {key}: {value}")

    # Print footer
    print(f"\n{DIM}For detailed results, check the output JSON file.{RESET}")

def main():
    """
    Main function that orchestrates the scanning process

    Returns:
        int: Exit code (0 for success, 1 for threats detected, 2 for errors)
    """
    start_time = time.time()

    try:
        # Parse arguments
        args = parse_arguments()

        # Set verbose logging if requested
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")

        # Load configuration
        config = load_config()
        scanner_info = config.get("scanner", {})
        scanner_name = scanner_info.get("name", "SBARDS Security Scanner")
        scanner_version = scanner_info.get("version", "1.0.0")
        scanner_description = scanner_info.get("description", "Comprehensive Security Analysis Tool")

        # Print banner
        print("\n" + "=" * 60)
        print(f"{scanner_name} v{scanner_version}".center(60))
        print(f"{scanner_description}".center(60))
        print("=" * 60 + "\n")

        # Register signal handlers for graceful shutdown
        try:
            import signal

            # pylint: disable=unused-argument
            def signal_handler(sig, frame):
                """Handle interrupt signals gracefully"""
                print("\n\nScan interrupted by user. Exiting gracefully...")
                sys.exit(130)  # 128 + SIGINT

            signal.signal(signal.SIGINT, signal_handler)
            logger.debug("Signal handlers registered")
        except (ImportError, AttributeError):
            logger.debug("Signal handling not available on this platform")

        # Ensure required directories exist
        ensure_directories()

        # Update rules if requested
        if args.update_rules:
            logger.info("Updating YARA rules...")
            if update_rules():
                print("YARA rules updated successfully")
            else:
                print("Failed to update YARA rules")

        # Initialize orchestrator with performance monitoring
        logger.info("Initializing scanner orchestrator")
        print("Initializing scanner...")
        orchestrator = Orchestrator()

        # Determine output file
        output_file = args.output if args.output else os.path.join('output', f'scan_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        logger.info(f"Output will be saved to {output_file}")

        # Perform scan with timing
        scan_start_time = time.time()
        print("Starting scan...")

        try:
            if args.all:
                # Scan all files in samples directory
                logger.info("Scanning all files in samples directory")
                if not os.path.exists('samples'):
                    os.makedirs('samples', exist_ok=True)
                    logger.warning("Samples directory did not exist, created it")
                    print("Samples directory did not exist, created it")

                if not os.listdir('samples'):
                    logger.warning("Samples directory is empty")
                    print("Samples directory is empty. Please add files to scan.")
                    return 0

                results = scan_directory(orchestrator, 'samples', args.recursive, args.verbose)
            elif os.path.isdir(args.target):
                # Scan directory
                logger.info(f"Scanning directory: {args.target}")
                if not os.path.exists(args.target):
                    logger.error(f"Directory not found: {args.target}")
                    print(f"Error: Directory not found: {args.target}")
                    return 2

                results = scan_directory(orchestrator, args.target, args.recursive, args.verbose)
            elif os.path.isfile(args.target):
                # Scan single file
                logger.info(f"Scanning file: {args.target}")
                results = scan_file(orchestrator, args.target, args.verbose)
            else:
                logger.error(f"Target not found: {args.target}")
                print(f"Error: Target not found: {args.target}")
                return 2
        except Exception as e:
            logger.error(f"Error during scan: {str(e)}")
            print(f"Error during scan: {str(e)}")
            return 2

        scan_duration = time.time() - scan_start_time
        logger.info(f"Scan completed in {scan_duration:.2f} seconds")

        # Print results
        print_results(results, args.verbose)

        # Save results if not disabled
        if not args.no_save:
            logger.info(f"Saving results to {output_file}")
            if save_results(results, output_file):
                print(f"Results saved to {output_file}")
            else:
                print(f"Error: Failed to save results to {output_file}")

        # Calculate statistics for exit code
        if isinstance(results, list):
            threat_count = sum(1 for r in results if r.get('recommendation') == 'Quarantine')
            error_count = sum(1 for r in results if r.get('recommendation') == 'Error')

            if error_count > 0 and threat_count == 0:
                logger.warning(f"Scan completed with {error_count} errors")
                exit_code = 2
            elif threat_count > 0:
                logger.warning(f"Scan completed with {threat_count} threats detected")
                exit_code = 1
            else:
                logger.info("Scan completed successfully, no threats detected")
                exit_code = 0
        else:
            if results.get('recommendation') == 'Error':
                logger.warning("Scan completed with errors")
                exit_code = 2
            elif results.get('recommendation') == 'Quarantine':
                logger.warning("Scan completed, threats detected")
                exit_code = 1
            else:
                logger.info("Scan completed successfully, no threats detected")
                exit_code = 0

        # Print total execution time
        total_duration = time.time() - start_time
        logger.info(f"Total execution time: {total_duration:.2f} seconds")
        print(f"\nTotal execution time: {total_duration:.2f} seconds")

        return exit_code

    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        print(f"Error: {str(e)}")
        return 2

if __name__ == '__main__':
    sys.exit(main())
