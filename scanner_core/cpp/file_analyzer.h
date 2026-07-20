#ifndef FILE_ANALYZER_H
#define FILE_ANALYZER_H

#include "shared_utils.h"

// Structure to hold file analysis results
struct FileAnalysisResult {
    std::string file_path;
    bool is_binary;
    std::vector<std::string> suspicious_patterns;
    std::string file_type;
    int64_t file_size;
    std::string permissions;
    bool has_suid_bit;
    bool has_sgid_bit;
    bool requires_admin;
    bool is_protected_system_file;
    std::string recommendation;
};

class FileAnalyzer {
public:
    FileAnalyzer();
    ~FileAnalyzer();
    
    // Analyze a file and return results
    FileAnalysisResult analyze_file(const std::string& file_path);
    
    // Check for suspicious patterns in file content
    std::vector<std::string> check_suspicious_patterns(const std::string& file_path);
    
    // Determine if file is potentially malicious
    bool is_potentially_malicious(const FileAnalysisResult& result);
    
    // Get recommendation based on analysis
    std::string get_recommendation(const FileAnalysisResult& result);
    
private:
    // Check for suspicious patterns in text file
    std::vector<std::string> check_text_file(const std::string& content);
    
    // Check for suspicious patterns in binary file
    std::vector<std::string> check_binary_file(const std::string& file_path);
    
    // Check for suspicious URLs in file
    std::vector<std::string> check_suspicious_urls(const std::string& content);
    
    // Check for suspicious commands in file
    std::vector<std::string> check_suspicious_commands(const std::string& content);
    
    // Check for suspicious file permissions
    bool has_suspicious_permissions(const std::string& permissions);
};

#endif // FILE_ANALYZER_H
