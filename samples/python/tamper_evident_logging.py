"""
MITRE ATT&CK T1070 - Indicator Removal on Host

Attackers often try to cover their tracks by deleting, modifying, or 
clearing logs. Tamper-evident logging makes it cryptographically detectable
when logs have been modified or deleted.

This module demonstrates:
- Tamper-evident log chain using cryptographic hashes
- Each log entry includes the hash of the previous entry
- Verification function to detect tampering

Educational purpose: Shows how to make logs tamper-evident to detect T1070 attacks.
Reference: https://attack.mitre.org/techniques/T1070/
"""

import hashlib
import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path


class TamperEvidentLogger:
    """
    Implements tamper-evident logging to defend against T1070 (Indicator Removal).
    
    Each log entry contains:
    - Timestamp
    - Log message/data
    - Hash of the previous entry
    - Hash of current entry (includes all above + previous hash)
    
    This creates a chain where tampering with any entry breaks the chain,
    making attacks detectable.
    """
    
    def __init__(self, log_file: str, secret_key: Optional[str] = None):
        """
        Initialize the tamper-evident logger.
        
        Args:
            log_file: Path to the log file
            secret_key: Optional secret for HMAC (makes tampering harder)
        """
        self.log_file = Path(log_file)
        self.secret_key = secret_key or ""
        self.entries: List[Dict] = []
        self.last_hash = "GENESIS"  # Genesis block for the chain
        
        # Load existing entries if file exists
        if self.log_file.exists():
            self._load_entries()
    
    def _calculate_hash(self, entry_data: Dict) -> str:
        """
        Calculate cryptographic hash of an entry.
        
        Uses SHA-256 with optional secret key for additional security.
        The hash includes:
        - Previous entry's hash (creates the chain)
        - Current timestamp
        - Current log data
        - Secret key (if provided)
        """
        # Create a canonical representation of the entry
        hash_input = json.dumps({
            'previous_hash': entry_data.get('previous_hash', ''),
            'timestamp': entry_data['timestamp'],
            'sequence': entry_data['sequence'],
            'level': entry_data['level'],
            'message': entry_data['message'],
            'data': entry_data.get('data', {}),
            'secret': self.secret_key  # Include secret in hash
        }, sort_keys=True)
        
        # Calculate SHA-256 hash
        hash_obj = hashlib.sha256(hash_input.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def _load_entries(self):
        """Load existing log entries from file."""
        try:
            with open(self.log_file, 'r') as f:
                self.entries = [json.loads(line) for line in f if line.strip()]
            
            if self.entries:
                self.last_hash = self.entries[-1]['hash']
                
        except Exception as e:
            print(f"Warning: Could not load existing log: {e}")
            self.entries = []
    
    def _append_to_file(self, entry: Dict):
        """Append entry to log file (append-only for security)."""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"Error writing to log: {e}")
    
    def log(self, level: str, message: str, data: Optional[Dict] = None) -> Dict:
        """
        Create a tamper-evident log entry.
        
        Args:
            level: Log level (INFO, WARNING, ERROR, SECURITY, etc.)
            message: Log message
            data: Optional additional data to log
            
        Returns:
            The created log entry
        """
        # Create entry with previous hash (chain link)
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'sequence': len(self.entries) + 1,
            'level': level,
            'message': message,
            'data': data or {},
            'previous_hash': self.last_hash
        }
        
        # Calculate hash of this entry
        entry['hash'] = self._calculate_hash(entry)
        
        # Update last hash for next entry
        self.last_hash = entry['hash']
        
        # Store and persist
        self.entries.append(entry)
        self._append_to_file(entry)
        
        return entry
    
    def verify_integrity(self) -> Tuple[bool, List[str]]:
        """
        Verify the integrity of the log chain.
        
        This detects:
        - Modified log entries (hash mismatch)
        - Deleted log entries (broken chain)
        - Reordered log entries (sequence mismatch)
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        if not self.entries:
            return True, []
        
        # Verify first entry connects to genesis
        if self.entries[0]['previous_hash'] != "GENESIS":
            issues.append(
                f"Entry 1: Invalid genesis link. Expected 'GENESIS', "
                f"got '{self.entries[0]['previous_hash']}'"
            )
        
        # Verify each entry in the chain
        for i, entry in enumerate(self.entries, 1):
            # Check sequence number
            if entry['sequence'] != i:
                issues.append(
                    f"Entry {i}: Sequence mismatch. Expected {i}, "
                    f"got {entry['sequence']}"
                )
            
            # Recalculate hash and verify it matches
            stored_hash = entry['hash']
            
            # Temporarily remove hash for recalculation
            entry_copy = entry.copy()
            del entry_copy['hash']
            
            calculated_hash = self._calculate_hash(entry_copy)
            
            if calculated_hash != stored_hash:
                issues.append(
                    f"Entry {i}: Hash mismatch (entry was modified). "
                    f"Expected {stored_hash[:16]}..., got {calculated_hash[:16]}..."
                )
            
            # Verify chain link (except for first entry)
            if i > 1:
                expected_previous = self.entries[i - 2]['hash']
                actual_previous = entry['previous_hash']
                
                if actual_previous != expected_previous:
                    issues.append(
                        f"Entry {i}: Broken chain link. "
                        f"Previous hash should be {expected_previous[:16]}..., "
                        f"got {actual_previous[:16]}..."
                    )
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def get_entries(
        self, 
        level: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve log entries with optional filtering.
        
        Args:
            level: Filter by log level
            start_time: Filter entries after this timestamp
            end_time: Filter entries before this timestamp
            
        Returns:
            Filtered log entries
        """
        filtered = self.entries
        
        if level:
            filtered = [e for e in filtered if e['level'] == level]
        
        if start_time:
            filtered = [e for e in filtered if e['timestamp'] >= start_time]
        
        if end_time:
            filtered = [e for e in filtered if e['timestamp'] <= end_time]
        
        return filtered
    
    def export_for_archival(self, output_file: str):
        """
        Export logs with verification hashes for secure archival.
        
        Defense against T1070: Logs should be archived to secure, 
        append-only storage (e.g., WORM drives, immutable cloud storage)
        """
        with open(output_file, 'w') as f:
            # Write metadata
            metadata = {
                'export_time': datetime.utcnow().isoformat(),
                'total_entries': len(self.entries),
                'first_entry': self.entries[0]['timestamp'] if self.entries else None,
                'last_entry': self.entries[-1]['timestamp'] if self.entries else None,
                'chain_root': "GENESIS",
                'chain_tip': self.last_hash
            }
            f.write("=== TAMPER-EVIDENT LOG EXPORT ===\n")
            f.write(json.dumps(metadata, indent=2) + "\n")
            f.write("=== ENTRIES ===\n")
            
            # Write all entries
            for entry in self.entries:
                f.write(json.dumps(entry) + "\n")


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demo_normal_logging():
    """Demonstrate normal tamper-evident logging."""
    print("\n" + "=" * 70)
    print("NORMAL LOGGING DEMONSTRATION")
    print("=" * 70)
    
    # Create logger with secret key
    logger = TamperEvidentLogger('/tmp/demo_secure.log', secret_key='demo_secret_123')
    
    # Log various events
    print("\n1. Creating tamper-evident log entries:")
    
    logger.log('INFO', 'Application started', {'version': '1.0.0'})
    time.sleep(0.1)
    
    logger.log('INFO', 'User authentication', {'user': 'alice', 'ip': '192.168.1.100'})
    time.sleep(0.1)
    
    logger.log('WARNING', 'Failed login attempt', {'user': 'admin', 'ip': '203.0.113.66'})
    time.sleep(0.1)
    
    logger.log('SECURITY', 'Suspicious activity detected', {
        'user': 'bob',
        'action': 'multiple_failed_logins',
        'count': 5
    })
    time.sleep(0.1)
    
    logger.log('ERROR', 'Database connection failed', {'error': 'timeout'})
    
    print(f"   Created {len(logger.entries)} log entries")
    print(f"   Chain tip hash: {logger.last_hash[:16]}...")
    
    # Verify integrity
    print("\n2. Verifying log integrity:")
    is_valid, issues = logger.verify_integrity()
    
    if is_valid:
        print("   ✅ Log chain is valid - no tampering detected")
    else:
        print("   ⚠️  Issues found:")
        for issue in issues:
            print(f"      - {issue}")
    
    return logger


