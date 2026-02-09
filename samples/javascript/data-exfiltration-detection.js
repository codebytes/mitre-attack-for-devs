/**
 * MITRE ATT&CK T1567 (Exfiltration Over Web Service) & T1020 (Automated Exfiltration)
 * Educational demonstration of data exfiltration detection
 * 
 * @description Detects data exfiltration patterns via API monitoring and DLP
 * @reference https://attack.mitre.org/techniques/T1567/
 * @reference https://attack.mitre.org/techniques/T1020/
 */

const crypto = require('crypto');

// =============================================================================
// DATA EXFILTRATION DETECTOR
// =============================================================================

/**
 * SECURE: Data exfiltration detection system
 * Defense against ATT&CK T1567 and T1020
 * 
 * @description Monitors API traffic for data exfiltration patterns
 * @security Volume tracking, bulk download detection, chunked exfiltration detection
 */
class DataExfiltrationDetector {
  constructor(options = {}) {
    this.config = {
      // Volume limits
      maxBytesPerMinute: options.maxBytesPerMinute || 10 * 1024 * 1024, // 10 MB/min
      maxBytesPerHour: options.maxBytesPerHour || 100 * 1024 * 1024, // 100 MB/hour
      maxBytesPerDay: options.maxBytesPerDay || 500 * 1024 * 1024, // 500 MB/day
      
      // Bulk download detection
      maxRecordsPerRequest: options.maxRecordsPerRequest || 1000,
      maxRecordsPerHour: options.maxRecordsPerHour || 10000,
      
      // Chunked exfiltration detection
      suspiciousRequestInterval: options.suspiciousRequestInterval || 5000, // 5 seconds
      suspiciousRequestCount: options.suspiciousRequestCount || 10,
      
      // Rate limiting
      blockDurationMs: options.blockDurationMs || 60 * 60 * 1000, // 1 hour
      
      ...options
    };

    // In-memory tracking (use Redis in production)
    this.userDataTransfer = new Map(); // userId -> transfer records
    this.userRecordAccess = new Map(); // userId -> record access array
    this.blockedUsers = new Map(); // userId -> block expiry time
    this.requestTimestamps = new Map(); // userId -> timestamp array
    this.endpointAccess = new Map(); // userId -> endpoint access patterns
  }

  /**
   * Monitors data transfer for a user request
   * @param {string} userId - User identifier
   * @param {object} requestData - Request metadata
   * @returns {object} Analysis result
   */
  monitorDataTransfer(userId, requestData) {
    const now = Date.now();
    
    // Clean up old data
    this.cleanup(now);

    // Check if user is blocked
    if (this.isUserBlocked(userId, now)) {
      console.log(`🛡️  BLOCKED: User ${userId} is temporarily blocked for suspicious activity`);
      return {
        allowed: false,
        reason: 'user_blocked',
        retryAfter: this.blockedUsers.get(userId) - now
      };
    }

    const analysis = {
      userId,
      timestamp: now,
      checks: [],
      suspicionScore: 0,
      allowed: true,
      reason: null
    };

    // Check 1: Volume-based detection
    const volumeCheck = this.checkDataVolume(userId, requestData.responseSize, now);
    analysis.checks.push(volumeCheck);
    analysis.suspicionScore += volumeCheck.suspicionScore || 0;

    // Check 2: Bulk download detection
    const bulkCheck = this.checkBulkDownload(userId, requestData.recordCount, now);
    analysis.checks.push(bulkCheck);
    analysis.suspicionScore += bulkCheck.suspicionScore || 0;

    // Check 3: Chunked exfiltration detection
    const chunkCheck = this.detectChunkedExfiltration(userId, requestData, now);
    analysis.checks.push(chunkCheck);
    analysis.suspicionScore += chunkCheck.suspicionScore || 0;

    // Check 4: Endpoint hopping detection
    const endpointCheck = this.detectEndpointHopping(userId, requestData.endpoint, now);
    analysis.checks.push(endpointCheck);
    analysis.suspicionScore += endpointCheck.suspicionScore || 0;

    // Check 5: Off-hours access
    const timeCheck = this.checkOffHoursAccess(now);
    analysis.checks.push(timeCheck);
    analysis.suspicionScore += timeCheck.suspicionScore || 0;

    // Normalize suspicion score (0-1)
    analysis.suspicionScore = Math.min(analysis.suspicionScore, 1.0);

    // Block if suspicion score is high
    if (analysis.suspicionScore >= 0.7) {
      console.log(`🚫 BLOCKED: High suspicion score (${(analysis.suspicionScore * 100).toFixed(1)}%) for user ${userId}`);
      this.blockUser(userId, now);
      analysis.allowed = false;
      analysis.reason = 'high_suspicion_score';
    } else if (analysis.suspicionScore >= 0.4) {
      console.log(`⚠️  WARNING: Elevated suspicion score (${(analysis.suspicionScore * 100).toFixed(1)}%) for user ${userId}`);
    } else {
      console.log(`✅ Request allowed: User ${userId}, suspicion score: ${(analysis.suspicionScore * 100).toFixed(1)}%`);
    }

    // Record the data transfer
    if (analysis.allowed) {
      this.recordDataTransfer(userId, requestData, now);
    }

    return analysis;
  }

