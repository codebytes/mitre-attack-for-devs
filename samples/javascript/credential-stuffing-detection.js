/**
 * MITRE ATT&CK T1110.004: Credential Stuffing - Detection and Prevention
 * Educational demonstration of credential stuffing attack detection
 * 
 * @description Detects credential stuffing patterns via rate limiting and behavioral analysis
 * @reference https://attack.mitre.org/techniques/T1110/004/
 */

const crypto = require('crypto');

// =============================================================================
// CREDENTIAL STUFFING DETECTOR
// =============================================================================

/**
 * SECURE: Credential stuffing detection system
 * Defense against ATT&CK T1110.004
 * 
 * @description Detects and blocks credential stuffing attacks using multiple signals
 * @security Rate limiting, distributed attack detection, bot detection
 */
class CredentialStuffingDetector {
  constructor(options = {}) {
    this.config = {
      // Rate limits
      maxAttemptsPerIP: options.maxAttemptsPerIP || 5,
      maxAttemptsPerAccount: options.maxAttemptsPerAccount || 3,
      windowMs: options.windowMs || 15 * 60 * 1000, // 15 minutes
      
      // Distributed attack detection
      maxFailedAccountsPerIP: options.maxFailedAccountsPerIP || 10,
      distributedWindowMs: options.distributedWindowMs || 60 * 60 * 1000, // 1 hour
      
      // Bot detection
      minRequestInterval: options.minRequestInterval || 500, // milliseconds
      maxBurstRequests: options.maxBurstRequests || 3,
      
      // Blocking
      blockDurationMs: options.blockDurationMs || 60 * 60 * 1000, // 1 hour
      
      ...options
    };

    // In-memory tracking (use Redis in production)
    this.ipAttempts = new Map(); // IP -> attempts array
    this.accountAttempts = new Map(); // account -> attempts array
    this.ipAccountFailures = new Map(); // IP -> Set of failed accounts
    this.blockedIPs = new Map(); // IP -> block expiry time
    this.blockedAccounts = new Map(); // account -> block expiry time
    this.requestTimestamps = new Map(); // IP -> timestamps array
  }

  /**
   * Checks if login attempt is allowed
   * @param {string} ipAddress - Client IP address
   * @param {string} username - Account username
   * @param {object} metadata - Additional request metadata
   * @returns {object} Result with allowed flag and reason
   */
  checkLoginAttempt(ipAddress, username, metadata = {}) {
    const now = Date.now();
    
    // Clean up old data
    this.cleanup(now);

    // Check 1: Is IP blocked?
    if (this.isIPBlocked(ipAddress, now)) {
      console.log(`🛡️  BLOCKED: IP ${ipAddress} is temporarily blocked`);
      return {
        allowed: false,
        reason: 'ip_blocked',
        retryAfter: this.blockedIPs.get(ipAddress) - now
      };
    }

    // Check 2: Is account blocked?
    if (this.isAccountBlocked(username, now)) {
      console.log(`🛡️  BLOCKED: Account ${username} is temporarily blocked`);
      return {
        allowed: false,
        reason: 'account_blocked',
        retryAfter: this.blockedAccounts.get(username) - now
      };
    }

    // Check 3: Bot detection (rapid requests)
    const botScore = this.detectBot(ipAddress, now);
    if (botScore > 0.7) {
      console.log(`🛡️  BLOCKED: Bot detected from IP ${ipAddress} (score: ${botScore.toFixed(2)})`);
      this.blockIP(ipAddress, now);
      return {
        allowed: false,
        reason: 'bot_detected',
        botScore
      };
    }

    // Check 4: Rate limit per IP
    const ipAttemptCount = this.getRecentAttempts(this.ipAttempts, ipAddress, now);
    if (ipAttemptCount >= this.config.maxAttemptsPerIP) {
      console.log(`🛡️  BLOCKED: Too many attempts from IP ${ipAddress} (${ipAttemptCount}/${this.config.maxAttemptsPerIP})`);
      this.blockIP(ipAddress, now);
      return {
        allowed: false,
        reason: 'rate_limit_ip',
        attempts: ipAttemptCount
      };
    }

    // Check 5: Rate limit per account
    const accountAttemptCount = this.getRecentAttempts(this.accountAttempts, username, now);
    if (accountAttemptCount >= this.config.maxAttemptsPerAccount) {
      console.log(`🛡️  BLOCKED: Too many attempts for account ${username} (${accountAttemptCount}/${this.config.maxAttemptsPerAccount})`);
      this.blockAccount(username, now);
      return {
        allowed: false,
        reason: 'rate_limit_account',
        attempts: accountAttemptCount
      };
    }

    // Check 6: Distributed credential stuffing (many accounts from one IP)
    const failedAccountsCount = this.getFailedAccountsCount(ipAddress, now);
    if (failedAccountsCount >= this.config.maxFailedAccountsPerIP) {
      console.log(`🛡️  BLOCKED: Distributed credential stuffing detected from IP ${ipAddress} (${failedAccountsCount} accounts)`);
      this.blockIP(ipAddress, now);
      return {
        allowed: false,
        reason: 'distributed_attack',
        failedAccounts: failedAccountsCount
      };
    }

    console.log(`✅ Login attempt allowed: IP=${ipAddress}, User=${username}`);
    
    return {
      allowed: true,
      ipAttempts: ipAttemptCount + 1,
      accountAttempts: accountAttemptCount + 1,
      failedAccounts: failedAccountsCount,
      botScore
    };
  }

