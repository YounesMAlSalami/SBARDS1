import os
import hashlib
import requests
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

class RuleUpdater:
    """
    Updates YARA rules from various sources
    """
    
    def __init__(self, rules_dir: str = None):
        """
        Initialize the rule updater
        
        Args:
            rules_dir: Directory where rules are stored
        """
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("RuleUpdater")
        
        # Set rules directory
        if rules_dir:
            self.rules_dir = rules_dir
        else:
            # Use default rules directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.rules_dir = os.path.abspath(os.path.join(base_dir, "../..", "rules"))
        
        # Create rules directory if it doesn't exist
        os.makedirs(self.rules_dir, exist_ok=True)
        
        # Map of rule categories to remote sources
        self.rule_sources = {
            "windows_executables": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_AZORULT.yar",
            "multimedia": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_LURK.yar",
            "documents": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_LURK.yar",
            "archives": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_LURK.yar",
            "programming": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_LURK.yar",
            "gaming": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_LURK.yar",
            "network": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_LURK.yar",
            "certificates": "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_LURK.yar",
            "custom_rules": None  # No remote source for custom rules
        }
        
        # Initialize hash cache
        self.hash_cache = self._load_hash_cache()
    
    def update_all_rules(self) -> Dict[str, bool]:
        """
        Update all rule files from remote sources
        
        Returns:
            Dictionary mapping rule categories to update status (True if updated, False otherwise)
        """
        self.logger.info("Starting rule update process")
        
        results = {}
        for category, source_url in self.rule_sources.items():
            if source_url:  # Skip categories with no remote source
                results[category] = self.update_rule(category, source_url)
            else:
                results[category] = False
        
        self.logger.info(f"Rule update process completed: {results}")
        return results
    
    def update_rule(self, category: str, source_url: str) -> bool:
        """
        Update a specific rule file from a remote source
        
        Args:
            category: Rule category
            source_url: URL to download the rule from
            
        Returns:
            True if the rule was updated, False otherwise
        """
        self.logger.info(f"Updating rule: {category} from {source_url}")
        
        rule_file = os.path.join(self.rules_dir, f"{category}.yar")
        
        try:
            # Download rule file
            response = requests.get(source_url, timeout=10)
            response.raise_for_status()
            
            # Get content
            content = response.text
            
            # Calculate hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Check if the rule has changed
            if self._has_rule_changed(category, content_hash):
                # Save the rule
                with open(rule_file, "w", encoding="utf-8") as f:
                    f.write(content)
                
                # Update hash cache
                self._update_hash_cache(category, content_hash)
                
                self.logger.info(f"Rule {category} updated successfully")
                return True
            else:
                self.logger.info(f"Rule {category} is already up to date")
                return False
        
        except Exception as e:
            self.logger.error(f"Error updating rule {category}: {e}")
            return False
    
    def _has_rule_changed(self, category: str, new_hash: str) -> bool:
        """
        Check if a rule has changed by comparing hashes
        
        Args:
            category: Rule category
            new_hash: New hash to compare
            
        Returns:
            True if the rule has changed, False otherwise
        """
        if category not in self.hash_cache:
            return True
        
        return self.hash_cache[category] != new_hash
    
    def _update_hash_cache(self, category: str, new_hash: str) -> None:
        """
        Update the hash cache for a rule
        
        Args:
            category: Rule category
            new_hash: New hash to store
        """
        self.hash_cache[category] = new_hash
        
        # Save hash cache
        cache_file = os.path.join(self.rules_dir, "hash_cache.txt")
        with open(cache_file, "w", encoding="utf-8") as f:
            for cat, hash_val in self.hash_cache.items():
                f.write(f"{cat}:{hash_val}\n")
    
    def _load_hash_cache(self) -> Dict[str, str]:
        """
        Load the hash cache from disk
        
        Returns:
            Dictionary mapping rule categories to hashes
        """
        cache_file = os.path.join(self.rules_dir, "hash_cache.txt")
        cache = {}
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if ":" in line:
                            category, hash_val = line.split(":", 1)
                            cache[category] = hash_val
            except Exception as e:
                self.logger.error(f"Error loading hash cache: {e}")
        
        return cache
    
    def get_rule_info(self, category: str) -> Dict[str, Any]:
        """
        Get information about a rule
        
        Args:
            category: Rule category
            
        Returns:
            Dictionary with rule information
        """
        rule_file = os.path.join(self.rules_dir, f"{category}.yar")
        
        if not os.path.exists(rule_file):
            return {
                "category": category,
                "exists": False,
                "size": 0,
                "last_modified": None,
                "hash": None,
                "has_remote_source": category in self.rule_sources and self.rule_sources[category] is not None
            }
        
        # Get file stats
        stats = os.stat(rule_file)
        
        # Calculate hash
        with open(rule_file, "rb") as f:
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()
        
        return {
            "category": category,
            "exists": True,
            "size": stats.st_size,
            "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "hash": file_hash,
            "has_remote_source": category in self.rule_sources and self.rule_sources[category] is not None
        }
    
    def get_all_rule_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all rules
        
        Returns:
            List of dictionaries with rule information
        """
        return [self.get_rule_info(category) for category in self.rule_sources.keys()]
