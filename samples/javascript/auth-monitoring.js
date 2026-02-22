/**
 * MITRE ATT&CK T1078: Valid Accounts - Authentication Monitoring
 * Educational demonstration of behavioral authentication monitoring
 * 
 * @description Detects misuse of valid credentials through behavioral analysis
 * @reference https://attack.mitre.org/techniques/T1078/
 */

const crypto = require('crypto');

// =============================================================================
// BEHAVIORAL BASELINE TRACKER
// =============================================================================

/**
 * SECURE: Tracks user behavioral baselines
 * Defense against ATT&CK T1078
 * 
 * @description Establishes normal patterns for detecting anomalies
 * @security Behavioral analysis, anomaly detection
 */
class UserBehaviorBaseline {
  constructor(username) {
    this.username = username;
    this.loginHours = []; // Typical login hours (0-23)
    this.locations = []; // Recent login locations
    this.deviceFingerprints = new Set(); // Known device fingerprints
    this.accessedResources = new Set(); // Resources user typically accesses
    this.privilegeLevel = 'user';
    this.lastLoginTime = null;
    this.lastLoginLocation = null;
  }

  updateBaseline(loginTime, location, deviceFp, accessedResource = null) {
    const loginDate = new Date(loginTime);
    this.loginHours.push(loginDate.getHours());
    
    // Keep only last 100 login hours
    if (this.loginHours.length > 100) {
      this.loginHours = this.loginHours.slice(-100);
    }
    
    this.locations.push(location);
    if (this.locations.length > 50) {
      this.locations = this.locations.slice(-50);
    }
    
    this.deviceFingerprints.add(deviceFp);
    
    if (accessedResource) {
      this.accessedResources.add(accessedResource);
    }
    
    this.lastLoginTime = loginTime;
    this.lastLoginLocation = location;
  }

  getTypicalHours() {
    if (this.loginHours.length < 5) {
      return new Set(Array.from({length: 24}, (_, i) => i));
    }
    
    // Count hour frequencies
    const hourCounts = {};
    for (const hour of this.loginHours) {
      hourCounts[hour] = (hourCounts[hour] || 0) + 1;
    }
    
    // Hours appearing in at least 20% of logins
    const threshold = this.loginHours.length * 0.2;
    return new Set(
      Object.entries(hourCounts)
        .filter(([_, count]) => count >= threshold)
        .map(([hour, _]) => parseInt(hour))
    );
  }

  isTypicalHour(loginTime) {
    const loginDate = new Date(loginTime);
    const typicalHours = this.getTypicalHours();
    return typicalHours.has(loginDate.getHours());
  }

  isKnownDevice(deviceFp) {
    return this.deviceFingerprints.has(deviceFp);
  }

  isTypicalLocation(location) {
    if (this.locations.length < 3) {
      return true;
    }
    
    // Location is typical if it appears in recent history
    return this.locations.slice(-10).includes(location);
  }
}

// =============================================================================
// AUTHENTICATION MONITOR
// =============================================================================

/**
 * SECURE: Authentication monitoring system
 * Defense against ATT&CK T1078
 * 
 * @description Detects account misuse through behavioral analysis
 * @security Impossible travel, device fingerprinting, anomaly detection
 */
class AuthenticationMonitor {
  constructor(options = {}) {
    this.config = {
      impossibleTravelThresholdKm: options.impossibleTravelThresholdKm || 500,
      impossibleTravelTimeHours: options.impossibleTravelTimeHours || 1,
      riskThresholdHigh: options.riskThresholdHigh || 0.7,
      riskThresholdCritical: options.riskThresholdCritical || 0.9,
      ...options
    };

    this.baselines = new Map(); // username -> UserBehaviorBaseline
    
    // Simple location coordinates (use real geolocation API in production)
    this.locationCoords = {
      'New York': [40.7128, -74.0060],
      'London': [51.5074, -0.1278],
      'Tokyo': [35.6762, 139.6503],
      'Sydney': [-33.8688, 151.2093],
      'Paris': [48.8566, 2.3522],
      'Los Angeles': [34.0522, -118.2437],
      'Mumbai': [19.0760, 72.8777],
      'Beijing': [39.9042, 116.4074]
    };
  }

