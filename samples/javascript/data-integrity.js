/**
 * MITRE ATT&CK T1565: Data Manipulation - Integrity Verification
 * Educational demonstration of data integrity protection
 * 
 * @description Detects and prevents unauthorized data modifications
 * @reference https://attack.mitre.org/techniques/T1565/
 */

const crypto = require('crypto');

// =============================================================================
// DATA INTEGRITY MANAGER
// =============================================================================

/**
 * SECURE: Data integrity management system
 * Defense against ATT&CK T1565
 * 
 * @description Protects data integrity with HMAC signatures and audit trails
 * @security HMAC verification, audit trails, modification monitoring
 */
class DataIntegrityManager {
  constructor(secretKey) {
    this.secretKey = secretKey;
    
    // Audit trail: [{timestamp, user, recordId, field, oldValue, newValue, signature}, ...]
    this.auditTrail = [];
    
    // Change velocity tracking: user -> [{timestamp, recordId}, ...]
    this.userModifications = new Map();
    
    // Field sensitivity levels (higher = more sensitive)
    this.fieldSensitivity = {
      balance: 10,
      salary: 10,
      role: 9,
      permissions: 9,
      status: 8,
      email: 7,
      name: 5,
      description: 3
    };
    
    // Alert thresholds
    this.config = {
      massModificationThreshold: 10,
      massModificationWindowMs: 60 * 1000, // 60 seconds
      highValueChangeThreshold: 1000
    };
  }

  /**
   * Compute HMAC signature for a record
   * @param {string} recordId - Record identifier
   * @param {object} data - Record data
   * @returns {string} HMAC signature
   */
  computeSignature(recordId, data) {
    const dataCopy = {...data};
    delete dataCopy._signature;
    
    const canonical = JSON.stringify(dataCopy, Object.keys(dataCopy).sort());
    const message = `${recordId}:${canonical}`;
    
    return crypto.createHmac('sha256', this.secretKey)
      .update(message)
      .digest('hex');
  }

  /**
   * Sign a record with HMAC signature
   * @param {string} recordId - Record identifier
   * @param {object} data - Record data
   * @returns {object} Record with signature
   */
  signRecord(recordId, data) {
    const dataCopy = {...data};
    delete dataCopy._signature;
    
    const signature = this.computeSignature(recordId, dataCopy);
    
    return {
      ...dataCopy,
      _signature: signature
    };
  }

  /**
   * Verify record integrity
   * @param {string} recordId - Record identifier
   * @param {object} data - Record data
   * @returns {object} Verification result
   */
  verifyRecord(recordId, data) {
    if (!data._signature) {
      console.log(`❌ No signature found for record ${recordId}`);
      return {
        isValid: false,
        reason: 'No signature found - record may have been tampered with'
      };
    }

    const storedSignature = data._signature;
    const dataCopy = {...data};
    delete dataCopy._signature;
    
    const expectedSignature = this.computeSignature(recordId, dataCopy);
    
    const isValid = crypto.timingSafeEqual(
      Buffer.from(storedSignature),
      Buffer.from(expectedSignature)
    );

    if (!isValid) {
      console.log(`❌ Signature mismatch for record ${recordId}`);
      return {
        isValid: false,
        reason: 'Signature mismatch - record has been tampered with (T1565)'
      };
    }

    console.log(`✅ Record ${recordId} integrity verified`);
    return {
      isValid: true,
      reason: 'Record integrity verified'
    };
  }

