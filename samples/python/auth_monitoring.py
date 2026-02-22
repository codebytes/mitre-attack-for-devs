"""
MITRE ATT&CK T1078 - Valid Accounts: Authentication Monitoring

Valid accounts can be misused by attackers to maintain access and evade detection.
This module demonstrates defensive measures to detect anomalous authentication behavior.

Defenses implemented:
- Impossible travel detection (geolocation anomalies)
- Device fingerprint tracking (browser/OS changes)
- Behavioral baseline modeling (access patterns)
- Privilege escalation monitoring
- Anomalous resource access detection
- Risk-based step-up authentication

Educational purpose: Shows how to detect misuse of valid credentials through behavioral analysis.
"""

import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import math


class UserBehaviorBaseline:
    """
    Tracks normal user behavior patterns to detect anomalies.
    
    Defends against T1078 (Valid Accounts) by establishing:
    - Normal login hours
    - Typical device fingerprints
    - Geographic patterns
    - Resource access patterns
    """
    
    def __init__(self, username: str):
        self.username = username
        self.login_hours: List[int] = []  # Typical login hours (0-23)
        self.locations: List[str] = []  # Recent login locations
        self.device_fingerprints: set = set()  # Known device fingerprints
        self.accessed_resources: set = set()  # Resources user typically accesses
        self.privilege_level: str = "user"  # Current privilege level
        self.last_login_time: Optional[float] = None
        self.last_login_location: Optional[str] = None
    
    def update_baseline(self, login_time: float, location: str, device_fp: str, 
                        accessed_resource: Optional[str] = None) -> None:
        """Update user's behavioral baseline with new data."""
        login_dt = datetime.fromtimestamp(login_time)
        self.login_hours.append(login_dt.hour)
        
        # Keep only last 100 login hours for baseline
        if len(self.login_hours) > 100:
            self.login_hours = self.login_hours[-100:]
        
        self.locations.append(location)
        if len(self.locations) > 50:
            self.locations = self.locations[-50:]
        
        self.device_fingerprints.add(device_fp)
        
        if accessed_resource:
            self.accessed_resources.add(accessed_resource)
        
        self.last_login_time = login_time
        self.last_login_location = location
    
    def get_typical_hours(self) -> set:
        """Get the typical hours when user logs in."""
        if len(self.login_hours) < 5:
            return set(range(24))  # Not enough data, allow all hours
        
        # Get hours that appear in at least 20% of logins
        hour_counts = defaultdict(int)
        for hour in self.login_hours:
            hour_counts[hour] += 1
        
        threshold = len(self.login_hours) * 0.2
        return {hour for hour, count in hour_counts.items() if count >= threshold}
    
    def is_typical_hour(self, login_time: float) -> bool:
        """Check if login time matches typical pattern."""
        login_dt = datetime.fromtimestamp(login_time)
        typical_hours = self.get_typical_hours()
        return login_dt.hour in typical_hours
    
    def is_known_device(self, device_fp: str) -> bool:
        """Check if device fingerprint is recognized."""
        return device_fp in self.device_fingerprints
    
    def is_typical_location(self, location: str) -> bool:
        """Check if location is typical for this user."""
        if len(self.locations) < 3:
            return True  # Not enough data
        
        # Location is typical if it appears in recent history
        return location in self.locations[-10:]


