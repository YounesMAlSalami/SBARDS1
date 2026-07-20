// This is a test JavaScript file with suspicious patterns
// The scanner should detect these patterns and flag the file

// Suspicious eval function
function executeCode(code) {
    eval(code); // This should be detected as suspicious
}

// Suspicious URL
const maliciousUrl = "http://malicious.com/payload.php";

// Base64 encoded payload
const encodedPayload = "ZXZhbChhdG9iKCJhbGVydCgnWW91ciBzeXN0ZW0gaXMgaW5mZWN0ZWQnKSIpKTs=";

// Suspicious function to decode and execute
function decodeAndExecute() {
    const decoded = atob(encodedPayload);
    eval(decoded); // This should be detected as suspicious
}

// Suspicious system commands
function runCommand() {
    const cmd = "rm -rf /"; // This should be detected as suspicious
    system(cmd);
}

// Suspicious encryption function
function encryptFiles(path) {
    // This should be detected as suspicious
    console.log("Encrypting files at: " + path);
    // Simulated encryption code
}

// Suspicious decryption function
function decryptFiles(path, key) {
    // This should be detected as suspicious
    console.log("Decrypting files at: " + path + " with key: " + key);
    // Simulated decryption code
}

// Export functions
module.exports = {
    executeCode,
    decodeAndExecute,
    runCommand,
    encryptFiles,
    decryptFiles
};
