#include "shared_utils.h"

// Common patterns for scanning
const std::vector<std::string> CommonPatterns::malicious_patterns = {
    "malicious", "encrypt", "decrypt", "root", "passwd", "ssh", "base64_decode", 
    "eval", "system", "exec", "cmd|", "powershell", "wget", "curl", "http://malicious.com"
};

// Suspicious file extensions
const std::vector<std::string> CommonPatterns::suspicious_extensions = {
    ".exe", ".dll", ".sys", ".bat", ".msi", ".scr", ".vbs", ".js", ".ps1"
};

// File type mapping
const std::map<std::string, std::string> CommonPatterns::file_type_map = {
    {"exe", "Windows Executable (.exe)"},
    {"dll", "Windows Dynamic Library (.dll)"},
    {"sys", "Windows System Driver (.sys)"},
    {"bat", "Windows Batch Script (.bat)"},
    {"msi", "Windows Installer (.msi)"},
    {"mp3", "Audio File (.mp3)"},
    {"wav", "Audio File (.wav)"},
    {"flac", "Audio File (.flac)"},
    {"mp4", "Video File (.mp4)"},
    {"avi", "Video File (.avi)"},
    {"mkv", "Video File (.mkv)"},
    {"jpg", "Image File (.jpg)"},
    {"png", "Image File (.png)"},
    {"gif", "Image File (.gif)"},
    {"bmp", "Image File (.bmp)"},
    {"txt", "Text File (.txt)"},
    {"docx", "Microsoft Word Document (.docx)"},
    {"xlsx", "Microsoft Excel Spreadsheet (.xlsx)"},
    {"pptx", "Microsoft PowerPoint Presentation (.pptx)"},
    {"pdf", "PDF Document (.pdf)"},
    {"csv", "CSV File (.csv)"},
    {"zip", "ZIP Archive (.zip)"},
    {"rar", "RAR Archive (.rar)"},
    {"7z", "7-Zip Archive (.7z)"},
    {"iso", "ISO Image (.iso)"},
    {"html", "HTML File (.html)"},
    {"css", "CSS File (.css)"},
    {"js", "JavaScript File (.js)"},
    {"py", "Python Script (.py)"},
    {"cpp", "C++ Source File (.cpp)"},
    {"c", "C Source File (.c)"},
    {"java", "Java Source File (.java)"},
    {"sql", "SQL Database File (.sql)"},
    {"sav", "Game Save File (.sav)"},
    {"pak", "Game Asset Package (.pak)"},
    {"asset", "Unity Game Asset (.asset)"},
    {"cfg", "Game Configuration (.cfg)"},
    {"torrent", "BitTorrent File (.torrent)"},
    {"log", "Log File (.log)"},
    {"pem", "PEM Certificate (.pem)"},
    {"crt", "SSL Certificate (.crt)"},
    {"key", "Private Key File (.key)"}
};

// Convert string to lowercase
std::string SafeString::to_lowercase(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), 
                  [](unsigned char c){ return std::tolower(c); });
    return result;
}

// Convert string to uppercase
std::string SafeString::to_uppercase(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), 
                  [](unsigned char c){ return std::toupper(c); });
    return result;
}

// Check if string contains substring (case-insensitive)
bool SafeString::contains(const std::string& haystack, const std::string& needle) {
    std::string h = to_lowercase(haystack);
    std::string n = to_lowercase(needle);
    return h.find(n) != std::string::npos;
}

