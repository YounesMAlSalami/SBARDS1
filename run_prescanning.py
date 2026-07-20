import os
import sys
import subprocess
import json
import platform
import argparse
from datetime import datetime

def get_python_command():
    """Get the appropriate Python command for the current platform"""
    if platform.system() == "Windows":
        return "python"
    else:
        return "python3"

def get_pipenv_command():
    """Get the appropriate pipenv command for the current platform"""
    if platform.system() == "Windows":
        return "pipenv"
    else:
        return "pipenv"

def run_cpp_scanner(rules_file, target_file):
    """Run the C++ scanner (mock version) on a single file"""
    print(f"Running C++ scanner on {target_file}...")

    python_cmd = get_python_command()

    # Use platform-specific path separators
    scanner_path = os.path.join("scanner_core", "cpp", "mock_scanner.py")

    # Use the Python mock scanner since we couldn't compile the C++ version
    try:
        result = subprocess.run(
            [python_cmd, scanner_path, rules_file, target_file],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the output to extract matched rules
        matches = []
        for line in result.stdout.splitlines():
            if line.startswith("Matched rule:"):
                rule_name = line.split("(")[0].replace("Matched rule:", "").strip()
                matches.append(rule_name)

        return matches
    except subprocess.CalledProcessError as e:
        print(f"Error running C++ scanner: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return []
    except Exception as e:
        print(f"Unexpected error running C++ scanner: {e}")
        return []

def run_python_orchestrator():
    """Run the Python orchestrator"""
    print("Running Python orchestrator...")

    python_cmd = get_python_command()
    pipenv_cmd = get_pipenv_command()

    # Use platform-specific path separators
    orchestrator_path = os.path.join("scanner_core", "python", "orchestrator.py")

    try:
        result = subprocess.run(
            [pipenv_cmd, "run", python_cmd, orchestrator_path],
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Python orchestrator: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error running Python orchestrator: {e}")
        return False

def run_integrated_scan():
    """Run the integrated scan (C++ scanner + Python orchestration)"""
    print(f"Running integrated pre-scanning phase on {platform.system()}...")

    # Use absolute paths with os.path.join for cross-platform compatibility
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rule_path = os.path.join(base_dir, "rules", "custom_rules.yar")
    target_dir = os.path.join(base_dir, "samples")
    log_dir = os.path.join(base_dir, "logs")
    out_dir = os.path.join(base_dir, "output")

    # Create directories if they don't exist
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    # Scan each file in the samples directory using the C++ scanner
    for root, _, files in os.walk(target_dir):
        for file in files:
            full_path = os.path.join(root, file)
            matches = run_cpp_scanner(rule_path, full_path)

            # Log the results with proper encoding for cross-platform compatibility
            log_file = os.path.join(log_dir, "integrated_scan_log.txt")
            with open(log_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().isoformat()
                f.write(f"{timestamp} - Scanned: {full_path} - Matches: {matches}\n")

            # Save JSON output with proper encoding for cross-platform compatibility
            out_file = os.path.join(out_dir, f"{os.path.basename(full_path)}_integrated.json")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump({"file": full_path, "matches": matches}, f, indent=2)

            print(f"[INFO] Integrated scan of {file}: {matches}")

    return True

def update_rules():
    """Update YARA rules from remote sources"""
    try:
        # Import the rule updater
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scanner_core", "python"))
        from rule_updater import RuleUpdater

        print("Updating YARA rules...")
        updater = RuleUpdater()
        results = updater.update_all_rules()

        # Print results
        for category, updated in results.items():
            if updated:
                print(f"- {category}: Updated")
            else:
                print(f"- {category}: No update needed")

        return True
    except Exception as e:
        print(f"Error updating rules: {e}")
        return False

def scan_file(file_path, verbose=False):
    """Scan a single file"""
    print(f"Scanning file: {file_path}")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False

    # Run C++ scanner
    rule_file = os.path.join("rules", "custom_rules.yar")
    cpp_result = run_cpp_scanner(rule_file, file_path)

    if verbose:
        print(f"C++ Scanner Result: {cpp_result}")

    # Log results
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "logs")
    out_dir = os.path.join(base_dir, "output")

    # Create directories if they don't exist
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    # Log the results with proper encoding for cross-platform compatibility
    log_file = os.path.join(log_dir, "scan_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - Scanned: {file_path} - Matches: {cpp_result}\n")

    # Save JSON output with proper encoding for cross-platform compatibility
    out_file = os.path.join(out_dir, f"{os.path.basename(file_path)}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"file": file_path, "matches": cpp_result}, f, indent=2)

    return True

def scan_all_files():
    """Scan all files in the samples directory"""
    print("Scanning all files in samples directory...")

    # Get samples directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(base_dir, "samples")

    # Create directory if it doesn't exist
    os.makedirs(samples_dir, exist_ok=True)

    # Scan each file
    for root, _, files in os.walk(samples_dir):
        for file in files:
            full_path = os.path.join(root, file)
            scan_file(full_path)

    return True

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="SBARDS Project - Pre-scanning Phase")
    parser.add_argument("file", nargs="?", help="File to scan")
    parser.add_argument("--all", action="store_true", help="Scan all files in samples directory")
    parser.add_argument("--update-rules", action="store_true", help="Update YARA rules from remote sources")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--no-save", action="store_true", help="Don't save results to disk")
    args = parser.parse_args()

    print(f"=== SBARDS PROJECT - PRE-SCANNING PHASE ({platform.system()}) ===")

    # Check if all required directories exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    required_dirs = [
        os.path.join(base_dir, "rules"),
        os.path.join(base_dir, "samples"),
        os.path.join(base_dir, "logs"),
        os.path.join(base_dir, "output"),
        os.path.join(base_dir, "scanner_core", "cpp"),
        os.path.join(base_dir, "scanner_core", "python")
    ]

    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)

    # Check if test sample exists
    test_file = os.path.join("samples", "test_sample.txt")
    if not os.path.exists(test_file):
        print(f"Creating test sample file: {test_file}")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("This is a test file that contains the word malicious to trigger our YARA rule.\n")
            f.write("It does not contain any actual malware but is used for testing the scanner functionality.\n\n")
            f.write("The file also mentions the words encrypt and decrypt to potentially trigger the PotentialRansomware rule.")

    # Check if YARA rules exist
    rule_files = [
        os.path.join("rules", "custom_rules.yar"),
        os.path.join("rules", "windows_executables.yar"),
        os.path.join("rules", "multimedia.yar"),
        os.path.join("rules", "documents.yar"),
        os.path.join("rules", "archives.yar"),
        os.path.join("rules", "programming.yar"),
        os.path.join("rules", "gaming.yar"),
        os.path.join("rules", "network.yar"),
        os.path.join("rules", "certificates.yar")
    ]

    # Count existing rule files
    existing_rules = sum(1 for rule_file in rule_files if os.path.exists(rule_file))
    print(f"Found {existing_rules} out of {len(rule_files)} YARA rule files")

    # Handle command-line arguments
    if args.update_rules:
        update_rules()
        sys.exit(0)

    if args.all:
        scan_all_files()
        sys.exit(0)

    if args.file:
        scan_file(args.file, args.verbose)
        sys.exit(0)

    # If no specific command-line arguments, run the default workflow
    print("\n=== STEP 1: Running C++ Scanner Component ===")
    rule_file = os.path.join("rules", "custom_rules.yar")
    cpp_result = run_cpp_scanner(rule_file, test_file)
    print(f"C++ Scanner Result: {cpp_result}")

    print("\n=== STEP 2: Running Python Orchestrator Component ===")
    python_result = run_python_orchestrator()
    print(f"Python Orchestrator Result: {python_result}")

    print("\n=== STEP 3: Running Integrated Pre-scanning Phase ===")
    integrated_result = run_integrated_scan()
    print(f"Integrated Scan Result: {integrated_result}")

    print("\n=== Pre-scanning Phase Complete ===")
    print("\nResults are available in the following locations:")
    print(f"- Logs: {os.path.join(base_dir, 'logs')}")
    print(f"- Scan Results: {os.path.join(base_dir, 'output')}")

    # Print summary of findings
    if not args.no_save:
        try:
            output_dir = os.path.join(base_dir, "output")
            json_files = [f for f in os.listdir(output_dir) if f.endswith(".json")]

            if json_files:
                print("\nSummary of Findings:")
                for json_file in json_files:
                    try:
                        with open(os.path.join(output_dir, json_file), "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if "recommendation" in data:
                                print(f"- {os.path.basename(data['file_path'])}: {data['recommendation']} (Risk: {data.get('risk_level', 'Unknown')})")
                            elif "matches" in data:
                                matches = data.get("matches", [])
                                if matches:
                                    print(f"- {os.path.basename(data['file'])}: {len(matches)} matches found")
                                else:
                                    print(f"- {os.path.basename(data['file'])}: No matches found")
                    except Exception as e:
                        print(f"Error reading {json_file}: {e}")
        except Exception as e:
            print(f"Error generating summary: {e}")