  /**
   * Record a data change and check for anomalies
   * @param {object} changeDetails - Change details
   * @returns {object} Result with allowed flag, reason, and alerts
   */
  recordChange({user, recordId, field, oldValue, newValue}) {
    const now = Date.now();
    const alerts = [];

    // Create audit entry
    const auditEntry = {
      timestamp: now,
      user,
      recordId,
      field,
      oldValue,
      newValue
    };

    // Sign audit entry
    const auditSignature = crypto.createHmac('sha256', this.secretKey)
      .update(JSON.stringify(auditEntry))
      .digest('hex');

    this.auditTrail.push({
      ...auditEntry,
      signature: auditSignature
    });

    // Track modification for velocity analysis
    if (!this.userModifications.has(user)) {
      this.userModifications.set(user, []);
    }
    this.userModifications.get(user).push({timestamp: now, recordId});

    // Check 1: Mass modification detection
    const recentChanges = this.userModifications.get(user)
      .filter(m => now - m.timestamp <= this.config.massModificationWindowMs);

    if (recentChanges.length >= this.config.massModificationThreshold) {
      alerts.push(
        `ALERT (T1565): Mass modification detected! User ${user} modified ` +
        `${recentChanges.length} records in ${this.config.massModificationWindowMs / 1000}s`
      );
    }

    // Check 2: High-sensitivity field changes
    const fieldSensitivity = this.fieldSensitivity[field] || 1;
    if (fieldSensitivity >= 8) {
      alerts.push(
        `WARNING (T1565): High-sensitivity field '${field}' modified by ${user}`
      );
    }

    // Check 3: Suspicious value changes
    if (['balance', 'salary'].includes(field) && 
        typeof oldValue === 'number' && 
        typeof newValue === 'number') {
      const changeAmount = Math.abs(newValue - oldValue);
      if (changeAmount >= this.config.highValueChangeThreshold) {
        alerts.push(
          `ALERT (T1565): Large value change detected! ${field}: ` +
          `${oldValue} → ${newValue} (Δ${changeAmount})`
        );
      }
    }

    // Check 4: Multiple rapid changes to same record
    const recentRecordChanges = this.auditTrail
      .slice(-20)
      .filter(entry => 
        entry.recordId === recordId && 
        now - entry.timestamp <= 10000
      );

    if (recentRecordChanges.length >= 5) {
      alerts.push(
        `WARNING (T1565): Multiple rapid changes to record ${recordId}`
      );
    }

    // Determine if change should be allowed
    let allowed = true;
    let reason = 'Change recorded in audit trail';

    for (const alert of alerts) {
      if (alert.includes('ALERT') && alert.includes('Mass modification')) {
        allowed = false;
        reason = 'BLOCKED: Mass modification pattern detected (T1565)';
        break;
      }
    }

    if (alerts.length > 0) {
      console.log('⚠️  Anomalies detected:');
      alerts.forEach(alert => console.log(`   ${alert}`));
    }

    return {
      allowed,
      reason,
      alerts
    };
  }

  /**
   * Verify audit trail integrity
   * @returns {object} Verification result
   */
  verifyAuditTrail() {
    const issues = [];

    for (let i = 0; i < this.auditTrail.length; i++) {
      const entry = this.auditTrail[i];
      
      if (!entry.signature) {
        issues.push(`Entry ${i}: Missing signature`);
        continue;
      }

      const {signature, ...auditEntry} = entry;
      
      const expectedSignature = crypto.createHmac('sha256', this.secretKey)
        .update(JSON.stringify(auditEntry))
        .digest('hex');

      if (signature !== expectedSignature) {
        issues.push(
          `Entry ${i}: Audit trail tampering detected! (T1565) ` +
          `Record: ${entry.recordId}, User: ${entry.user}`
        );
      }
    }

    const isValid = issues.length === 0;

    if (isValid) {
      console.log('✅ Audit trail integrity verified');
    } else {
      console.log('❌ Audit trail tampering detected!');
      issues.forEach(issue => console.log(`   ${issue}`));
    }

    return {isValid, issues};
  }

  /**
   * Get change statistics
   * @param {string} user - Optional user filter
   * @returns {object} Statistics
   */
  getChangeReport(user = null) {
    const changes = user 
      ? this.auditTrail.filter(e => e.user === user)
      : this.auditTrail;

    const changesByUser = {};
    const changesByField = {};

    for (const entry of changes) {
      changesByUser[entry.user] = (changesByUser[entry.user] || 0) + 1;
      changesByField[entry.field] = (changesByField[entry.field] || 0) + 1;
    }

    const now = Date.now();
    const highVelocityUsers = [];
    
    for (const [username, modifications] of this.userModifications.entries()) {
      const recent = modifications.filter(
        m => now - m.timestamp <= 5 * 60 * 1000
      );
      if (recent.length >= 5) {
        highVelocityUsers.push({user: username, count: recent.length});
      }
    }

    return {
      totalChanges: changes.length,
      changesByUser,
      changesByField,
      highVelocityUsers: highVelocityUsers.sort((a, b) => b.count - a.count),
      auditTrailSize: this.auditTrail.length
    };
  }
}

// =============================================================================
// VULNERABLE IMPLEMENTATION (DO NOT USE IN PRODUCTION)
// =============================================================================

