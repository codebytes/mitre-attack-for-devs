/**
 * MITRE ATT&CK T1185: Browser Session Hijacking - Defense Implementation
 * Educational demonstration of session security and hijacking detection
 * 
 * @description Shows vulnerable vs secure session management in Express.js
 * @reference https://attack.mitre.org/techniques/T1185/
 */

const crypto = require('crypto');

// =============================================================================
// SESSION STORAGE (In-Memory for Demo)
// =============================================================================

/**
 * In-memory session store
 * In production, use Redis, Memcached, or encrypted database storage
 */
class SessionStore {
  constructor() {
    this.sessions = new Map();
    this.userSessions = new Map(); // Track sessions per user
  }

  /**
   * Create a new session
   * @param {string} sessionId - Unique session identifier
   * @param {object} data - Session data
   */
  create(sessionId, data) {
    this.sessions.set(sessionId, {
      ...data,
      createdAt: Date.now(),
      lastActivity: Date.now()
    });

    // Track user's sessions for concurrent session limits
    const userId = data.userId;
    if (!this.userSessions.has(userId)) {
      this.userSessions.set(userId, new Set());
    }
    this.userSessions.get(userId).add(sessionId);
  }

  /**
   * Get session data
   * @param {string} sessionId - Session identifier
   * @returns {object|null} Session data or null
   */
  get(sessionId) {
    return this.sessions.get(sessionId) || null;
  }

  /**
   * Update session data
   * @param {string} sessionId - Session identifier
   * @param {object} updates - Data to update
   */
  update(sessionId, updates) {
    const session = this.sessions.get(sessionId);
    if (session) {
      this.sessions.set(sessionId, { ...session, ...updates, lastActivity: Date.now() });
    }
  }

  /**
   * Delete a session
   * @param {string} sessionId - Session identifier
   */
  delete(sessionId) {
    const session = this.sessions.get(sessionId);
    if (session) {
      // Remove from user's session list
      const userSessionSet = this.userSessions.get(session.userId);
      if (userSessionSet) {
        userSessionSet.delete(sessionId);
      }
      this.sessions.delete(sessionId);
    }
  }

  /**
   * Get all sessions for a user
   * @param {string} userId - User identifier
   * @returns {Array} Array of session IDs
   */
  getUserSessions(userId) {
    return Array.from(this.userSessions.get(userId) || []);
  }

  /**
   * Delete all sessions for a user
   * @param {string} userId - User identifier
   */
  deleteUserSessions(userId) {
    const sessionIds = this.getUserSessions(userId);
    sessionIds.forEach(sid => this.sessions.delete(sid));
    this.userSessions.delete(userId);
  }
}

// =============================================================================
// VULNERABLE SESSION MANAGEMENT
// =============================================================================

/**
 * VULNERABLE: Basic session management without security controls
 * ATT&CK T1185 - Browser Session Hijacking
 * 
 * @description Vulnerable to session hijacking, fixation, and replay attacks
 * @vulnerability No fingerprinting, no rotation, no hijack detection
 */
class VulnerableSessionManager {
  constructor() {
    this.store = new SessionStore();
  }

  /**
   * VULNERABLE: Creates session without security controls
   * @param {object} req - Request object
   * @param {string} userId - User identifier
   * @returns {string} Session ID
   */
  createSession(req, userId) {
    // VULNERABLE: Predictable session ID (just a counter or timestamp)
    const sessionId = `session_${Date.now()}_${Math.random()}`;
    
    console.log('🔴 VULNERABLE: Creating session without security controls');
    
    this.store.create(sessionId, {
      userId,
      // VULNERABLE: No fingerprinting data stored
    });

    return sessionId;
  }

  /**
   * VULNERABLE: Validates session without security checks
   * @param {object} req - Request object
   * @param {string} sessionId - Session ID
   * @returns {object|null} Session data
   */
  validateSession(req, sessionId) {
    const session = this.store.get(sessionId);
    
    if (!session) {
      return null;
    }

    // VULNERABLE: No fingerprinting validation
    // VULNERABLE: No hijacking detection
    // VULNERABLE: Sessions never expire or rotate
    
    console.log('🔴 VULNERABLE: Session validated without security checks');
    
    return session;
  }
}