  /**
   * Records a failed login attempt
   * @param {string} ipAddress - Client IP address
   * @param {string} username - Account username
   * @param {object} metadata - Additional metadata
   */
  recordFailedAttempt(ipAddress, username, metadata = {}) {
    const now = Date.now();

    // Record attempt for IP
    if (!this.ipAttempts.has(ipAddress)) {
      this.ipAttempts.set(ipAddress, []);
    }
    this.ipAttempts.get(ipAddress).push({ timestamp: now, username, success: false });

    // Record attempt for account
    if (!this.accountAttempts.has(username)) {
      this.accountAttempts.set(username, []);
    }
    this.accountAttempts.get(username).push({ timestamp: now, ipAddress, success: false });

    // Record failed account for distributed attack detection
    if (!this.ipAccountFailures.has(ipAddress)) {
      this.ipAccountFailures.set(ipAddress, []);
    }
    this.ipAccountFailures.get(ipAddress).push({ timestamp: now, username });

    // Record request timestamp for bot detection
    if (!this.requestTimestamps.has(ipAddress)) {
      this.requestTimestamps.set(ipAddress, []);
    }
    this.requestTimestamps.get(ipAddress).push(now);

    console.log(`❌ Failed login recorded: IP=${ipAddress}, User=${username}`);
  }

  /**
   * Records a successful login attempt
   * @param {string} ipAddress - Client IP address
   * @param {string} username - Account username
   */
  recordSuccessfulAttempt(ipAddress, username) {
    const now = Date.now();

    // Clear attempts for this account (successful login resets counter)
    this.accountAttempts.delete(username);
    
    // Don't clear IP attempts (could still be attacking other accounts)
    
    console.log(`✅ Successful login recorded: IP=${ipAddress}, User=${username}`);
  }

