/**
 * MITRE ATT&CK T1552: Unsecured Credentials - Secrets Detection
 * Educational demonstration of hardcoded secrets detection
 * 
 * @description Scans code for hardcoded secrets, API keys, tokens, and credentials
 * @reference https://attack.mitre.org/techniques/T1552/
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// =============================================================================
// SECRETS DETECTION SCANNER
// =============================================================================

/**
 * SECURE: Hardcoded secrets detection system
 * Defense against ATT&CK T1552
 * 
 * @description Scans files for hardcoded credentials and sensitive data
 * @security Pattern-based detection of various secret types
 */
class SecretsDetector {
  constructor() {
    // Secret detection patterns
    this.patterns = [
      // API Keys
      {
        name: 'Generic API Key',
        pattern: /['"]?[a-zA-Z0-9_-]*api[_-]?key['"]?\s*[:=]\s*['"]([a-zA-Z0-9_\-]{20,})['"]?/gi,
        severity: 'high',
        description: 'Hardcoded API key detected'
      },
      
      // AWS Keys
      {
        name: 'AWS Access Key ID',
        pattern: /(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}/g,
        severity: 'critical',
        description: 'AWS Access Key ID detected'
      },
      {
        name: 'AWS Secret Key',
        pattern: /['"]?aws[_-]?secret[_-]?access[_-]?key['"]?\s*[:=]\s*['"]([A-Za-z0-9/+=]{40})['"]?/gi,
        severity: 'critical',
        description: 'AWS Secret Access Key detected'
      },
      
      // GitHub Tokens
      {
        name: 'GitHub Token',
        pattern: /ghp_[a-zA-Z0-9]{36}/g,
        severity: 'critical',
        description: 'GitHub Personal Access Token detected'
      },
      {
        name: 'GitHub OAuth Token',
        pattern: /gho_[a-zA-Z0-9]{36}/g,
        severity: 'critical',
        description: 'GitHub OAuth Token detected'
      },
      
      // Slack Tokens
      {
        name: 'Slack Token',
        pattern: /xox[baprs]-[a-zA-Z0-9-]{10,48}/g,
        severity: 'high',
        description: 'Slack API token detected'
      },
      {
        name: 'Slack Webhook',
        pattern: /https:\/\/hooks\.slack\.com\/services\/T[a-zA-Z0-9_]+\/B[a-zA-Z0-9_]+\/[a-zA-Z0-9_]+/g,
        severity: 'high',
        description: 'Slack webhook URL detected'
      },
      
      // Google API Keys
      {
        name: 'Google API Key',
        pattern: /AIza[0-9A-Za-z\\-_]{35}/g,
        severity: 'high',
        description: 'Google API key detected'
      },
      {
        name: 'Google OAuth',
        pattern: /[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com/g,
        severity: 'high',
        description: 'Google OAuth client ID detected'
      },
      
      // Generic Secrets
      {
        name: 'Generic Secret',
        pattern: /['"]?[a-zA-Z0-9_-]*secret['"]?\s*[:=]\s*['"]([a-zA-Z0-9_\-!@#$%^&*()+=]{16,})['"]?/gi,
        severity: 'high',
        description: 'Hardcoded secret detected'
      },
      
      // Passwords
      {
        name: 'Password',
        pattern: /['"]?password['"]?\s*[:=]\s*['"]([^'"]{8,})['"]?/gi,
        severity: 'high',
        description: 'Hardcoded password detected',
        exclude: ['password', 'your_password', 'changeme', 'example', 'placeholder']
      },
      
      // Database Connection Strings
      {
        name: 'Database Connection String',
        pattern: /(postgres|mysql|mongodb|redis):\/\/[^\s'"]+:[^\s'"]+@[^\s'"]+/gi,
        severity: 'critical',
        description: 'Database connection string with credentials detected'
      },
      
      // Private Keys
      {
        name: 'Private Key',
        pattern: /-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----/g,
        severity: 'critical',
        description: 'Private key detected'
      },
      
      // JWT Tokens
      {
        name: 'JWT Token',
        pattern: /eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*/g,
        severity: 'medium',
        description: 'JWT token detected'
      },
      
      // Stripe Keys
      {
        name: 'Stripe API Key',
        pattern: /(sk|pk)_(test|live)_[0-9a-zA-Z]{24,}/g,
        severity: 'critical',
        description: 'Stripe API key detected'
      },
      
      // Twilio Keys
      {
        name: 'Twilio API Key',
        pattern: /SK[a-z0-9]{32}/g,
        severity: 'high',
        description: 'Twilio API key detected'
      },
      
      // SendGrid Keys
      {
        name: 'SendGrid API Key',
        pattern: /SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}/g,
        severity: 'high',
        description: 'SendGrid API key detected'
      },
      
      // MailChimp Keys
      {
        name: 'MailChimp API Key',
        pattern: /[a-f0-9]{32}-us[0-9]{1,2}/g,
        severity: 'high',
        description: 'MailChimp API key detected'
      },
      
      // Generic Token
      {
        name: 'Generic Token',
        pattern: /['"]?[a-zA-Z0-9_-]*token['"]?\s*[:=]\s*['"]([a-zA-Z0-9_\-]{20,})['"]?/gi,
        severity: 'medium',
        description: 'Hardcoded token detected'
      },
      
      // Bearer Token
      {
        name: 'Bearer Token',
        pattern: /Bearer\s+[a-zA-Z0-9_\-\.]{20,}/gi,
        severity: 'high',
        description: 'Bearer token detected'
      }
    ];

    // File extensions to scan
    this.scannableExtensions = [
      '.js', '.jsx', '.ts', '.tsx', '.json', '.env',
      '.yml', '.yaml', '.xml', '.config', '.conf',
      '.py', '.rb', '.java', '.go', '.cs', '.php'
    ];

    // Files/directories to skip
    this.excludePatterns = [
      'node_modules',
      '.git',
      'dist',
      'build',
      'coverage',
      '.next',
      'vendor',
      'package-lock.json',
      'yarn.lock'
    ];
  }

  /**
   * Scans a directory or file for secrets
   * @param {string} targetPath - Path to scan
   * @param {object} options - Scan options
   * @returns {object} Scan results
   */
  scan(targetPath, options = {}) {
    const results = {
      scannedFiles: 0,
      findings: [],
      errors: [],
      timestamp: new Date().toISOString()
    };

    try {
      const stats = fs.statSync(targetPath);

      if (stats.isDirectory()) {
        this.scanDirectory(targetPath, results, options);
      } else if (stats.isFile()) {
        this.scanFile(targetPath, results, options);
      }

      // Sort findings by severity
      results.findings.sort((a, b) => {
        const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
        return severityOrder[a.severity] - severityOrder[b.severity];
      });

    } catch (error) {
      results.errors.push({
        path: targetPath,
        error: error.message
      });
    }

    return results;
  }

  /**
   * Scans a directory recursively
   * @param {string} dirPath - Directory path
   * @param {object} results - Results object
   * @param {object} options - Scan options
   */
  scanDirectory(dirPath, results, options = {}) {
    try {
      const entries = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);

        // Skip excluded paths
        if (this.shouldExclude(entry.name)) {
          continue;
        }

        if (entry.isDirectory()) {
          this.scanDirectory(fullPath, results, options);
        } else if (entry.isFile()) {
          this.scanFile(fullPath, results, options);
        }
      }
    } catch (error) {
      results.errors.push({
        path: dirPath,
        error: error.message
      });
    }
  }

  /**
   * Scans a single file for secrets
   * @param {string} filePath - File path
   * @param {object} results - Results object
   * @param {object} options - Scan options
   */
  scanFile(filePath, results, options = {}) {
    // Check if file extension is scannable
    const ext = path.extname(filePath);
    if (!this.scannableExtensions.includes(ext) && !options.scanAll) {
      return;
    }

    try {
      const content = fs.readFileSync(filePath, 'utf8');
      results.scannedFiles++;

      const lines = content.split('\n');

      // Apply each pattern
      for (const patternDef of this.patterns) {
        const matches = content.matchAll(patternDef.pattern);

        for (const match of matches) {
          const matchedText = match[0];
          const capturedValue = match[1] || matchedText;

          // Skip if in exclusion list
          if (patternDef.exclude && patternDef.exclude.includes(capturedValue.toLowerCase())) {
            continue;
          }

          // Find line number
          const lineNumber = this.findLineNumber(content, match.index);
          const lineContent = lines[lineNumber - 1]?.trim();

          // Calculate entropy (high entropy = likely random secret)
          const entropy = this.calculateEntropy(capturedValue);

          // Skip low-entropy values (likely not real secrets)
          if (entropy < 3.0 && patternDef.severity !== 'critical') {
            continue;
          }

          results.findings.push({
            file: filePath,
            line: lineNumber,
            column: match.index - content.lastIndexOf('\n', match.index),
            type: patternDef.name,
            severity: patternDef.severity,
            description: patternDef.description,
            matched: this.maskSecret(matchedText),
            lineContent: this.maskSecret(lineContent),
            entropy: entropy.toFixed(2),
            recommendation: this.getRecommendation(patternDef.name)
          });
        }
      }

    } catch (error) {
      results.errors.push({
        path: filePath,
        error: error.message
      });
    }
  }

  /**
   * Finds line number for a character index
   * @param {string} content - File content
   * @param {number} index - Character index
   * @returns {number} Line number (1-indexed)
   */
  findLineNumber(content, index) {
    const upToMatch = content.substring(0, index);
    return upToMatch.split('\n').length;
  }

  /**
   * Calculates Shannon entropy of a string
   * @param {string} str - Input string
   * @returns {number} Entropy value
   */
  calculateEntropy(str) {
    const len = str.length;
    const frequencies = {};

    // Count character frequencies
    for (const char of str) {
      frequencies[char] = (frequencies[char] || 0) + 1;
    }

    // Calculate entropy
    let entropy = 0;
    for (const freq of Object.values(frequencies)) {
      const p = freq / len;
      entropy -= p * Math.log2(p);
    }

    return entropy;
  }

  /**
   * Masks a secret value for display
   * @param {string} text - Text containing secret
   * @returns {string} Masked text
   */
  maskSecret(text) {
    if (!text || text.length < 8) {
      return '***REDACTED***';
    }

    // Show first 4 and last 4 characters
    const start = text.substring(0, 4);
    const end = text.substring(text.length - 4);
    const middle = '*'.repeat(Math.min(text.length - 8, 20));

    return `${start}${middle}${end}`;
  }

  /**
   * Checks if path should be excluded
   * @param {string} name - File or directory name
   * @returns {boolean} True if should be excluded
   */
  shouldExclude(name) {
    return this.excludePatterns.some(pattern => name.includes(pattern));
  }

  /**
   * Gets remediation recommendation for a secret type
   * @param {string} secretType - Type of secret
   * @returns {string} Recommendation
   */
  getRecommendation(secretType) {
    const recommendations = {
      'AWS Access Key ID': 'Rotate AWS credentials immediately and use IAM roles or AWS Secrets Manager',
      'AWS Secret Key': 'Rotate AWS credentials immediately and use IAM roles or AWS Secrets Manager',
      'GitHub Token': 'Revoke token at https://github.com/settings/tokens and use encrypted secrets',
      'GitHub OAuth Token': 'Revoke token and use GitHub Actions secrets or encrypted storage',
      'Slack Token': 'Revoke token and use environment variables or secret management',
      'Google API Key': 'Rotate key and restrict by IP/referrer in Google Cloud Console',
      'Database Connection String': 'Use environment variables and never commit connection strings',
      'Private Key': 'Remove immediately and regenerate key pair',
      'Stripe API Key': 'Rotate key at https://dashboard.stripe.com/apikeys',
      'Bearer Token': 'Revoke token and use secure token storage',
      'Password': 'Remove password and use environment variables or secret management',
      'Generic Secret': 'Move to environment variables or use a secret management service',
      'Generic API Key': 'Rotate key and use environment variables',
      'Generic Token': 'Rotate token and use secure storage'
    };

    return recommendations[secretType] || 'Move to environment variables or secret management service';
  }

  /**
   * Generates a detailed report
   * @param {object} results - Scan results
   * @returns {string} Formatted report
   */
  generateReport(results) {
    let report = '\n' + '='.repeat(80) + '\n';
    report += 'SECRETS DETECTION REPORT - MITRE ATT&CK T1552\n';
    report += '='.repeat(80) + '\n\n';
    report += `Scan Date: ${results.timestamp}\n`;
    report += `Files Scanned: ${results.scannedFiles}\n`;
    report += `Secrets Found: ${results.findings.length}\n`;
    report += `Errors: ${results.errors.length}\n\n`;

    // Summary by severity
    const bySeverity = {
      critical: results.findings.filter(f => f.severity === 'critical').length,
      high: results.findings.filter(f => f.severity === 'high').length,
      medium: results.findings.filter(f => f.severity === 'medium').length,
      low: results.findings.filter(f => f.severity === 'low').length
    };

    report += 'SEVERITY BREAKDOWN:\n';
    report += `  🔴 Critical: ${bySeverity.critical}\n`;
    report += `  🟠 High: ${bySeverity.high}\n`;
    report += `  🟡 Medium: ${bySeverity.medium}\n`;
    report += `  🟢 Low: ${bySeverity.low}\n\n`;

    if (results.findings.length > 0) {
      report += 'FINDINGS:\n\n';

      results.findings.forEach((finding, index) => {
        const severityIcon = {
          critical: '🔴',
          high: '🟠',
          medium: '🟡',
          low: '🟢'
        }[finding.severity];

        report += `${index + 1}. ${severityIcon} ${finding.type} (${finding.severity.toUpperCase()})\n`;
        report += `   File: ${finding.file}:${finding.line}\n`;
        report += `   Description: ${finding.description}\n`;
        report += `   Matched: ${finding.matched}\n`;
        report += `   Entropy: ${finding.entropy}\n`;
        report += `   Line: ${finding.lineContent}\n`;
        report += `   Recommendation: ${finding.recommendation}\n\n`;
      });
    }

    if (results.errors.length > 0) {
      report += 'ERRORS:\n';
      results.errors.forEach((error, index) => {
        report += `  ${index + 1}. ${error.path}: ${error.error}\n`;
      });
      report += '\n';
    }

    report += '='.repeat(80) + '\n';
    report += '⚠️  IMPORTANT: If secrets are found:\n';
    report += '   1. Rotate/revoke the exposed credentials immediately\n';
    report += '   2. Remove secrets from code and commit history (use git filter-branch)\n';
    report += '   3. Use environment variables or secret management (Vault, AWS Secrets Manager)\n';
    report += '   4. Implement pre-commit hooks to prevent future exposures\n';
    report += '='.repeat(80) + '\n';

    return report;
  }

  /**
   * Creates a sample vulnerable code file for testing
   * @param {string} outputPath - Output file path
   */
  static createVulnerableSample(outputPath) {
    const sampleCode = `
// VULNERABLE CODE SAMPLE - FOR EDUCATIONAL PURPOSES ONLY
// This file contains intentional security vulnerabilities

// AWS Credentials (VULNERABLE!)
const AWS_ACCESS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE';
const AWS_SECRET_ACCESS_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY';

// API Keys (VULNERABLE!)
const STRIPE_KEY = 'sk_live_EXAMPLE_FAKE_KEY_DO_NOT_USE';
const GITHUB_TOKEN = 'ghp_1234567890abcdefghijklmnopqrstuv';
const SLACK_TOKEN = 'xoxb-EXAMPLE-FAKE-TOKEN-DO-NOT-USE';

// Database Connection (VULNERABLE!)
const DB_URL = 'mongodb://admin:SuperSecret123@prod-db.example.com:27017/mydb';

// Google API Key (VULNERABLE!)
const GOOGLE_API_KEY = 'AIzaSyD1234567890abcdefghijklmnopqrstuvw';

// JWT Token (VULNERABLE!)
const JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';

// Password (VULNERABLE!)
const adminPassword = 'MySecretPassword123!';

// Private Key (VULNERABLE!)
const privateKey = \`-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890...
-----END RSA PRIVATE KEY-----\`;

// SECURE ALTERNATIVE:
// Use environment variables instead:
// const AWS_ACCESS_KEY_ID = process.env.AWS_ACCESS_KEY_ID;
// const STRIPE_KEY = process.env.STRIPE_KEY;
// const DB_URL = process.env.DATABASE_URL;
`;

    fs.writeFileSync(outputPath, sampleCode);
    console.log(`✅ Created vulnerable sample at: ${outputPath}`);
  }
}

// =============================================================================
// EXAMPLE USAGE
// =============================================================================

if (require.main === module) {
  console.log('='.repeat(80));
  console.log('MITRE ATT&CK T1552: Secrets Detection Demo');
  console.log('='.repeat(80));
  console.log();

  const detector = new SecretsDetector();

  // Example 1: Create vulnerable sample file
  console.log('--- Creating Vulnerable Sample File ---\n');
  const samplePath = path.join(__dirname, 'vulnerable-sample.js');
  SecretsDetector.createVulnerableSample(samplePath);

  // Example 2: Scan the sample file
  console.log('\n--- Scanning for Secrets ---\n');
  const results = detector.scan(samplePath);

  // Generate and display report
  const report = detector.generateReport(results);
  console.log(report);

  // Clean up sample file
  try {
    fs.unlinkSync(samplePath);
    console.log(`🧹 Cleaned up sample file: ${samplePath}\n`);
  } catch (error) {
    console.log(`⚠️  Could not clean up sample file: ${error.message}\n`);
  }

  console.log('To scan your project, run:');
  console.log(`  const detector = new SecretsDetector();`);
  console.log(`  const results = detector.scan('/path/to/your/project');`);
  console.log(`  console.log(detector.generateReport(results));`);
  console.log('\n' + '='.repeat(80));
}

module.exports = { SecretsDetector };