def demo_tamper_detection():
    """Demonstrate detection of log tampering (T1070)."""
    print("\n" + "=" * 70)
    print("TAMPER DETECTION DEMONSTRATION (T1070)")
    print("=" * 70)
    
    # Create a new logger
    logger = TamperEvidentLogger('/tmp/demo_tampered.log', secret_key='demo_secret_123')
    
    # Create some logs
    logger.log('INFO', 'Normal activity', {'user': 'alice'})
    logger.log('SECURITY', 'Attacker compromised system', {'attacker_ip': '203.0.113.66'})
    logger.log('SECURITY', 'Attacker accessed sensitive data', {'files': ['passwords.db']})
    logger.log('INFO', 'More normal activity', {'user': 'bob'})
    
    print("\n1. Original logs created successfully")
    print(f"   Total entries: {len(logger.entries)}")
    
    # Verify before tampering
    is_valid, _ = logger.verify_integrity()
    print(f"   Integrity check: {'✅ Valid' if is_valid else '⚠️ Invalid'}")
    
    # ATTACKER ACTION: Try to hide tracks by modifying a log entry (T1070)
    print("\n2. ATTACK: Attacker attempts to modify security log (T1070)")
    print("   Changing: 'Attacker compromised system'")
    print("   To:       'Normal system activity'")
    
    # Modify an entry (simulating attacker tampering)
    logger.entries[1]['message'] = 'Normal system activity'
    logger.entries[1]['data'] = {'user': 'alice'}
    
    # Verify after tampering
    print("\n3. Verifying log integrity after modification:")
    is_valid, issues = logger.verify_integrity()
    
    if is_valid:
        print("   ⚠️  Tampering NOT detected (this shouldn't happen)")
    else:
        print("   ✅ TAMPERING DETECTED! (T1070 defense successful)")
        print(f"   Issues found: {len(issues)}")
        for issue in issues:
            print(f"      - {issue}")
    
    # ATTACKER ACTION: Try to delete a log entry
    print("\n4. ATTACK: Attacker attempts to delete security log (T1070)")
    print("   Deleting: 'Attacker accessed sensitive data'")
    
    # Delete an entry
    del logger.entries[2]
    
    print("\n5. Verifying log integrity after deletion:")
    is_valid, issues = logger.verify_integrity()
    
    if is_valid:
        print("   ⚠️  Deletion NOT detected (this shouldn't happen)")
    else:
        print("   ✅ DELETION DETECTED! (T1070 defense successful)")
        print(f"   Issues found: {len(issues)}")
        for issue in issues:
            print(f"      - {issue}")


