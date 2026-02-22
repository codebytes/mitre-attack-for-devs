"""
MITRE ATT&CK T1565 - Data Manipulation: Integrity Verification

Data manipulation attacks involve unauthorized modification of data to compromise
integrity. This module demonstrates defensive measures to detect and prevent tampering.

Defenses implemented:
- HMAC-based record integrity verification
- Change audit trails with tamper-evident logging
- Modification velocity monitoring (detect mass changes)
- Field-level change tracking
- Cryptographic signatures for critical data

Educational purpose: Shows how to detect unauthorized data modifications and
maintain data integrity in the face of insider threats or compromised systems.
"""

import hmac
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict


class DataIntegrityManager:
    """
    Manages data integrity using HMAC signatures and audit trails.
    
    Defends against T1565 (Data Manipulation) by:
    - Signing records with HMAC for integrity verification
    - Tracking all data modifications in tamper-evident audit log
    - Detecting unusual modification patterns
    - Monitoring field-level changes
    """
    
    def __init__(self, secret_key: str):
        """
        Initialize the integrity manager.
        
        Args:
            secret_key: Secret key for HMAC signing (keep secure!)
        """
        self.secret_key = secret_key.encode()
        
        # Audit trail: [(timestamp, user, record_id, field, old_value, new_value, signature), ...]
        self.audit_trail: List[Tuple[float, str, str, str, Any, Any, str]] = []
        
        # Change velocity tracking: {user: [(timestamp, record_id), ...]}
        self.user_modifications: Dict[str, List[Tuple[float, str]]] = defaultdict(list)
        
        # Field sensitivity levels (higher = more sensitive)
        self.field_sensitivity = {
            "balance": 10,
            "salary": 10,
            "role": 9,
            "permissions": 9,
            "status": 8,
            "email": 7,
            "name": 5,
            "description": 3
        }
        
        # Alert thresholds
        self.mass_modification_threshold = 10  # changes in short time
        self.mass_modification_window = 60  # seconds
        self.high_value_change_threshold = 1000.0
    
    def _compute_signature(self, record_id: str, data: Dict) -> str:
        """Compute HMAC signature for a record."""
        # Create canonical representation of data
        canonical = json.dumps(data, sort_keys=True)
        message = f"{record_id}:{canonical}".encode()
        
        signature = hmac.new(
            self.secret_key,
            message,
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def sign_record(self, record_id: str, data: Dict) -> Dict:
        """
        Sign a record with HMAC signature for integrity verification.
        
        Args:
            record_id: Unique identifier for the record
            data: Record data to sign
        
        Returns:
            Record with '_signature' field added
        """
        data_copy = data.copy()
        
        # Remove signature field if present
        data_copy.pop('_signature', None)
        
        # Compute signature
        signature = self._compute_signature(record_id, data_copy)
        
        # Add signature to record
        data_copy['_signature'] = signature
        
        return data_copy
    
    def verify_record(self, record_id: str, data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Verify the integrity of a signed record.
        
        Args:
            record_id: Unique identifier for the record
            data: Record data to verify
        
        Returns:
            Tuple of (is_valid, reason)
        """
        if '_signature' not in data:
            return False, "No signature found - record may have been tampered with"
        
        stored_signature = data['_signature']
        
        # Create copy without signature
        data_copy = data.copy()
        data_copy.pop('_signature', None)
        
        # Compute expected signature
        expected_signature = self._compute_signature(record_id, data_copy)
        
        # Constant-time comparison
        is_valid = hmac.compare_digest(stored_signature, expected_signature)
        
        if not is_valid:
            return False, "Signature mismatch - record has been tampered with (T1565)"
        
        return True, "Record integrity verified"
    
    def record_change(
        self,
        user: str,
        record_id: str,
        field: str,
        old_value: Any,
        new_value: Any
    ) -> Tuple[bool, str, List[str]]:
        """
        Record a data change in the audit trail and check for anomalies.
        
        Args:
            user: User making the change
            record_id: Record being modified
            field: Field being changed
            old_value: Previous value
            new_value: New value
        
        Returns:
            Tuple of (allowed, reason, alerts)
        """
        current_time = time.time()
        alerts = []
        
        # Create audit entry with signature
        audit_entry = (current_time, user, record_id, field, old_value, new_value)
        audit_signature = hmac.new(
            self.secret_key,
            json.dumps(audit_entry).encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Store audit entry with signature
        self.audit_trail.append((*audit_entry, audit_signature))
        
        # Track modification for velocity analysis
        self.user_modifications[user].append((current_time, record_id))
        
        # Check 1: Mass modification detection
        recent_changes = [
            (ts, rid) for ts, rid in self.user_modifications[user]
            if current_time - ts <= self.mass_modification_window
        ]
        
        if len(recent_changes) >= self.mass_modification_threshold:
            alerts.append(
                f"ALERT (T1565): Mass modification detected! User {user} modified "
                f"{len(recent_changes)} records in {self.mass_modification_window}s"
            )
        
        # Check 2: High-value field changes
        field_sensitivity = self.field_sensitivity.get(field, 1)
        if field_sensitivity >= 8:
            alerts.append(
                f"WARNING (T1565): High-sensitivity field '{field}' modified by {user}"
            )
        
        # Check 3: Suspicious value changes (e.g., large balance increases)
        if field in ["balance", "salary"] and isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
            change_amount = abs(new_value - old_value)
            if change_amount >= self.high_value_change_threshold:
                alerts.append(
                    f"ALERT (T1565): Large value change detected! {field}: "
                    f"{old_value} → {new_value} (Δ{change_amount})"
                )
        
        # Check 4: Multiple fields modified on same record (potential data corruption)
        recent_record_changes = [
            (ts, fld) for ts, user_id, rec_id, fld, _, _, _ in self.audit_trail[-20:]
            if rec_id == record_id and current_time - ts <= 10
        ]
        
        if len(recent_record_changes) >= 5:
            alerts.append(
                f"WARNING (T1565): Multiple rapid changes to record {record_id}"
            )
        
        # Determine if change should be allowed
        allowed = True
        reason = "Change recorded in audit trail"
        
        # Block if critical alert detected
        for alert in alerts:
            if "ALERT" in alert and "Mass modification" in alert:
                allowed = False
                reason = "BLOCKED: Mass modification pattern detected (T1565)"
                break
        
        return allowed, reason, alerts
    
    def verify_audit_trail(self) -> Tuple[bool, List[str]]:
        """
        Verify the integrity of the audit trail.
        
        Returns:
            Tuple of (is_valid, issues)
        """
        issues = []
        
        for i, entry in enumerate(self.audit_trail):
            if len(entry) != 7:
                issues.append(f"Entry {i}: Malformed audit entry")
                continue
            
            timestamp, user, record_id, field, old_val, new_val, signature = entry
            
            # Re-compute signature
            audit_entry = (timestamp, user, record_id, field, old_val, new_val)
            expected_signature = hmac.new(
                self.secret_key,
                json.dumps(audit_entry).encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                issues.append(
                    f"Entry {i}: Audit trail tampering detected! (T1565) "
                    f"Record: {record_id}, User: {user}"
                )
        
        is_valid = len(issues) == 0
        
        return is_valid, issues
    
    def get_change_report(self, user: Optional[str] = None) -> Dict:
        """Generate change statistics report."""
        current_time = time.time()
        
        if user:
            changes = [
                entry for entry in self.audit_trail
                if entry[1] == user
            ]
        else:
            changes = self.audit_trail
        
        # Count changes by user
        changes_by_user = defaultdict(int)
        for entry in changes:
            changes_by_user[entry[1]] += 1
        
        # Count changes by field
        changes_by_field = defaultdict(int)
        for entry in changes:
            changes_by_field[entry[3]] += 1
        
        # Find recent high-velocity users
        high_velocity_users = []
        for username, modifications in self.user_modifications.items():
            recent = [
                ts for ts, _ in modifications
                if current_time - ts <= 300  # Last 5 minutes
            ]
            if len(recent) >= 5:
                high_velocity_users.append((username, len(recent)))
        
        return {
            "total_changes": len(changes),
            "changes_by_user": dict(sorted(changes_by_user.items(), key=lambda x: x[1], reverse=True)),
            "changes_by_field": dict(sorted(changes_by_field.items(), key=lambda x: x[1], reverse=True)),
            "high_velocity_users": sorted(high_velocity_users, key=lambda x: x[1], reverse=True),
            "audit_trail_size": len(self.audit_trail)
        }


# =============================================================================
# VULNERABLE IMPLEMENTATION (DO NOT USE IN PRODUCTION)
# =============================================================================

def vulnerable_update_record(record_id: str, data: Dict) -> Dict:
    """
    VULNERABLE: Direct data modification with no integrity checks.
    
    Issues:
    - No integrity verification
    - No audit trail
    - No change monitoring
    - Attacker can modify data undetected
    
    ATT&CK T1565: Attacker can tamper with data silently.
    """
    # Just update the data - no verification or logging
    return data


# =============================================================================
# DEMONSTRATION
# =============================================================================

def simulate_normal_operations(manager: DataIntegrityManager) -> None:
    """Simulate normal data operations."""
    print("\n--- Normal Operations ---")
    
    # Create and sign a record
    record_id = "user_12345"
    user_data = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "balance": 1000.0,
        "role": "user"
    }
    
    signed_record = manager.sign_record(record_id, user_data)
    print(f"Created record: {record_id}")
    
    # Verify integrity
    is_valid, reason = manager.verify_record(record_id, signed_record)
    print(f"Integrity check: {reason}")
    
    # Record a normal change
    allowed, reason, alerts = manager.record_change(
        user="admin",
        record_id=record_id,
        field="email",
        old_value="alice@example.com",
        new_value="alice.smith@example.com"
    )
    print(f"Email update: {reason}")


def simulate_tampering_attempt(manager: DataIntegrityManager) -> None:
    """
    Simulate T1565 attack: Attacker tries to modify data without proper authorization.
    """
    print("\n--- Simulating Data Tampering Attack (T1565) ---")
    
    # Create legitimate record
    record_id = "account_999"
    account_data = {
        "account_number": "999",
        "balance": 5000.0,
        "owner": "Bob Jones"
    }
    
    signed_record = manager.sign_record(record_id, account_data)
    print(f"Original balance: ${account_data['balance']}")
    
    # Attacker tampers with balance
    tampered_record = signed_record.copy()
    tampered_record['balance'] = 50000.0  # Attacker adds a zero!
    
    print(f"Attacker changes balance to: ${tampered_record['balance']}")
    
    # Verify integrity (should fail)
    is_valid, reason = manager.verify_record(record_id, tampered_record)
    print(f"Integrity check result: {reason}")


def simulate_mass_modification_attack(manager: DataIntegrityManager) -> None:
    """
    Simulate T1565 attack: Attacker performs mass data modification.
    """
    print("\n--- Simulating Mass Modification Attack (T1565) ---")
    
    attacker = "compromised_admin"
    
    # Attacker tries to modify many records quickly
    for i in range(15):
        record_id = f"record_{i}"
        allowed, reason, alerts = manager.record_change(
            user=attacker,
            record_id=record_id,
            field="status",
            old_value="active",
            new_value="deleted"
        )
        
        if not allowed:
            print(f"  Attempt {i + 1}: BLOCKED!")
            print(f"    Reason: {reason}")
            break
        
        if alerts:
            for alert in alerts:
                print(f"    {alert}")
            if not allowed:
                break
        
        if i % 5 == 4:
            print(f"  Modified {i + 1} records so far...")


def simulate_high_value_fraud(manager: DataIntegrityManager) -> None:
    """
    Simulate T1565 attack: Attacker modifies high-value fields.
    """
    print("\n--- Simulating High-Value Field Modification (T1565) ---")
    
    allowed, reason, alerts = manager.record_change(
        user="insider_threat",
        record_id="salary_database_001",
        field="salary",
        old_value=75000.0,
        new_value=175000.0
    )
    
    print(f"Salary modification: {reason}")
    if alerts:
        for alert in alerts:
            print(f"  {alert}")


def simulate_audit_trail_tampering(manager: DataIntegrityManager) -> None:
    """
    Simulate T1565 attack: Attacker tries to modify audit trail.
    """
    print("\n--- Simulating Audit Trail Tampering (T1565) ---")
    
    # Add some legitimate entries
    manager.record_change("user1", "rec1", "status", "active", "inactive")
    manager.record_change("user2", "rec2", "balance", 100, 200)
    
    print("Audit trail created with 2 entries")
    
    # Attacker tries to tamper with audit trail
    if len(manager.audit_trail) > 0:
        print("Attacker attempts to modify audit entry...")
        original_entry = manager.audit_trail[0]
        
        # Tamper with the entry (change user)
        tampered_entry = (
            original_entry[0],  # timestamp
            "attacker",  # changed user
            original_entry[2],  # record_id
            original_entry[3],  # field
            original_entry[4],  # old_value
            original_entry[5],  # new_value
            original_entry[6]   # signature (now invalid)
        )
        
        manager.audit_trail[0] = tampered_entry
    
    # Verify audit trail
    is_valid, issues = manager.verify_audit_trail()
    
    if is_valid:
        print("  Audit trail is valid")
    else:
        print("  Audit trail tampering detected!")
        for issue in issues:
            print(f"    {issue}")


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1565 - Data Manipulation: Integrity Verification")
    print("=" * 70)
    print("\nThis demo shows how to detect and prevent unauthorized data")
    print("modifications using cryptographic integrity verification and")
    print("behavioral monitoring.")
    
    # Create integrity manager with secret key
    secret_key = "super_secret_integrity_key_DO_NOT_HARDCODE"
    manager = DataIntegrityManager(secret_key)
    
    # Run simulations
    simulate_normal_operations(manager)
    simulate_tampering_attempt(manager)
    simulate_mass_modification_attack(manager)
    simulate_high_value_fraud(manager)
    simulate_audit_trail_tampering(manager)
    
    # Generate change report
    print("\n--- Change Report ---")
    report = manager.get_change_report()
    print(f"Total changes: {report['total_changes']}")
    print(f"Changes by user: {report['changes_by_user']}")
    
    if report['high_velocity_users']:
        print("\nHigh-velocity users (potential mass modification):")
        for user, count in report['high_velocity_users']:
            print(f"  {user}: {count} changes in 5 minutes")
    
    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("- Use HMAC signatures to ensure data integrity")
    print("- Maintain tamper-evident audit trails")
    print("- Monitor for mass modification patterns")
    print("- Track high-sensitivity field changes")
    print("- Verify audit trail integrity regularly")
    print("- Alert on unusual data modification patterns")
    print("=" * 70)
