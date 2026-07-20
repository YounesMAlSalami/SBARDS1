#include "yara_scanner.h"
#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>
#include <map>

YaraScanner::YaraScanner() : rules(nullptr), compiler(nullptr), initialized(false) {
    // Constructor
}

YaraScanner::~YaraScanner() {
    // Destructor
    finalize();
}

bool YaraScanner::initialize() {
    if (initialized) {
        return true;
    }

    if (yr_initialize() != ERROR_SUCCESS) {
        std::cerr << "Failed to initialize YARA library" << std::endl;
        return false;
    }

    if (yr_compiler_create(&compiler) != ERROR_SUCCESS) {
        std::cerr << "Failed to create YARA compiler" << std::endl;
        yr_finalize();
        return false;
    }

    initialized = true;
    return true;
}

bool YaraScanner::load_rules(const std::string& rules_file) {
    if (!initialized) {
        if (!initialize()) {
            return false;
        }
    }

    FILE* rule_fp = fopen(rules_file.c_str(), "r");
    if (!rule_fp) {
        std::cerr << "Could not open rules file: " << rules_file << std::endl;
        return false;
    }

    int errors = yr_compiler_add_file(compiler, rule_fp, nullptr, rules_file.c_str());
    fclose(rule_fp);

    if (errors > 0) {
        std::cerr << "Errors compiling YARA rules: " << errors << std::endl;
        return false;
    }

    if (yr_compiler_get_rules(compiler, &rules) != ERROR_SUCCESS) {
        std::cerr << "Failed to get compiled rules" << std::endl;
        return false;
    }

    return true;
}

bool YaraScanner::load_rules_from_directory(const std::string& rules_dir) {
    if (!initialized) {
        if (!initialize()) {
            return false;
        }
    }

    bool success = true;

    for (const auto& entry : std::filesystem::directory_iterator(rules_dir)) {
        if (entry.is_regular_file() && entry.path().extension() == ".yar") {
            std::string rules_file = entry.path().string();
            std::cout << "Loading rules from: " << rules_file << std::endl;

            FILE* rule_fp = fopen(rules_file.c_str(), "r");
            if (!rule_fp) {
                std::cerr << "Could not open rules file: " << rules_file << std::endl;
                success = false;
                continue;
            }

            int errors = yr_compiler_add_file(compiler, rule_fp, nullptr, rules_file.c_str());
            fclose(rule_fp);

            if (errors > 0) {
                std::cerr << "Errors compiling YARA rules in " << rules_file << ": " << errors << std::endl;
                success = false;
            }
        }
    }

    if (yr_compiler_get_rules(compiler, &rules) != ERROR_SUCCESS) {
        std::cerr << "Failed to get compiled rules" << std::endl;
        return false;
    }

    return success;
}

YaraScanResult YaraScanner::scan_file(const std::string& file_path) {
    YaraScanResult result;
    result.file_path = file_path;
    result.has_threats = false;

    if (!initialized || !rules) {
        std::cerr << "YARA scanner not initialized or no rules loaded" << std::endl;
        result.recommendation = "Error: YARA scanner not initialized";
        return result;
    }

    std::vector<ScanResult> matches;

    int scan_result = yr_rules_scan_file(
        rules, file_path.c_str(), 0,
        scan_callback,
        &matches, 0
    );

    if (scan_result != ERROR_SUCCESS && scan_result != ERROR_TOO_MANY_MATCHES) {
        std::cerr << "Error scanning file: " << file_path << std::endl;
        result.recommendation = "Error: Failed to scan file";
        return result;
    }

    result.matches = matches;
    result.has_threats = !matches.empty();
    result.recommendation = get_recommendation(result);

    return result;
}

