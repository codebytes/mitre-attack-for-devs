/**
 * MITRE ATT&CK T1195.001: Compromise Software Dependencies - Supply Chain Verification
 * Educational demonstration of supply chain security verification
 * 
 * @description Detects malicious packages, typosquatting, and integrity issues
 * @reference https://attack.mitre.org/techniques/T1195/001/
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync } = require('child_process');

// =============================================================================
// SUPPLY CHAIN SECURITY VERIFIER
// =============================================================================

/**
 * SECURE: Supply chain security verification system
 * Defense against ATT&CK T1195.001
 * 
 * @description Verifies package integrity, detects typosquatting, and checks for malicious patterns
 * @security Multi-layered supply chain security checks
 */
class SupplyChainVerifier {
  constructor(projectRoot = process.cwd()) {
    this.projectRoot = projectRoot;
    this.packageJsonPath = path.join(projectRoot, 'package.json');
    this.packageLockPath = path.join(projectRoot, 'package-lock.json');
    
    // Known popular packages for typosquatting detection
    this.popularPackages = [
      'express', 'react', 'lodash', 'axios', 'moment', 'webpack',
      'babel', 'eslint', 'typescript', 'vue', 'angular', 'next',
      'jest', 'mocha', 'chai', 'commander', 'dotenv', 'cors',
      'body-parser', 'nodemon', 'prettier', 'chalk', 'debug'
    ];

    // Suspicious patterns in package names
    this.suspiciousPatterns = [
      /^@[^/]+\/.*-utils$/i,     // Generic utility packages in scopes
      /test|temp|poc|demo/i,      // Test/temporary packages
      /v\d+$/,                     // Versioned package names (e.g., lodashv2)
      /^(js|node)-.+/i,           // js- or node- prefixes (common in typosquats)
    ];

    // Dangerous npm lifecycle scripts
    this.dangerousScripts = [
      'preinstall', 'install', 'postinstall',
      'preuninstall', 'uninstall', 'postuninstall'
    ];
  }

  /**
   * Runs comprehensive supply chain verification
   * @returns {object} Verification results
   */
  verifySupplyChain() {
    console.log('🔍 Starting supply chain verification...\n');

    const results = {
      timestamp: new Date().toISOString(),
      checks: [],
      warnings: [],
      errors: [],
      passed: true
    };

    try {
      // Check 1: Verify package.json exists
      results.checks.push(this.checkPackageJsonExists());

      // Check 2: Verify package-lock.json integrity
      results.checks.push(this.checkLockfileIntegrity());

      // Check 3: Detect typosquatting
      results.checks.push(this.detectTyposquatting());

      // Check 4: Check for dangerous install scripts
      results.checks.push(this.checkDangerousScripts());

      // Check 5: Run npm audit
      results.checks.push(this.runNpmAudit());

      // Check 6: Verify package signatures (simulated)
      results.checks.push(this.verifyPackageSignatures());

      // Check 7: Check for unexpected dependencies
      results.checks.push(this.checkUnexpectedDependencies());

      // Aggregate results
      results.checks.forEach(check => {
        if (check.warnings) {
          results.warnings.push(...check.warnings);
        }
        if (check.errors) {
          results.errors.push(...check.errors);
        }
        if (check.status === 'failed') {
          results.passed = false;
        }
      });

    } catch (error) {
      results.errors.push({
        message: 'Verification failed',
        error: error.message
      });
      results.passed = false;
    }

    return results;
  }

  /**
   * Check 1: Verify package.json exists
   */
  checkPackageJsonExists() {
    console.log('📋 Checking package.json...');
    
    if (!fs.existsSync(this.packageJsonPath)) {
      console.log('   ❌ package.json not found');
      return {
        name: 'package.json existence',
        status: 'failed',
        errors: [{ message: 'package.json not found' }]
      };
    }

    console.log('   ✅ package.json found');
    return {
      name: 'package.json existence',
      status: 'passed'
    };
  }

