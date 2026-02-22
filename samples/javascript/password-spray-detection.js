/**
 * MITRE ATT&CK T1110.003: Password Spraying - Detection and Prevention
 * Educational demonstration of password spray attack detection
 * 
 * @description Detects password spraying patterns across multiple accounts
 * @reference https://attack.mitre.org/techniques/T1110/003/
 */

const crypto = require('crypto');

// =============================================================================
// PASSWORD SPRAY DETECTOR
// =============================================================================

/**
 * SECURE: Password spray detection system
 * Defense against ATT&CK T1110.003
 * 
 * @description Detects spray attacks by analyzing cross-account patterns
 * @security Cross-account analysis, distributed attack detection, timing analysis
 */
class PasswordSprayDetector {
  constructor(options = {}) {
    this.config = {
      sprayThresholdAccounts: options.sprayThresholdAccounts || 5,
      sprayTimeWindowMs: options.sprayTimeWindowMs || 5 * 60 * 1000, // 5 minutes
      maxFailuresPerIP: options.maxFailuresPerIP || 20,
      ipBlockDurationMs: options.ipBlockDurationMs || 30 * 60 * 1000, // 30 minutes
      slowSprayWindowHours: options.slowSprayWindowHours || 24,
      slowSprayThreshold: options.slowSprayThreshold || 10,
      ...options
    };

    // Track password attempts: passwordHash -> [{timestamp, username, ip}, ...]
    this.passwordAttempts = new Map();
    
    // Track IP attempts: ip -> [{timestamp, username, passwordHash}, ...]
    this.ipAttempts = new Map();
    
    // Blocked IPs: ip -> blockUntilTimestamp
    this.blockedIPs = new Map();
    
    // IP reputation: ip -> score (0.0 = good, 1.0 = malicious)
    this.ipReputation = new Map();
    
    // Progressive delays: ip -> delaySeconds
    this.progressiveDelays = new Map();
  }

  /**
   * Hash password for pattern detection
   * @param {string} password - Password to hash
   * @returns {string} Password hash
   */
  hashPassword(password) {
    return crypto.createHash('sha256')
      .update(password)
      .digest('hex')
      .substring(0, 16);
  }

  /**
   * Clean old attempts from tracking
   * @param {number} now - Current timestamp
   */
  cleanOldAttempts(now) {
    const cutoffShort = now - this.config.sprayTimeWindowMs;
    const cutoffLong = now - (this.config.slowSprayWindowHours * 60 * 60 * 1000);

    // Clean password attempts
    for (const [hash, attempts] of this.passwordAttempts.entries()) {
      const recent = attempts.filter(a => a.timestamp > cutoffShort);
      if (recent.length === 0) {
        this.passwordAttempts.delete(hash);
      } else {
        this.passwordAttempts.set(hash, recent);
      }
    }

    // Clean IP attempts
    for (const [ip, attempts] of this.ipAttempts.entries()) {
      const recent = attempts.filter(a => a.timestamp > cutoffLong);
      if (recent.length === 0) {
        this.ipAttempts.delete(ip);
      } else {
        this.ipAttempts.set(ip, recent);
      }
    }

    // Clean expired blocks
    for (const [ip, blockUntil] of this.blockedIPs.entries()) {
      if (now >= blockUntil) {
        this.blockedIPs.delete(ip);
        this.progressiveDelays.set(ip, 0);
      }
    }
  }

  /**
   * Detect password spray pattern
   * @param {string} passwordHash - Password hash
   * @param {number} now - Current timestamp
   * @returns {object} Detection result
   */
  detectSprayPattern(passwordHash, now) {
    const attempts = this.passwordAttempts.get(passwordHash) || [];
    const recent = attempts.filter(
      a => now - a.timestamp <= this.config.sprayTimeWindowMs
    );

    const uniqueUsernames = new Set(recent.map(a => a.username));
    const isSpray = uniqueUsernames.size >= this.config.sprayThresholdAccounts;

    return {
      isSpray,
      accountCount: uniqueUsernames.size,
      usernames: Array.from(uniqueUsernames)
    };
  }