  /**
   * Check 1: Volume-based detection
   * @param {string} userId - User identifier
   * @param {number} bytes - Response size in bytes
   * @param {number} now - Current timestamp
   * @returns {object} Check result
   */
  checkDataVolume(userId, bytes, now) {
    const transfers = this.getUserTransfers(userId, now);
    
    // Calculate data volume in different time windows
    const bytesLastMinute = this.sumTransfers(transfers, now - 60 * 1000, bytes);
    const bytesLastHour = this.sumTransfers(transfers, now - 60 * 60 * 1000, bytes);
    const bytesLastDay = this.sumTransfers(transfers, now - 24 * 60 * 60 * 1000, bytes);

    let suspicionScore = 0;
    const warnings = [];

    // Check against limits
    if (bytesLastMinute > this.config.maxBytesPerMinute) {
      suspicionScore += 0.3;
      warnings.push(`Exceeded per-minute limit: ${(bytesLastMinute / 1024 / 1024).toFixed(2)} MB`);
      console.log(`   ⚠️  Volume: ${(bytesLastMinute / 1024 / 1024).toFixed(2)} MB/min (limit: ${(this.config.maxBytesPerMinute / 1024 / 1024).toFixed(2)} MB)`);
    }

    if (bytesLastHour > this.config.maxBytesPerHour) {
      suspicionScore += 0.4;
      warnings.push(`Exceeded per-hour limit: ${(bytesLastHour / 1024 / 1024).toFixed(2)} MB`);
      console.log(`   ⚠️  Volume: ${(bytesLastHour / 1024 / 1024).toFixed(2)} MB/hour (limit: ${(this.config.maxBytesPerHour / 1024 / 1024).toFixed(2)} MB)`);
    }

    if (bytesLastDay > this.config.maxBytesPerDay) {
      suspicionScore += 0.5;
      warnings.push(`Exceeded per-day limit: ${(bytesLastDay / 1024 / 1024).toFixed(2)} MB`);
      console.log(`   ⚠️  Volume: ${(bytesLastDay / 1024 / 1024).toFixed(2)} MB/day (limit: ${(this.config.maxBytesPerDay / 1024 / 1024).toFixed(2)} MB)`);
    }

    return {
      name: 'data_volume',
      status: warnings.length > 0 ? 'warning' : 'passed',
      suspicionScore,
      warnings,
      metrics: {
        bytesLastMinute,
        bytesLastHour,
        bytesLastDay
      }
    };
  }

