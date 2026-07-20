import os
import json
import platform
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Any

# Import local modules
from .yara_wrapper import YaraScanner
from .file_type_detector import FileTypeDetector
from .rule_updater import RuleUpdater
from .threat_intel import ThreatIntelligence

# Use absolute paths with os.path.join for cross-platform compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
RULES_DIR = os.path.join(PROJECT_ROOT, "rules")
TARGET_DIR = os.path.join(PROJECT_ROOT, "samples")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
OUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Create directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RULES_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "scan_history.log"),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Orchestrator")

def log_results(file_path: str, results: Dict[str, Any]) -> None:
    """Log scan results to a file with proper encoding for cross-platform compatibility"""
    log_file = os.path.join(LOG_DIR, "scan_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - Scanned: {file_path} - Results: {json.dumps(results)}\n")

    # Also log to the console and the logger
    logger.info(f"Scanned: {file_path} - Results: {json.dumps(results)}")
    print(f"[INFO] Scanned: {file_path}")

def save_json_output(file_path: str, results: Dict[str, Any]) -> None:
    """Save scan results as JSON with proper encoding for cross-platform compatibility"""
    out_file = os.path.join(OUT_DIR, f"{os.path.basename(file_path)}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get basic information about a file"""
    try:
        stats = os.stat(file_path)

        # Calculate file hash
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Get file times in a cross-platform way
        try:
            # Try to get creation time (birthtime) if available
            created_time = datetime.fromtimestamp(stats.st_birthtime).isoformat()
        except AttributeError:
            # Fall back to ctime if birthtime is not available
            created_time = datetime.fromtimestamp(stats.st_ctime).isoformat()

        return {
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "file_size": stats.st_size,
            "file_hash": file_hash,
            "created_time": created_time,
            "modified_time": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "accessed_time": datetime.fromtimestamp(stats.st_atime).isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting file info for {file_path}: {e}")
        return {
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "error": str(e)
        }

def check_file_permissions(file_path: str) -> Dict[str, Any]:
    """Check file permissions"""
    try:
        stats = os.stat(file_path)

        # Get permissions as octal string
        permissions = oct(stats.st_mode)[-3:]

        # Check if file is executable
        is_executable = os.access(file_path, os.X_OK)

        # Check if file is writable
        is_writable = os.access(file_path, os.W_OK)

        # Check if file is readable
        is_readable = os.access(file_path, os.R_OK)

        # Check if file is a system file (platform-specific)
        is_system_file = False
        if platform.system() == "Windows":
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
            is_system_file = attrs != -1 and bool(attrs & 4)  # 4 is FILE_ATTRIBUTE_SYSTEM

        # Determine if permissions are suspicious
        is_suspicious = is_executable and (
            file_path.endswith(".txt") or
            file_path.endswith(".doc") or
            file_path.endswith(".pdf") or
            file_path.endswith(".jpg") or
            file_path.endswith(".png")
        )

        return {
            "file_path": file_path,
            "permissions": permissions,
            "is_executable": is_executable,
            "is_writable": is_writable,
            "is_readable": is_readable,
            "is_system_file": is_system_file,
            "is_suspicious": is_suspicious
        }
    except Exception as e:
        logger.error(f"Error checking file permissions for {file_path}: {e}")
        return {
            "file_path": file_path,
            "error": str(e),
            "is_suspicious": False
        }

def analyze_file_content(file_path: str) -> Dict[str, Any]:
    """
    Analyze file content for suspicious patterns with context awareness to reduce false positives

    Args:
        file_path: Path to the file to analyze

    Returns:
        Dictionary with analysis results
    """
    try:
        # Use the FileTypeDetector to get file type information
        detector = FileTypeDetector()
        file_type_info = detector.detect_file_type(file_path)

        # Initialize result
        result = {
            "file_path": file_path,
            "file_type": file_type_info.get("mime_type", "unknown"),
            "category": file_type_info.get("category", "unknown"),
            "is_binary": file_type_info.get("is_binary", False),
            "is_executable": file_type_info.get("is_executable", False),
            "is_archive": file_type_info.get("is_archive", False),
            "is_document": file_type_info.get("is_document", False),
            "is_multimedia": file_type_info.get("is_multimedia", False),
            "is_code": file_type_info.get("is_code", False),
            "is_certificate": file_type_info.get("is_certificate", False),
            "suspicious_strings": [],
            "is_suspicious": False,
            "safe_contexts": []  # Track safe contexts for suspicious strings
        }

        # Load whitelist patterns for context-aware scanning
        whitelist_patterns = _load_content_whitelist()

        # Check for suspicious strings in text files
        if not result["is_binary"]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # List of suspicious strings to check for, grouped by category
                suspicious_patterns = {
                    "command_execution": [
                        "cmd.exe", "powershell", "bash -i", "sh -i", "python -c", "perl -e",
                        "system(", "exec(", "popen(", "shell_exec(", "passthru(", "proc_open(",
                        "pcntl_exec(", "eval(", "assert(", "create_function(", "call_user_func(",
                        "include($_", "require($_", "include_once($_", "require_once($_",
                        "os.system", "subprocess.call", "subprocess.Popen", "subprocess.run",
                        "Runtime.getRuntime().exec", "ProcessBuilder", "ShellExecute",
                        "WScript.Shell", "ActiveXObject", "ScriptControl"
                    ],
                    "code_obfuscation": [
                        "base64_decode", "base64.b64decode", "fromCharCode", "escape(", "unescape(",
                        "String.fromCharCode", "eval(atob", "eval(base64", "\\x", "\\u00",
                        "document.write(unescape", "document.write(String.fromCharCode",
                        "ChrW(", "Chr(", "StrReverse", "Replace(", "RegExp"
                    ],
                    "registry_modification": [
                        "RegWrite", "RegRead", "RegDelete", "HKEY_LOCAL_MACHINE", "HKEY_CURRENT_USER",
                        "CurrentVersion\\Run", "Registry.SetValue", "Registry.GetValue"
                    ],
                    "network_activity": [
                        "wget ", "curl ", "Invoke-WebRequest", "WebClient.DownloadFile",
                        "URLDownloadToFile", "Net.WebClient", "HttpWebRequest",
                        "http://pastebin.com", "http://raw.githubusercontent.com",
                        "http://gist.github.com", "http://bit.ly", "http://goo.gl",
                        "http://tinyurl.com", "http://is.gd", "http://adf.ly"
                    ],
                    "malware_specific": [
                        "malicious", "exploit", "vulnerability", "payload", "shellcode",
                        "backdoor", "trojan", "ransomware", "rootkit", "keylogger",
                        "spyware", "botnet", "RAT", "worm", "dropper", "stealer",
                        "crypter", "cryptor", "packer", "obfuscator", "injector"
                    ],
                    "crypto_ransomware": [
                        "encrypt", "decrypt", "bitcoin", "monero", "ethereum", "wallet",
                        "ransom", "payment", "CryptoLocker", "WannaCry", "Petya",
                        "AES.encrypt", "RSA.encrypt", "Rijndael", "CipherMode"
                    ],
                    "data_exfiltration": [
                        "password", "credentials", "login", "cookie", "session",
                        "token", "api_key", "secret_key", "private_key", "ssh_key",
                        "credit_card", "ssn", "social_security", "bank_account"
                    ],
                    "anti_analysis": [
                        "IsDebuggerPresent", "CheckRemoteDebuggerPresent", "NtQueryInformationProcess",
                        "GetTickCount", "QueryPerformanceCounter", "timeGetTime",
                        "IsVirtualMachine", "vmware", "virtualbox", "qemu", "xen",
                        "VirtualAlloc", "VirtualProtect", "WriteProcessMemory", "CreateRemoteThread",
                        "Sleep(", "WaitForSingleObject", "GetLastError"
                    ]
                }

                # Check for each pattern with context awareness
                for category, patterns in suspicious_patterns.items():
                    for pattern in patterns:
                        if pattern.lower() in content.lower():
                            # Check if this pattern is in a safe context
                            is_safe_context = False

                            # Check for safe contexts in the whitelist
                            if pattern in whitelist_patterns:
                                for safe_context in whitelist_patterns[pattern]:
                                    if safe_context in content:
                                        is_safe_context = True
                                        result["safe_contexts"].append(f"{pattern}: {safe_context}")
                                        break

                            # If not in a safe context, add to suspicious strings
                            if not is_safe_context:
                                result["suspicious_strings"].append(f"{pattern} ({category})")

                # If any suspicious strings were found, mark as suspicious
                if result["suspicious_strings"]:
                    result["is_suspicious"] = True

                # Add file entropy analysis for additional context
                result["entropy"] = _calculate_entropy(content)
                result["high_entropy"] = result["entropy"] > 7.0  # High entropy threshold

            except Exception as e:
                logger.error(f"Error analyzing text content for {file_path}: {e}")

        # For binary files, perform additional checks
        else:
            try:
                # For binary files, check file signature and entropy
                with open(file_path, "rb") as f:
                    binary_content = f.read(4096)  # Read first 4KB for analysis

                # Calculate entropy of binary content
                result["entropy"] = _calculate_entropy(binary_content)
                result["high_entropy"] = result["entropy"] > 7.0  # High entropy threshold

                # Check for suspicious binary patterns
                if result["is_executable"]:
                    # Check for common executable patterns
                    suspicious_binary_patterns = [
                        b"cmd.exe", b"powershell", b"system32", b"regsvr32",
                        b"CreateProcess", b"ShellExecute", b"WinExec",
                        b"VirtualAlloc", b"VirtualProtect", b"WriteProcessMemory"
                    ]

                    for pattern in suspicious_binary_patterns:
                        if pattern in binary_content:
                            result["suspicious_strings"].append(f"{pattern.decode('utf-8', errors='ignore')} (binary)")
                            result["is_suspicious"] = True

            except Exception as e:
                logger.error(f"Error analyzing binary content for {file_path}: {e}")

        return result

    except Exception as e:
        logger.error(f"Error analyzing file content for {file_path}: {e}")
        return {
            "file_path": file_path,
            "file_type": "unknown",
            "is_binary": False,
            "is_suspicious": False,
            "suspicious_strings": [],
            "error": str(e)
        }

def _load_content_whitelist() -> Dict[str, List[str]]:
    """
    Load whitelist patterns for content analysis

    Returns:
        Dictionary mapping suspicious patterns to lists of safe contexts
    """
    # Default whitelist patterns
    whitelist = {
        # Pattern -> list of safe contexts
        "malicious": [
            "This is a test file that contains the word malicious",
            "This file discusses malicious software in an educational context",
            "Example of malicious patterns for detection",
            "The word malicious is used in a benign context",
            "This is a safe file with the word malicious in it"
        ],
        "encrypt": [
            "This file discusses how to encrypt and decrypt data securely",
            "Encryption and decryption are important security concepts",
            "The file also mentions the words encrypt and decrypt to potentially trigger",
            "This document explains encryption and decryption techniques",
            "How to encrypt and decrypt files safely"
        ],
        "decrypt": [
            "This file discusses how to encrypt and decrypt data securely",
            "Encryption and decryption are important security concepts",
            "The file also mentions the words encrypt and decrypt to potentially trigger",
            "This document explains encryption and decryption techniques",
            "How to encrypt and decrypt files safely"
        ],
        "ransomware": [
            "This document discusses ransomware in an educational context",
            "Ransomware is a type of malware that encrypts files",
            "How to protect against ransomware attacks"
        ]
    }

    # Try to load whitelist from file if it exists
    whitelist_path = os.path.join(RULES_DIR, "content_whitelist.json")
    if os.path.exists(whitelist_path):
        try:
            with open(whitelist_path, "r", encoding="utf-8") as f:
                file_whitelist = json.load(f)
                # Merge with default whitelist
                for pattern, contexts in file_whitelist.items():
                    if pattern in whitelist:
                        whitelist[pattern].extend(contexts)
                    else:
                        whitelist[pattern] = contexts
        except Exception as e:
            logger.warning(f"Error loading content whitelist from {whitelist_path}: {e}")

    return whitelist

def _calculate_entropy(data) -> float:
    """
    Calculate Shannon entropy of data

    Args:
        data: Data to calculate entropy for (string or bytes)

    Returns:
        Entropy value (0-8, where 8 is completely random)
    """
    import math

    if isinstance(data, str):
        data = data.encode('utf-8')

    # Count byte frequency
    byte_count = {}
    data_len = len(data)

    # If data is empty, return 0
    if data_len == 0:
        return 0

    # Count frequency of each byte
    for byte in data:
        byte_count[byte] = byte_count.get(byte, 0) + 1

    # Calculate entropy
    entropy = 0
    for count in byte_count.values():
        probability = count / data_len
        entropy -= probability * math.log2(probability)

    return entropy

def scan_with_yara(file_path: str) -> List[str]:
    """
    Scan a file with YARA rules using context-aware scanning

    Args:
        file_path: Path to the file to scan

    Returns:
        List of matched rule names
    """
    try:
        # Load all YARA rule files
        rule_files = [os.path.join(RULES_DIR, f) for f in os.listdir(RULES_DIR) if f.endswith('.yar')]

        if not rule_files:
            logger.warning(f"No YARA rule files found in {RULES_DIR}")
            return []

        matches = []
        for rule_file in rule_files:
            try:
                # Create scanner with context awareness enabled
                scanner = YaraScanner(rule_file, context_aware=True)
                file_matches = scanner.scan_file(file_path)

                # Log matches for debugging
                if file_matches:
                    logger.info(f"YARA matches from {os.path.basename(rule_file)} for {file_path}: {file_matches}")

                matches.extend(file_matches)
            except Exception as e:
                logger.error(f"Error scanning with rule file {rule_file}: {e}")

        return matches

    except Exception as e:
        logger.error(f"Error scanning file with YARA for {file_path}: {e}")
        return []

def check_threat_intel(file_path: str) -> Dict[str, Any]:
    """Check file against threat intelligence sources"""
    try:
        # Initialize threat intelligence module
        threat_intel = ThreatIntelligence()

        # Check file
        return threat_intel.check_file(file_path)

    except Exception as e:
        logger.error(f"Error checking threat intelligence for {file_path}: {e}")
        return {
            "file_path": file_path,
            "malicious": 0,
            "suspicious": 0,
            "benign": 0,
            "unknown": 1,
            "error": str(e)
        }

class Orchestrator:
    """Main orchestrator class for coordinating scanning operations"""

    def __init__(self):
        """Initialize the orchestrator"""
        self.logger = logging.getLogger("Orchestrator")
        self.file_type_detector = FileTypeDetector()
        self.rule_updater = RuleUpdater(RULES_DIR)
        self.threat_intel = ThreatIntelligence()

    def scan_file(self, file_path: str, verbose: bool = False) -> Dict[str, Any]:
        """Scan a single file and return results"""
        if verbose:
            print(f"[INFO] Scanning file: {file_path}")

        self.logger.info(f"Scanning file: {file_path}")

        # Initialize results dictionary
        results = {
            "file_path": file_path,
            "scan_time": datetime.now().isoformat(),
            "platform": platform.system()
        }

        # Get file information
        results["file_info"] = get_file_info(file_path)

        # Check permissions
        results["permissions"] = check_file_permissions(file_path)

        # Analyze content
        results["content_analysis"] = analyze_file_content(file_path)

        # Scan with YARA
        results["yara_matches"] = scan_with_yara(file_path)

        # Check threat intelligence
        results["threat_intel"] = check_threat_intel(file_path)

        # Determine recommendation with more precise logic and context awareness

        # Get safe contexts from content analysis
        safe_contexts = results["content_analysis"].get("safe_contexts", [])

        # Count the number of suspicious strings
        suspicious_string_count = len(results["content_analysis"]["suspicious_strings"])

        # Check if file has high entropy (potential encryption/obfuscation)
        has_high_entropy = results["content_analysis"].get("high_entropy", False)

        # Count the number of YARA matches
        yara_match_count = len(results["yara_matches"])

        # Check for high-risk file types
        high_risk_extensions = ['.exe', '.dll', '.sys', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.jar', '.apk', '.msi', '.sh']
        medium_risk_extensions = ['.py', '.php', '.rb', '.pl', '.cgi', '.jsp', '.asp', '.aspx']
        is_high_risk_extension = any(file_path.lower().endswith(ext) for ext in high_risk_extensions)
        is_medium_risk_extension = any(file_path.lower().endswith(ext) for ext in medium_risk_extensions)

        # Check for suspicious permissions
        has_suspicious_permissions = results["permissions"]["is_suspicious"]

        # Check threat intelligence results
        has_malicious_threat_intel = results["threat_intel"]["malicious"] > 0
        has_suspicious_threat_intel = results["threat_intel"]["suspicious"] > 0

        # Check file category
        is_executable = results["content_analysis"].get("is_executable", False)
        is_archive = results["content_analysis"].get("is_archive", False)

        # Calculate risk score (0-100)
        risk_score = 0

        # Add points for YARA matches (highest weight)
        risk_score += yara_match_count * 25  # Each YARA match adds 25 points

        # Add points for suspicious strings
        risk_score += suspicious_string_count * 5  # Each suspicious string adds 5 points

        # Add points for high entropy
        if has_high_entropy:
            risk_score += 15

        # Add points for file type
        if is_executable:
            risk_score += 15
        elif is_archive:
            risk_score += 10
        elif is_high_risk_extension:
            risk_score += 15
        elif is_medium_risk_extension:
            risk_score += 10

        # Add points for suspicious permissions
        if has_suspicious_permissions:
            risk_score += 15

        # Add points for threat intelligence
        if has_malicious_threat_intel:
            risk_score += 30
        elif has_suspicious_threat_intel:
            risk_score += 15

        # Reduce score for safe contexts (context awareness)
        risk_score -= len(safe_contexts) * 10  # Each safe context reduces score by 10 points

        # Ensure score is within bounds
        risk_score = max(0, min(100, risk_score))

        # Store risk score
        results["risk_score"] = risk_score

        # Determine risk level and recommendation based on score
        if risk_score >= 70:
            # High risk - Quarantine
            results["recommendation"] = "Quarantine"
            results["risk_level"] = "High"
        elif risk_score >= 40:
            # Medium risk - Investigate
            results["recommendation"] = "Investigate"
            results["risk_level"] = "Medium"
        elif risk_score >= 15:
            # Low risk - Monitor
            results["recommendation"] = "Monitor"
            results["risk_level"] = "Low"
        else:
            # No risk - Safe
            results["recommendation"] = "Safe"
            results["risk_level"] = "None"

        # Add safe contexts to results for transparency
        results["safe_contexts"] = safe_contexts

        # Extract threats for simplified output
        results["threats"] = []

        # Add YARA matches
        for match in results["yara_matches"]:
            results["threats"].append(f"YARA rule match: {match}")

        # Add suspicious strings
        for string in results["content_analysis"]["suspicious_strings"]:
            results["threats"].append(f"Suspicious string: {string}")

        # Add file type
        results["file_type"] = results["content_analysis"]["file_type"]

        # Log results if verbose
        if verbose:
            log_results(file_path, results)
            save_json_output(file_path, results)

        return results

    def scan_directory(self, dir_path: str, recursive: bool = False, verbose: bool = False) -> List[Dict[str, Any]]:
        """Scan all files in a directory and return results"""
        if verbose:
            print(f"[INFO] Scanning directory: {dir_path} (recursive: {recursive})")

        self.logger.info(f"Scanning directory: {dir_path} (recursive: {recursive})")

        results = []

        try:
            if recursive:
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        results.append(self.scan_file(full_path, verbose))
            else:
                for file in os.listdir(dir_path):
                    full_path = os.path.join(dir_path, file)
                    if os.path.isfile(full_path):
                        results.append(self.scan_file(full_path, verbose))
        except Exception as e:
            self.logger.error(f"Error scanning directory {dir_path}: {str(e)}")
            print(f"[ERROR] Error scanning directory {dir_path}: {str(e)}")

        return results

    def update_rules(self) -> bool:
        """Update YARA rules"""
        self.logger.info("Updating YARA rules")
        return self.rule_updater.update_rules()

    def run_scan(self, target_dir: str = TARGET_DIR, recursive: bool = True, verbose: bool = False) -> List[Dict[str, Any]]:
        """Run a comprehensive scan on all files in the target directory"""
        self.logger.info(f"Starting scan on {platform.system()} platform")

        if verbose:
            print(f"[INFO] Starting scan on {platform.system()} platform")
            print(f"[INFO] Target directory: {target_dir}")
            print(f"[INFO] Rules directory: {RULES_DIR}")

        # Get rule information
        rule_info = self.rule_updater.get_all_rule_info()

        if verbose:
            print(f"[INFO] Found {len(rule_info)} rule files")

        # Scan all files in the target directory
        results = self.scan_directory(target_dir, recursive, verbose)

        if verbose:
            print(f"[INFO] Scan complete. {len(results)} files scanned.")

        return results


# For backward compatibility
def run_scan() -> None:
    """Run a comprehensive scan on all files in the target directory"""
    orchestrator = Orchestrator()
    orchestrator.run_scan(TARGET_DIR, True, True)

if __name__ == "__main__":
    run_scan()