  /**
   * Detect slow-and-low spray attack
   * @param {string} ip - IP address
   * @param {number} now - Current timestamp
   * @returns {object} Detection result
   */
  detectSlowSpray(ip, now) {
    const attempts = this.ipAttempts.get(ip) || [];
    const cutoff = now - (this.config.slowSprayWindowHours * 60 * 60 * 1000);
    const recent = attempts.filter(a => a.timestamp > cutoff);

    const uniqueAccounts = new Set(recent.map(a => a.username));
    const isSlowSpray = uniqueAccounts.size >= this.config.slowSprayThreshold;

    return {
      isSlowSpray,
      accountCount: uniqueAccounts.size
    };
  }

  /**
   * Detect distributed spray attack
   * @param {string} passwordHash - Password hash
   * @param {number} now - Current timestamp
   * @returns {object} Detection result
   */
  detectDistributedSpray(passwordHash, now) {
    const attempts = this.passwordAttempts.get(passwordHash) || [];
    const recent = attempts.filter(
      a => now - a.timestamp <= this.config.sprayTimeWindowMs
    );

    const uniqueIPs = new Set(recent.map(a => a.ip));
    const isDistributed = uniqueIPs.size >= 3 && 
                         recent.length >= this.config.sprayThresholdAccounts;

    return {
      isDistributed,
      ipCount: uniqueIPs.size,
      ips: Array.from(uniqueIPs)
    };
  }

  /**
   * Check if IP is blocked
   * @param {string} ip - IP address
   * @param {number} now - Current timestamp
   * @returns {boolean} True if blocked
   */
  isIPBlocked(ip, now) {
    const blockUntil = this.blockedIPs.get(ip);
    return blockUntil && now < blockUntil;
  }

  /**
   * Block an IP address
   * @param {string} ip - IP address
   * @param {number} now - Current timestamp
   */
  blockIP(ip, now) {
    this.blockedIPs.set(ip, now + this.config.ipBlockDurationMs);
    const currentRep = this.ipReputation.get(ip) || 0;
    this.ipReputation.set(ip, Math.min(1.0, currentRep + 0.3));
    console.log(`🚫 Blocked IP ${ip} for ${this.config.ipBlockDurationMs / 60000} minutes`);
  }

  /**
   * Apply progressive delay
   * @param {string} ip - IP address
   * @returns {number} Delay in seconds
   */
  applyProgressiveDelay(ip) {
    const currentDelay = this.progressiveDelays.get(ip) || 0.5;
    const newDelay = Math.min(16.0, currentDelay * 2);
    this.progressiveDelays.set(ip, newDelay);
    return newDelay;
  }