  /**
   * Detects bot behavior based on request timing
   * @param {string} ipAddress - Client IP address
   * @param {number} now - Current timestamp
   * @returns {number} Bot score (0-1, higher = more likely bot)
   */
  detectBot(ipAddress, now) {
    const timestamps = this.requestTimestamps.get(ipAddress) || [];
    
    if (timestamps.length < 2) {
      return 0;
    }

    // Get recent timestamps (last 30 seconds)
    const recentTimestamps = timestamps.filter(ts => now - ts < 30000);
    
    if (recentTimestamps.length < 2) {
      return 0;
    }

    let botScore = 0;

    // Signal 1: Too many requests in burst
    if (recentTimestamps.length >= this.config.maxBurstRequests) {
      botScore += 0.5;
      console.log(`⚠️  Burst detected: ${recentTimestamps.length} requests in 30s`);
    }

    // Signal 2: Suspiciously consistent timing (bots often have regular intervals)
    const intervals = [];
    for (let i = 1; i < recentTimestamps.length; i++) {
      intervals.push(recentTimestamps[i] - recentTimestamps[i - 1]);
    }

    if (intervals.length >= 3) {
      const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
      const variance = intervals.reduce((sum, interval) => {
        return sum + Math.pow(interval - avgInterval, 2);
      }, 0) / intervals.length;
      const stdDev = Math.sqrt(variance);

      // Low variance = suspiciously consistent = likely bot
      if (stdDev < 100) { // Less than 100ms variation
        botScore += 0.4;
        console.log(`⚠️  Suspicious timing pattern: stdDev=${stdDev.toFixed(2)}ms`);
      }
    }

    // Signal 3: Requests faster than minimum interval
    const tooFast = intervals.filter(i => i < this.config.minRequestInterval).length;
    if (tooFast > 0) {
      botScore += 0.3 * (tooFast / intervals.length);
      console.log(`⚠️  ${tooFast} requests faster than ${this.config.minRequestInterval}ms`);
    }

    return Math.min(botScore, 1.0);
  }

  /**
   * Gets count of recent attempts
   * @param {Map} attemptsMap - Map of attempts
   * @param {string} key - Key to check
   * @param {number} now - Current timestamp
   * @returns {number} Count of recent attempts
   */
  getRecentAttempts(attemptsMap, key, now) {
    const attempts = attemptsMap.get(key) || [];
    return attempts.filter(a => now - a.timestamp < this.config.windowMs).length;
  }

  /**
   * Gets count of unique failed accounts from an IP
   * @param {string} ipAddress - IP address
   * @param {number} now - Current timestamp
   * @returns {number} Count of unique failed accounts
   */
  getFailedAccountsCount(ipAddress, now) {
    const failures = this.ipAccountFailures.get(ipAddress) || [];
    const recentFailures = failures.filter(f => now - f.timestamp < this.config.distributedWindowMs);
    const uniqueAccounts = new Set(recentFailures.map(f => f.username));
    return uniqueAccounts.size;
  }

  /**
   * Checks if IP is blocked
   * @param {string} ipAddress - IP address
   * @param {number} now - Current timestamp
   * @returns {boolean} True if blocked
   */
  isIPBlocked(ipAddress, now) {
    const blockExpiry = this.blockedIPs.get(ipAddress);
    return blockExpiry && now < blockExpiry;
  }

  /**
   * Checks if account is blocked
   * @param {string} username - Account username
   * @param {number} now - Current timestamp
   * @returns {boolean} True if blocked
   */
  isAccountBlocked(username, now) {
    const blockExpiry = this.blockedAccounts.get(username);
    return blockExpiry && now < blockExpiry;
  }

  /**
   * Blocks an IP address
   * @param {string} ipAddress - IP address
   * @param {number} now - Current timestamp
   */
  blockIP(ipAddress, now) {
    this.blockedIPs.set(ipAddress, now + this.config.blockDurationMs);
    console.log(`🚫 IP ${ipAddress} blocked for ${this.config.blockDurationMs / 60000} minutes`);
  }

  /**
   * Blocks an account
   * @param {string} username - Account username
   * @param {number} now - Current timestamp
   */
  blockAccount(username, now) {
    this.blockedAccounts.set(username, now + this.config.blockDurationMs);
    console.log(`🚫 Account ${username} blocked for ${this.config.blockDurationMs / 60000} minutes`);
  }

