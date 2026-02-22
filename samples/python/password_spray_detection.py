"""
MITRE ATT&CK T1110.003 - Password Spraying Detection

Password spraying is a brute force technique where attackers try one common password
against many accounts to avoid account lockouts triggered by per-account rate limiting.

This module demonstrates defensive measures:
- Cross-account password pattern detection
- Distributed attack detection (multiple source IPs)
- Slow-and-low attack detection (attacks spread over time)
- IP reputation tracking
- Progressive delays and lockouts

Educational purpose: Shows how to detect password spray attacks that bypass
traditional per-account rate limiting.
"""

import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, deque


class PasswordSprayDetector:
    """
    Detects password spray attacks by analyzing login patterns across accounts.
    
    Defends against T1110.003 (Password Spraying) by tracking:
    - Same password hash attempted across multiple accounts
    - Failed login distribution across accounts
    - Attack velocity and timing patterns
    - IP reputation and distributed attacks
    """
    
    def __init__(
        self,
        spray_threshold_accounts: int = 5,  # Same password on N accounts
        spray_time_window_seconds: int = 300,  # 5 minutes
        max_failures_per_ip: int = 20,
        ip_block_duration_seconds: int = 1800,  # 30 minutes
        slow_spray_window_hours: int = 24,
        slow_spray_threshold: int = 10
    ):
        self.spray_threshold_accounts = spray_threshold_accounts
        self.spray_time_window_seconds = spray_time_window_seconds
        self.max_failures_per_ip = max_failures_per_ip
        self.ip_block_duration_seconds = ip_block_duration_seconds
        self.slow_spray_window_hours = slow_spray_window_hours
        self.slow_spray_threshold = slow_spray_threshold
        
        # Track password hashes used: {password_hash: [(timestamp, username, ip), ...]}
        self.password_attempts: Dict[str, List[Tuple[float, str, str]]] = defaultdict(list)
        
        # Track IP addresses: {ip: [(timestamp, username, password_hash), ...]}
        self.ip_attempts: Dict[str, List[Tuple[float, str, str]]] = defaultdict(list)
        
        # Blocked IPs: {ip: block_until_timestamp}
        self.blocked_ips: Dict[str, float] = {}
        
        # IP reputation scores: {ip: score} (0.0 = good, 1.0 = malicious)
        self.ip_reputation: Dict[str, float] = defaultdict(float)
        
        # Failed login delays: {ip: delay_seconds}
        self.progressive_delays: Dict[str, float] = defaultdict(float)
    
    def _hash_password(self, password: str) -> str:
        """Create a hash of the password for pattern detection."""
        return hashlib.sha256(password.encode()).hexdigest()[:16]
    
    def _clean_old_attempts(self, current_time: float) -> None:
        """Remove attempts older than the time windows."""
        # Clean password attempts (short window)
        cutoff_short = current_time - self.spray_time_window_seconds
        for password_hash in list(self.password_attempts.keys()):
            self.password_attempts[password_hash] = [
                (ts, username, ip) for ts, username, ip in self.password_attempts[password_hash]
                if ts > cutoff_short
            ]
            if not self.password_attempts[password_hash]:
                del self.password_attempts[password_hash]
        
        # Clean IP attempts (longer window for slow spray detection)
        cutoff_long = current_time - (self.slow_spray_window_hours * 3600)
        for ip in list(self.ip_attempts.keys()):
            self.ip_attempts[ip] = [
                (ts, username, pw_hash) for ts, username, pw_hash in self.ip_attempts[ip]
                if ts > cutoff_long
            ]
            if not self.ip_attempts[ip]:
                del self.ip_attempts[ip]
        
        # Clean expired IP blocks
        for ip in list(self.blocked_ips.keys()):
            if current_time >= self.blocked_ips[ip]:
                del self.blocked_ips[ip]
                # Reset progressive delay when block expires
                self.progressive_delays[ip] = 0.0
    
    def _detect_spray_pattern(
        self, 
        password_hash: str, 
        current_time: float
    ) -> Tuple[bool, int, List[str]]:
        """
        Detect if a password is being sprayed across multiple accounts.
        
        Returns:
            (is_spray, account_count, usernames)
        """
        recent_attempts = [
            (ts, username, ip) for ts, username, ip in self.password_attempts[password_hash]
            if current_time - ts <= self.spray_time_window_seconds
        ]
        
        # Get unique usernames
        unique_usernames = set(username for _, username, _ in recent_attempts)
        
        is_spray = len(unique_usernames) >= self.spray_threshold_accounts
        
        return is_spray, len(unique_usernames), list(unique_usernames)
    
    def _detect_slow_spray(self, ip: str, current_time: float) -> Tuple[bool, int]:
        """
        Detect slow-and-low password spray (spread over many hours).
        
        Returns:
            (is_slow_spray, unique_accounts_count)
        """
        cutoff = current_time - (self.slow_spray_window_hours * 3600)
        recent_attempts = [
            (ts, username, pw_hash) for ts, username, pw_hash in self.ip_attempts[ip]
            if ts > cutoff
        ]
        
        # Count unique accounts attempted from this IP
        unique_accounts = set(username for _, username, _ in recent_attempts)
        
        is_slow_spray = len(unique_accounts) >= self.slow_spray_threshold
        
        return is_slow_spray, len(unique_accounts)
    
    def _detect_distributed_spray(
        self, 
        password_hash: str, 
        current_time: float
    ) -> Tuple[bool, int, List[str]]:
        """
        Detect distributed spray (same password from multiple IPs).
        
        Returns:
            (is_distributed, ip_count, ips)
        """
        recent_attempts = [
            (ts, username, ip) for ts, username, ip in self.password_attempts[password_hash]
            if current_time - ts <= self.spray_time_window_seconds
        ]
        
        unique_ips = set(ip for _, _, ip in recent_attempts)
        
        is_distributed = len(unique_ips) >= 3 and len(recent_attempts) >= self.spray_threshold_accounts
        
        return is_distributed, len(unique_ips), list(unique_ips)
    
    def _is_ip_blocked(self, ip: str, current_time: float) -> bool:
        """Check if IP is currently blocked."""
        if ip in self.blocked_ips:
            return current_time < self.blocked_ips[ip]
        return False
    
    def _block_ip(self, ip: str, current_time: float) -> None:
        """Block an IP address."""
        self.blocked_ips[ip] = current_time + self.ip_block_duration_seconds
        self.ip_reputation[ip] = min(1.0, self.ip_reputation[ip] + 0.3)
    
    def _apply_progressive_delay(self, ip: str) -> float:
        """
        Calculate progressive delay for IP based on failure history.
        Returns delay in seconds.
        """
        if ip not in self.progressive_delays:
            self.progressive_delays[ip] = 0.5
        else:
            # Exponential backoff: 0.5s, 1s, 2s, 4s, 8s, ...
            self.progressive_delays[ip] = min(16.0, self.progressive_delays[ip] * 2)
        
        return self.progressive_delays[ip]
    
    def check_login_attempt(
        self,
        username: str,
        password: str,
        ip_address: str
    ) -> Tuple[bool, str, Optional[float]]:
        """
        Check if login attempt shows signs of password spray attack.
        
        Args:
            username: Account username
            password: Password being attempted
            ip_address: Source IP address
        
        Returns:
            Tuple of (allowed, reason, delay_seconds)
            - allowed: Whether attempt should proceed
            - reason: Explanation
            - delay_seconds: Required delay before processing (None if blocked)
        """
        current_time = time.time()
        
        # Clean old data
        self._clean_old_attempts(current_time)
        
        # Check if IP is blocked
        if self._is_ip_blocked(ip_address, current_time):
            return False, f"IP {ip_address} is blocked due to spray attack (T1110.003)", None
        
        # Hash the password for pattern analysis
        password_hash = self._hash_password(password)
        
        # Record this attempt
        self.password_attempts[password_hash].append((current_time, username, ip_address))
        self.ip_attempts[ip_address].append((current_time, username, password_hash))
        
        # Detect spray pattern: same password across multiple accounts
        is_spray, account_count, usernames = self._detect_spray_pattern(
            password_hash, current_time
        )
        
        if is_spray:
            self._block_ip(ip_address, current_time)
            return False, (
                f"SPRAY ATTACK DETECTED (T1110.003): Password tried on {account_count} accounts. "
                f"Blocking IP {ip_address}."
            ), None
        
        # Detect distributed spray: same password from multiple IPs
        is_distributed, ip_count, ips = self._detect_distributed_spray(
            password_hash, current_time
        )
        
        if is_distributed:
            # Block all involved IPs
            for involved_ip in ips:
                self._block_ip(involved_ip, current_time)
            return False, (
                f"DISTRIBUTED SPRAY DETECTED (T1110.003): Password tried from {ip_count} IPs. "
                f"Blocking all involved IPs."
            ), None
        
        # Detect slow-and-low spray: many accounts over longer period
        is_slow_spray, unique_accounts = self._detect_slow_spray(ip_address, current_time)
        
        if is_slow_spray:
            self._block_ip(ip_address, current_time)
            return False, (
                f"SLOW SPRAY DETECTED (T1110.003): {unique_accounts} accounts attempted "
                f"from {ip_address} over {self.slow_spray_window_hours}h. Blocking IP."
            ), None
        
        # Check IP failure count
        recent_failures = len([
            1 for ts, _, _ in self.ip_attempts[ip_address]
            if current_time - ts <= self.spray_time_window_seconds
        ])
        
        if recent_failures >= self.max_failures_per_ip:
            self._block_ip(ip_address, current_time)
            return False, (
                f"Too many failed attempts from {ip_address} ({recent_failures}). "
                f"Blocking IP (T1110.003 defense)."
            ), None
        
        # Apply progressive delay for suspicious activity
        delay = self._apply_progressive_delay(ip_address)
        
        # Warning if approaching spray threshold
        if account_count >= self.spray_threshold_accounts - 2:
            return True, (
                f"WARNING: Password pattern approaching spray threshold "
                f"({account_count}/{self.spray_threshold_accounts} accounts). "
                f"Applying {delay:.1f}s delay."
            ), delay
        
        return True, (
            f"Login attempt allowed with {delay:.1f}s delay. "
            f"IP reputation: {self.ip_reputation[ip_address]:.2f}"
        ), delay
    
    def record_successful_login(self, username: str, ip_address: str) -> None:
        """Record successful login (improves IP reputation)."""
        self.ip_reputation[ip_address] = max(0.0, self.ip_reputation[ip_address] - 0.1)
        self.progressive_delays[ip_address] = 0.0  # Reset delay
    
    def get_security_report(self) -> Dict:
        """Generate security report of detected threats."""
        current_time = time.time()
        
        # Find most commonly sprayed passwords
        spray_patterns = []
        for password_hash, attempts in self.password_attempts.items():
            recent = [
                (ts, username, ip) for ts, username, ip in attempts
                if current_time - ts <= self.spray_time_window_seconds
            ]
            unique_accounts = set(username for _, username, _ in recent)
            if len(unique_accounts) >= 3:
                spray_patterns.append((password_hash, len(unique_accounts), list(unique_accounts)[:5]))
        
        # Find most aggressive IPs
        aggressive_ips = []
        for ip, attempts in self.ip_attempts.items():
            recent = [a for a in attempts if current_time - a[0] <= 3600]
            if len(recent) >= 5:
                unique_accounts = set(username for _, username, _ in recent)
                aggressive_ips.append((ip, len(recent), len(unique_accounts)))
        
        return {
            "timestamp": datetime.fromtimestamp(current_time).isoformat(),
            "blocked_ips": len(self.blocked_ips),
            "tracked_password_patterns": len(self.password_attempts),
            "spray_patterns_detected": sorted(spray_patterns, key=lambda x: x[1], reverse=True)[:5],
            "aggressive_ips": sorted(aggressive_ips, key=lambda x: x[1], reverse=True)[:5],
            "high_reputation_risk_ips": [
                (ip, score) for ip, score in self.ip_reputation.items() if score > 0.5
            ]
        }