  /**
   * Check 2: Verify package-lock.json integrity
   */
  checkLockfileIntegrity() {
    console.log('🔒 Checking lockfile integrity...');

    const warnings = [];
    const errors = [];

    if (!fs.existsSync(this.packageLockPath)) {
      console.log('   ⚠️  package-lock.json not found (recommended for security)');
      warnings.push({
        message: 'No package-lock.json found',
        recommendation: 'Use package-lock.json to lock dependency versions'
      });
      return {
        name: 'lockfile integrity',
        status: 'warning',
        warnings
      };
    }

    try {
      const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf8'));
      const packageLock = JSON.parse(fs.readFileSync(this.packageLockPath, 'utf8'));

      // Check if lockfile version matches package.json version
      if (packageJson.version !== packageLock.version) {
        warnings.push({
          message: 'Version mismatch between package.json and package-lock.json',
          packageJson: packageJson.version,
          packageLock: packageLock.version
        });
        console.log('   ⚠️  Version mismatch detected');
      }

      // Check lockfile version (lockfileVersion)
      if (!packageLock.lockfileVersion) {
        warnings.push({
          message: 'Old lockfile format detected',
          recommendation: 'Run npm install with npm v7+ to upgrade'
        });
        console.log('   ⚠️  Old lockfile format');
      }

      // Verify integrity hashes exist
      if (packageLock.packages) {
        let missingIntegrity = 0;
        for (const [pkgPath, pkg] of Object.entries(packageLock.packages)) {
          if (pkgPath !== '' && pkg.resolved && !pkg.integrity) {
            missingIntegrity++;
          }
        }
        if (missingIntegrity > 0) {
          warnings.push({
            message: `${missingIntegrity} packages missing integrity hashes`,
            recommendation: 'Regenerate package-lock.json'
          });
          console.log(`   ⚠️  ${missingIntegrity} packages missing integrity hashes`);
        }
      }

      if (warnings.length === 0) {
        console.log('   ✅ Lockfile integrity verified');
      }

      return {
        name: 'lockfile integrity',
        status: warnings.length > 0 ? 'warning' : 'passed',
        warnings
      };

    } catch (error) {
      console.log('   ❌ Failed to parse lockfile');
      return {
        name: 'lockfile integrity',
        status: 'failed',
        errors: [{ message: 'Failed to parse lockfile', error: error.message }]
      };
    }
  }

  /**
   * Check 3: Detect typosquatting
   */
  detectTyposquatting() {
    console.log('🎯 Detecting typosquatting...');

    const warnings = [];

    try {
      const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf8'));
      const allDeps = {
        ...packageJson.dependencies,
        ...packageJson.devDependencies
      };

      const installedPackages = Object.keys(allDeps);

      for (const pkg of installedPackages) {
        // Skip scoped packages from known organizations
        if (pkg.startsWith('@')) {
          continue;
        }

        // Check for suspicious patterns
        for (const pattern of this.suspiciousPatterns) {
          if (pattern.test(pkg)) {
            warnings.push({
              package: pkg,
              issue: 'Suspicious package name pattern',
              pattern: pattern.toString()
            });
            console.log(`   ⚠️  Suspicious: ${pkg} matches pattern ${pattern}`);
          }
        }

        // Check for typosquatting (similar to popular packages)
        for (const popular of this.popularPackages) {
          const distance = this.levenshteinDistance(pkg.toLowerCase(), popular.toLowerCase());
          
          // If edit distance is 1-2, it's likely a typosquat
          if (distance > 0 && distance <= 2) {
            warnings.push({
              package: pkg,
              issue: 'Possible typosquatting',
              similarTo: popular,
              editDistance: distance,
              recommendation: `Did you mean '${popular}'?`
            });
            console.log(`   ⚠️  Typosquat alert: '${pkg}' is similar to '${popular}' (distance: ${distance})`);
          }
        }
      }

      if (warnings.length === 0) {
        console.log('   ✅ No typosquatting detected');
      }

      return {
        name: 'typosquatting detection',
        status: warnings.length > 0 ? 'warning' : 'passed',
        warnings
      };

    } catch (error) {
      console.log('   ❌ Failed to check for typosquatting');
      return {
        name: 'typosquatting detection',
        status: 'failed',
        errors: [{ message: 'Failed to check for typosquatting', error: error.message }]
      };
    }
  }