/**
 * VULNERABLE: Direct data modification with no integrity checks
 * 
 * Issues:
 * - No integrity verification
 * - No audit trail
 * - No change monitoring
 * - Attacker can modify data undetected
 * 
 * ATT&CK T1565: Attacker can tamper with data silently
 */
function vulnerableUpdateRecord(recordId, data) {
  // Just update the data - no verification or logging
  return data;
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1565: Data Manipulation - Integrity Verification Demo');
  console.log('='.repeat(80));
  console.log('\nDetecting and preventing unauthorized data modifications\n');

  const secretKey = 'super_secret_integrity_key_DO_NOT_HARDCODE';
  const manager = new DataIntegrityManager(secretKey);

  // Scenario 1: Normal operations
  console.log('--- Scenario 1: Normal Operations ---\n');
  
  const recordId = 'user_12345';
  const userData = {
    name: 'Alice Smith',
    email: 'alice@example.com',
    balance: 1000,
    role: 'user'
  };

  const signedRecord = manager.signRecord(recordId, userData);
  console.log('Created and signed record:', recordId);

  manager.verifyRecord(recordId, signedRecord);

  manager.recordChange({
    user: 'admin',
    recordId,
    field: 'email',
    oldValue: 'alice@example.com',
    newValue: 'alice.smith@example.com'
  });

  // Scenario 2: Data tampering attempt
  console.log('\n--- Scenario 2: Data Tampering Attack (T1565) ---\n');
  
  const accountId = 'account_999';
  const accountData = {
    accountNumber: '999',
    balance: 5000,
    owner: 'Bob Jones'
  };

  const signedAccount = manager.signRecord(accountId, accountData);
  console.log('Original balance: $5000');

  const tamperedAccount = {...signedAccount};
  tamperedAccount.balance = 50000;
  console.log('Attacker changes balance to: $50000\n');

  manager.verifyRecord(accountId, tamperedAccount);

  // Scenario 3: Mass modification attack
  console.log('\n--- Scenario 3: Mass Modification Attack (T1565) ---\n');
  console.log('Attacker performing mass data modification...\n');
  
  const attacker = 'compromised_admin';
  
  for (let i = 0; i < 15; i++) {
    const result = manager.recordChange({
      user: attacker,
      recordId: `record_${i}`,
      field: 'status',
      oldValue: 'active',
      newValue: 'deleted'
    });

    if (!result.allowed) {
      console.log(`\n🛡️  Mass modification blocked after ${i + 1} attempts!`);
      console.log(`   Reason: ${result.reason}`);
      break;
    }
  }

  // Scenario 4: High-value field modification
  console.log('\n--- Scenario 4: High-Value Field Modification (T1565) ---\n');
  
  manager.recordChange({
    user: 'insider_threat',
    recordId: 'salary_database_001',
    field: 'salary',
    oldValue: 75000,
    newValue: 175000
  });

  // Scenario 5: Audit trail tampering
  console.log('\n--- Scenario 5: Audit Trail Tampering (T1565) ---\n');
  
  manager.recordChange({
    user: 'user1',
    recordId: 'rec1',
    field: 'status',
    oldValue: 'active',
    newValue: 'inactive'
  });

  console.log('Attacker attempts to modify audit trail...\n');
  
  if (manager.auditTrail.length > 0) {
    const original = manager.auditTrail[0];
    manager.auditTrail[0] = {
      ...original,
      user: 'attacker' // Tampered!
    };
  }

  manager.verifyAuditTrail();

  // Statistics
  console.log('\n--- Change Report ---\n');
  const report = manager.getChangeReport();
  console.log('Total changes:', report.totalChanges);
  console.log('Changes by user:', report.changesByUser);
  
  if (report.highVelocityUsers.length > 0) {
    console.log('\n⚠️  High-velocity users:');
    report.highVelocityUsers.forEach(({user, count}) => {
      console.log(`   ${user}: ${count} changes in 5 minutes`);
    });
  }

  console.log('\n' + '='.repeat(80));
  console.log('Protection mechanisms demonstrated:');
  console.log('  ✅ HMAC signatures for data integrity');
  console.log('  ✅ Tamper-evident audit trails');
  console.log('  ✅ Mass modification detection');
  console.log('  ✅ High-sensitivity field monitoring');
  console.log('  ✅ Audit trail integrity verification');
  console.log('  ✅ Modification velocity tracking');
  console.log('='.repeat(80));
}

module.exports = {
  DataIntegrityManager
};