  /**
   * Calculate distance between two locations using Haversine formula
   * @param {string} loc1 - First location
   * @param {string} loc2 - Second location
   * @returns {number} Distance in kilometers
   */
  calculateDistanceKm(loc1, loc2) {
    if (!this.locationCoords[loc1] || !this.locationCoords[loc2]) {
      return 0;
    }

    const [lat1, lon1] = this.locationCoords[loc1];
    const [lat2, lon2] = this.locationCoords[loc2];

    const R = 6371; // Earth radius in km
    
    const dLat = this.toRadians(lat2 - lat1);
    const dLon = this.toRadians(lon2 - lon1);
    
    const a = Math.sin(dLat / 2) ** 2 +
              Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) *
              Math.sin(dLon / 2) ** 2;
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    
    return R * c;
  }

  toRadians(degrees) {
    return degrees * Math.PI / 180;
  }

  /**
   * Generate device fingerprint
   * @param {string} userAgent - Browser user agent
   * @param {string} ipAddress - IP address
   * @returns {string} Device fingerprint
   */
  generateDeviceFingerprint(userAgent, ipAddress) {
    return crypto.createHash('md5')
      .update(`${userAgent}:${ipAddress}`)
      .digest('hex')
      .substring(0, 16);
  }

  /**
   * Get or create behavioral baseline for user
   * @param {string} username - Username
   * @returns {UserBehaviorBaseline} Baseline object
   */
  getOrCreateBaseline(username) {
    if (!this.baselines.has(username)) {
      this.baselines.set(username, new UserBehaviorBaseline(username));
    }
    return this.baselines.get(username);
  }

  /**
   * Check authentication for anomalies
   * @param {object} authRequest - Authentication request details
   * @returns {object} Result with allowed flag, reason, risk score, and anomalies
   */
  checkAuthentication({
    username,
    location,
    userAgent,
    ipAddress,
    privilegeRequested = 'user',
    accessedResource = null
  }) {
    const currentTime = Date.now();
    const baseline = this.getOrCreateBaseline(username);
    const deviceFp = this.generateDeviceFingerprint(userAgent, ipAddress);
    
    let riskScore = 0;
    const anomalies = [];

    // Check 1: Impossible travel detection
    if (baseline.lastLoginLocation && baseline.lastLoginTime) {
      const timeDiffHours = (currentTime - baseline.lastLoginTime) / (1000 * 60 * 60);
      const distanceKm = this.calculateDistanceKm(baseline.lastLoginLocation, location);
      
      if (timeDiffHours < this.config.impossibleTravelTimeHours && 
          distanceKm > this.config.impossibleTravelThresholdKm) {
        riskScore += 0.5;
        anomalies.push(
          `Impossible travel: ${distanceKm.toFixed(0)}km in ${timeDiffHours.toFixed(1)}h ` +
          `(${baseline.lastLoginLocation} → ${location})`
        );
      }
    }

    // Check 2: Unknown device fingerprint
    if (!baseline.isKnownDevice(deviceFp)) {
      riskScore += 0.2;
      anomalies.push(`New device fingerprint: ${deviceFp}`);
    }

    // Check 3: Unusual login time
    if (!baseline.isTypicalHour(currentTime)) {
      riskScore += 0.15;
      const loginHour = new Date(currentTime).getHours();
      anomalies.push(`Unusual login hour: ${loginHour}:00`);
    }

    // Check 4: Atypical location
    if (!baseline.isTypicalLocation(location)) {
      riskScore += 0.15;
      anomalies.push(`Atypical location: ${location}`);
    }

    // Check 5: Privilege escalation
    if (privilegeRequested !== baseline.privilegeLevel) {
      if (['admin', 'root', 'superuser'].includes(privilegeRequested)) {
        riskScore += 0.3;
        anomalies.push(
          `Privilege escalation: ${baseline.privilegeLevel} → ${privilegeRequested}`
        );
      }
    }

    // Check 6: Never-before-accessed resource
    if (accessedResource && !baseline.accessedResources.has(accessedResource)) {
      riskScore += 0.1;
      anomalies.push(`New resource access: ${accessedResource}`);
    }

    // Determine if authentication should be allowed
    let allowed = true;
    let reason = 'Authentication allowed';

    if (riskScore >= this.config.riskThresholdCritical) {
      allowed = false;
      reason = `CRITICAL RISK (T1078): Score ${riskScore.toFixed(2)} - BLOCKED`;
    } else if (riskScore >= this.config.riskThresholdHigh) {
      reason = `HIGH RISK (T1078): Score ${riskScore.toFixed(2)} - Requires MFA/step-up auth`;
    } else if (riskScore > 0) {
      reason = `MODERATE RISK (T1078): Score ${riskScore.toFixed(2)} - Monitoring`;
    }

    // Update baseline if allowed (learning from successful logins)
    if (allowed && riskScore < this.config.riskThresholdHigh) {
      baseline.updateBaseline(currentTime, location, deviceFp, accessedResource);
    }

    console.log(`🔐 Auth check for ${username}: ${reason}`);
    if (anomalies.length > 0) {
      console.log('   Anomalies:', anomalies);
    }

    return {
      allowed,
      reason,
      riskScore,
      anomalies
    };
  }
}

