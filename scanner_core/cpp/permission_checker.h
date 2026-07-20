#ifndef PERMISSION_CHECKER_H
#define PERMISSION_CHECKER_H

#include "shared_utils.h"

// Structure to hold permission check results
struct PermissionCheckResult {
    std::string file_path;
    std::string permissions;
    bool has_suid_bit;
    bool has_sgid_bit;
    bool is_world_writable;
    bool is_world_readable;
    bool is_executable;
    bool requires_admin;
    bool is_protected_system_file;
    std::string recommendation;
};

class PermissionChecker {
public:
    PermissionChecker();
    ~PermissionChecker();
    
    // Check file permissions and return results
    PermissionCheckResult check_permissions(const std::string& file_path);
    
    // Check if file has suspicious permissions
    bool has_suspicious_permissions(const std::string& permissions);
    
    // Get recommendation based on permission check
    std::string get_recommendation(const PermissionCheckResult& result);
    
private:
    // Check if file is world-writable
    bool is_world_writable(const std::string& permissions);
    
    // Check if file is world-readable
    bool is_world_readable(const std::string& permissions);
    
    // Check if file is executable
    bool is_executable(const std::string& permissions);
    
    // Check if file is in system directory
    bool is_in_system_directory(const std::string& file_path);
};

#endif // PERMISSION_CHECKER_H
