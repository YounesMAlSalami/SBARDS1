#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>
#include <map>
#include <sstream>
#include <iomanip>
#include <cstring>

// This is a simplified mock version of the YARA scanner for demonstration purposes
// It simulates scanning a file for specific patterns without requiring the YARA library

// Case-insensitive string search for cross-platform consistency
bool contains_pattern(const std::string& content, const std::string& pattern) {
    std::string content_lower = content;
    std::string pattern_lower = pattern;

    // Convert to lowercase for case-insensitive comparison
    std::transform(content_lower.begin(), content_lower.end(), content_lower.begin(),
                  [](unsigned char c){ return std::tolower(c); });
    std::transform(pattern_lower.begin(), pattern_lower.end(), pattern_lower.begin(),
                  [](unsigned char c){ return std::tolower(c); });

    return content_lower.find(pattern_lower) != std::string::npos;
}

// Check if a pattern appears in a safe context
bool is_safe_context(const std::string& content, const std::string& pattern,
                     const std::vector<std::string>& safe_contexts) {
    for (const auto& safe_context : safe_contexts) {
        if (content.find(safe_context) != std::string::npos) {
            return true;
        }
    }
    return false;
}

// Calculate SHA-256 hash of a string (simplified version)
std::string calculate_hash(const std::string& content) {
    // This is a simplified hash function for demonstration purposes
    // In a real implementation, you would use a proper SHA-256 library
    size_t hash = 0;
    for (char c : content) {
        hash = hash * 31 + c;
    }

    std::stringstream ss;
    ss << std::hex << std::setfill('0') << std::setw(16) << hash;
    return ss.str();
}

// Load default whitelist patterns
std::map<std::string, std::vector<std::string>> load_default_whitelist() {
    std::map<std::string, std::vector<std::string>> whitelist;

    // Default whitelist patterns
    whitelist["malicious"] = {
        "This is a test file that contains the word malicious",
        "This file discusses malicious software in an educational context"
    };

    whitelist["encrypt"] = {
        "This file discusses how to encrypt and decrypt data securely",
        "The file also mentions the words encrypt and decrypt to potentially trigger"
    };

    whitelist["decrypt"] = {
        "This file discusses how to encrypt and decrypt data securely",
        "The file also mentions the words encrypt and decrypt to potentially trigger"
    };

    return whitelist;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << (argc > 0 ? argv[0] : "mock_scanner")
                  << " <rules_file> <target_file> [--context-aware]\n";
        return 1;
    }

    const char* rules_file = argv[1];
    const char* target_file = argv[2];

    // Check if context-aware scanning is enabled
    bool context_aware = false;
    for (int i = 3; i < argc; i++) {
        if (strcmp(argv[i], "--context-aware") == 0) {
            context_aware = true;
            break;
        }
    }

    std::cout << "Mock YARA Scanner (C++ Implementation)\n";
    std::cout << "Rules file: " << rules_file << "\n";
    std::cout << "Target file: " << target_file << "\n";
    std::cout << "Context-aware: " << (context_aware ? "true" : "false") << "\n";

    // Read the target file with binary mode for cross-platform compatibility
    std::ifstream file(target_file, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Could not open target file: " << target_file << "\n";
        return 1;
    }

    std::string content;
    std::string line;
    while (std::getline(file, line)) {
        content += line + "\n";
    }
    file.close();

    // Calculate file hash
    std::string file_hash = calculate_hash(content);
    std::cout << "File hash: " << file_hash << "\n";

    // Load whitelist if context-aware scanning is enabled
    std::map<std::string, std::vector<std::string>> whitelist;
    if (context_aware) {
        whitelist = load_default_whitelist();
    }

    // Simulate rule matching with context awareness
    std::vector<std::string> matched_rules;

    // Check for malicious pattern
    if (contains_pattern(content, "malicious")) {
        if (context_aware &&
            whitelist.find("malicious") != whitelist.end() &&
            is_safe_context(content, "malicious", whitelist["malicious"])) {
            std::cout << "Pattern 'malicious' found in safe context, not reporting\n";
        } else {
            matched_rules.push_back("ExampleRule");
            std::cout << "Matched rule: ExampleRule (found 'malicious')\n";
        }
    }

    // Check for encrypt and decrypt patterns
    if (contains_pattern(content, "encrypt") && contains_pattern(content, "decrypt")) {
        if (context_aware &&
            whitelist.find("encrypt") != whitelist.end() &&
            is_safe_context(content, "encrypt", whitelist["encrypt"])) {
            std::cout << "Patterns 'encrypt' and 'decrypt' found in safe context, not reporting\n";
        } else {
            matched_rules.push_back("PotentialRansomware");
            std::cout << "Matched rule: PotentialRansomware (found 'encrypt' and 'decrypt')\n";
        }
    }

    // Check for suspicious network activity
    if (contains_pattern(content, "wget") || contains_pattern(content, "curl") ||
        contains_pattern(content, "http://")) {
        matched_rules.push_back("SuspiciousNetworkActivity");
        std::cout << "Matched rule: SuspiciousNetworkActivity (found network commands)\n";
    }

    // Check for suspicious script patterns
    if (contains_pattern(content, "eval(") || contains_pattern(content, "exec(") ||
        contains_pattern(content, "system(")) {
        matched_rules.push_back("SuspiciousScript");
        std::cout << "Matched rule: SuspiciousScript (found script execution)\n";
    }

    // Print summary
    if (!matched_rules.empty()) {
        std::cout << "\nSummary: Found " << matched_rules.size() << " matches: ";
        for (size_t i = 0; i < matched_rules.size(); i++) {
            std::cout << matched_rules[i];
            if (i < matched_rules.size() - 1) {
                std::cout << ", ";
            }
        }
        std::cout << "\n";
    } else {
        std::cout << "\nSummary: No matches found\n";
    }

    return 0;
}
