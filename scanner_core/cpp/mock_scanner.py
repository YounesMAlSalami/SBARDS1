import sys
import os
import json
import hashlib
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MockScanner")

def contains_pattern(content: str, pattern: str) -> bool:
    """Check if a pattern is contained in the content (case-insensitive)"""
    return pattern.lower() in content.lower()

def is_safe_context(content: str, pattern: str, safe_contexts: List[str]) -> bool:
    """Check if a pattern appears in a safe context"""
    for safe_context in safe_contexts:
        if safe_context in content:
            return True
    return False

def load_whitelist(rules_dir: str) -> Dict[str, List[str]]:
    """Load whitelist patterns from a JSON file"""
    whitelist_path = os.path.join(rules_dir, "whitelist.json")

    # Default whitelist if file doesn't exist
    default_whitelist = {
        "malicious": [
            "This is a test file that contains the word malicious",
            "This file discusses malicious software in an educational context"
        ],
        "encrypt": [
            "This file discusses how to encrypt and decrypt data securely",
            "The file also mentions the words encrypt and decrypt to potentially trigger"
        ],
        "decrypt": [
            "This file discusses how to encrypt and decrypt data securely",
            "The file also mentions the words encrypt and decrypt to potentially trigger"
        ]
    }

    if not os.path.exists(whitelist_path):
        logger.warning(f"Whitelist file not found: {whitelist_path}")
        return default_whitelist

    try:
        with open(whitelist_path, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)
        logger.info(f"Loaded whitelist from {whitelist_path}")
        return whitelist
    except Exception as e:
        logger.error(f"Error loading whitelist: {e}")
        return default_whitelist

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash
    except Exception as e:
        logger.error(f"Error calculating hash for {file_path}: {e}")
        return ""

def main():
    """Main function for the mock scanner"""
    if len(sys.argv) < 3:
        script_name = os.path.basename(sys.argv[0]) if len(sys.argv) > 0 else "mock_scanner.py"
        print(f"Usage: python {script_name} <rules_file> <target_file> [--context-aware]")
        return 1

    rules_file = sys.argv[1]
    target_file = sys.argv[2]

    # Check if context-aware scanning is enabled
    context_aware = "--context-aware" in sys.argv

    print(f"Mock YARA Scanner (C++ Module Simulation)")
    print(f"Rules file: {rules_file}")
    print(f"Target file: {target_file}")
    print(f"Context-aware: {context_aware}")

    # Get rules directory
    rules_dir = os.path.dirname(rules_file)

    # Load whitelist if context-aware scanning is enabled
    whitelist = load_whitelist(rules_dir) if context_aware else {}

    # Read the target file with universal newlines mode for cross-platform compatibility
    try:
        with open(target_file, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        print(f"Could not open target file: {target_file}")
        print(f"Error: {e}")
        return 1

    # Calculate file hash
    file_hash = calculate_file_hash(target_file)
    print(f"File hash: {file_hash}")

    # Simulate rule matching with context awareness
    matched_rules = []

    # Check for malicious pattern
    if contains_pattern(content, "malicious"):
        if context_aware and "malicious" in whitelist and is_safe_context(content, "malicious", whitelist["malicious"]):
            print("Pattern 'malicious' found in safe context, not reporting")
        else:
            matched_rules.append("ExampleRule")
            print("Matched rule: ExampleRule (found 'malicious')")

    # Check for encrypt and decrypt patterns
    if contains_pattern(content, "encrypt") and contains_pattern(content, "decrypt"):
        if context_aware and "encrypt" in whitelist and is_safe_context(content, "encrypt", whitelist["encrypt"]):
            print("Patterns 'encrypt' and 'decrypt' found in safe context, not reporting")
        else:
            matched_rules.append("PotentialRansomware")
            print("Matched rule: PotentialRansomware (found 'encrypt' and 'decrypt')")

    # Check for suspicious network activity
    if contains_pattern(content, "wget") or contains_pattern(content, "curl") or contains_pattern(content, "http://"):
        matched_rules.append("SuspiciousNetworkActivity")
        print("Matched rule: SuspiciousNetworkActivity (found network commands)")

    # Check for suspicious script patterns
    if contains_pattern(content, "eval(") or contains_pattern(content, "exec(") or contains_pattern(content, "system("):
        matched_rules.append("SuspiciousScript")
        print("Matched rule: SuspiciousScript (found script execution)")

    # Print summary
    if matched_rules:
        print(f"\nSummary: Found {len(matched_rules)} matches: {', '.join(matched_rules)}")
    else:
        print("\nSummary: No matches found")

    return 0

if __name__ == "__main__":
    sys.exit(main())