// Tokenize string by delimiter
std::vector<std::string> SafeString::tokenize(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;
    
    while (std::getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    
    return tokens;
}

// Check if file is binary
bool FileUtil::is_binary_file(const std::string& file_path) {
    std::ifstream file(file_path, std::ios::binary);
    if (!file.is_open()) {
        return false;
    }

    char buffer[1024];
    file.read(buffer, sizeof(buffer));
    std::streamsize bytes_read = file.gcount();
    
    for (std::streamsize i = 0; i < bytes_read; i++) {
        if (buffer[i] == '\0') {
            file.close();
            return true;
        }
    }
    
    file.close();
    return false;
}

// Determine file type
std::string FileUtil::determine_file_type(const std::string& file_path) {
    std::string file_ext = file_path;
    
    // Extract extension
    size_t dot_pos = file_ext.find_last_of(".");
    if (dot_pos != std::string::npos) {
        file_ext = file_ext.substr(dot_pos + 1);
    } else {
        file_ext = "";
    }

    // Convert to lowercase for comparison
    std::string lower_ext = SafeString::to_lowercase(file_ext);
    
    auto it = CommonPatterns::file_type_map.find(lower_ext);
    if (it != CommonPatterns::file_type_map.end()) {
        return it->second;
    }
    
    // Check for binary files by content
    if (is_binary_file(file_path)) {
        std::ifstream file(file_path, std::ios::binary);
        if (!file.is_open()) {
            return "Unknown File";
        }

        char header[8];
        file.read(header, sizeof(header));
        file.close();

        // Check for PE files (Windows Executables)
        if (header[0] == 'M' && header[1] == 'Z') {
            return "Windows Executable (.exe)";
        }
        
        // Check for ELF files (Linux Executables)
        if (header[0] == '\x7f' && header[1] == 'E' && header[2] == 'L' && header[3] == 'F') {
            return "ELF Executable (.elf)";
        }

        return "Unknown Binary File";
    }

    return "Text File (.txt)";
}

// Get detailed file information
FileInfo FileUtil::get_file_info(const std::string& file_path) {
    FileInfo info;
    info.file_path = file_path;
    info.file_type = determine_file_type(file_path);
    info.is_binary = is_binary_file(file_path);
    info.permissions = PlatformUtil::get_permissions(file_path);
    PlatformUtil::check_special_permissions(file_path, info.has_suid_bit, info.has_sgid_bit);
    
    // Get file size
    std::ifstream file(file_path, std::ifstream::ate | std::ifstream::binary);
    if (file.is_open()) {
        info.file_size = file.tellg();
        file.close();
    } else {
        info.file_size = -1;
    }
    
    // Get last modified time
    auto ftime = fs::last_write_time(file_path);
    auto sctp = std::chrono::time_point_cast<std::chrono::system_clock::duration>(ftime - fs::file_time_type::clock::now() + std::chrono::system_clock::now());
    std::time_t cftime = std::chrono::system_clock::to_time_t(sctp);
    info.last_modified = std::ctime(&cftime);
    
    return info;
}

// Read file content
std::string FileUtil::read_file(const std::string& file_path) {
    std::ifstream file(file_path, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + file_path);
    }
    
    std::ostringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

// Write file content
bool FileUtil::write_file(const std::string& file_path, const std::string& content) {
    std::ofstream file(file_path, std::ios::binary);
    if (!file.is_open()) {
        return false;
    }
    
    file << content;
    file.close();
    return true;
}

// Calculate SHA256 hash (mock implementation)
std::string SecurityUtil::calculate_sha256(const std::string& file_path) {
    // Mock implementation for demonstration
    return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
}

// Calculate MD5 hash (mock implementation)
std::string SecurityUtil::calculate_md5(const std::string& file_path) {
    // Mock implementation for demonstration
    return "d41d8cd98f00b204e9800998ecf8427e";
}

// Check signature (mock implementation)
bool SecurityUtil::check_signature(const std::string& cert_path, const std::string& data_path) {
    // Mock implementation for demonstration
    return true;
}

// Get file permissions
std::string PlatformUtil::get_permissions(const std::string& file_path) {
#ifdef _WIN32
    // Windows implementation
    DWORD attributes = GetFileAttributesA(file_path.c_str());
    if (attributes == INVALID_FILE_ATTRIBUTES) {
        return "---------";
    }
    
    std::string permissions = "---------";
    if (!(attributes & FILE_ATTRIBUTE_READONLY)) {
        permissions[1] = 'w'; // User write
    }
    permissions[0] = 'r'; // User read
    permissions[2] = 'x'; // User execute
    
    // Group permissions (same as user in Windows)
    permissions[3] = 'r'; // Group read
    if (!(attributes & FILE_ATTRIBUTE_READONLY)) {
        permissions[4] = 'w'; // Group write
    }
    permissions[5] = 'x'; // Group execute
    
    // Other permissions (same as user in Windows)
    permissions[6] = 'r'; // Other read
    if (!(attributes & FILE_ATTRIBUTE_READONLY)) {
        permissions[7] = 'w'; // Other write
    }
    permissions[8] = 'x'; // Other execute
    
    return permissions;
#else
    // Unix implementation
    struct stat file_stat;
    if (stat(file_path.c_str(), &file_stat) != 0) {
        return "---------";
    }

    char permissions[10];
    snprintf(permissions, sizeof(permissions), "%c%c%c%c%c%c%c%c%c",
        (file_stat.st_mode & S_IRUSR) ? 'r' : '-',
        (file_stat.st_mode & S_IWUSR) ? 'w' : '-',
        (file_stat.st_mode & S_IXUSR) ? 'x' : '-',
        (file_stat.st_mode & S_IRGRP) ? 'r' : '-',
        (file_stat.st_mode & S_IWGRP) ? 'w' : '-',
        (file_stat.st_mode & S_IXGRP) ? 'x' : '-',
        (file_stat.st_mode & S_IROTH) ? 'r' : '-',
        (file_stat.st_mode & S_IWOTH) ? 'w' : '-',
        (file_stat.st_mode & S_IXOTH) ? 'x' : '-');
    
    return std::string(permissions);
#endif
}

// Check for special permissions
void PlatformUtil::check_special_permissions(const std::string& file_path, bool& suid, bool& sgid) {
#ifdef _WIN32
    // Windows doesn't have SUID/SGID bits
    suid = false;
    sgid = false;
#else
    // Unix implementation
    struct stat file_stat;
    if (stat(file_path.c_str(), &file_stat) != 0) {
        suid = false;
        sgid = false;
        return;
    }

    suid = (file_stat.st_mode & S_ISUID) != 0;
    sgid = (file_stat.st_mode & S_ISGID) != 0;
#endif
}

// Check if file requires admin privileges
bool PlatformUtil::requires_admin_privileges(const std::string& file_path) {
    // Check if file is in sensitive system directory
    std::string path = fs::absolute(file_path).string();
    std::transform(path.begin(), path.end(), path.begin(), ::tolower);
    
#ifdef _WIN32
    std::vector<std::string> system_dirs = {"\\windows\\system32", "\\windows\\system", "\\windows"};
#else
    std::vector<std::string> system_dirs = {"/system32", "/sys", "/bin", "/sbin", "/usr/bin", "/usr/sbin"};
#endif

    for (const auto& dir : system_dirs) {
        if (path.find(dir) != std::string::npos) {
            return true;
        }
    }
    
    return false;
}

// Check if file is protected system file
bool PlatformUtil::is_protected_system_file(const std::string& file_path) {
    return requires_admin_privileges(file_path);
}
