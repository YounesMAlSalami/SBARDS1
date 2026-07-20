#include "permission_checker.h"

PermissionChecker::PermissionChecker() {
    // Constructor
}

PermissionChecker::~PermissionChecker() {
    // Destructor
}

PermissionCheckResult PermissionChecker::check_permissions(const std::string& file_path) {
    PermissionCheckResult result;
    result.file_path = file_path;
    
    // Get file permissions
    result.permissions = PlatformUtil::get_permissions(file_path);
    
    // Check for special permissions
    PlatformUtil::check_special_permissions(file_path, result.has_suid_bit, result.has_sgid_bit);
    
    // Check if file is world-writable
    result.is_world_writable = is_world_writable(result.permissions);
    
    // Check if file is world-readable
    result.is_world_readable = is_world_readable(result.permissions);
    
    // Check if file is executable
    result.is_executable = is_executable(result.permissions);
    
    // Check if file requires admin privileges
    result.requires_admin = PlatformUtil::requires_admin_privileges(file_path);
    
    // Check if file is protected system file
    result.is_protected_system_file = PlatformUtil::is_protected_system_file(file_path);
    
    // Get recommendation
    result.recommendation = get_recommendation(result);
    
    return result;
}

bool PermissionChecker::has_suspicious_permissions(const std::string& permissions) {
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

bool PermissionChecker::is_world_writable(const std::string& permissions) {
    return permissions[7] == 'w';
}

bool PermissionChecker::is_world_readable(const std::string& permissions) {
    return permissions[6] == 'r';
}

bool PermissionChecker::is_executable(const std::string& permissions) {
    return permissions[2] == 'x' || permissions[5] == 'x' || permissions[8] == 'x';
}

bool PermissionChecker::is_in_system_directory(const std::string& file_path) {
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

std::string PermissionChecker::get_recommendation(const PermissionCheckResult& result) {
    // Check for suspicious permissions
    if (has_suspicious_permissions(result.permissions)) {
        return "Suspicious permissions detected. Consider reviewing file permissions.";
    }
    
    // Check for SUID/SGID bits
    if (result.has_suid_bit || result.has_sgid_bit) {
        return "Special permissions (SUID/SGID) detected. Review for security implications.";
    }
    
    // Check if file is world-writable and executable
    if (result.is_world_writable && result.is_executable) {
        return "File is world-writable and executable. This is a security risk.";
    }
    
    // Check if file is in system directory
    if (is_in_system_directory(result.file_path)) {
        return "File is in system directory. Ensure it is a legitimate system file.";
    }
    
    // Check if file requires admin privileges
    if (result.requires_admin) {
        return "File requires administrative privileges to access.";
    }
    
    // Check if file is protected system file
    if (result.is_protected_system_file) {
        return "File is a protected system file. Exercise caution when modifying.";
    }
    
    return "No permission issues detected.";
}
