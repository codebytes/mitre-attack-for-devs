"""
MITRE ATT&CK T1110.004 - Credential Stuffing Detection

Credential stuffing is a brute force technique where attackers use lists of 
compromised username/password pairs to gain unauthorized access to accounts.

This module demonstrates defensive measures:
- Rate limiting per IP and per account
- Detection of automation patterns (rapid attempts, distributed sources)
- Account lockout and IP blocking
- Anomaly detection based on behavioral patterns

Educational purpose: Shows how to detect and prevent credential stuffing attacks.
"""

import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import hashlib


class LoginMonitor:
    """
    Monitors login attempts and detects credential stuffing patterns.
    
    Defends against T1110.004 (Credential Stuffing) by tracking:
    - Failed login attempts per IP
    - Failed login attempts per account
    - Login velocity (attempts per time window)
    - Distributed attack patterns (many accounts from same IP)
    """
    
    def __init__(
        self,
        max_failures_per_ip: int = 10,
        max_failures_per_account: int = 5,
        time_window_seconds: int = 300,  # 5 minutes
        lockout_duration_seconds: int = 900,  # 15 minutes
        suspicious_account_threshold: int = 20  # Many accounts from one IP
    ):
        self.max_failures_per_ip = max_failures_per_ip
        self.max_failures_per_account = max_failures_per_account
        self.time_window_seconds = time_window_seconds
        self.lockout_duration_seconds = lockout_duration_seconds
        self.suspicious_account_threshold = suspicious_account_threshold
        
        # Track failed attempts: {ip: [(timestamp, username), ...]}
        self.ip_failures: Dict[str, deque] = defaultdict(lambda: deque())
        
        # Track failed attempts per account: {username: [(timestamp, ip), ...]}
        self.account_failures: Dict[str, deque] = defaultdict(lambda: deque())
        
        # Blocked IPs: {ip: block_until_timestamp}
        self.blocked_ips: Dict[str, float] = {}
        
        # Locked accounts: {username: lock_until_timestamp}
        self.locked_accounts: Dict[str, float] = {}
        
        # Track unique accounts attempted per IP
        self.ip_account_attempts: Dict[str, set] = defaultdict(set)
    
    def _clean_old_entries(self, entries: deque, current_time: float) -> None:
        """Remove entries older than the time window."""
        cutoff_time = current_time - self.time_window_seconds
        while entries and entries[0][0] < cutoff_time:
            entries.popleft()
    
    def _is_ip_blocked(self, ip_address: str, current_time: float) -> bool:
        """Check if IP is currently blocked."""
        if ip_address in self.blocked_ips:
            if current_time < self.blocked_ips[ip_address]:
                return True
            else:
                # Block expired, remove it
                del self.blocked_ips[ip_address]
        return False
    
    def _is_account_locked(self, username: str, current_time: float) -> bool:
        """Check if account is currently locked."""
        if username in self.locked_accounts:
            if current_time < self.locked_accounts[username]:
                return True
            else:
                # Lock expired, remove it
                del self.locked_accounts[username]
        return False
    
    def _detect_distributed_attack(self, ip_address: str) -> bool:
        """
        Detect if an IP is attempting many different accounts.
        This is a common credential stuffing pattern.
        """
        unique_accounts = len(self.ip_account_attempts[ip_address])
        return unique_accounts >= self.suspicious_account_threshold
    
    def record_login_attempt(
        self, 
        username: str, 
        ip_address: str, 
        success: bool
    ) -> Tuple[bool, str]:
        """
        Record a login attempt and check for attack patterns.
        
        Args:
            username: The username attempting to log in
            ip_address: Source IP address
            success: Whether the login succeeded
            
        Returns:
            Tuple of (allowed, reason) where:
            - allowed: True if the attempt should be processed, False if blocked
            - reason: Explanation of the decision
        """
        current_time = time.time()
        
        # Check if IP is blocked
        if self._is_ip_blocked(ip_address, current_time):
            return False, f"IP {ip_address} is temporarily blocked (T1110.004 defense)"
        
        # Check if account is locked
        if self._is_account_locked(username, current_time):
            return False, f"Account {username} is temporarily locked (T1110.004 defense)"
        
        # If login succeeded, clear failure records
        if success:
            # Clear failures for this IP and account
            if ip_address in self.ip_failures:
                self.ip_failures[ip_address].clear()
            if username in self.account_failures:
                self.account_failures[username].clear()
            if ip_address in self.ip_account_attempts:
                self.ip_account_attempts[ip_address].clear()
            
            return True, "Login successful"
        
        # Record failed attempt
        self.ip_failures[ip_address].append((current_time, username))
        self.account_failures[username].append((current_time, ip_address))
        self.ip_account_attempts[ip_address].add(username)
        
        # Clean old entries
        self._clean_old_entries(self.ip_failures[ip_address], current_time)
        self._clean_old_entries(self.account_failures[username], current_time)
        
        # Check for distributed credential stuffing attack
        if self._detect_distributed_attack(ip_address):
            self.blocked_ips[ip_address] = current_time + self.lockout_duration_seconds
            return False, (
                f"ALERT: Credential stuffing detected! IP {ip_address} attempted "
                f"{len(self.ip_account_attempts[ip_address])} different accounts. "
                f"Blocking IP for {self.lockout_duration_seconds}s (T1110.004 detected)"
            )
        
        # Check IP failure rate
        ip_failure_count = len(self.ip_failures[ip_address])
        if ip_failure_count >= self.max_failures_per_ip:
            self.blocked_ips[ip_address] = current_time + self.lockout_duration_seconds
            return False, (
                f"ALERT: Too many failed attempts from IP {ip_address} "
                f"({ip_failure_count} failures). Blocking IP (T1110.004 defense)"
            )
        
        # Check account failure rate
        account_failure_count = len(self.account_failures[username])
        if account_failure_count >= self.max_failures_per_account:
            self.locked_accounts[username] = current_time + self.lockout_duration_seconds
            return False, (
                f"ALERT: Too many failed attempts for account {username} "
                f"({account_failure_count} failures). Locking account (T1110.004 defense)"
            )
        
        # Calculate velocity (attempts per minute)
        velocity = ip_failure_count / (self.time_window_seconds / 60)
        
        return True, (
            f"Login failed. Warning: {ip_failure_count} failures from this IP "
            f"(velocity: {velocity:.1f} attempts/min)"
        )
    
    def get_security_report(self) -> Dict:
        """Generate a security report of current threats."""
        current_time = time.time()
        
        # Find IPs with most failures
        top_offending_ips = sorted(
            [(ip, len(failures)) for ip, failures in self.ip_failures.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Find accounts with most failures
        top_targeted_accounts = sorted(
            [(username, len(failures)) for username, failures in self.account_failures.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Find IPs attempting many accounts (credential stuffing indicators)
        credential_stuffing_suspects = [
            (ip, len(accounts))
            for ip, accounts in self.ip_account_attempts.items()
            if len(accounts) >= self.suspicious_account_threshold // 2
        ]
        
        return {
            "timestamp": datetime.fromtimestamp(current_time).isoformat(),
            "blocked_ips": len(self.blocked_ips),
            "locked_accounts": len(self.locked_accounts),
            "top_offending_ips": top_offending_ips,
            "top_targeted_accounts": top_targeted_accounts,
            "credential_stuffing_suspects": sorted(
                credential_stuffing_suspects,
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


def simulate_normal_traffic(monitor: LoginMonitor) -> None:
    """Simulate normal login traffic."""
    print("\n--- Simulating Normal Traffic ---")
    
    # Normal successful login
    allowed, reason = monitor.record_login_attempt("alice", "192.168.1.100", success=True)
    print(f"✓ Alice login: {reason}")
    
    # Normal failed login (wrong password)
    allowed, reason = monitor.record_login_attempt("bob", "192.168.1.101", success=False)
    print(f"✗ Bob login failed: {reason}")
    
    # Retry succeeds
    allowed, reason = monitor.record_login_attempt("bob", "192.168.1.101", success=True)
    print(f"✓ Bob retry: {reason}")


def simulate_credential_stuffing_attack(monitor: LoginMonitor) -> None:
    """
    Simulate a credential stuffing attack (T1110.004).
    Attacker tries many username/password combinations from leaked databases.
    """
    print("\n--- Simulating Credential Stuffing Attack (T1110.004) ---")
    
    attacker_ip = "203.0.113.66"
    
    # Attacker tries many different accounts (typical credential stuffing)
    leaked_credentials = [
        f"user{i}@example.com" for i in range(25)
    ]
    
    for i, username in enumerate(leaked_credentials, 1):
        allowed, reason = monitor.record_login_attempt(username, attacker_ip, success=False)
        if not allowed:
            print(f"\n🛡️  BLOCKED after {i} attempts!")
            print(f"   Reason: {reason}")
            break
        elif i % 5 == 0:
            print(f"   Attempt {i}: Failed login for {username}")


def simulate_distributed_attack(monitor: LoginMonitor) -> None:
    """
    Simulate an attacker trying the same credentials from multiple IPs.
    This is an attempt to evade per-IP rate limiting.
    """
    print("\n--- Simulating Distributed Attack ---")
    
    target_account = "admin"
    
    # Attacker uses multiple IPs to avoid per-IP blocking
    for i in range(8):
        attacker_ip = f"198.51.100.{10 + i}"
        allowed, reason = monitor.record_login_attempt(
            target_account, 
            attacker_ip, 
            success=False
        )
        print(f"   Attempt from {attacker_ip}: {allowed}")
    
    # Eventually the account gets locked
    allowed, reason = monitor.record_login_attempt(
        target_account, 
        "198.51.100.99", 
        success=False
    )
    print(f"\n🛡️  Account protection: {reason}")


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1110.004 - Credential Stuffing Detection Demo")
    print("=" * 70)
    print("\nThis demo shows how to detect and prevent credential stuffing attacks")
    print("where attackers use leaked username/password combinations.")
    
    # Create monitor with defensive settings
    monitor = LoginMonitor(
        max_failures_per_ip=10,
        max_failures_per_account=5,
        time_window_seconds=300,
        lockout_duration_seconds=900,
        suspicious_account_threshold=20
    )
    
    # Run simulations
    simulate_normal_traffic(monitor)
    simulate_credential_stuffing_attack(monitor)
    simulate_distributed_attack(monitor)
    
    # Generate security report
    print("\n--- Security Report ---")
    report = monitor.get_security_report()
    print(f"Blocked IPs: {report['blocked_ips']}")
    print(f"Locked Accounts: {report['locked_accounts']}")
    
    if report['credential_stuffing_suspects']:
        print("\n⚠️  Credential Stuffing Suspects:")
        for ip, account_count in report['credential_stuffing_suspects']:
            print(f"   {ip}: attempted {account_count} different accounts")
    
    if report['top_targeted_accounts']:
        print("\n⚠️  Most Targeted Accounts:")
        for username, failure_count in report['top_targeted_accounts'][:5]:
            print(f"   {username}: {failure_count} failed attempts")
    
    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("- Monitor login velocity and failure patterns")
    print("- Detect when one IP tries many different accounts (credential stuffing)")
    print("- Implement account lockout AND IP blocking")
    print("- Use CAPTCHA or MFA for high-risk login attempts")
    print("=" * 70)
