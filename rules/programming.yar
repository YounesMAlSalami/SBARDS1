rule SuspiciousProgrammingFile
{
    meta:
        description = "Detects suspicious patterns in programming files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // Suspicious functions in various programming languages
        // PHP
        $php_func1 = "eval(" nocase
        $php_func2 = "system(" nocase
        $php_func3 = "exec(" nocase
        $php_func4 = "shell_exec(" nocase
        $php_func5 = "passthru(" nocase
        $php_func6 = "popen(" nocase
        $php_func7 = "proc_open(" nocase
        $php_func8 = "base64_decode(" nocase
        $php_func9 = "create_function(" nocase
        $php_func10 = "assert(" nocase
        
        // JavaScript
        $js_func1 = "eval(" nocase
        $js_func2 = "Function(" nocase
        $js_func3 = "setTimeout(" nocase
        $js_func4 = "setInterval(" nocase
        $js_func5 = "document.write(" nocase
        $js_func6 = "fromCharCode" nocase
        $js_func7 = "atob(" nocase
        $js_func8 = "btoa(" nocase
        $js_func9 = "unescape(" nocase
        $js_func10 = "decodeURI(" nocase
        
        // Python
        $py_func1 = "exec(" nocase
        $py_func2 = "eval(" nocase
        $py_func3 = "os.system(" nocase
        $py_func4 = "subprocess.call(" nocase
        $py_func5 = "subprocess.Popen(" nocase
        $py_func6 = "subprocess.run(" nocase
        $py_func7 = "pickle.loads(" nocase
        $py_func8 = "yaml.load(" nocase
        $py_func9 = "base64.b64decode(" nocase
        $py_func10 = "__import__(" nocase
    
    condition:
        3 of ($php_func*) or 3 of ($js_func*) or 3 of ($py_func*)
}

rule ObfuscatedCode
{
    meta:
        description = "Detects obfuscated code in programming files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // Common obfuscation techniques
        $obf1 = "\\x" nocase
        $obf2 = "\\u00" nocase
        $obf3 = "\\141" nocase // Octal
        $obf4 = "base64" nocase
        $obf5 = "eval(" nocase
        $obf6 = "String.fromCharCode" nocase
        $obf7 = "unescape" nocase
        $obf8 = "decode" nocase
        $obf9 = "atob" nocase
        $obf10 = "btoa" nocase
        
        // Long strings that might be obfuscated code
        $long_string1 = /["'`][a-zA-Z0-9+\/=]{100,}["'`]/
        $long_string2 = /["'`][0-9a-fA-F\\x]{100,}["'`]/
    
    condition:
        4 of ($obf*) or any of ($long_string*)
}