// =============================================================================
// VULNERABLE IMPLEMENTATION (DO NOT USE IN PRODUCTION)
// =============================================================================

/**
 * VULNERABLE: Simple authentication with no monitoring
 * 
 * Issues:
 * - No behavioral analysis
 * - No anomaly detection
 * - Attacker with valid credentials has unlimited access
 * - Cannot detect account misuse
 * 
 * ATT&CK T1078: Attacker can use stolen credentials freely
 */
function vulnerableSimpleAuth(username, password) {
  const validUsers = {
    'alice': 'pass123',
    'bob': 'secret456'
  };
  
  return validUsers[username] === password;
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1078: Valid Accounts - Authentication Monitoring Demo');
  console.log('='.repeat(80));
  console.log('\nDetecting misuse of valid credentials through behavioral analysis\n');

  const monitor = new AuthenticationMonitor({
    impossibleTravelThresholdKm: 500,
    impossibleTravelTimeHours: 1,
    riskThresholdHigh: 0.7,
    riskThresholdCritical: 0.9
  });

  // Scenario 1: Establish baseline (normal behavior)
  console.log('--- Scenario 1: Establishing Baseline (Normal Behavior) ---\n');
  
  for (let day = 0; day < 5; day++) {
    const result = monitor.checkAuthentication({
      username: 'alice',
      location: 'New York',
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
      ipAddress: '192.168.1.100',
      accessedResource: '/dashboard'
    });
    console.log(`Day ${day + 1}: Risk ${result.riskScore.toFixed(2)}`);
  }

  // Scenario 2: Impossible travel attack
  console.log('\n--- Scenario 2: Impossible Travel Attack (T1078) ---\n');
  
  monitor.checkAuthentication({
    username: 'alice',
    location: 'New York',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    ipAddress: '192.168.1.100'
  });
  
  console.log('(10 minutes pass...)\n');
  
  const impossibleTravelResult = monitor.checkAuthentication({
    username: 'alice',
    location: 'Tokyo',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    ipAddress: '203.0.113.50'
  });

  // Scenario 3: Device change attack
  console.log('\n--- Scenario 3: Device Change Attack (T1078) ---\n');
  
  const deviceChangeResult = monitor.checkAuthentication({
    username: 'alice',
    location: 'New York',
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ipAddress: '198.51.100.75',
    accessedResource: '/admin/users'
  });

  // Scenario 4: Privilege escalation
  console.log('\n--- Scenario 4: Privilege Escalation (T1078) ---\n');
  
  const privEscResult = monitor.checkAuthentication({
    username: 'alice',
    location: 'New York',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    ipAddress: '192.168.1.100',
    privilegeRequested: 'admin',
    accessedResource: '/admin/system-config'
  });

  console.log('\n' + '='.repeat(80));
  console.log('Detection mechanisms demonstrated:');
  console.log('  ✅ Impossible travel detection (geolocation anomalies)');
  console.log('  ✅ Device fingerprint tracking');
  console.log('  ✅ Behavioral baseline establishment');
  console.log('  ✅ Privilege escalation monitoring');
  console.log('  ✅ Risk-based authentication decisions');
  console.log('  ✅ Anomalous resource access detection');
  console.log('='.repeat(80));
}

module.exports = {
  AuthenticationMonitor,
  UserBehaviorBaseline
};