class AuthenticationMonitor:
    """
    Monitors authentication events for signs of account misuse.
    
    Defends against T1078 (Valid Accounts) by detecting:
    - Impossible travel (login from distant locations in short time)
    - Device fingerprint changes (different browser/OS)
    - Unusual login hours
    - Privilege escalation attempts
    - Access to never-before-seen resources
    """
    
    def __init__(
        self,
        impossible_travel_threshold_km: float = 500.0,  # km
        impossible_travel_time_hours: float = 1.0,  # hours
        risk_threshold_high: float = 0.7,
        risk_threshold_critical: float = 0.9
    ):
        self.baselines: Dict[str, UserBehaviorBaseline] = {}
        self.impossible_travel_threshold_km = impossible_travel_threshold_km
        self.impossible_travel_time_hours = impossible_travel_time_hours
        self.risk_threshold_high = risk_threshold_high
        self.risk_threshold_critical = risk_threshold_critical
        
        # Simple location to coordinates mapping (in real system, use geolocation API)
        self.location_coords = {
            "New York": (40.7128, -74.0060),
            "London": (51.5074, -0.1278),
            "Tokyo": (35.6762, 139.6503),
            "Sydney": (-33.8688, 151.2093),
            "Paris": (48.8566, 2.3522),
            "Los Angeles": (34.0522, -118.2437),
            "Mumbai": (19.0760, 72.8777),
            "Beijing": (39.9042, 116.4074)
        }
    
    def _calculate_distance_km(self, loc1: str, loc2: str) -> float:
        """Calculate distance between two locations in kilometers (Haversine formula)."""
        if loc1 not in self.location_coords or loc2 not in self.location_coords:
            return 0.0
        
        lat1, lon1 = self.location_coords[loc1]
        lat2, lon2 = self.location_coords[loc2]
        
        # Haversine formula
        R = 6371  # Earth radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _generate_device_fingerprint(self, user_agent: str, ip_address: str) -> str:
        """Generate a device fingerprint from user agent and IP."""
        return hashlib.md5(f"{user_agent}:{ip_address}".encode()).hexdigest()[:16]
    
    def _get_or_create_baseline(self, username: str) -> UserBehaviorBaseline:
        """Get existing baseline or create new one."""
        if username not in self.baselines:
            self.baselines[username] = UserBehaviorBaseline(username)
        return self.baselines[username]
    
    def check_authentication(
        self,
        username: str,
        location: str,
        user_agent: str,
        ip_address: str,
        privilege_requested: str = "user",
        accessed_resource: Optional[str] = None
    ) -> Tuple[bool, str, float, List[str]]:
        """
        Check authentication for anomalies.
        
        Args:
            username: User attempting to authenticate
            location: Geographic location (city name)
            user_agent: Browser user agent string
            ip_address: Source IP address
            privilege_requested: Privilege level being requested
            accessed_resource: Resource being accessed (if any)
        
        Returns:
            Tuple of (allowed, reason, risk_score, anomalies)
        """
        current_time = time.time()
        baseline = self._get_or_create_baseline(username)
        device_fp = self._generate_device_fingerprint(user_agent, ip_address)
        
        risk_score = 0.0
        anomalies = []
        
        # Check 1: Impossible travel detection
        if baseline.last_login_location and baseline.last_login_time:
            time_diff_hours = (current_time - baseline.last_login_time) / 3600
            distance_km = self._calculate_distance_km(baseline.last_login_location, location)
            
            if time_diff_hours < self.impossible_travel_time_hours and distance_km > self.impossible_travel_threshold_km:
                risk_score += 0.5
                anomalies.append(
                    f"Impossible travel: {distance_km:.0f}km in {time_diff_hours:.1f}h "
                    f"({baseline.last_login_location} → {location})"
                )
        
        # Check 2: Unknown device fingerprint
        if not baseline.is_known_device(device_fp):
            risk_score += 0.2
            anomalies.append(f"New device fingerprint: {device_fp}")
        
        # Check 3: Unusual login time
        if not baseline.is_typical_hour(current_time):
            risk_score += 0.15
            login_hour = datetime.fromtimestamp(current_time).hour
            anomalies.append(f"Unusual login hour: {login_hour}:00")
        
        # Check 4: Atypical location
        if not baseline.is_typical_location(location):
            risk_score += 0.15
            anomalies.append(f"Atypical location: {location}")
        
        # Check 5: Privilege escalation
        if privilege_requested != baseline.privilege_level:
            if privilege_requested in ["admin", "root", "superuser"]:
                risk_score += 0.3
                anomalies.append(
                    f"Privilege escalation: {baseline.privilege_level} → {privilege_requested}"
                )
        
        # Check 6: Never-before-accessed resource
        if accessed_resource and accessed_resource not in baseline.accessed_resources:
            risk_score += 0.1
            anomalies.append(f"New resource access: {accessed_resource}")
        
        # Determine if authentication should be allowed
        allowed = True
        reason = "Authentication allowed"
        
        if risk_score >= self.risk_threshold_critical:
            allowed = False
            reason = f"CRITICAL RISK (T1078): Score {risk_score:.2f} - BLOCKED"
        elif risk_score >= self.risk_threshold_high:
            reason = f"HIGH RISK (T1078): Score {risk_score:.2f} - Requires MFA/step-up auth"
        elif risk_score > 0:
            reason = f"MODERATE RISK (T1078): Score {risk_score:.2f} - Monitoring"
        
        # Update baseline if allowed (learning from successful logins)
        if allowed and risk_score < self.risk_threshold_high:
            baseline.update_baseline(current_time, location, device_fp, accessed_resource)
        
        return allowed, reason, risk_score, anomalies


# =============================================================================
# VULNERABLE IMPLEMENTATION (DO NOT USE IN PRODUCTION)
# =============================================================================