# =============================================================================
# VULNERABLE IMPLEMENTATION (DO NOT USE IN PRODUCTION)
# =============================================================================

def vulnerable_auth_no_spray_detection(username: str, password: str, ip: str) -> bool:
    """
    VULNERABLE: Authentication with only per-account rate limiting.
    
    Issues:
    - No cross-account analysis
    - No password pattern detection
    - Attacker can spray one password across many accounts
    - No distributed attack detection
    
    ATT&CK T1110.003: Attacker can spray passwords across accounts.
    """
    # Simple per-account lockout (easily bypassed by trying different accounts)
    valid_users = {"user1": "password", "user2": "password", "user3": "password"}
    return valid_users.get(username) == password


# =============================================================================
# DEMONSTRATION
# =============================================================================

def simulate_normal_failed_logins(detector: PasswordSprayDetector) -> None:
    """Simulate normal failed logins (users forgetting passwords)."""
    print("\n--- Simulating Normal Failed Logins ---")
    
    attempts = [
        ("alice", "wrong1", "192.168.1.100"),
        ("alice", "wrong2", "192.168.1.100"),
        ("bob", "incorrect", "192.168.1.101"),
    ]
    
    for username, password, ip in attempts:
        allowed, reason, delay = detector.check_login_attempt(username, password, ip)
        status = "ALLOWED" if allowed else "BLOCKED"
        print(f"  {username} from {ip}: {status}")