  /**
   * Check 4: Check for dangerous install scripts
   */
  checkDangerousScripts() {
    console.log('⚠️  Checking for dangerous install scripts...');

    const warnings = [];

    try {
      if (!fs.existsSync(this.packageLockPath)) {
        return {
          name: 'dangerous scripts',
          status: 'skipped',
          warnings: [{ message: 'No package-lock.json to analyze' }]
        };
      }

      const packageLock = JSON.parse(fs.readFileSync(this.packageLockPath, 'utf8'));

      if (packageLock.packages) {
        for (const [pkgPath, pkg] of Object.entries(packageLock.packages)) {
          if (pkgPath === '') continue; // Skip root

          // Check if package has install scripts
          const hasInstallScript = pkg.hasInstallScript || 
            (pkg.scripts && this.dangerousScripts.some(s => pkg.scripts[s]));

          if (hasInstallScript) {
            const packageName = pkgPath.replace(/^node_modules\//, '');
            warnings.push({
              package: packageName,
              issue: 'Has install/lifecycle scripts',
              risk: 'Scripts run automatically and could be malicious',
              recommendation: 'Review package source code before installing'
            });
            console.log(`   ⚠️  ${packageName} has install scripts`);
          }
        }
      }

      if (warnings.length === 0) {
        console.log('   ✅ No dangerous install scripts found');
      }

      return {
        name: 'dangerous scripts',
        status: warnings.length > 0 ? 'warning' : 'passed',
        warnings
      };

    } catch (error) {
      console.log('   ❌ Failed to check for dangerous scripts');
      return {
        name: 'dangerous scripts',
        status: 'failed',
        errors: [{ message: 'Failed to check scripts', error: error.message }]
      };
    }
  }

  /**
   * Check 5: Run npm audit
   */
  runNpmAudit() {
    console.log('🔍 Running npm audit...');

    try {
      // Run npm audit in JSON format
      const auditResult = execSync('npm audit --json', {
        cwd: this.projectRoot,
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      });

      const audit = JSON.parse(auditResult);
      const vulnerabilities = audit.metadata?.vulnerabilities || {};
      const total = Object.values(vulnerabilities).reduce((sum, count) => sum + count, 0);

      if (total === 0) {
        console.log('   ✅ No vulnerabilities found');
        return {
          name: 'npm audit',
          status: 'passed',
          vulnerabilities
        };
      }

      console.log(`   ⚠️  Found ${total} vulnerabilities`);
      console.log(`      Critical: ${vulnerabilities.critical || 0}`);
      console.log(`      High: ${vulnerabilities.high || 0}`);
      console.log(`      Moderate: ${vulnerabilities.moderate || 0}`);
      console.log(`      Low: ${vulnerabilities.low || 0}`);

      return {
        name: 'npm audit',
        status: (vulnerabilities.critical || vulnerabilities.high) ? 'failed' : 'warning',
        vulnerabilities,
        warnings: [{
          message: `Found ${total} vulnerabilities`,
          recommendation: 'Run npm audit fix to resolve'
        }]
      };

    } catch (error) {
      // npm audit returns non-zero exit code when vulnerabilities found
      if (error.stdout) {
        try {
          const audit = JSON.parse(error.stdout);
          const vulnerabilities = audit.metadata?.vulnerabilities || {};
          const total = Object.values(vulnerabilities).reduce((sum, count) => sum + count, 0);

          console.log(`   ⚠️  Found ${total} vulnerabilities`);

          return {
            name: 'npm audit',
            status: (vulnerabilities.critical || vulnerabilities.high) ? 'failed' : 'warning',
            vulnerabilities,
            warnings: [{
              message: `Found ${total} vulnerabilities`,
              recommendation: 'Run npm audit fix to resolve'
            }]
          };
        } catch (parseError) {
          // Fall through to error case
        }
      }

      console.log('   ⚠️  Could not run npm audit (may not be in a project)');
      return {
        name: 'npm audit',
        status: 'skipped',
        warnings: [{ message: 'Could not run npm audit', error: error.message }]
      };
    }
  }

  /**
   * Check 6: Verify package signatures (simulated - npm doesn't fully support this yet)
   */
  verifyPackageSignatures() {
    console.log('🔐 Verifying package signatures...');

    // Note: Full package signature verification is not yet widely supported in npm
    // This is a simulated check showing what should be done

    console.log('   ℹ️  Package signature verification not fully supported by npm yet');
    console.log('   ℹ️  Consider using tools like Sigstore for enhanced verification');

    return {
      name: 'package signatures',
      status: 'skipped',
      warnings: [{
        message: 'Package signature verification not available',
        recommendation: 'Monitor npm for signature verification support'
      }]
    };
  }

  /**
   * Check 7: Check for unexpected dependencies
   */
  checkUnexpectedDependencies() {
    console.log('📦 Checking for unexpected dependencies...');

    const warnings = [];

    try {
      const packageJson = JSON.parse(fs.readFileSync(this.packageJsonPath, 'utf8'));
      
      if (fs.existsSync(this.packageLockPath)) {
        const packageLock = JSON.parse(fs.readFileSync(this.packageLockPath, 'utf8'));
        
        // Count total packages
        const totalPackages = packageLock.packages ? Object.keys(packageLock.packages).length - 1 : 0;
        const directDeps = Object.keys({
          ...packageJson.dependencies,
          ...packageJson.devDependencies
        }).length;

        // High ratio of transitive dependencies can be suspicious
        const ratio = totalPackages / Math.max(directDeps, 1);

        console.log(`   📊 Direct dependencies: ${directDeps}`);
        console.log(`   📊 Total packages: ${totalPackages}`);
        console.log(`   📊 Ratio: ${ratio.toFixed(1)}:1`);

        if (ratio > 20) {
          warnings.push({
            message: 'Unusually high number of transitive dependencies',
            directDeps,
            totalPackages,
            ratio: ratio.toFixed(1),
            recommendation: 'Review dependency tree for unnecessary packages'
          });
          console.log('   ⚠️  High transitive dependency ratio');
        } else {
          console.log('   ✅ Dependency ratio looks normal');
        }
      }

      return {
        name: 'unexpected dependencies',
        status: warnings.length > 0 ? 'warning' : 'passed',
        warnings
      };

    } catch (error) {
      console.log('   ❌ Failed to check dependencies');
      return {
        name: 'unexpected dependencies',
        status: 'failed',
        errors: [{ message: 'Failed to check dependencies', error: error.message }]
      };
    }
  }

  /**
   * Calculates Levenshtein distance between two strings
   * @param {string} str1 - First string
   * @param {string} str2 - Second string
   * @returns {number} Edit distance
   */
  levenshteinDistance(str1, str2) {
    const len1 = str1.length;
    const len2 = str2.length;
    const matrix = Array(len1 + 1).fill(null).map(() => Array(len2 + 1).fill(0));

    for (let i = 0; i <= len1; i++) matrix[i][0] = i;
    for (let j = 0; j <= len2; j++) matrix[0][j] = j;

    for (let i = 1; i <= len1; i++) {
      for (let j = 1; j <= len2; j++) {
        const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,      // deletion
          matrix[i][j - 1] + 1,      // insertion
          matrix[i - 1][j - 1] + cost // substitution
        );
      }
    }

    return matrix[len1][len2];
  }