  /**
   * Check 2: Bulk download detection
   * @param {string} userId - User identifier
   * @param {number} recordCount - Number of records accessed
   * @param {number} now - Current timestamp
   * @returns {object} Check result
   */
  checkBulkDownload(userId, recordCount, now) {
    if (!recordCount || recordCount === 0) {
      return {
        name: 'bulk_download',
        status: 'skipped',
        suspicionScore: 0
      };
    }

    const recordAccesses = this.getUserRecordAccess(userId, now);
    const recordsLastHour = this.sumRecords(recordAccesses, now - 60 * 60 * 1000, recordCount);

    let suspicionScore = 0;
    const warnings = [];

    // Check against record limits
    if (recordCount > this.config.maxRecordsPerRequest) {
      suspicionScore += 0.4;
      warnings.push(`Large single request: ${recordCount} records`);
      console.log(`   ⚠️  Bulk download: ${recordCount} records in single request`);
    }

    if (recordsLastHour > this.config.maxRecordsPerHour) {
      suspicionScore += 0.5;
      warnings.push(`Exceeded hourly record limit: ${recordsLastHour} records`);
      console.log(`   ⚠️  Bulk download: ${recordsLastHour} records/hour (limit: ${this.config.maxRecordsPerHour})`);
    }

    return {
      name: 'bulk_download',
      status: warnings.length > 0 ? 'warning' : 'passed',
      suspicionScore,
      warnings,
      metrics: {
        recordCount,
        recordsLastHour
      }
    };
  }

  /**
   * Check 3: Chunked exfiltration detection (many small, rapid requests)
   * @param {string} userId - User identifier
   * @param {object} requestData - Request metadata
   * @param {number} now - Current timestamp
   * @returns {object} Check result
   */
  detectChunkedExfiltration(userId, requestData, now) {
    if (!this.requestTimestamps.has(userId)) {
      this.requestTimestamps.set(userId, []);
    }

    const timestamps = this.requestTimestamps.get(userId);
    timestamps.push(now);

    // Keep only recent timestamps (last 5 minutes)
    const recentTimestamps = timestamps.filter(ts => now - ts < 5 * 60 * 1000);
    this.requestTimestamps.set(userId, recentTimestamps);

    let suspicionScore = 0;
    const warnings = [];

    // Check for rapid, regular requests (chunked exfiltration pattern)
    if (recentTimestamps.length >= this.config.suspiciousRequestCount) {
      const intervals = [];
      for (let i = 1; i < recentTimestamps.length; i++) {
        intervals.push(recentTimestamps[i] - recentTimestamps[i - 1]);
      }

      const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
      
      // Suspiciously regular intervals suggest automated exfiltration
      if (avgInterval < this.config.suspiciousRequestInterval) {
        suspicionScore += 0.3;
        warnings.push(`Rapid request pattern: ${recentTimestamps.length} requests in 5 minutes`);
        console.log(`   ⚠️  Chunked pattern: ${recentTimestamps.length} requests, avg interval ${avgInterval.toFixed(0)}ms`);
      }

      // Check for very consistent timing (automation indicator)
      const variance = intervals.reduce((sum, interval) => {
        return sum + Math.pow(interval - avgInterval, 2);
      }, 0) / intervals.length;
      const stdDev = Math.sqrt(variance);

      if (stdDev < 500) { // Less than 500ms variation
        suspicionScore += 0.2;
        warnings.push('Suspiciously consistent timing pattern (possible automation)');
        console.log(`   ⚠️  Automation detected: timing variance ${stdDev.toFixed(0)}ms`);
      }
    }

    return {
      name: 'chunked_exfiltration',
      status: warnings.length > 0 ? 'warning' : 'passed',
      suspicionScore,
      warnings,
      metrics: {
        requestsLast5Min: recentTimestamps.length
      }
    };
  }