  /**
   * Check login attempt for spray patterns
   * @param {string} username - Account username
   * @param {string} password - Password being attempted
   * @param {string} ipAddress - Source IP address
   * @returns {object} Result with allowed flag, reason, and delay
   */
  checkLoginAttempt(username, password, ipAddress) {
    const now = Date.now();
    
    this.cleanOldAttempts(now);

    // Check if IP is blocked
    if (this.isIPBlocked(ipAddress, now)) {
      console.log(`🛡️  BLOCKED: IP ${ipAddress} is blocked`);
      return {
        allowed: false,
        reason: 'ip_blocked',
        delay: null
      };
    }

    // Hash password for pattern analysis
    const passwordHash = this.hashPassword(password);

    // Record this attempt
    if (!this.passwordAttempts.has(passwordHash)) {
      this.passwordAttempts.set(passwordHash, []);
    }
    this.passwordAttempts.get(passwordHash).push({
      timestamp: now,
      username,
      ip: ipAddress
    });

    if (!this.ipAttempts.has(ipAddress)) {
      this.ipAttempts.set(ipAddress, []);
    }
    this.ipAttempts.get(ipAddress).push({
      timestamp: now,
      username,
      passwordHash
    });

    // Detect spray pattern
    const sprayResult = this.detectSprayPattern(passwordHash, now);
    if (sprayResult.isSpray) {
      this.blockIP(ipAddress, now);
      console.log(`🛡️  SPRAY ATTACK: Password tried on ${sprayResult.accountCount} accounts`);
      return {
        allowed: false,
        reason: 'spray_detected',
        accountCount: sprayResult.accountCount
      };
    }

    // Detect distributed spray
    const distributedResult = this.detectDistributedSpray(passwordHash, now);
    if (distributedResult.isDistributed) {
      distributedResult.ips.forEach(ip => this.blockIP(ip, now));
      console.log(`🛡️  DISTRIBUTED SPRAY: Password from ${distributedResult.ipCount} IPs`);
      return {
        allowed: false,
        reason: 'distributed_spray',
        ipCount: distributedResult.ipCount
      };
    }

    // Detect slow spray
    const slowSprayResult = this.detectSlowSpray(ipAddress, now);
    if (slowSprayResult.isSlowSpray) {
      this.blockIP(ipAddress, now);
      console.log(`🛡️  SLOW SPRAY: ${slowSprayResult.accountCount} accounts over ${this.config.slowSprayWindowHours}h`);
      return {
        allowed: false,
        reason: 'slow_spray',
        accountCount: slowSprayResult.accountCount
      };
    }

    // Check IP failure count
    const recentFailures = (this.ipAttempts.get(ipAddress) || [])
      .filter(a => now - a.timestamp <= this.config.sprayTimeWindowMs).length;

    if (recentFailures >= this.config.maxFailuresPerIP) {
      this.blockIP(ipAddress, now);
      console.log(`🛡️  TOO MANY FAILURES: ${recentFailures} from ${ipAddress}`);
      return {
        allowed: false,
        reason: 'rate_limit',
        failures: recentFailures
      };
    }

    // Apply progressive delay
    const delay = this.applyProgressiveDelay(ipAddress);

    // Warning if approaching threshold
    if (sprayResult.accountCount >= this.config.sprayThresholdAccounts - 2) {
      console.log(`⚠️  WARNING: Approaching spray threshold (${sprayResult.accountCount}/${this.config.sprayThresholdAccounts})`);
    }

    console.log(`✅ Login allowed: ${username} from ${ipAddress} (delay: ${delay.toFixed(1)}s)`);

    return {
      allowed: true,
      delay,
      ipReputation: this.ipReputation.get(ipAddress) || 0
    };
  }

  /**
   * Record successful login
   * @param {string} username - Username
   * @param {string} ipAddress - IP address
   */
  recordSuccessfulLogin(username, ipAddress) {
    const currentRep = this.ipReputation.get(ipAddress) || 0;
    this.ipReputation.set(ipAddress, Math.max(0, currentRep - 0.1));
    this.progressiveDelays.set(ipAddress, 0);
    console.log(`✅ Successful login: ${username} from ${ipAddress}`);
  }

  /**
   * Get security statistics
   * @returns {object} Statistics
   */
  getStats() {
    return {
      blockedIPs: this.blockedIPs.size,
      trackedPasswordPatterns: this.passwordAttempts.size,
      trackedIPs: this.ipAttempts.size,
      highRiskIPs: Array.from(this.ipReputation.entries())
        .filter(([_, score]) => score > 0.5)
        .length
    };
  }
}

// =============================================================================
// VULNERABLE IMPLEMENTATION (DO NOT USE IN PRODUCTION)
// =============================================================================

/**
 * VULNERABLE: Auth with only per-account rate limiting
 * 
 * Issues:
 * - No cross-account analysis
 * - No password pattern detection
 * - Attacker can spray passwords across accounts
 * - No distributed attack detection
 * 
 * ATT&CK T1110.003: Attacker can spray passwords
 */