def simulate_password_spray_attack(detector: PasswordSprayDetector) -> None:
    """
    Simulate T1110.003 attack: Try common password across many accounts.
    """
    print("\n--- Simulating Password Spray Attack (T1110.003) ---")
    print("Attacker trying 'Summer2024!' across multiple accounts...")
    
    attacker_ip = "203.0.113.66"
    common_password = "Summer2024!"
    
    target_accounts = [
        "alice", "bob", "charlie", "david", "eve", "frank", "grace", "henry"
    ]
    
    for i, username in enumerate(target_accounts, 1):
        allowed, reason, delay = detector.check_login_attempt(
            username, common_password, attacker_ip
        )
        
        if not allowed:
            print(f"  Attempt {i}: 🛡️  BLOCKED!")
            print(f"    Reason: {reason}")
            break
        else:
            print(f"  Attempt {i}: {username} - allowed (delay: {delay:.1f}s)")


def simulate_distributed_spray(detector: PasswordSprayDetector) -> None:
    """
    Simulate distributed password spray from multiple IPs.
    """
    print("\n--- Simulating Distributed Password Spray (T1110.003) ---")
    print("Attacker using multiple IPs to spray password...")
    
    common_password = "Winter2024!"
    attacker_ips = ["198.51.100.10", "198.51.100.11", "198.51.100.12"]
    target_accounts = ["user1", "user2", "user3", "user4", "user5", "user6"]
    
    for i, username in enumerate(target_accounts, 1):
        ip = attacker_ips[i % len(attacker_ips)]
        allowed, reason, delay = detector.check_login_attempt(
            username, common_password, ip
        )
        
        if not allowed:
            print(f"  Attempt {i}: 🛡️  BLOCKED!")
            print(f"    Reason: {reason}")
            break
        else:
            print(f"  Attempt {i}: {username} from {ip} - status: {allowed}")


