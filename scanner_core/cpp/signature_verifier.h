#ifndef SIGNATURE_VERIFIER_H
#define SIGNATURE_VERIFIER_H

#include "shared_utils.h"

class SignatureVerifier {
public:
    SignatureVerifier();
    ~SignatureVerifier();
    
    // Verify digital signature of a file
    SignatureResult verify_signature(const std::string& file_path);
    
    // Verify certificate
    std::string verify_certificate(const std::string& cert_path);
    
    // Check if certificate is valid
    bool is_certificate_valid(const std::string& cert_path);
    
    // Get certificate information
    std::map<std::string, std::string> get_certificate_info(const std::string& cert_path);
    
private:
    // Check if file is signed
    bool is_file_signed(const std::string& file_path);
    
    // Extract certificate from signed file
    std::string extract_certificate(const std::string& file_path);
    
    // Verify certificate chain
    bool verify_certificate_chain(const std::string& cert_path);
    
    // Check certificate revocation
    bool check_certificate_revocation(const std::string& cert_path);
    
    // Get certificate validity period
    std::pair<std::string, std::string> get_certificate_validity(const std::string& cert_path);
};

#endif // SIGNATURE_VERIFIER_H
