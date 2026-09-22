/**
 * MITRE ATT&CK T1567 (Exfiltration Over Web Service) and
 * T1020 (Automated Exfiltration).
 *
 * Exfiltration through an API rarely looks like an attack at the request level.
 * Every call is authenticated, authorized, and individually reasonable. The
 * attack is the aggregate.
 *
 * This is a hard budget, not an anomaly score. A fixed limit is testable, is
 * explainable in a runbook, and fails in a predictable direction. A floating
 * "suspicion score" is something nobody can debug during an incident.
 *
 * Deliberately omitted: off-hours and weekend scoring. Distributed teams work at
 * all hours, so that signal generates noise rather than detections.
 *
 * @reference https://attack.mitre.org/techniques/T1567/
 * @reference https://attack.mitre.org/techniques/T1020/
 */

'use strict';

const HOUR_MS = 60 * 60 * 1000;

class ExportBudget {
  /**
   * @param {object} [options]
   * @param {number} [options.maxBytesPerHour] - Rolling outbound byte ceiling per subject.
   * @param {number} [options.maxRowsPerHour]  - Rolling row ceiling per subject.
   */
  constructor(options = {}) {
    this.maxBytesPerHour = options.maxBytesPerHour ?? 100 * 1024 * 1024; // 100 MiB
    this.maxRowsPerHour = options.maxRowsPerHour ?? 50_000;

    // Per-process state. In production this belongs in shared atomic storage
    // (Redis INCR with TTL, or a counter row). A per-instance Map is reset by
    // every deploy and is trivially defeated by spreading calls across replicas.
    this.usage = new Map();
  }

  /**
   * Decide BEFORE serving the response.
   *
   * Checking after the payload is built means the query already ran and the
   * data is one serialization path away from leaving the process.
   *
   * @returns {{allowed: boolean, reason?: string, technique?: string}}
   */
  check(subject, { bytes = 0, rows = 0 }, now = Date.now()) {
    const recent = (this.usage.get(subject) ?? []).filter(e => now - e.at < HOUR_MS);

    const usedBytes = recent.reduce((sum, e) => sum + e.bytes, 0);
    const usedRows = recent.reduce((sum, e) => sum + e.rows, 0);

    // Include the candidate response in the decision. Excluding it lets an
    // attacker always stay one large response under the limit.
    if (usedBytes + bytes > this.maxBytesPerHour) {
      return {
        allowed: false,
        technique: 'T1567',
        reason: `hourly transfer budget exhausted (${usedBytes + bytes} of ${this.maxBytesPerHour} bytes)`
      };
    }

    if (usedRows + rows > this.maxRowsPerHour) {
      return {
        allowed: false,
        technique: 'T1020',
        reason: `hourly row budget exhausted (${usedRows + rows} of ${this.maxRowsPerHour} rows)`
      };
    }

    recent.push({ at: now, bytes, rows });
    this.usage.set(subject, recent);
    return { allowed: true };
  }
}

/**
 * Express middleware.
 *
 * Applied only to export-style routes. Wrapping every endpoint turns a security
 * control into a latency problem and trains the team to raise the limit.
 */
function enforceExportBudget(budget, logger = console) {
  return (req, res, next) => {
    const subject = req.auth?.claims?.sub;
    if (!subject) return res.status(401).json({ error: 'authentication required' });

    const originalJson = res.json.bind(res);

    res.json = (payload) => {
      const rows = Array.isArray(payload) ? payload.length
        : Array.isArray(payload?.data) ? payload.data.length
          : 0;
      const bytes = Buffer.byteLength(JSON.stringify(payload ?? ''));

      const verdict = budget.check(subject, { bytes, rows });

      if (!verdict.allowed) {
        logger.warn({
          event: 'export.blocked',
          attack_technique: verdict.technique,
          subject,
          tenant: req.auth.claims.tid,
          endpoint: req.path,
          rows,
          bytes,
          reason: verdict.reason
        });

        // The caller must not receive the payload that was already assembled.
        res.status(429);
        return originalJson({ error: 'export_budget_exhausted', retryAfterSeconds: 3600 });
      }

      return originalJson(payload);
    };

    next();
  };
}

// =============================================================================
// EXAMPLE
// =============================================================================

if (require.main === module) {
  const budget = new ExportBudget({ maxBytesPerHour: 10 * 1024 * 1024, maxRowsPerHour: 5_000 });
  const now = Date.now();

  console.log('Budget: 10 MiB and 5,000 rows per hour\n');

  console.log('Routine paged reads (200 rows, 400 KiB each):');
  for (let i = 1; i <= 3; i++) {
    const v = budget.check('analyst-1', { bytes: 400 * 1024, rows: 200 }, now);
    console.log(`  request ${i}: ${v.allowed ? 'allowed' : 'BLOCKED - ' + v.reason}`);
  }

  console.log('\nScripted extraction, 900 rows at a time:');
  for (let i = 1; i <= 8; i++) {
    const v = budget.check('analyst-2', { bytes: 900 * 1024, rows: 900 }, now);
    if (!v.allowed) {
      console.log(`  request ${i}: BLOCKED [${v.technique}] ${v.reason}`);
      console.log('\n  Every individual request was authorized and reasonable.');
      console.log('  The budget caught the accumulation, which is the attack.');
      break;
    }
    console.log(`  request ${i}: allowed (${i * 900} rows so far)`);
  }
}

module.exports = { ExportBudget, enforceExportBudget };