  /**
   * Cleans up old data
   * @param {number} now - Current timestamp
   */
  cleanup(now) {
    // Clean up old attempts
    for (const [key, attempts] of this.ipAttempts.entries()) {
      const recent = attempts.filter(a => now - a.timestamp < this.config.windowMs);
      if (recent.length === 0) {
        this.ipAttempts.delete(key);
      } else {
        this.ipAttempts.set(key, recent);
      }
    }

    for (const [key, attempts] of this.accountAttempts.entries()) {
      const recent = attempts.filter(a => now - a.timestamp < this.config.windowMs);
      if (recent.length === 0) {
        this.accountAttempts.delete(key);
      } else {
        this.accountAttempts.set(key, recent);
      }
    }

    // Clean up old IP account failures
    for (const [key, failures] of this.ipAccountFailures.entries()) {
      const recent = failures.filter(f => now - f.timestamp < this.config.distributedWindowMs);
      if (recent.length === 0) {
        this.ipAccountFailures.delete(key);
      } else {
        this.ipAccountFailures.set(key, recent);
      }
    }

    // Clean up expired blocks
    for (const [ip, expiry] of this.blockedIPs.entries()) {
      if (now >= expiry) {
        this.blockedIPs.delete(ip);
      }
    }

    for (const [username, expiry] of this.blockedAccounts.entries()) {
      if (now >= expiry) {
        this.blockedAccounts.delete(username);
      }
    }

    // Clean up old request timestamps
    for (const [ip, timestamps] of this.requestTimestamps.entries()) {
      const recent = timestamps.filter(ts => now - ts < 60000); // Keep 1 minute
      if (recent.length === 0) {
        this.requestTimestamps.delete(ip);
      } else {
        this.requestTimestamps.set(ip, recent);
      }
    }
  }

  /**
   * Gets current statistics
   * @returns {object} Statistics
   */
  getStats() {
    return {
      trackedIPs: this.ipAttempts.size,
      trackedAccounts: this.accountAttempts.size,
      blockedIPs: this.blockedIPs.size,
      blockedAccounts: this.blockedAccounts.size
    };
  }
}

// =============================================================================
// EXPRESS MIDDLEWARE
// =============================================================================

/**
 * Creates Express middleware for credential stuffing detection
 * @param {CredentialStuffingDetector} detector - Detector instance
 * @returns {Function} Express middleware
 */