// =============================================================================
// SECURE SESSION MANAGEMENT
// =============================================================================

/**
 * SECURE: Session management with anti-hijacking controls
 * Defense against ATT&CK T1185
 * 
 * @description Implements fingerprinting, rotation, hijack detection, and session limits
 * @security Multiple layers of session security
 */
class SecureSessionManager {
  constructor(options = {}) {
    this.store = new SessionStore();
    this.config = {
      maxConcurrentSessions: options.maxConcurrentSessions || 3,
      sessionTimeout: options.sessionTimeout || 30 * 60 * 1000, // 30 minutes
      rotationInterval: options.rotationInterval || 15 * 60 * 1000, // 15 minutes
      fingerprintStrength: options.fingerprintStrength || 'medium', // low, medium, high
      ...options
    };
  }

  /**
   * SECURE: Creates session with security controls
   * @param {object} req - Request object with IP and headers
   * @param {string} userId - User identifier
   * @returns {string} Session ID
   */
  createSession(req, userId) {
    // Defense 1: Cryptographically secure session ID
    const sessionId = this.generateSecureSessionId();
    
    // Defense 2: Create session fingerprint
    const fingerprint = this.createFingerprint(req);
    
    // Defense 3: Check concurrent session limits
    this.enforceConcurrentSessionLimit(userId);
    
    console.log('✅ SECURE: Creating session with fingerprinting and limits');
    
    this.store.create(sessionId, {
      userId,
      fingerprint,
      rotationDue: Date.now() + this.config.rotationInterval,
      expiresAt: Date.now() + this.config.sessionTimeout
    });

    return sessionId;
  }

  /**
   * SECURE: Validates session with multiple security checks
   * @param {object} req - Request object
   * @param {string} sessionId - Session ID
   * @returns {object|null} Session data or null if invalid/hijacked
   */
  validateSession(req, sessionId) {
    const session = this.store.get(sessionId);
    
    if (!session) {
      console.log('🛡️  Session not found');
      return null;
    }

    // Defense 1: Check session expiration
    if (Date.now() > session.expiresAt) {
      console.log('🛡️  BLOCKED: Session expired');
      this.store.delete(sessionId);
      return null;
    }

    // Defense 2: Detect session hijacking via fingerprint validation
    const currentFingerprint = this.createFingerprint(req);
    const hijackScore = this.detectHijacking(session.fingerprint, currentFingerprint);
    
    if (hijackScore > 0.5) {
      console.log('🛡️  BLOCKED: Possible session hijacking detected!');
      console.log(`    Hijack confidence: ${(hijackScore * 100).toFixed(1)}%`);
      
      // Invalidate all user sessions on hijack detection
      this.store.deleteUserSessions(session.userId);
      return null;
    }

    // Defense 3: Session rotation
    if (Date.now() > session.rotationDue) {
      console.log('🔄 Session rotation required');
      return { ...session, rotationRequired: true };
    }

    // Defense 4: Update activity timestamp
    this.store.update(sessionId, {
      lastActivity: Date.now(),
      expiresAt: Date.now() + this.config.sessionTimeout
    });

    console.log('✅ Session validated successfully');
    
    return session;
  }

  /**
   * Rotates session ID while preserving session data
   * @param {string} oldSessionId - Old session ID
   * @param {object} req - Request object
   * @returns {string} New session ID
   */
  rotateSession(oldSessionId, req) {
    const session = this.store.get(oldSessionId);
    if (!session) {
      return null;
    }

    // Create new session with same data
    const newSessionId = this.generateSecureSessionId();
    
    this.store.create(newSessionId, {
      ...session,
      fingerprint: this.createFingerprint(req),
      rotationDue: Date.now() + this.config.rotationInterval,
      rotationCount: (session.rotationCount || 0) + 1
    });

    // Delete old session
    this.store.delete(oldSessionId);

    console.log('🔄 Session rotated successfully');
    
    return newSessionId;
  }