def demo_log_query():
    """Demonstrate log querying and analysis."""
    print("\n" + "=" * 70)
    print("LOG QUERY AND ANALYSIS")
    print("=" * 70)
    
    logger = TamperEvidentLogger('/tmp/demo_query.log', secret_key='demo_secret_123')
    
    # Create diverse logs
    logger.log('INFO', 'User login', {'user': 'alice', 'ip': '192.168.1.100'})
    logger.log('INFO', 'User login', {'user': 'bob', 'ip': '192.168.1.101'})
    logger.log('WARNING', 'Failed login', {'user': 'admin', 'ip': '203.0.113.66'})
    logger.log('SECURITY', 'Multiple failed logins', {'user': 'admin', 'ip': '203.0.113.66'})
    logger.log('ERROR', 'System error', {'component': 'database'})
    
    print("\n1. All logs:")
    for entry in logger.get_entries():
        print(f"   [{entry['level']}] {entry['message']}")
    
    print("\n2. Security logs only:")
    security_logs = logger.get_entries(level='SECURITY')
    for entry in security_logs:
        print(f"   [{entry['timestamp']}] {entry['message']}: {entry['data']}")
    
    print("\n3. Export for archival:")
    logger.export_for_archival('/tmp/demo_archive.log')
    print("   ✅ Logs exported to /tmp/demo_archive.log")
    print("   Recommendation: Store in immutable storage (WORM, S3 Object Lock)")


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1070 - Tamper-Evident Logging Demo")
    print("=" * 70)
    print("\nThis demo shows how to detect log tampering and deletion attempts")
    print("using cryptographic hash chains.")
    
    # Clean up old demo files
    for f in ['/tmp/demo_secure.log', '/tmp/demo_tampered.log', 
              '/tmp/demo_query.log', '/tmp/demo_archive.log']:
        try:
            Path(f).unlink(missing_ok=True)
        except:
            pass
    
    # Run demonstrations
    demo_normal_logging()
    demo_tamper_detection()
    demo_log_query()
    
    # Summary
    print("\n" + "=" * 70)
    print("KEY DEFENSES AGAINST T1070 (Indicator Removal):")
    print("=" * 70)
    print("1. ✅ Use tamper-evident logging (cryptographic hash chains)")
    print("2. ✅ Store logs in append-only, immutable storage")
    print("3. ✅ Forward logs to remote SIEM immediately")
    print("4. ✅ Implement log integrity verification")
    print("5. ✅ Use digital signatures for log entries")
    print("6. ✅ Monitor for log deletion/modification attempts")
    print("7. ✅ Restrict access to log files (least privilege)")
    print("8. ✅ Regularly archive logs to secure storage")
    print("=" * 70)
