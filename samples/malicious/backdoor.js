// Malicious backdoor script (FOR TESTING ONLY - NOT ACTUALLY FUNCTIONAL)
// This is a simulated malicious JavaScript file for testing security tools

// Obfuscated function to establish reverse shell
function c2Connect() {
    var host = "malicious-backdoor.com";
    var port = 4444;
    
    console.log("[*] Attempting to establish connection to " + host + ":" + port);
    
    // This is just a simulation - no actual connection is made
    return {status: "connected", session: Math.random().toString(36).substring(2, 15)};
}

// Function to gather system information
function gatherSystemInfo() {
    var info = {
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        cookiesEnabled: navigator.cookieEnabled,
        localStorage: typeof(Storage) !== "undefined",
        screenWidth: screen.width,
        screenHeight: screen.height,
        location: window.location.href,
        referrer: document.referrer
    };
    
    console.log("[+] System information gathered");
    return info;
}

// Function to execute commands received from C2
function executeCommand(cmd) {
    console.log("[*] Executing command: " + cmd);
    
    // This is just a simulation - no actual commands are executed
    if (cmd.startsWith("download")) {
        console.log("[+] Downloading file from remote server...");
        return "File downloaded successfully";
    } else if (cmd.startsWith("upload")) {
        console.log("[+] Uploading local file to remote server...");
        return "File uploaded successfully";
    } else if (cmd.startsWith("exec")) {
        console.log("[+] Executing system command...");
        return "Command executed successfully";
    } else if (cmd.startsWith("keylog")) {
        console.log("[+] Starting keylogger...");
        return "Keylogger started";
    } else if (cmd.startsWith("screenshot")) {
        console.log("[+] Taking screenshot...");
        return "Screenshot taken and sent";
    } else if (cmd.startsWith("webcam")) {
        console.log("[+] Accessing webcam...");
        return "Webcam accessed and image sent";
    } else {
        return "Unknown command";
    }
}

// Function to establish persistence
function establishPersistence() {
    console.log("[*] Establishing persistence mechanisms");
    
    // This is just a simulation - no actual persistence is established
    console.log("[+] Added startup registry key");
    console.log("[+] Created scheduled task");
    console.log("[+] Installed service");
    console.log("[+] Added browser extension");
    
    return true;
}

// Function to evade detection
function evadeDetection() {
    console.log("[*] Implementing detection evasion techniques");
    
    // This is just a simulation - no actual evasion techniques are implemented
    console.log("[+] Checking for virtual environment");
    console.log("[+] Checking for debugging tools");
    console.log("[+] Implementing sleep techniques");
    console.log("[+] Encrypting communication");
    
    return true;
}

// Main function
function main() {
    console.log("MALICIOUS BACKDOOR SIMULATION STARTING");
    console.log("THIS IS A SIMULATION FOR TESTING SECURITY TOOLS");
    console.log("NO ACTUAL MALICIOUS ACTIONS WILL BE PERFORMED");
    console.log("-".repeat(60));
    
    // Evade detection
    evadeDetection();
    
    // Connect to C2 server
    var connection = c2Connect();
    console.log("[+] Connection established: " + JSON.stringify(connection));
    
    // Gather system information
    var sysInfo = gatherSystemInfo();
    console.log("[+] System info: " + JSON.stringify(sysInfo));
    
    // Establish persistence
    establishPersistence();
    
    // Simulate command execution
    var commands = ["download malware.exe", "exec whoami", "keylog start", "screenshot", "webcam capture"];
    for (var i = 0; i < commands.length; i++) {
        var result = executeCommand(commands[i]);
        console.log("[+] Result: " + result);
    }
    
    console.log("-".repeat(60));
    console.log("SIMULATION COMPLETE");
    console.log("THIS WAS A TEST - NO ACTUAL MALICIOUS ACTIONS WERE PERFORMED");
}

// Base64 encoded "evil" payload (just a string for testing)
var encodedPayload = "ZXZhbChmdW5jdGlvbihwLGEsYyxrLGUsZCl7ZT1mdW5jdGlvbihjKXtyZXR1cm4oYzxhPycnOmUocGFyc2VJbnQoYy9hKSkpKygoYz1jJWEpPjM1P1N0cmluZy5mcm9tQ2hhckNvZGUoYysyOSk6Yy50b1N0cmluZygzNikpfTtpZighJycucmVwbGFjZSgvXi8sU3RyaW5nKSl7d2hpbGUoYy0tKXtkW2UoYyldPWtbY118fGUoYyl9az1bZnVuY3Rpb24oZSl7cmV0dXJuIGRbZV19XTtlPWZ1bmN0aW9uKCl7cmV0dXJuJ1xcdysnfTtjPTF9O3doaWxlKGMtLSl7aWYoa1tjXSl7cD1wLnJlcGxhY2UobmV3IFJlZ0V4cCgnXFxiJytlKGMpKydcXGInLCdnJyksa1tjXSl9fXJldHVybiBwfSgnMiAxPXsiNSI6IjQgMyJ9OzYuNygxKTs4IDkoYSl7YS5hKCl9JyxbXSxbJ2InLCdvYmonLCd2YXInLCdwYXlsb2FkJywnbWFsaWNpb3VzJywnbmFtZScsJ2NvbnNvbGUnLCdsb2cnLCdmdW5jdGlvbiddKSk=";

// Simulate decoding and executing the payload
function decodeAndExecute() {
    var decoded = atob(encodedPayload);
    console.log("[*] Decoded payload: " + decoded);
    
    // This is just a simulation - no actual eval is performed
    console.log("[+] Executed decoded payload");
}

// Call the main function
main();

// Decode and execute the payload
decodeAndExecute();
