"""
MITRE ATT&CK T1213 (Data from Information Repositories) & T1020 (Automated Exfiltration)

Attackers who gain access to systems often attempt to access and exfiltrate
large amounts of sensitive data. Monitoring data access patterns can detect
these attacks.

This module demonstrates:
- Tracking user data access patterns (baseline behavior)
- Detecting anomalies: unusual volume, timing, data types
- Alerting on potential data exfiltration attempts
- Rate limiting data access

Educational purpose: Shows how to detect T1213 and T1020 through behavioral monitoring.
References:
- https://attack.mitre.org/techniques/T1213/
- https://attack.mitre.org/techniques/T1020/
"""

import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum


class DataSensitivity(Enum):
    """Classification levels for data sensitivity."""
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    RESTRICTED = 4


@dataclass
class DataAccessEvent:
    """Represents a single data access event."""
    timestamp: float
    user: str
    resource: str
    resource_type: str
    sensitivity: DataSensitivity
    size_bytes: int
    ip_address: str
    action: str  # 'read', 'download', 'export', 'copy'


class DataAccessMonitor:
    """
    Monitors data access patterns to detect T1213 and T1020.
    
    Defends against:
    - T1213: Data from Information Repositories
    - T1020: Automated Exfiltration
    
    Detection methods:
    - Volume anomalies (accessing more data than normal)
    - Velocity anomalies (accessing data faster than normal)
    - Time anomalies (accessing data at unusual hours)
    - Pattern anomalies (accessing unusual data types)
    - Sensitivity anomalies (accessing more sensitive data)
    """
    
    def __init__(
        self,
        baseline_days: int = 7,
        alert_volume_multiplier: float = 3.0,
        alert_velocity_threshold: int = 10,  # accesses per minute
        max_size_per_hour_mb: float = 100.0,
        business_hours: Tuple[int, int] = (8, 18)  # 8 AM to 6 PM
    ):
        self.baseline_days = baseline_days
        self.alert_volume_multiplier = alert_volume_multiplier
        self.alert_velocity_threshold = alert_velocity_threshold
        self.max_size_per_hour_bytes = max_size_per_hour_mb * 1024 * 1024
        self.business_hours = business_hours
        
        # Track all access events
        self.events: List[DataAccessEvent] = []
        
        # User access patterns (for baseline)
        self.user_baselines: Dict[str, Dict] = defaultdict(lambda: {
            'total_accesses': 0,
            'total_bytes': 0,
            'resource_types': set(),
            'avg_accesses_per_day': 0,
            'avg_bytes_per_day': 0,
            'typical_hours': set(),
            'sensitivity_levels': defaultdict(int)
        })
        
        # Recent access tracking (for velocity detection)
        self.recent_accesses: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        # Hourly data volume tracking
        self.hourly_volumes: Dict[str, deque] = defaultdict(lambda: deque())
        
        # Alerts generated
        self.alerts: List[Dict] = []
    
    def _is_business_hours(self, timestamp: float) -> bool:
        """Check if timestamp falls within business hours."""
        dt = datetime.fromtimestamp(timestamp)
        hour = dt.hour
        return self.business_hours[0] <= hour < self.business_hours[1]
    
    def _get_user_baseline(self, user: str) -> Dict:
        """Get or create baseline for a user."""
        return self.user_baselines[user]
    
    def _update_baseline(self, event: DataAccessEvent):
        """Update user baseline with new event."""
        baseline = self._get_user_baseline(event.user)
        
        baseline['total_accesses'] += 1
        baseline['total_bytes'] += event.size_bytes
        baseline['resource_types'].add(event.resource_type)
        baseline['sensitivity_levels'][event.sensitivity] += 1
        
        # Track typical access hours
        hour = datetime.fromtimestamp(event.timestamp).hour
        baseline['typical_hours'].add(hour)
        
        # Calculate averages (simplified - in production, use time windows)
        days_tracked = max(1, len(self.events) / 10)  # Rough estimate
        baseline['avg_accesses_per_day'] = baseline['total_accesses'] / days_tracked
        baseline['avg_bytes_per_day'] = baseline['total_bytes'] / days_tracked
    
    def _detect_volume_anomaly(self, event: DataAccessEvent) -> Optional[Dict]:
        """
        Detect if user is accessing unusually large volume of data.
        
        Indicator of T1020 (Automated Exfiltration).
        """
        baseline = self._get_user_baseline(event.user)
        
        # Need sufficient baseline data
        if baseline['total_accesses'] < 10:
            return None
        
        # Check recent hourly volume
        current_time = event.timestamp
        hour_ago = current_time - 3600
        
        # Calculate volume in last hour
        recent_bytes = sum(
            e.size_bytes for e in self.events
            if e.user == event.user and e.timestamp >= hour_ago
        )
        
        # Alert if exceeds threshold
        if recent_bytes > self.max_size_per_hour_bytes:
            return {
                'type': 'VOLUME_ANOMALY',
                'severity': 'HIGH',
                'technique': 'T1020 (Automated Exfiltration)',
                'user': event.user,
                'recent_bytes': recent_bytes,
                'threshold_bytes': self.max_size_per_hour_bytes,
                'message': f'User {event.user} accessed {recent_bytes / 1024 / 1024:.1f} MB in last hour (threshold: {self.max_size_per_hour_bytes / 1024 / 1024:.1f} MB)'
            }
        
        return None
    
    def _detect_velocity_anomaly(self, event: DataAccessEvent) -> Optional[Dict]:
        """
        Detect if user is accessing data at an unusual rate.
        
        Indicator of T1020 (Automated Exfiltration) - automated tools
        access data much faster than humans.
        """
        # Get recent accesses for this user
        recent = self.recent_accesses[event.user]
        recent.append(event.timestamp)
        
        # Need sufficient data
        if len(recent) < 10:
            return None
        
        # Calculate accesses per minute
        time_window = recent[-1] - recent[0]
        if time_window == 0:
            return None
        
        accesses_per_minute = len(recent) / (time_window / 60)
        
        # Alert if velocity is too high
        if accesses_per_minute > self.alert_velocity_threshold:
            return {
                'type': 'VELOCITY_ANOMALY',
                'severity': 'HIGH',
                'technique': 'T1020 (Automated Exfiltration)',
                'user': event.user,
                'accesses_per_minute': round(accesses_per_minute, 2),
                'threshold': self.alert_velocity_threshold,
                'message': f'User {event.user} accessing data at {accesses_per_minute:.1f} accesses/min (threshold: {self.alert_velocity_threshold})'
            }
        
        return None
    
    def _detect_time_anomaly(self, event: DataAccessEvent) -> Optional[Dict]:
        """
        Detect if user is accessing data at unusual hours.
        
        Indicator of T1213/T1020 - attackers often work outside business hours.
        """
        baseline = self._get_user_baseline(event.user)
        
        # Need sufficient baseline
        if baseline['total_accesses'] < 20:
            return None
        
        current_hour = datetime.fromtimestamp(event.timestamp).hour
        
        # Check if this hour is unusual for this user
        if current_hour not in baseline['typical_hours']:
            # Also check if outside business hours
            if not self._is_business_hours(event.timestamp):
                return {
                    'type': 'TIME_ANOMALY',
                    'severity': 'MEDIUM',
                    'technique': 'T1213 (Data from Information Repositories)',
                    'user': event.user,
                    'access_hour': current_hour,
                    'typical_hours': sorted(list(baseline['typical_hours'])),
                    'message': f'User {event.user} accessing data at unusual hour {current_hour}:00 (typical: {sorted(list(baseline["typical_hours"]))})'
                }
        
        return None
    
    def _detect_sensitivity_anomaly(self, event: DataAccessEvent) -> Optional[Dict]:
        """
        Detect if user is accessing unusually sensitive data.
        
        Indicator of T1213 - attackers target high-value data.
        """
        baseline = self._get_user_baseline(event.user)
        
        # Need sufficient baseline
        if baseline['total_accesses'] < 10:
            return None
        
        # Check if this sensitivity level is unusual
        sensitivity_counts = baseline['sensitivity_levels']
        
        # If user rarely accesses RESTRICTED/CONFIDENTIAL data
        if event.sensitivity in [DataSensitivity.RESTRICTED, DataSensitivity.CONFIDENTIAL]:
            high_sensitivity_count = (
                sensitivity_counts.get(DataSensitivity.RESTRICTED, 0) +
                sensitivity_counts.get(DataSensitivity.CONFIDENTIAL, 0)
            )
            
            # If less than 10% of accesses are to sensitive data
            if high_sensitivity_count / baseline['total_accesses'] < 0.1:
                return {
                    'type': 'SENSITIVITY_ANOMALY',
                    'severity': 'HIGH',
                    'technique': 'T1213 (Data from Information Repositories)',
                    'user': event.user,
                    'sensitivity': event.sensitivity.name,
                    'resource': event.resource,
                    'message': f'User {event.user} accessing {event.sensitivity.name} data (unusual for this user)'
                }
        
        return None
    
    def _detect_resource_type_anomaly(self, event: DataAccessEvent) -> Optional[Dict]:
        """
        Detect if user is accessing unusual types of data.
        
        Indicator of T1213 - attackers may access data types they don't normally use.
        """
        baseline = self._get_user_baseline(event.user)
        
        # Need sufficient baseline
        if baseline['total_accesses'] < 15:
            return None
        
        # Check if this resource type is new for this user
        if event.resource_type not in baseline['resource_types']:
            return {
                'type': 'RESOURCE_TYPE_ANOMALY',
                'severity': 'MEDIUM',
                'technique': 'T1213 (Data from Information Repositories)',
                'user': event.user,
                'resource_type': event.resource_type,
                'typical_types': sorted(list(baseline['resource_types'])),
                'message': f'User {event.user} accessing new resource type: {event.resource_type} (typical: {sorted(list(baseline["resource_types"]))})'
            }
        
        return None
    
    def record_access(
        self,
        user: str,
        resource: str,
        resource_type: str,
        sensitivity: DataSensitivity,
        size_bytes: int,
        ip_address: str,
        action: str = 'read'
    ) -> Tuple[bool, List[Dict]]:
        """
        Record a data access event and check for anomalies.
        
        Args:
            user: Username accessing the data
            resource: Resource identifier (file path, database table, etc.)
            resource_type: Type of resource (document, database, code, etc.)
            sensitivity: Data sensitivity level
            size_bytes: Size of data accessed
            ip_address: Source IP address
            action: Type of access (read, download, export, copy)
            
        Returns:
            Tuple of (allowed, alerts) where:
            - allowed: Whether the access should be permitted
            - alerts: List of alert dictionaries
        """
        # Create event
        event = DataAccessEvent(
            timestamp=time.time(),
            user=user,
            resource=resource,
            resource_type=resource_type,
            sensitivity=sensitivity,
            size_bytes=size_bytes,
            ip_address=ip_address,
            action=action
        )
        
        # Store event
        self.events.append(event)
        
        # Update baseline
        self._update_baseline(event)
        
        # Run anomaly detection
        alerts = []
        
        # Check for various anomalies
        for detector in [
            self._detect_volume_anomaly,
            self._detect_velocity_anomaly,
            self._detect_time_anomaly,
            self._detect_sensitivity_anomaly,
            self._detect_resource_type_anomaly
        ]:
            alert = detector(event)
            if alert:
                alert['timestamp'] = datetime.fromtimestamp(event.timestamp).isoformat()
                alert['resource'] = resource
                alert['ip_address'] = ip_address
                alerts.append(alert)
                self.alerts.append(alert)
        
        # Determine if access should be blocked
        # In production, you might block on HIGH severity alerts
        high_severity_alerts = [a for a in alerts if a.get('severity') == 'HIGH']
        allowed = len(high_severity_alerts) == 0
        
        return allowed, alerts
    
    def get_user_report(self, user: str) -> Dict:
        """Generate a report of user's data access patterns."""
        baseline = self._get_user_baseline(user)
        user_events = [e for e in self.events if e.user == user]
        
        # Calculate statistics
        resource_type_counts = defaultdict(int)
        sensitivity_counts = defaultdict(int)
        
        for event in user_events:
            resource_type_counts[event.resource_type] += 1
            sensitivity_counts[event.sensitivity.name] += 1
        
        return {
            'user': user,
            'total_accesses': baseline['total_accesses'],
            'total_bytes': baseline['total_bytes'],
            'total_mb': round(baseline['total_bytes'] / 1024 / 1024, 2),
            'avg_accesses_per_day': round(baseline['avg_accesses_per_day'], 2),
            'resource_types': sorted(list(baseline['resource_types'])),
            'resource_type_counts': dict(resource_type_counts),
            'sensitivity_counts': dict(sensitivity_counts),
            'typical_hours': sorted(list(baseline['typical_hours'])),
            'alerts_triggered': len([a for a in self.alerts if a['user'] == user])
        }
    
    def get_security_dashboard(self) -> Dict:
        """Generate security dashboard with threat indicators."""
        return {
            'total_events': len(self.events),
            'total_alerts': len(self.alerts),
            'users_monitored': len(self.user_baselines),
            'high_severity_alerts': len([a for a in self.alerts if a.get('severity') == 'HIGH']),
            'alert_types': {
                alert_type: len([a for a in self.alerts if a['type'] == alert_type])
                for alert_type in set(a['type'] for a in self.alerts)
            },
            'recent_alerts': self.alerts[-10:]  # Last 10 alerts
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def simulate_normal_behavior(monitor: DataAccessMonitor):
    """Simulate normal user data access patterns."""
    print("\n" + "=" * 70)
    print("NORMAL USER BEHAVIOR")
    print("=" * 70)
    
    print("\nSimulating Alice's normal work pattern (1 week baseline)...")
    
    # Alice normally accesses documents and databases during business hours
    for day in range(7):
        for hour in range(9, 17):  # 9 AM to 5 PM
            # Simulate a few accesses per hour
            for _ in range(3):
                allowed, alerts = monitor.record_access(
                    user='alice',
                    resource=f'/documents/project_{day}_{hour}.docx',
                    resource_type='document',
                    sensitivity=DataSensitivity.INTERNAL,
                    size_bytes=50 * 1024,  # 50 KB
                    ip_address='192.168.1.100',
                    action='read'
                )
                time.sleep(0.001)  # Small delay
    
    print(f"✓ Created baseline: {monitor.user_baselines['alice']['total_accesses']} accesses")
    
    # Show Alice's baseline
    report = monitor.get_user_report('alice')
    print(f"  - Average accesses/day: {report['avg_accesses_per_day']}")
    print(f"  - Typical hours: {report['typical_hours']}")
    print(f"  - Resource types: {report['resource_types']}")


def simulate_data_exfiltration(monitor: DataAccessMonitor):
    """Simulate T1020 (Automated Exfiltration) attack."""
    print("\n" + "=" * 70)
    print("ATTACK SIMULATION: T1020 (Automated Exfiltration)")
    print("=" * 70)
    
    print("\nAttacker compromises Alice's account and attempts to exfiltrate data...")
    
    # Attacker uses automated tool to rapidly download files
    print("\n1. High-velocity access (automated tool):")
    for i in range(15):
        allowed, alerts = monitor.record_access(
            user='alice',
            resource=f'/confidential/data_{i}.pdf',
            resource_type='document',
            sensitivity=DataSensitivity.CONFIDENTIAL,
            size_bytes=500 * 1024,  # 500 KB
            ip_address='203.0.113.66',  # Attacker IP
            action='download'
        )
        
        if alerts:
            print(f"\n   🚨 ALERT TRIGGERED:")
            for alert in alerts:
                print(f"      [{alert['severity']}] {alert['type']}")
                print(f"      {alert['message']}")
            break
        
        time.sleep(0.01)
    
    # Attacker tries to access large volume
    print("\n2. Large volume access:")
    for i in range(5):
        allowed, alerts = monitor.record_access(
            user='alice',
            resource=f'/database/export_{i}.sql',
            resource_type='database',
            sensitivity=DataSensitivity.RESTRICTED,
            size_bytes=25 * 1024 * 1024,  # 25 MB
            ip_address='203.0.113.66',
            action='export'
        )
        
        if alerts:
            print(f"\n   🚨 ALERT TRIGGERED:")
            for alert in alerts:
                print(f"      [{alert['severity']}] {alert['type']}")
                print(f"      {alert['message']}")
        
        time.sleep(0.1)


def simulate_insider_threat(monitor: DataAccessMonitor):
    """Simulate T1213 (Data from Information Repositories) by insider."""
    print("\n" + "=" * 70)
    print("ATTACK SIMULATION: T1213 (Insider Threat)")
    print("=" * 70)
    
    print("\nInsider (Bob) accessing sensitive data outside normal patterns...")
    
    # Create baseline for Bob
    print("\n1. Establishing Bob's baseline (normal developer):")
    for _ in range(20):
        monitor.record_access(
            user='bob',
            resource='/code/src/main.py',
            resource_type='source_code',
            sensitivity=DataSensitivity.INTERNAL,
            size_bytes=10 * 1024,
            ip_address='192.168.1.101',
            action='read'
        )
        time.sleep(0.001)
    
    print(f"   ✓ Baseline: {monitor.user_baselines['bob']['total_accesses']} accesses")
    
    # Bob (insider) starts accessing sensitive financial data at night
    print("\n2. Bob accessing unusual data types at unusual hours:")
    
    # Simulate night time (hour 23 = 11 PM)
    current_time = time.time()
    night_time = current_time - (datetime.fromtimestamp(current_time).hour * 3600) + (23 * 3600)
    
    # Temporarily modify timestamp for demo
    original_time = time.time
    time.time = lambda: night_time
    
    allowed, alerts = monitor.record_access(
        user='bob',
        resource='/finance/salaries_2024.xlsx',
        resource_type='spreadsheet',
        sensitivity=DataSensitivity.RESTRICTED,
        size_bytes=2 * 1024 * 1024,
        ip_address='192.168.1.101',
        action='download'
    )
    
    # Restore time function
    time.time = original_time
    
    if alerts:
        print(f"\n   🚨 ALERTS TRIGGERED:")
        for alert in alerts:
            print(f"      [{alert['severity']}] {alert['type']}")
            print(f"      {alert['message']}")


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1213 & T1020 - Data Access Monitoring Demo")
    print("=" * 70)
    print("\nThis demo shows how to detect data exfiltration and unauthorized")
    print("data access through behavioral monitoring.")
    
    # Create monitor
    monitor = DataAccessMonitor(
        alert_volume_multiplier=3.0,
        alert_velocity_threshold=10,
        max_size_per_hour_mb=100,
        business_hours=(8, 18)
    )
    
    # Run simulations
    simulate_normal_behavior(monitor)
    simulate_data_exfiltration(monitor)
    simulate_insider_threat(monitor)
    
    # Show security dashboard
    print("\n" + "=" * 70)
    print("SECURITY DASHBOARD")
    print("=" * 70)
    
    dashboard = monitor.get_security_dashboard()
    print(f"\nTotal Events: {dashboard['total_events']}")
    print(f"Total Alerts: {dashboard['total_alerts']}")
    print(f"High Severity: {dashboard['high_severity_alerts']}")
    
    print("\nAlert Types:")
    for alert_type, count in dashboard['alert_types'].items():
        print(f"  - {alert_type}: {count}")
    
    # Summary
    print("\n" + "=" * 70)
    print("KEY DEFENSES AGAINST T1213 & T1020:")
    print("=" * 70)
    print("1. ✅ Monitor data access patterns and establish baselines")
    print("2. ✅ Detect velocity anomalies (automated exfiltration)")
    print("3. ✅ Detect volume anomalies (large data transfers)")
    print("4. ✅ Alert on unusual access times (after hours)")
    print("5. ✅ Monitor access to sensitive data")
    print("6. ✅ Detect access to unusual resource types")
    print("7. ✅ Implement DLP (Data Loss Prevention) controls")
    print("8. ✅ Rate limit data export/download operations")
    print("9. ✅ Require additional authentication for sensitive data")
    print("10. ✅ Log and audit all data access events")
    print("=" * 70)