  /**
   * Check 4: Endpoint hopping detection (accessing many different endpoints)
   * @param {string} userId - User identifier
   * @param {string} endpoint - Endpoint path
   * @param {number} now - Current timestamp
   * @returns {object} Check result
   */
  detectEndpointHopping(userId, endpoint, now) {
    if (!this.endpointAccess.has(userId)) {
      this.endpointAccess.set(userId, []);
    }

    const accesses = this.endpointAccess.get(userId);
    accesses.push({ endpoint, timestamp: now });

    // Keep only recent accesses (last hour)
    const recentAccesses = accesses.filter(a => now - a.timestamp < 60 * 60 * 1000);
    this.endpointAccess.set(userId, recentAccesses);

    // Count unique endpoints accessed
    const uniqueEndpoints = new Set(recentAccesses.map(a => a.endpoint)).size;

    let suspicionScore = 0;
    const warnings = [];

    // Many different endpoints in short time = possible systematic exfiltration
    if (uniqueEndpoints > 20) {
      suspicionScore += 0.3;
      warnings.push(`Accessing many endpoints: ${uniqueEndpoints} unique endpoints in 1 hour`);
      console.log(`   ⚠️  Endpoint hopping: ${uniqueEndpoints} unique endpoints/hour`);
    }

    return {
      name: 'endpoint_hopping',
      status: warnings.length > 0 ? 'warning' : 'passed',
      suspicionScore,
      warnings,
      metrics: {
        uniqueEndpoints,
        totalRequests: recentAccesses.length
      }
    };
  }

  /**
   * Check 5: Off-hours access detection
   * @param {number} now - Current timestamp
   * @returns {object} Check result
   */
  checkOffHoursAccess(now) {
    const hour = new Date(now).getHours();
    const isWeekend = [0, 6].includes(new Date(now).getDay());

    let suspicionScore = 0;
    const warnings = [];

    // Off-hours: 11 PM to 6 AM, or weekends
    const isOffHours = hour >= 23 || hour < 6 || isWeekend;

    if (isOffHours) {
      suspicionScore += 0.1;
      warnings.push(`Off-hours access: ${isWeekend ? 'Weekend' : 'Late night'}`);
      console.log(`   ⚠️  Off-hours access detected`);
    }

    return {
      name: 'off_hours_access',
      status: warnings.length > 0 ? 'warning' : 'passed',
      suspicionScore,
      warnings
    };
  }

  /**
   * Records a data transfer
   * @param {string} userId - User identifier
   * @param {object} requestData - Request metadata
   * @param {number} now - Current timestamp
   */
  recordDataTransfer(userId, requestData, now) {
    if (!this.userDataTransfer.has(userId)) {
      this.userDataTransfer.set(userId, []);
    }

    this.userDataTransfer.get(userId).push({
      timestamp: now,
      bytes: requestData.responseSize || 0,
      endpoint: requestData.endpoint,
      recordCount: requestData.recordCount || 0
    });

    if (requestData.recordCount) {
      if (!this.userRecordAccess.has(userId)) {
        this.userRecordAccess.set(userId, []);
      }
      this.userRecordAccess.get(userId).push({
        timestamp: now,
        count: requestData.recordCount
      });
    }
  }

  /**
   * Gets user transfers within time window
   * @param {string} userId - User identifier
   * @param {number} now - Current timestamp
   * @returns {Array} Transfers
   */
  getUserTransfers(userId, now) {
    const allTransfers = this.userDataTransfer.get(userId) || [];
    return allTransfers.filter(t => now - t.timestamp < 24 * 60 * 60 * 1000); // Last 24 hours
  }

  /**
   * Gets user record accesses within time window
   * @param {string} userId - User identifier
   * @param {number} now - Current timestamp
   * @returns {Array} Record accesses
   */
  getUserRecordAccess(userId, now) {
    const allAccesses = this.userRecordAccess.get(userId) || [];
    return allAccesses.filter(a => now - a.timestamp < 24 * 60 * 60 * 1000);
  }