def simulate_slow_spray(detector: PasswordSprayDetector) -> None:
    """
    Simulate slow-and-low password spray spread over time.
    """
    print("\n--- Simulating Slow Password Spray (T1110.003) ---")
    print("Attacker trying many accounts slowly to evade detection...")
    
    attacker_ip = "10.0.0.50"
    
    for i in range(12):
        username = f"user{i + 1}"
        password = "CommonPass123"
        
        allowed, reason, delay = detector.check_login_attempt(
            username, password, attacker_ip
        )
        
        if not allowed:
            print(f"  Attempt {i + 1}: 🛡️  BLOCKED!")
            print(f"    Reason: {reason}")
            break
        elif i % 3 == 0:
            print(f"  Attempt {i + 1}: {username} - still allowed...")


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1110.003 - Password Spraying Detection Demo")
    print("=" * 70)
    print("\nThis demo shows how to detect password spray attacks that try")
    print("one common password across many accounts to bypass per-account")
    print("rate limiting.")
    
    # Create detector
    detector = PasswordSprayDetector(
        spray_threshold_accounts=5,
        spray_time_window_seconds=300,
        max_failures_per_ip=20,
        ip_block_duration_seconds=1800,
        slow_spray_window_hours=24,
        slow_spray_threshold=10
    )
    
    # Run simulations
    simulate_normal_failed_logins(detector)
    simulate_password_spray_attack(detector)
    simulate_distributed_spray(detector)
    simulate_slow_spray(detector)
    
    # Generate report
    print("\n--- Security Report ---")
    report = detector.get_security_report()
    print(f"Blocked IPs: {report['blocked_ips']}")
    print(f"Tracked Password Patterns: {report['tracked_password_patterns']}")
    
    if report['spray_patterns_detected']:
        print("\n⚠️  Spray Patterns Detected:")
        for pw_hash, account_count, sample_accounts in report['spray_patterns_detected']:
            print(f"  Password {pw_hash}: {account_count} accounts")
            print(f"    Sample accounts: {', '.join(sample_accounts)}")
    
    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("- Monitor password usage patterns across accounts")
    print("- Detect when same password is tried on multiple accounts")
    print("- Track distributed attacks from multiple IPs")
    print("- Implement progressive delays and IP reputation scoring")
    print("- Detect slow-and-low sprays over longer time windows")
    print("- Use CAPTCHA/MFA when spray patterns detected")
    print("=" * 70)