function createDetectionMiddleware(detector) {
  return (req, res, next) => {
    // Only apply to login endpoints
    if (req.path !== '/api/login' && req.path !== '/login') {
      return next();
    }

    const ipAddress = req.ip || req.connection?.remoteAddress || 'unknown';
    const username = req.body?.username || req.body?.email || 'unknown';

    // Check if attempt is allowed
    const result = detector.checkLoginAttempt(ipAddress, username, {
      userAgent: req.headers['user-agent'],
      referer: req.headers['referer']
    });

    if (!result.allowed) {
      // Attach detection result to request
      req.credentialStuffingBlocked = result;

      // Return 429 Too Many Requests
      return res.status(429).json({
        error: 'Too many attempts',
        reason: result.reason,
        retryAfter: result.retryAfter ? Math.ceil(result.retryAfter / 1000) : undefined
      });
    }

    // Attach detector to request for recording results later
    req.credentialStuffingDetector = detector;
    req.credentialStuffingContext = { ipAddress, username };

    next();
  };
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1110.004: Credential Stuffing Detection Demo');
  console.log('='.repeat(80));

  const detector = new CredentialStuffingDetector({
    maxAttemptsPerIP: 5,
    maxAttemptsPerAccount: 3,
    windowMs: 15 * 60 * 1000,
    maxFailedAccountsPerIP: 10,
    minRequestInterval: 500,
    maxBurstRequests: 3,
    blockDurationMs: 60 * 60 * 1000
  });

  console.log('\n--- Scenario 1: Normal Failed Logins ---\n');
  
  for (let i = 1; i <= 3; i++) {
    const result = detector.checkLoginAttempt('192.168.1.100', 'user@example.com');
    if (result.allowed) {
      detector.recordFailedAttempt('192.168.1.100', 'user@example.com');
    }
    console.log(`Attempt ${i}: ${result.allowed ? 'ALLOWED' : 'BLOCKED'}`);
  }

  console.log('\n--- Scenario 2: Rate Limit Triggered (Same Account) ---\n');
  
  const result4 = detector.checkLoginAttempt('192.168.1.100', 'user@example.com');
  console.log(`Attempt 4: ${result4.allowed ? 'ALLOWED' : 'BLOCKED'} (${result4.reason || 'N/A'})`);

  console.log('\n--- Scenario 3: Distributed Credential Stuffing (Many Accounts) ---\n');
  
  const attackerIP = '10.0.0.50';
  const accounts = [
    'admin@example.com', 'user1@example.com', 'user2@example.com',
    'user3@example.com', 'user4@example.com', 'user5@example.com',
    'user6@example.com', 'user7@example.com', 'user8@example.com',
    'user9@example.com', 'user10@example.com', 'user11@example.com'
  ];

  for (let i = 0; i < accounts.length; i++) {
    const result = detector.checkLoginAttempt(attackerIP, accounts[i]);
    if (result.allowed) {
      detector.recordFailedAttempt(attackerIP, accounts[i]);
      console.log(`Attempt ${i + 1}: ${accounts[i]} - ALLOWED`);
    } else {
      console.log(`Attempt ${i + 1}: ${accounts[i]} - BLOCKED (${result.reason})`);
      break;
    }
  }

  console.log('\n--- Scenario 4: Bot Detection (Rapid Requests) ---\n');
  
  const botIP = '10.0.0.75';
  const startTime = Date.now();
  
  for (let i = 0; i < 5; i++) {
    // Simulate rapid-fire requests (no delay)
    const result = detector.checkLoginAttempt(botIP, `bot_target_${i}@example.com`);
    if (result.allowed) {
      detector.recordFailedAttempt(botIP, `bot_target_${i}@example.com`);
      console.log(`Bot attempt ${i + 1}: ALLOWED (bot score: ${result.botScore?.toFixed(2) || 0})`);
    } else {
      console.log(`Bot attempt ${i + 1}: BLOCKED (${result.reason})`);
      break;
    }
  }

  console.log('\n--- Scenario 5: Successful Login (Resets Account Counter) ---\n');
  
  const legitIP = '192.168.1.200';
  const legitUser = 'gooduser@example.com';
  
  // Two failed attempts
  detector.checkLoginAttempt(legitIP, legitUser);
  detector.recordFailedAttempt(legitIP, legitUser);
  console.log('Failed attempt 1: recorded');
  
  detector.checkLoginAttempt(legitIP, legitUser);
  detector.recordFailedAttempt(legitIP, legitUser);
  console.log('Failed attempt 2: recorded');
  
  // Successful login
  detector.recordSuccessfulAttempt(legitIP, legitUser);
  console.log('Successful login: account counter reset');
  
  // Should be allowed again
  const resultAfterSuccess = detector.checkLoginAttempt(legitIP, legitUser);
  console.log('Next attempt after success:', resultAfterSuccess.allowed ? 'ALLOWED' : 'BLOCKED');

  console.log('\n--- Statistics ---\n');
  const stats = detector.getStats();
  console.log('Tracked IPs:', stats.trackedIPs);
  console.log('Tracked Accounts:', stats.trackedAccounts);
  console.log('Blocked IPs:', stats.blockedIPs);
  console.log('Blocked Accounts:', stats.blockedAccounts);

  console.log('\n' + '='.repeat(80));
  console.log('Detection mechanisms demonstrated:');
  console.log('  ✅ Rate limiting per IP address');
  console.log('  ✅ Rate limiting per account');
  console.log('  ✅ Distributed attack detection (many accounts from one IP)');
  console.log('  ✅ Bot detection via request timing analysis');
  console.log('  ✅ Temporary blocking of attackers');
  console.log('  ✅ Account counter reset on successful login');
  console.log('='.repeat(80));
}

module.exports = {
  CredentialStuffingDetector,
  createDetectionMiddleware
};