  /**
   * Generates verification report
   * @param {object} results - Verification results
   * @returns {string} Formatted report
   */
  generateReport(results) {
    let report = '\n' + '='.repeat(80) + '\n';
    report += 'SUPPLY CHAIN SECURITY VERIFICATION REPORT\n';
    report += '='.repeat(80) + '\n\n';
    report += `Timestamp: ${results.timestamp}\n`;
    report += `Overall Status: ${results.passed ? '✅ PASSED' : '❌ FAILED'}\n`;
    report += `Warnings: ${results.warnings.length}\n`;
    report += `Errors: ${results.errors.length}\n\n`;

    report += 'CHECKS:\n';
    results.checks.forEach(check => {
      const statusIcon = check.status === 'passed' ? '✅' : 
                        check.status === 'warning' ? '⚠️' : 
                        check.status === 'skipped' ? 'ℹ️' : '❌';
      report += `  ${statusIcon} ${check.name}: ${check.status.toUpperCase()}\n`;
    });

    if (results.warnings.length > 0) {
      report += '\nWARNINGS:\n';
      results.warnings.forEach((warning, i) => {
        report += `  ${i + 1}. ${warning.message}\n`;
        if (warning.recommendation) {
          report += `     Recommendation: ${warning.recommendation}\n`;
        }
      });
    }

    if (results.errors.length > 0) {
      report += '\nERRORS:\n';
      results.errors.forEach((error, i) => {
        report += `  ${i + 1}. ${error.message}\n`;
      });
    }

    report += '\n' + '='.repeat(80) + '\n';

    return report;
  }
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1195.001: Supply Chain Verification Demo');
  console.log('='.repeat(80));
  console.log();

  // Example 1: Typosquatting detection
  console.log('--- Example 1: Typosquatting Detection ---\n');
  
  const verifier = new SupplyChainVerifier();
  
  const testPackages = ['expres', 'recat', 'loadash', 'axioz', 'express'];
  console.log('Testing package names for typosquatting:\n');
  
  testPackages.forEach(pkg => {
    const distances = verifier.popularPackages.map(popular => ({
      popular,
      distance: verifier.levenshteinDistance(pkg, popular)
    })).filter(d => d.distance > 0 && d.distance <= 2);
    
    if (distances.length > 0) {
      console.log(`⚠️  "${pkg}" - Possible typosquat of: ${distances.map(d => `"${d.popular}" (distance: ${d.distance})`).join(', ')}`);
    } else {
      console.log(`✅ "${pkg}" - No typosquatting detected`);
    }
  });

  // Example 2: Run full verification if in a node project
  console.log('\n--- Example 2: Full Supply Chain Verification ---\n');
  
  const projectVerifier = new SupplyChainVerifier(process.cwd());
  const results = projectVerifier.verifySupplyChain();
  const report = projectVerifier.generateReport(results);
  
  console.log(report);

  console.log('Defense mechanisms demonstrated:');
  console.log('  ✅ Package-lock.json integrity verification');
  console.log('  ✅ Typosquatting detection via edit distance');
  console.log('  ✅ Dangerous install script detection');
  console.log('  ✅ npm audit vulnerability scanning');
  console.log('  ✅ Unexpected dependency analysis');
  console.log('  ✅ Package signature awareness');
  console.log('='.repeat(80));
}

module.exports = { SupplyChainVerifier };