std::vector<YaraScanResult> YaraScanner::scan_directory(const std::string& dir_path, bool recursive) {
    std::vector<YaraScanResult> results;

    if (!initialized || !rules) {
        std::cerr << "YARA scanner not initialized or no rules loaded" << std::endl;
        return results;
    }

    try {
        if (recursive) {
            for (const auto& entry : std::filesystem::recursive_directory_iterator(dir_path)) {
                if (entry.is_regular_file()) {
                    results.push_back(scan_file(entry.path().string()));
                }
            }
        } else {
            for (const auto& entry : std::filesystem::directory_iterator(dir_path)) {
                if (entry.is_regular_file()) {
                    results.push_back(scan_file(entry.path().string()));
                }
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Error scanning directory: " << e.what() << std::endl;
    }

    return results;
}

std::string YaraScanner::get_recommendation(const YaraScanResult& result) {
    if (result.has_threats) {
        // Check for high severity threats
        for (const auto& match : result.matches) {
            if (match.severity == "high") {
                return "Quarantine";
            }
        }

        // Check for medium severity threats
        for (const auto& match : result.matches) {
            if (match.severity == "medium") {
                return "Review";
            }
        }

        // Low severity threats
        return "Monitor";
    } else {
        return "Safe";
    }
}

void YaraScanner::finalize() {
    if (rules) {
        yr_rules_destroy(rules);
        rules = nullptr;
    }

    if (compiler) {
        yr_compiler_destroy(compiler);
        compiler = nullptr;
    }

    if (initialized) {
        yr_finalize();
        initialized = false;
    }
}

int YaraScanner::scan_callback(YR_SCAN_CONTEXT* context, int message, void* message_data, void* user_data) {
    if (message == CALLBACK_MSG_RULE_MATCHING) {
        YR_RULE* rule = (YR_RULE*)message_data;
        std::vector<ScanResult>* matches = (std::vector<ScanResult>*)user_data;

        YaraScanner scanner;
        scanner.process_rule_match(rule, "", *matches);
    }

    return CALLBACK_CONTINUE;
}

void YaraScanner::process_rule_match(YR_RULE* rule, const std::string& file_path, std::vector<ScanResult>& matches) {
    ScanResult result;
    result.rule_name = rule->identifier;
    result.file_path = file_path;

    // Get rule metadata
    result.meta = get_rule_metadata(rule);

    // Set description and severity from metadata
    auto desc_it = result.meta.find("description");
    if (desc_it != result.meta.end()) {
        result.description = desc_it->second;
    } else {
        result.description = "No description available";
    }

    auto severity_it = result.meta.find("severity");
    if (severity_it != result.meta.end()) {
        result.severity = severity_it->second;
    } else {
        result.severity = "medium"; // Default severity
    }

    matches.push_back(result);
}

std::map<std::string, std::string> YaraScanner::get_rule_metadata(YR_RULE* rule) {
    std::map<std::string, std::string> metadata;

    YR_META* meta;
    yr_rule_metas_foreach(rule, meta) {
        if (meta->type == META_TYPE_STRING) {
            metadata[meta->identifier] = meta->string;
        } else if (meta->type == META_TYPE_INTEGER) {
            metadata[meta->identifier] = std::to_string(meta->integer);
        }
    }

    return metadata;
}

std::vector<std::string> YaraScanner::get_matched_strings(YR_RULE* rule, YR_SCAN_CONTEXT* context) {
    std::vector<std::string> matched_strings;

    YR_STRING* string;
    yr_rule_strings_foreach(rule, string) {
        YR_MATCH* match;
        yr_string_matches_foreach(context, string, match) {
            char* str = (char*)match->data;
            size_t str_len = match->data_length;

            std::string matched_string(str, str_len);
            matched_strings.push_back(matched_string);
        }
    }

    return matched_strings;
}

// Main function for standalone usage
int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: yara_scanner <rules_file_or_dir> <target_file_or_dir> [--recursive]" << std::endl;
        return 1;
    }

    std::string rules_path = argv[1];
    std::string target_path = argv[2];
    bool recursive = (argc > 3 && std::string(argv[3]) == "--recursive");

    YaraScanner scanner;

    if (!scanner.initialize()) {
        std::cerr << "Failed to initialize YARA scanner" << std::endl;
        return 1;
    }

    bool rules_loaded = false;

    if (std::filesystem::is_directory(rules_path)) {
        rules_loaded = scanner.load_rules_from_directory(rules_path);
    } else {
        rules_loaded = scanner.load_rules(rules_path);
    }

    if (!rules_loaded) {
        std::cerr << "Failed to load YARA rules" << std::endl;
        return 1;
    }

    if (std::filesystem::is_directory(target_path)) {
        std::vector<YaraScanResult> results = scanner.scan_directory(target_path, recursive);

        std::cout << "Scan Results:" << std::endl;
        std::cout << "=============" << std::endl;

        for (const auto& result : results) {
            std::cout << "File: " << result.file_path << std::endl;
            std::cout << "Recommendation: " << result.recommendation << std::endl;

            if (result.has_threats) {
                std::cout << "Matches:" << std::endl;

                for (const auto& match : result.matches) {
                    std::cout << "  - Rule: " << match.rule_name << std::endl;
                    std::cout << "    Description: " << match.description << std::endl;
                    std::cout << "    Severity: " << match.severity << std::endl;
                }
            } else {
                std::cout << "No threats detected" << std::endl;
            }

            std::cout << std::endl;
        }
    } else {
        YaraScanResult result = scanner.scan_file(target_path);

        std::cout << "Scan Results:" << std::endl;
        std::cout << "=============" << std::endl;
        std::cout << "File: " << result.file_path << std::endl;
        std::cout << "Recommendation: " << result.recommendation << std::endl;

        if (result.has_threats) {
            std::cout << "Matches:" << std::endl;

            for (const auto& match : result.matches) {
                std::cout << "  - Rule: " << match.rule_name << std::endl;
                std::cout << "    Description: " << match.description << std::endl;
                std::cout << "    Severity: " << match.severity << std::endl;
            }
        } else {
            std::cout << "No threats detected" << std::endl;
        }
    }

    scanner.finalize();
    return 0;
}