  /**
   * Generates cryptographically secure session ID
   * @returns {string} Session ID
   */
  generateSecureSessionId() {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Creates session fingerprint from request characteristics
   * @param {object} req - Request object
   * @returns {object} Fingerprint data
   */
  createFingerprint(req) {
    const fingerprint = {
      ipAddress: req.ip || req.connection?.remoteAddress || 'unknown',
      userAgent: req.headers?.['user-agent'] || 'unknown'
    };

    // Higher strength includes more signals (but less flexible for legitimate use)
    if (this.config.fingerprintStrength === 'high') {
      fingerprint.acceptLanguage = req.headers?.['accept-language'];
      fingerprint.acceptEncoding = req.headers?.['accept-encoding'];
    }

    // Create hash of fingerprint
    fingerprint.hash = this.hashFingerprint(fingerprint);

    return fingerprint;
  }

  /**
   * Hashes fingerprint data
   * @param {object} fingerprint - Fingerprint data
   * @returns {string} Hash
   */
  hashFingerprint(fingerprint) {
    const data = JSON.stringify({
      ip: fingerprint.ipAddress,
      ua: fingerprint.userAgent,
      lang: fingerprint.acceptLanguage,
      enc: fingerprint.acceptEncoding
    });
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Detects potential session hijacking by comparing fingerprints
   * @param {object} original - Original fingerprint
   * @param {object} current - Current fingerprint
   * @returns {number} Hijack score (0-1, higher = more likely hijacked)
   */
  detectHijacking(original, current) {
    let suspicionScore = 0;
    let checks = 0;

    // Check 1: IP address change (HIGH severity)
    if (original.ipAddress !== current.ipAddress) {
      suspicionScore += 0.7;
      console.log(`⚠️  IP changed: ${original.ipAddress} → ${current.ipAddress}`);
    }
    checks++;

    // Check 2: User Agent change (MEDIUM severity)
    if (original.userAgent !== current.userAgent) {
      suspicionScore += 0.4;
      console.log(`⚠️  User Agent changed`);
    }
    checks++;

    // Check 3: Accept-Language change (LOW severity)
    if (this.config.fingerprintStrength === 'high') {
      if (original.acceptLanguage !== current.acceptLanguage) {
        suspicionScore += 0.1;
      }
      checks++;
    }

    return Math.min(suspicionScore, 1.0);
  }

  /**
   * Enforces concurrent session limits per user
   * @param {string} userId - User identifier
   */
  enforceConcurrentSessionLimit(userId) {
    const userSessions = this.store.getUserSessions(userId);
    
    if (userSessions.length >= this.config.maxConcurrentSessions) {
      console.log(`🛡️  Enforcing concurrent session limit (${this.config.maxConcurrentSessions})`);
      
      // Remove oldest session
      let oldestSession = null;
      let oldestTime = Infinity;
      
      userSessions.forEach(sessionId => {
        const session = this.store.get(sessionId);
        if (session && session.lastActivity < oldestTime) {
          oldestTime = session.lastActivity;
          oldestSession = sessionId;
        }
      });
      
      if (oldestSession) {
        this.store.delete(oldestSession);
        console.log('🗑️  Removed oldest session');
      }
    }
  }

  /**
   * Destroys a session
   * @param {string} sessionId - Session ID
   */
  destroySession(sessionId) {
    this.store.delete(sessionId);
    console.log('🗑️  Session destroyed');
  }

  /**
   * Destroys all sessions for a user
   * @param {string} userId - User identifier
   */
  destroyUserSessions(userId) {
    this.store.deleteUserSessions(userId);
    console.log('🗑️  All user sessions destroyed');
  }
}

// =============================================================================
// EXPRESS MIDDLEWARE
// =============================================================================

/**
 * Creates Express middleware for session management
 * @param {SecureSessionManager} sessionManager - Session manager instance
 * @returns {Function} Express middleware
 */
function createSessionMiddleware(sessionManager) {
  return (req, res, next) => {
    // Extract session ID from cookie or header
    const sessionId = req.cookies?.sessionId || req.headers['x-session-id'];

    if (!sessionId) {
      req.session = null;
      return next();
    }

    // Validate session
    const session = sessionManager.validateSession(req, sessionId);

    if (!session) {
      res.clearCookie('sessionId');
      req.session = null;
      return next();
    }

    // Check if rotation is required
    if (session.rotationRequired) {
      const newSessionId = sessionManager.rotateSession(sessionId, req);
      res.cookie('sessionId', newSessionId, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
      });
      session.sessionId = newSessionId;
    }

    req.session = session;
    next();
  };
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1185: Session Hijacking Defense Demo');
  console.log('='.repeat(80));

  // Mock request objects
  const createMockRequest = (ip, userAgent) => ({
    ip,
    headers: { 'user-agent': userAgent },
    connection: { remoteAddress: ip }
  });

  console.log('\n--- VULNERABLE SESSION MANAGER ---\n');
  
  const vulnerableManager = new VulnerableSessionManager();
  
  const vulnReq1 = createMockRequest('192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0)');
  const vulnSessionId = vulnerableManager.createSession(vulnReq1, 'user123');
  console.log('Session created:', vulnSessionId);
  
  // Simulate hijacker with different IP
  const hijackerReq = createMockRequest('10.0.0.50', 'Mozilla/5.0 (Linux; Android)');
  const vulnResult = vulnerableManager.validateSession(hijackerReq, vulnSessionId);
  console.log('⚠️  Hijacker validated:', vulnResult ? 'YES (VULNERABLE!)' : 'NO');

  console.log('\n--- SECURE SESSION MANAGER ---\n');
  
  const secureManager = new SecureSessionManager({
    maxConcurrentSessions: 2,
    sessionTimeout: 30 * 60 * 1000,
    rotationInterval: 15 * 60 * 1000,
    fingerprintStrength: 'medium'
  });
  
  // Create session for legitimate user
  console.log('1. Creating session for legitimate user:');
  const secureReq1 = createMockRequest('192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0)');
  const secureSessionId = secureManager.createSession(secureReq1, 'user456');
  console.log('   Session ID:', secureSessionId.substring(0, 16) + '...');
  
  // Validate with legitimate user
  console.log('\n2. Legitimate user validates session:');
  const legitResult = secureManager.validateSession(secureReq1, secureSessionId);
  console.log('   Validated:', legitResult ? 'YES' : 'NO');
  
  // Simulate hijacking attempt
  console.log('\n3. Hijacker attempts to use stolen session:');
  const secureHijackerReq = createMockRequest('10.0.0.50', 'Mozilla/5.0 (Linux; Android)');
  const hijackResult = secureManager.validateSession(secureHijackerReq, secureSessionId);
  console.log('   Hijacker blocked:', hijackResult ? 'NO (FAILED!)' : 'YES (SUCCESS!)');
  
  // Test concurrent session limits
  console.log('\n4. Testing concurrent session limits:');
  const session2 = secureManager.createSession(secureReq1, 'user789');
  const session3 = secureManager.createSession(secureReq1, 'user789');
  const session4 = secureManager.createSession(secureReq1, 'user789'); // Should remove oldest
  console.log('   Sessions created: 3, Limit: 2, Oldest removed: YES');
  
  // Test session rotation
  console.log('\n5. Testing session rotation:');
  const newSessionId = secureManager.rotateSession(session4, secureReq1);
  console.log('   Old session ID:', session4.substring(0, 16) + '...');
  console.log('   New session ID:', newSessionId.substring(0, 16) + '...');

  console.log('\n' + '='.repeat(80));
  console.log('Demo complete. Key defenses implemented:');
  console.log('  ✅ Session fingerprinting (IP + User-Agent)');
  console.log('  ✅ Hijacking detection with suspicion scoring');
  console.log('  ✅ Automatic session rotation');
  console.log('  ✅ Concurrent session limits');
  console.log('  ✅ Session timeout and expiration');
  console.log('  ✅ Cryptographically secure session IDs');
  console.log('='.repeat(80));
}

module.exports = {
  SessionStore,
  VulnerableSessionManager,
  SecureSessionManager,
  createSessionMiddleware
};
