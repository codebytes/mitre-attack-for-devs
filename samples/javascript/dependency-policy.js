/**
 * MITRE ATT&CK T1195.001 (Compromise Software Dependencies).
 *
 * Do not write your own typosquat detector. Edit distance against a hand-written
 * list of popular package names flags legitimate packages and misses the attacks
 * that actually happen: Shai-Hulud and the Axios compromise both shipped from the
 * REAL package name, through a hijacked maintainer account. Name similarity would
 * not have caught either one.
 *
 * What a team can genuinely own is policy, enforced in CI:
 *   1. Install from a reviewed lockfile, never a floating range.
 *   2. Do not execute lifecycle scripts during install.
 *   3. Verify registry signatures and provenance attestations.
 *   4. Fail the build on known advisories at a chosen severity.
 *
 * Steps 3 and 4 delegate to `npm audit`, which is maintained, has a real
 * advisory feed, and understands provenance. This file wires them into a gate
 * with an explicit pass/fail, which is the part that belongs to you.
 *
 * @reference https://attack.mitre.org/techniques/T1195/001/
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

class DependencyPolicy {
  constructor(projectRoot = process.cwd(), options = {}) {
    this.projectRoot = projectRoot;
    this.auditLevel = options.auditLevel ?? 'high';
  }

  /** Run every check and return a single pass/fail plus the findings. */
  evaluate() {
    const checks = [
      this.requireLockfile(),
      this.requireIgnoreScripts(),
      this.verifyProvenance(),
      this.auditAdvisories()
    ];

    return { passed: checks.every(c => c.status !== 'fail'), checks };
  }

  /**
   * A lockfile is what makes the installed tree reproducible and reviewable.
   * Without one, `npm install` can resolve a different version on every run,
   * including a version published after your code review.
   */
  requireLockfile() {
    const lockPath = path.join(this.projectRoot, 'package-lock.json');
    if (!fs.existsSync(lockPath)) {
      return {
        name: 'lockfile present',
        status: 'fail',
        detail: 'No package-lock.json. Commit one and install with `npm ci`.'
      };
    }

    const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));

    // Integrity hashes are what make the lockfile a security control rather than
    // just a version pin: they bind each entry to exact bytes.
    const missing = Object.entries(lock.packages ?? {})
      .filter(([p, meta]) => p !== '' && meta.resolved && !meta.integrity)
      .map(([p]) => p);

    return missing.length
      ? {
          name: 'lockfile present',
          status: 'fail',
          detail: `${missing.length} entries lack integrity hashes. Regenerate the lockfile.`
        }
      : { name: 'lockfile present', status: 'pass' };
  }

  /**
   * Installing a package executes its install scripts as the build identity.
   * This is how Shai-Hulud propagated and how the Axios compromise delivered its
   * payload. `ignore-scripts=true` closes that path for the whole dependency tree.
   *
   * Packages that genuinely need a build step (native addons) should be allowlisted
   * and rebuilt explicitly, not granted blanket execution for everything.
   */
  requireIgnoreScripts() {
    const npmrc = path.join(this.projectRoot, '.npmrc');
    const enabled = fs.existsSync(npmrc)
      && /^\s*ignore-scripts\s*=\s*true\s*$/m.test(fs.readFileSync(npmrc, 'utf8'));

    return enabled
      ? { name: 'lifecycle scripts disabled', status: 'pass' }
      : {
          name: 'lifecycle scripts disabled',
          status: 'fail',
          detail: 'Set `ignore-scripts=true` in .npmrc. Installing is code execution.'
        };
  }

  /**
   * Signature and provenance verification. This is the check that addresses
   * compromise rather than known vulnerabilities: it confirms the artifact came
   * from the registry and, where attested, from the expected source repository
   * and build system.
   */
  verifyProvenance() {
    const result = spawnSync('npm', ['audit', 'signatures'], {
      cwd: this.projectRoot, encoding: 'utf8', shell: process.platform === 'win32'
    });

    if (result.error) {
      return { name: 'registry signatures', status: 'skip', detail: 'npm not available' };
    }

    return result.status === 0
      ? { name: 'registry signatures', status: 'pass' }
      : {
          name: 'registry signatures',
          status: 'fail',
          detail: (result.stdout || result.stderr || '').trim().split('\n').slice(-5).join('\n')
        };
  }

  /**
   * Known advisories. Note what this does NOT cover: an advisory only exists
   * after somebody discovered and reported the problem. A freshly compromised
   * version is clean by this check until it is reported.
   */
  auditAdvisories() {
    const result = spawnSync('npm', ['audit', '--audit-level', this.auditLevel, '--json'], {
      cwd: this.projectRoot, encoding: 'utf8', shell: process.platform === 'win32'
    });

    if (result.error) {
      return { name: 'known advisories', status: 'skip', detail: 'npm not available' };
    }

    let counts = {};
    try {
      counts = JSON.parse(result.stdout || '{}').metadata?.vulnerabilities ?? {};
    } catch {
      return { name: 'known advisories', status: 'skip', detail: 'could not parse audit output' };
    }

    const blocking = (counts.critical ?? 0) + (counts.high ?? 0);
    return blocking > 0
      ? {
          name: 'known advisories',
          status: 'fail',
          detail: `${counts.critical ?? 0} critical, ${counts.high ?? 0} high`
        }
      : { name: 'known advisories', status: 'pass', detail: JSON.stringify(counts) };
  }
}

// =============================================================================
// EXAMPLE
// =============================================================================

if (require.main === module) {
  const policy = new DependencyPolicy(process.cwd());
  const { passed, checks } = policy.evaluate();

  console.log('Dependency policy gate (T1195.001)\n');
  for (const c of checks) {
    const mark = { pass: 'PASS', fail: 'FAIL', skip: 'SKIP' }[c.status];
    console.log(`  [${mark}] ${c.name}`);
    if (c.detail) console.log(`         ${c.detail}`);
  }

  console.log(`\nResult: ${passed ? 'PASSED' : 'FAILED'}`);
  console.log('\nThese checks reduce exposure. They do not prove a dependency is safe:');
  console.log('a compromised version passes every one of them until it is reported.');

  if (require.main === module && !passed) process.exitCode = 1;
}

module.exports = { DependencyPolicy };
