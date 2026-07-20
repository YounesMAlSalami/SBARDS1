#ifndef YARA_SCANNER_H
#define YARA_SCANNER_H

#include "shared_utils.h"
#include <yara.h>

// Structure to hold YARA scan results
struct YaraScanResult {
    std::string file_path;
    std::vector<ScanResult> matches;
    bool has_threats;
    std::string recommendation;
};

class YaraScanner {
public:
    YaraScanner();
    ~YaraScanner();
    
    // Initialize YARA scanner
    bool initialize();
    
    // Load YARA rules from file
    bool load_rules(const std::string& rules_file);
    
    // Load YARA rules from directory
    bool load_rules_from_directory(const std::string& rules_dir);
    
    // Scan file with loaded rules
    YaraScanResult scan_file(const std::string& file_path);
    
    // Scan directory with loaded rules
    std::vector<YaraScanResult> scan_directory(const std::string& dir_path, bool recursive = false);
    
    // Get recommendation based on scan results
    std::string get_recommendation(const YaraScanResult& result);
    
    // Finalize YARA scanner
    void finalize();
    
private:
    YR_RULES* rules;
    YR_COMPILER* compiler;
    bool initialized;
    
    // Callback function for YARA scanning
    static int scan_callback(YR_SCAN_CONTEXT* context, int message, void* message_data, void* user_data);
    
    // Process YARA rule match
    void process_rule_match(YR_RULE* rule, const std::string& file_path, std::vector<ScanResult>& matches);
    
    // Get rule metadata
    std::map<std::string, std::string> get_rule_metadata(YR_RULE* rule);
    
    // Get matched strings
    std::vector<std::string> get_matched_strings(YR_RULE* rule, YR_SCAN_CONTEXT* context);
};

#endif // YARA_SCANNER_H
