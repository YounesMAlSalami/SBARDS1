import os
import hashlib
import requests
import logging
import json
from typing import Dict, List, Any, Optional

class ThreatIntelligence:
    """
    Integrates with threat intelligence sources to check file reputation
    """
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        Initialize the threat intelligence module
        
        Args:
            api_keys: Dictionary mapping service names to API keys
        """
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("ThreatIntelligence")
        
        # Initialize API keys
        self.api_keys = api_keys or {}
        
        # Set cache directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.cache_dir = os.path.abspath(os.path.join(base_dir, "../..", "output", "threat_intel_cache"))
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def check_file(self, file_path: str) -> Dict[str, Any]:
        """
        Check a file against threat intelligence sources
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            Dictionary with threat intelligence results
        """
        self.logger.info(f"Checking file: {file_path}")
        
        if not os.path.exists(file_path):
            return {
                "file_path": file_path,
                "exists": False,
                "malicious": 0,
                "suspicious": 0,
                "benign": 0,
                "unknown": 1,
                "sources": []
            }
        
        # Calculate file hash
        file_hash = self._calculate_file_hash(file_path)
        
        # Check cache
        cached_result = self._check_cache(file_hash)
        if cached_result:
            self.logger.info(f"Using cached result for {file_path}")
            return cached_result
        
        # Initialize results
        results = {
            "file_path": file_path,
            "exists": True,
            "file_hash": file_hash,
            "malicious": 0,
            "suspicious": 0,
            "benign": 0,
            "unknown": 1,  # Default to unknown
            "sources": []
        }
        
        # Check VirusTotal if API key is available
        if "virustotal" in self.api_keys:
            vt_result = self._check_virustotal(file_hash)
            if vt_result:
                results["sources"].append({
                    "name": "VirusTotal",
                    "result": vt_result
                })
                
                # Update counts
                if vt_result.get("malicious", 0) > 0:
                    results["malicious"] += 1
                    results["unknown"] = 0
                elif vt_result.get("suspicious", 0) > 0:
                    results["suspicious"] += 1
                    results["unknown"] = 0
                elif vt_result.get("harmless", 0) > 0:
                    results["benign"] += 1
                    results["unknown"] = 0
        
        # Check AlienVault OTX if API key is available
        if "alienvault" in self.api_keys:
            otx_result = self._check_alienvault(file_hash)
            if otx_result:
                results["sources"].append({
                    "name": "AlienVault OTX",
                    "result": otx_result
                })
                
                # Update counts
                if otx_result.get("malicious", False):
                    results["malicious"] += 1
                    results["unknown"] = 0
                elif otx_result.get("suspicious", False):
                    results["suspicious"] += 1
                    results["unknown"] = 0
                elif otx_result.get("benign", False):
                    results["benign"] += 1
                    results["unknown"] = 0
        
        # Cache results
        self._cache_result(file_hash, results)
        
        return results
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file"""
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    def _check_cache(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """Check if a file hash is in the cache"""
        cache_file = os.path.join(self.cache_dir, f"{file_hash}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error reading cache file: {e}")
        
        return None
    
    def _cache_result(self, file_hash: str, result: Dict[str, Any]) -> None:
        """Cache a threat intelligence result"""
        cache_file = os.path.join(self.cache_dir, f"{file_hash}.json")
        
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error writing cache file: {e}")
    
    def _check_virustotal(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """
        Check a file hash against VirusTotal
        
        Note: This is a mock implementation. In a real system, you would use the VirusTotal API.
        """
        self.logger.info(f"Checking VirusTotal for hash: {file_hash}")
        
        # Mock implementation - in a real system, you would call the VirusTotal API
        # For demonstration purposes, we'll return a mock result
        if file_hash.startswith("a") or file_hash.startswith("b") or file_hash.startswith("c"):
            return {
                "malicious": 10,
                "suspicious": 5,
                "harmless": 50,
                "undetected": 10,
                "total": 75
            }
        elif file_hash.startswith("d") or file_hash.startswith("e") or file_hash.startswith("f"):
            return {
                "malicious": 0,
                "suspicious": 3,
                "harmless": 62,
                "undetected": 10,
                "total": 75
            }
        else:
            return {
                "malicious": 0,
                "suspicious": 0,
                "harmless": 65,
                "undetected": 10,
                "total": 75
            }
    
    def _check_alienvault(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """
        Check a file hash against AlienVault OTX
        
        Note: This is a mock implementation. In a real system, you would use the AlienVault OTX API.
        """
        self.logger.info(f"Checking AlienVault OTX for hash: {file_hash}")
        
        # Mock implementation - in a real system, you would call the AlienVault OTX API
        # For demonstration purposes, we'll return a mock result
        if file_hash.startswith("a") or file_hash.startswith("b"):
            return {
                "malicious": True,
                "suspicious": False,
                "benign": False,
                "pulses": 5,
                "references": [
                    "https://otx.alienvault.com/pulse/1234567890"
                ]
            }
        elif file_hash.startswith("c") or file_hash.startswith("d"):
            return {
                "malicious": False,
                "suspicious": True,
                "benign": False,
                "pulses": 2,
                "references": [
                    "https://otx.alienvault.com/pulse/0987654321"
                ]
            }
        else:
            return {
                "malicious": False,
                "suspicious": False,
                "benign": True,
                "pulses": 0,
                "references": []
            }
    
    def check_url(self, url: str) -> Dict[str, Any]:
        """
        Check a URL against threat intelligence sources
        
        Args:
            url: URL to check
            
        Returns:
            Dictionary with threat intelligence results
        """
        self.logger.info(f"Checking URL: {url}")
        
        # Initialize results
        results = {
            "url": url,
            "malicious": 0,
            "suspicious": 0,
            "benign": 0,
            "unknown": 1,  # Default to unknown
            "sources": []
        }
        
        # Mock implementation - in a real system, you would call threat intelligence APIs
        if "malware" in url or "phishing" in url or "exploit" in url:
            results["malicious"] = 1
            results["unknown"] = 0
        elif "suspicious" in url or "untrusted" in url:
            results["suspicious"] = 1
            results["unknown"] = 0
        elif "google.com" in url or "microsoft.com" in url or "apple.com" in url:
            results["benign"] = 1
            results["unknown"] = 0
        
        return results
