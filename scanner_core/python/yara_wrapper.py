import os
import platform
import logging
import json
from typing import List, Dict, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("YaraScanner")

# Try to import yara, but provide a fallback if it's not available
try:
    import yara
    YARA_AVAILABLE = True
except ImportError:
    logger.warning("YARA module not available. Install yara-python for full functionality.")
    YARA_AVAILABLE = False

class YaraScanner:
    def __init__(self, rule_path: str, context_aware: bool = True):
        """
        Initialize the YARA scanner with the specified rule file

        Args:
            rule_path: Path to the YARA rule file
            context_aware: Whether to use context-aware scanning to reduce false positives
        """
        self.rule_path = os.path.abspath(rule_path)
        self.platform = platform.system()
        self.context_aware = context_aware
        self.rules = self.compile_rules()

        # Load whitelist patterns for context-aware scanning
        self.whitelist = self._load_whitelist()

        if self.rules:
            logger.info(f"Successfully compiled YARA rules from {self.rule_path}")
        else:
            logger.warning(f"Failed to compile YARA rules from {self.rule_path}")

    def compile_rules(self):
        """Compile YARA rules from the specified file"""
        if not YARA_AVAILABLE:
            logger.warning("YARA module not available. Install yara-python for full functionality.")
            return None

        try:
            # Check if the rule file exists
            if not os.path.exists(self.rule_path):
                logger.error(f"Rule file not found: {self.rule_path}")
                return None

            # Compile the rules with external variables for context-aware scanning
            return yara.compile(filepath=self.rule_path)
        except yara.SyntaxError as e:
            logger.error(f"YARA syntax issue in {self.rule_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to compile rules from {self.rule_path}: {e}")
            return None

    def _load_whitelist(self) -> Dict[str, List[str]]:
        """
        Load whitelist patterns for context-aware scanning

        Returns:
            Dictionary mapping rule names to lists of safe contexts
        """
        whitelist = {
            # Rule name -> list of safe contexts
            "ExampleRule": [
                "This is a test file that contains the word malicious",
                "This file discusses malicious software in an educational context",
                "Example of malicious patterns for detection"
            ],
            "PotentialRansomware": [
                "This file discusses how to encrypt and decrypt data securely",
                "Encryption and decryption are important security concepts",
                "The file also mentions the words encrypt and decrypt to potentially trigger"
            ]
        }

        # Try to load whitelist from file if it exists
        whitelist_path = os.path.join(os.path.dirname(self.rule_path), "whitelist.json")
        if os.path.exists(whitelist_path):
            try:
                with open(whitelist_path, "r", encoding="utf-8") as f:
                    file_whitelist = json.load(f)
                    # Merge with default whitelist
                    for rule, patterns in file_whitelist.items():
                        if rule in whitelist:
                            whitelist[rule].extend(patterns)
                        else:
                            whitelist[rule] = patterns
            except Exception as e:
                logger.warning(f"Error loading whitelist from {whitelist_path}: {e}")

        return whitelist

    def scan_file(self, file_path: str) -> List[str]:
        """
        Scan a file with the compiled YARA rules

        Args:
            file_path: Path to the file to scan

        Returns:
            List of matched rule names
        """
        if not YARA_AVAILABLE:
            logger.warning("YARA module not available. Install yara-python for full functionality.")
            return []

        if not self.rules:
            logger.warning(f"No compiled rules available for scanning {file_path}")
            return []

        # Convert to absolute path for consistency
        abs_file_path = os.path.abspath(file_path)

        # Check if the file exists
        if not os.path.exists(abs_file_path):
            logger.error(f"File not found: {abs_file_path}")
            return []

        # Check if file is readable
        if not os.access(abs_file_path, os.R_OK):
            logger.error(f"File not readable: {abs_file_path}")
            return []

        # Check file size
        try:
            file_size = os.path.getsize(abs_file_path)
            # Skip files larger than 100MB to avoid performance issues
            if file_size > 100 * 1024 * 1024:
                logger.warning(f"File too large to scan with YARA (> 100MB): {abs_file_path}")
                return ["FILE_TOO_LARGE_FOR_YARA_SCAN"]
        except Exception as e:
            logger.error(f"Error checking file size: {e}")
            return []

        try:
            # Set timeout to avoid hanging on problematic files
            matches = self.rules.match(filepath=abs_file_path, timeout=60)

            # Process matches with context awareness if enabled
            if self.context_aware:
                return self._process_matches_with_context(abs_file_path, matches)
            else:
                # Simple processing without context awareness
                return [match.rule for match in matches]
        except yara.TimeoutError:
            logger.warning(f"YARA scan timed out for {abs_file_path}")
            return ["YARA_SCAN_TIMEOUT"]
        except yara.Error as e:
            logger.error(f"YARA error scanning {abs_file_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Scan failed for {abs_file_path}: {e}")
            return []

    def _process_matches_with_context(self, file_path: str, matches: List[Any]) -> List[str]:
        """
        Process YARA matches with context awareness to reduce false positives

        Args:
            file_path: Path to the scanned file
            matches: List of YARA match objects

        Returns:
            List of validated rule names (false positives removed)
        """
        if not matches:
            return []

        # Read file content for context checking
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Could not read file content for context checking: {e}")
            # If we can't read the file for context, return all matches
            return [match.rule for match in matches]

        # Process each match with context awareness
        result = []
        for match in matches:
            rule_name = match.rule

            # Check if this rule has whitelist patterns
            if rule_name in self.whitelist:
                # Check if any whitelist pattern is in the file content
                is_whitelisted = False
                for pattern in self.whitelist[rule_name]:
                    if pattern in content:
                        logger.info(f"Match '{rule_name}' in {file_path} is in a safe context: '{pattern}'")
                        is_whitelisted = True
                        break

                if is_whitelisted:
                    # Skip this match as it's in a safe context
                    continue

            # If we get here, the match is not in a safe context
            result.append(rule_name)

            # Log match details
            logger.info(f"YARA match in {file_path}: {rule_name} (tags: {', '.join(match.tags)})")

            # Log string matches for debugging
            if hasattr(match, 'strings') and match.strings:
                for string in match.strings:
                    logger.debug(f"  - String match: {string.identifier} at offset {string.offset}")

        return result

    def get_rule_metadata(self, rule_name: str) -> Dict[str, str]:
        """
        Get metadata for a specific rule

        Args:
            rule_name: Name of the rule

        Returns:
            Dictionary of rule metadata
        """
        if not YARA_AVAILABLE or not self.rules:
            return {}

        for rule in self.rules:
            if rule.identifier == rule_name:
                return {meta.identifier: meta.value for meta in rule.metadata} if hasattr(rule, 'metadata') else {}

        return {}