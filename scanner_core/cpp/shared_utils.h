#ifndef SHARED_UTILS_H
#define SHARED_UTILS_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <memory>
#include <filesystem>
#include <iomanip>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <ctime>
#include <chrono>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/stat.h>
#include <unistd.h>
#endif

namespace fs = std::filesystem;

// Structure to hold file information
struct FileInfo {
    std::string file_path;
    std::string file_type;
    bool is_binary;
    std::string permissions;
    bool has_suid_bit;
    bool has_sgid_bit;
    int64_t file_size;
    std::string last_modified;
    std::string creation_time;
};

// Structure to hold scan results
struct ScanResult {
    std::string rule_name;
    std::string description;
    std::string severity;
    std::string file_path;
    std::map<std::string, std::string> meta;
    std::vector<std::string> matched_strings;
};

// Structure for signature verification
struct SignatureResult {
    std::string file_path;
    std::string issuer;
    std::string subject;
    std::string validity;
    std::string status;
    bool is_valid;
};

// Structure for threat intelligence
struct ThreatIntel {
    std::map<std::string, int> virus_total;
    std::map<std::string, std::string> hybrid_analysis;
};

// Smart pointer for memory management
template<typename T>
using SafePtr = std::unique_ptr<T>;

// Safe string handling
class SafeString {
public:
    static std::string to_lowercase(const std::string& str);
    static std::string to_uppercase(const std::string& str);
    static bool contains(const std::string& haystack, const std::string& needle);
    static std::vector<std::string> tokenize(const std::string& str, char delimiter);
};

// File utilities
class FileUtil {
public:
    static bool is_binary_file(const std::string& file_path);
    static std::string determine_file_type(const std::string& file_path);
    static FileInfo get_file_info(const std::string& file_path);
    static std::string read_file(const std::string& file_path);
    static bool write_file(const std::string& file_path, const std::string& content);
};

// Security utilities
class SecurityUtil {
public:
    static std::string calculate_sha256(const std::string& file_path);
    static std::string calculate_md5(const std::string& file_path);
    static bool check_signature(const std::string& cert_path, const std::string& data_path);
};

// Platform-specific utilities
class PlatformUtil {
public:
    static std::string get_permissions(const std::string& file_path);
    static void check_special_permissions(const std::string& file_path, bool& suid, bool& sgid);
    static bool requires_admin_privileges(const std::string& file_path);
    static bool is_protected_system_file(const std::string& file_path);
};

// Safe memory management
class MemoryUtil {
public:
    template<typename T>
    static SafePtr<T> create_safe_ptr(T* ptr) {
        return SafePtr<T>(ptr);
    }
    
    template<typename T>
    static SafePtr<T[]> create_safe_array(size_t size) {
        return SafePtr<T[]>(new T[size]);
    }
};

// Common string patterns for scanning
class CommonPatterns {
public:
    static const std::vector<std::string> malicious_patterns;
    static const std::vector<std::string> suspicious_extensions;
    static const std::map<std::string, std::string> file_type_map;
};

#endif // SHARED_UTILS_H