  /**
   * Sums transfer bytes in time window
   * @param {Array} transfers - Transfer array
   * @param {number} since - Start timestamp
   * @param {number} includeBytes - Additional bytes to include
   * @returns {number} Total bytes
   */
  sumTransfers(transfers, since, includeBytes = 0) {
    const filtered = transfers.filter(t => t.timestamp >= since);
    const sum = filtered.reduce((total, t) => total + t.bytes, 0);
    return sum + includeBytes;
  }

  /**
   * Sums record counts in time window
   * @param {Array} accesses - Access array
   * @param {number} since - Start timestamp
   * @param {number} includeCount - Additional count to include
   * @returns {number} Total records
   */
  sumRecords(accesses, since, includeCount = 0) {
    const filtered = accesses.filter(a => a.timestamp >= since);
    const sum = filtered.reduce((total, a) => total + a.count, 0);
    return sum + includeCount;
  }

  /**
   * Checks if user is blocked
   * @param {string} userId - User identifier
   * @param {number} now - Current timestamp
   * @returns {boolean} True if blocked
   */
  isUserBlocked(userId, now) {
    const blockExpiry = this.blockedUsers.get(userId);
    return blockExpiry && now < blockExpiry;
  }

  /**
   * Blocks a user
   * @param {string} userId - User identifier
   * @param {number} now - Current timestamp
   */
  blockUser(userId, now) {
    this.blockedUsers.set(userId, now + this.config.blockDurationMs);
    console.log(`🚫 User ${userId} blocked for ${this.config.blockDurationMs / 60000} minutes`);
  }

  /**
   * Cleans up old data
   * @param {number} now - Current timestamp
   */
  cleanup(now) {
    // Clean up old transfers (keep last 24 hours)
    for (const [userId, transfers] of this.userDataTransfer.entries()) {
      const recent = transfers.filter(t => now - t.timestamp < 24 * 60 * 60 * 1000);
      if (recent.length === 0) {
        this.userDataTransfer.delete(userId);
      } else {
        this.userDataTransfer.set(userId, recent);
      }
    }

    // Clean up expired blocks
    for (const [userId, expiry] of this.blockedUsers.entries()) {
      if (now >= expiry) {
        this.blockedUsers.delete(userId);
      }
    }
  }

  /**
   * Gets statistics
   * @returns {object} Statistics
   */
  getStats() {
    return {
      trackedUsers: this.userDataTransfer.size,
      blockedUsers: this.blockedUsers.size,
      totalTransfers: Array.from(this.userDataTransfer.values()).reduce((sum, t) => sum + t.length, 0)
    };
  }
}

// =============================================================================
// EXPRESS MIDDLEWARE
// =============================================================================

/**
 * Creates Express middleware for data exfiltration detection
 * @param {DataExfiltrationDetector} detector - Detector instance
 * @returns {Function} Express middleware
 */