function vulnerableAuthNoSprayDetection(username, password, ip) {
  const validUsers = {
    'user1': 'password',
    'user2': 'password',
    'user3': 'password'
  };
  
  return validUsers[username] === password;
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1110.003: Password Spraying Detection Demo');
  console.log('='.repeat(80));
  console.log('\nDetecting password spray attacks across multiple accounts\n');

  const detector = new PasswordSprayDetector({
    sprayThresholdAccounts: 5,
    sprayTimeWindowMs: 5 * 60 * 1000,
    maxFailuresPerIP: 20,
    ipBlockDurationMs: 30 * 60 * 1000,
    slowSprayWindowHours: 24,
    slowSprayThreshold: 10
  });

  // Scenario 1: Normal failed logins
  console.log('--- Scenario 1: Normal Failed Logins ---\n');
  
  detector.checkLoginAttempt('alice', 'wrong1', '192.168.1.100');
  detector.checkLoginAttempt('alice', 'wrong2', '192.168.1.100');
  detector.checkLoginAttempt('bob', 'incorrect', '192.168.1.101');

  // Scenario 2: Password spray attack
  console.log('\n--- Scenario 2: Password Spray Attack (T1110.003) ---\n');
  console.log('Attacker trying "Summer2024!" across multiple accounts...\n');
  
  const attackerIP = '203.0.113.66';
  const commonPassword = 'Summer2024!';
  const targetAccounts = [
    'alice', 'bob', 'charlie', 'david', 'eve', 'frank', 'grace', 'henry'
  ];

  for (let i = 0; i < targetAccounts.length; i++) {
    const result = detector.checkLoginAttempt(
      targetAccounts[i],
      commonPassword,
      attackerIP
    );
    
    if (!result.allowed) {
      console.log(`\nAttack detected after ${i + 1} attempts!`);
      break;
    }
  }

  // Scenario 3: Distributed spray
  console.log('\n--- Scenario 3: Distributed Password Spray (T1110.003) ---\n');
  console.log('Attacker using multiple IPs...\n');
  
  const attackerIPs = ['198.51.100.10', '198.51.100.11', '198.51.100.12'];
  const targets = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6'];

  for (let i = 0; i < targets.length; i++) {
    const ip = attackerIPs[i % attackerIPs.length];
    const result = detector.checkLoginAttempt(
      targets[i],
      'Winter2024!',
      ip
    );
    
    if (!result.allowed) {
      console.log(`\nDistributed attack detected after ${i + 1} attempts!`);
      break;
    }
  }

  // Scenario 4: Slow spray
  console.log('\n--- Scenario 4: Slow Password Spray (T1110.003) ---\n');
  console.log('Attacker trying many accounts slowly...\n');
  
  const slowAttackerIP = '10.0.0.50';
  
  for (let i = 0; i < 12; i++) {
    const result = detector.checkLoginAttempt(
      `user${i + 1}`,
      'CommonPass123',
      slowAttackerIP
    );
    
    if (!result.allowed) {
      console.log(`\nSlow spray detected after ${i + 1} attempts!`);
      break;
    }
  }

  // Statistics
  console.log('\n--- Statistics ---\n');
  const stats = detector.getStats();
  console.log('Blocked IPs:', stats.blockedIPs);
  console.log('Tracked Password Patterns:', stats.trackedPasswordPatterns);
  console.log('High Risk IPs:', stats.highRiskIPs);

  console.log('\n' + '='.repeat(80));
  console.log('Detection mechanisms demonstrated:');
  console.log('  ✅ Cross-account password pattern detection');
  console.log('  ✅ Distributed spray detection (multiple IPs)');
  console.log('  ✅ Slow-and-low spray detection');
  console.log('  ✅ Progressive delays and IP blocking');
  console.log('  ✅ IP reputation tracking');
  console.log('='.repeat(80));
}

module.exports = {
  PasswordSprayDetector
};
