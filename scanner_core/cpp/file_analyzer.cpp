#include "file_analyzer.h"
#include <regex>

FileAnalyzer::FileAnalyzer() {
    // Constructor
}

FileAnalyzer::~FileAnalyzer() {
    // Destructor
}

FileAnalysisResult FileAnalyzer::analyze_file(const std::string& file_path) {
    FileAnalysisResult result;
    result.file_path = file_path;
    
    // Get file information
    FileInfo file_info = FileUtil::get_file_info(file_path);
    result.is_binary = file_info.is_binary;
    result.file_type = file_info.file_type;
    result.file_size = file_info.file_size;
    result.permissions = file_info.permissions;
    result.has_suid_bit = file_info.has_suid_bit;
    result.has_sgid_bit = file_info.has_sgid_bit;
    
    // Check if file requires admin privileges
    result.requires_admin = PlatformUtil::requires_admin_privileges(file_path);
    result.is_protected_system_file = PlatformUtil::is_protected_system_file(file_path);
    
    // Check for suspicious patterns
    result.suspicious_patterns = check_suspicious_patterns(file_path);
    
    // Get recommendation
    result.recommendation = get_recommendation(result);
    
    return result;
}

std::vector<std::string> FileAnalyzer::check_suspicious_patterns(const std::string& file_path) {
    std::vector<std::string> patterns;
    
    try {
        // Check if file is binary
        if (FileUtil::is_binary_file(file_path)) {
            patterns = check_binary_file(file_path);
        } else {
            // Read file content
            std::string content = FileUtil::read_file(file_path);
            patterns = check_text_file(content);
            
            // Check for suspicious URLs
            std::vector<std::string> urls = check_suspicious_urls(content);
            patterns.insert(patterns.end(), urls.begin(), urls.end());
            
            // Check for suspicious commands
            std::vector<std::string> commands = check_suspicious_commands(content);
            patterns.insert(patterns.end(), commands.begin(), commands.end());
        }
    } catch (const std::exception& e) {
        std::cerr << "Error analyzing file: " << e.what() << std::endl;
    }
    
    return patterns;
}

std::vector<std::string> FileAnalyzer::check_text_file(const std::string& content) {
    std::vector<std::string> patterns;
    
    // Check for malicious patterns
    for (const auto& pattern : CommonPatterns::malicious_patterns) {
        if (SafeString::contains(content, pattern)) {
            patterns.push_back("Found suspicious pattern: " + pattern);
        }
    }
    
    return patterns;
}

std::vector<std::string> FileAnalyzer::check_binary_file(const std::string& file_path) {
    std::vector<std::string> patterns;
    
    // Read file as binary
    std::ifstream file(file_path, std::ios::binary);
    if (!file.is_open()) {
        return patterns;
    }
    
    // Read file content
    std::string content;
    char buffer[1024];
    while (file.read(buffer, sizeof(buffer))) {
        content.append(buffer, file.gcount());
    }
    content.append(buffer, file.gcount());
    file.close();
    
    // Check for malicious patterns in binary file
    for (const auto& pattern : CommonPatterns::malicious_patterns) {
        if (content.find(pattern) != std::string::npos) {
            patterns.push_back("Found suspicious pattern in binary: " + pattern);
        }
    }
    
    return patterns;
}

std::vector<std::string> FileAnalyzer::check_suspicious_urls(const std::string& content) {
    std::vector<std::string> suspicious_urls;
    
    // Regular expression for URLs
    std::regex url_regex("(http|https|ftp)://([\\w_-]+(?:(?:\\.[\\w_-]+)+))([\\w.,@?^=%&:/~+#-]*[\\w@?^=%&/~+#-])?");
    
    // Find all URLs in content
    auto words_begin = std::sregex_iterator(content.begin(), content.end(), url_regex);
    auto words_end = std::sregex_iterator();
    
    for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
        std::string url = i->str();
        
        // Check if URL is suspicious
        if (url.find("malicious") != std::string::npos || 
            url.find("hack") != std::string::npos || 
            url.find("exploit") != std::string::npos) {
            suspicious_urls.push_back("Found suspicious URL: " + url);
        }
    }
    
    return suspicious_urls;
}

std::vector<std::string> FileAnalyzer::check_suspicious_commands(const std::string& content) {
    std::vector<std::string> suspicious_commands;
    
    // List of suspicious commands
    std::vector<std::string> commands = {
        "system(", "exec(", "eval(", "shell_exec(", "passthru(", 
        "popen(", "proc_open(", "pcntl_exec(", "assert(", "preg_replace",
        "powershell", "cmd.exe", "cmd /c", "bash -i", "nc -e", "netcat",
        "chmod 777", "chmod +s", "wget", "curl", "base64 -d"
    };
    
    // Check for suspicious commands
    for (const auto& cmd : commands) {
        if (SafeString::contains(content, cmd)) {
            suspicious_commands.push_back("Found suspicious command: " + cmd);
        }
    }
    
    return suspicious_commands;
}

bool FileAnalyzer::has_suspicious_permissions(const std::string& permissions) {
    // Check for world-writable permissions
    if (permissions[7] == 'w') {
        return true;
    }
    
    // Check for no user read/write permissions but group/other permissions
    if (permissions[0] == '-' && permissions[1] == '-' && 
        (permissions[3] != '-' || permissions[4] != '-' || 
         permissions[6] != '-' || permissions[7] != '-')) {
        return true;
    }
    
    return false;
}

bool FileAnalyzer::is_potentially_malicious(const FileAnalysisResult& result) {
    // Check if file has suspicious patterns
    if (!result.suspicious_patterns.empty()) {
        return true;
    }
    
    // Check if file has suspicious permissions
    if (has_suspicious_permissions(result.permissions)) {
        return true;
    }
    
    // Check if file has SUID/SGID bits
    if (result.has_suid_bit || result.has_sgid_bit) {
        return true;
    }
    
    // Check if file has suspicious extension
    std::string file_path = result.file_path;
    std::transform(file_path.begin(), file_path.end(), file_path.begin(), ::tolower);
    
    for (const auto& ext : CommonPatterns::suspicious_extensions) {
        if (file_path.find(ext) != std::string::npos) {
            return true;
        }
    }
    
    return false;
}

std::string FileAnalyzer::get_recommendation(const FileAnalysisResult& result) {
    if (is_potentially_malicious(result)) {
        return "Quarantine";
    } else {
        return "Safe";
    }
}