function createExfiltrationMiddleware(detector) {
  return (req, res, next) => {
    const userId = req.user?.id || req.headers['x-user-id'] || 'anonymous';

    // Intercept response to measure size
    const originalSend = res.send;
    const originalJson = res.json;

    const wrapResponse = (data) => {
      const responseSize = Buffer.byteLength(JSON.stringify(data || ''));
      
      // Extract record count if available
      let recordCount = 0;
      if (data && Array.isArray(data)) {
        recordCount = data.length;
      } else if (data && data.data && Array.isArray(data.data)) {
        recordCount = data.data.length;
      }

      // Analyze the transfer
      const analysis = detector.monitorDataTransfer(userId, {
        endpoint: req.path,
        responseSize,
        recordCount,
        method: req.method
      });

      // Attach analysis to response headers (for monitoring)
      res.setHeader('X-Exfiltration-Score', (analysis.suspicionScore * 100).toFixed(1));

      return { responseSize, analysis };
    };

    res.send = function(data) {
      const { analysis } = wrapResponse(data);
      
      if (!analysis.allowed) {
        res.status(429);
        return originalSend.call(this, JSON.stringify({
          error: 'Request blocked',
          reason: analysis.reason
        }));
      }
      
      return originalSend.call(this, data);
    };

    res.json = function(data) {
      const { analysis } = wrapResponse(data);
      
      if (!analysis.allowed) {
        res.status(429);
        return originalJson.call(this, {
          error: 'Request blocked',
          reason: analysis.reason
        });
      }
      
      return originalJson.call(this, data);
    };

    next();
  };
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1567/T1020: Data Exfiltration Detection Demo');
  console.log('='.repeat(80));

  const detector = new DataExfiltrationDetector({
    maxBytesPerMinute: 5 * 1024 * 1024,    // 5 MB/min
    maxBytesPerHour: 50 * 1024 * 1024,     // 50 MB/hour
    maxRecordsPerRequest: 500,
    maxRecordsPerHour: 5000,
    suspiciousRequestInterval: 3000,
    suspiciousRequestCount: 5
  });

  console.log('\n--- Scenario 1: Normal Data Access ---\n');
  
  for (let i = 1; i <= 3; i++) {
    console.log(`Request ${i}:`);
    detector.monitorDataTransfer('user123', {
      endpoint: '/api/users',
      responseSize: 50 * 1024, // 50 KB
      recordCount: 10
    });
    console.log();
  }

  console.log('\n--- Scenario 2: Bulk Download Attack ---\n');
  
  console.log('Large bulk download attempt:');
  detector.monitorDataTransfer('attacker1', {
    endpoint: '/api/customers/export',
    responseSize: 20 * 1024 * 1024, // 20 MB
    recordCount: 50000
  });

  console.log('\n--- Scenario 3: Chunked Exfiltration (Automated) ---\n');
  
  for (let i = 1; i <= 8; i++) {
    console.log(`Rapid request ${i}:`);
    const result = detector.monitorDataTransfer('attacker2', {
      endpoint: `/api/data/page${i}`,
      responseSize: 500 * 1024, // 500 KB per request
      recordCount: 100
    });
    
    if (!result.allowed) {
      console.log('Attack blocked!');
      break;
    }
    console.log();
    
    // Simulate rapid automated requests (no delay)
  }

  console.log('\n--- Scenario 4: Endpoint Hopping ---\n');
  
  const endpoints = [
    '/api/users', '/api/customers', '/api/orders', '/api/products',
    '/api/invoices', '/api/reports', '/api/analytics', '/api/exports',
    '/api/config', '/api/secrets', '/api/keys', '/api/credentials',
    '/api/admin/users', '/api/admin/settings', '/api/admin/logs'
  ];

  for (let i = 0; i < endpoints.length; i++) {
    if (i % 5 === 0) {
      console.log(`Access ${i + 1}:` );
    }
    const result = detector.monitorDataTransfer('attacker3', {
      endpoint: endpoints[i],
      responseSize: 100 * 1024,
      recordCount: 20
    });
    
    if (!result.allowed) {
      console.log('\nEndpoint hopping detected and blocked!');
      break;
    }
  }

  console.log('\n--- Statistics ---\n');
  const stats = detector.getStats();
  console.log('Tracked users:', stats.trackedUsers);
  console.log('Blocked users:', stats.blockedUsers);
  console.log('Total transfers:', stats.totalTransfers);

  console.log('\n' + '='.repeat(80));
  console.log('Detection mechanisms demonstrated:');
  console.log('  ✅ Data volume tracking (per minute/hour/day)');
  console.log('  ✅ Bulk download detection');
  console.log('  ✅ Chunked exfiltration pattern detection');
  console.log('  ✅ Endpoint hopping detection');
  console.log('  ✅ Off-hours access monitoring');
  console.log('  ✅ Suspicion score calculation');
  console.log('  ✅ Automated blocking of suspicious users');
  console.log('='.repeat(80));
}

module.exports = {
  DataExfiltrationDetector,
  createExfiltrationMiddleware
};