def vulnerable_simple_auth(username: str, password: str) -> bool:
    """
    VULNERABLE: Simple authentication with no monitoring.
    
    Issues:
    - No behavioral analysis
    - No anomaly detection
    - Attacker with valid credentials has unlimited access
    - Cannot detect account misuse
    
    ATT&CK T1078: Attacker can use stolen credentials freely.
    """
    # Just check if credentials are valid - no context awareness
    valid_users = {"alice": "pass123", "bob": "secret456"}
    return valid_users.get(username) == password


# =============================================================================
# DEMONSTRATION
# =============================================================================

def simulate_normal_behavior(monitor: AuthenticationMonitor) -> None:
    """Simulate normal user behavior to establish baseline."""
    print("\n--- Establishing Baseline (Normal Behavior) ---")
    
    # Alice logs in from New York during work hours
    for day in range(5):
        allowed, reason, risk, anomalies = monitor.check_authentication(
            username="alice",
            location="New York",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            ip_address="192.168.1.100",
            accessed_resource="/dashboard"
        )
        print(f"Day {day + 1} - Alice login: {reason} (risk: {risk:.2f})")
        time.sleep(0.1)  # Simulate time passing


def simulate_impossible_travel_attack(monitor: AuthenticationMonitor) -> None:
    """
    Simulate T1078 attack: Attacker uses stolen credentials from different location.
    Impossible travel: Login from New York, then Tokyo 10 minutes later.
    """
    print("\n--- Simulating Impossible Travel Attack (T1078) ---")
    
    # Normal login from New York
    allowed1, reason1, risk1, anomalies1 = monitor.check_authentication(
        username="alice",
        location="New York",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        ip_address="192.168.1.100"
    )
    print(f"Login 1 (New York): {reason1}")
    
    time.sleep(0.2)  # 0.2 seconds simulating ~10 minutes
    
    # Attacker tries to login from Tokyo immediately after
    allowed2, reason2, risk2, anomalies2 = monitor.check_authentication(
        username="alice",
        location="Tokyo",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        ip_address="203.0.113.50"
    )
    
    print(f"Login 2 (Tokyo): {reason2}")
    print(f"  Risk Score: {risk2:.2f}")
    print("  Anomalies detected:")
    for anomaly in anomalies2:
        print(f"    ⚠️  {anomaly}")


def simulate_device_change_attack(monitor: AuthenticationMonitor) -> None:
    """
    Simulate T1078 attack: Attacker uses different device/browser.
    """
    print("\n--- Simulating Device Change Attack (T1078) ---")
    
    # Attacker uses different browser/OS
    allowed, reason, risk, anomalies = monitor.check_authentication(
        username="alice",
        location="New York",
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        ip_address="198.51.100.75",
        accessed_resource="/admin/users"
    )
    
    print(f"Result: {reason}")
    print(f"  Risk Score: {risk:.2f}")
    print("  Anomalies detected:")
    for anomaly in anomalies:
        print(f"    ⚠️  {anomaly}")


def simulate_privilege_escalation(monitor: AuthenticationMonitor) -> None:
    """
    Simulate T1078 attack: Attacker tries to escalate privileges.
    """
    print("\n--- Simulating Privilege Escalation (T1078) ---")
    
    allowed, reason, risk, anomalies = monitor.check_authentication(
        username="alice",
        location="New York",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        ip_address="192.168.1.100",
        privilege_requested="admin",
        accessed_resource="/admin/system-config"
    )
    
    print(f"Result: {reason}")
    print(f"  Risk Score: {risk:.2f}")
    print("  Anomalies detected:")
    for anomaly in anomalies:
        print(f"    ⚠️  {anomaly}")


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1078 - Valid Accounts: Authentication Monitoring")
    print("=" * 70)
    print("\nThis demo shows how to detect misuse of valid credentials")
    print("through behavioral analysis and anomaly detection.")
    
    # Create monitor
    monitor = AuthenticationMonitor(
        impossible_travel_threshold_km=500.0,
        impossible_travel_time_hours=1.0,
        risk_threshold_high=0.7,
        risk_threshold_critical=0.9
    )
    
    # Run simulations
    simulate_normal_behavior(monitor)
    simulate_impossible_travel_attack(monitor)
    simulate_device_change_attack(monitor)
    simulate_privilege_escalation(monitor)
    
    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("- Monitor for impossible travel (geolocation anomalies)")
    print("- Track device fingerprints to detect new devices")
    print("- Establish behavioral baselines for each user")
    print("- Detect privilege escalation attempts")
    print("- Implement risk-based authentication (step-up auth for high risk)")
    print("- Log all authentication anomalies for investigation")
    print("=" * 70)
