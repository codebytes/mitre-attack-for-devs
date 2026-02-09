"""
MITRE ATT&CK T1552 - Unsecured Credentials

Attackers search for hardcoded credentials in source code, configuration files,
and other artifacts. This includes API keys, passwords, tokens, and connection strings.

This module demonstrates:
- Pattern-based detection of common credential types
- Scanning source files for hardcoded secrets
- Reporting potential security issues

Educational purpose: Shows what attackers look for and how to detect exposed credentials.
Reference: https://attack.mitre.org/techniques/T1552/
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class CredentialType(Enum):
    """Types of credentials that can be detected."""
    API_KEY = "API Key"
    PASSWORD = "Password"
    TOKEN = "Token"
    AWS_KEY = "AWS Access Key"
    PRIVATE_KEY = "Private Key"
    DATABASE_URL = "Database Connection String"
    GENERIC_SECRET = "Generic Secret"


@dataclass
class SecretFinding:
    """Represents a detected credential or secret."""
    file_path: str
    line_number: int
    credential_type: CredentialType
    matched_pattern: str
    context: str
    severity: str


class SecretsScanner:
    """
    Scans source code for hardcoded credentials and secrets.
    
    Detects T1552 (Unsecured Credentials) by identifying patterns
    commonly used for API keys, passwords, tokens, and other secrets.
    
    Educational tool showing what attackers look for when compromising
    source code repositories.
    """
    
    # Regex patterns for detecting various credential types
    PATTERNS = {
        CredentialType.AWS_KEY: [
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
            (r'aws_access_key_id\s*=\s*["\']?([A-Z0-9]{20})["\']?', 'AWS Access Key'),
            (r'aws_secret_access_key\s*=\s*["\']?([A-Za-z0-9/+=]{40})["\']?', 'AWS Secret Key'),
        ],
        
        CredentialType.API_KEY: [
            (r'api[_-]?key\s*[=:]\s*["\']([a-zA-Z0-9\-_]{20,})["\']', 'API Key'),
            (r'apikey\s*[=:]\s*["\']([a-zA-Z0-9\-_]{20,})["\']', 'API Key'),
            (r'api[_-]?secret\s*[=:]\s*["\']([a-zA-Z0-9\-_]{20,})["\']', 'API Secret'),
        ],
        
        CredentialType.PASSWORD: [
            (r'password\s*[=:]\s*["\']([^"\']{8,})["\']', 'Password'),
            (r'passwd\s*[=:]\s*["\']([^"\']{8,})["\']', 'Password'),
            (r'pwd\s*[=:]\s*["\']([^"\']{8,})["\']', 'Password'),
            (r'db_password\s*[=:]\s*["\']([^"\']{8,})["\']', 'Database Password'),
        ],
        
        CredentialType.TOKEN: [
            (r'["\']([a-zA-Z0-9\-_\.]{100,})["\']', 'Long Token (JWT-like)'),
            (r'token\s*[=:]\s*["\']([a-zA-Z0-9\-_]{20,})["\']', 'Token'),
            (r'auth[_-]?token\s*[=:]\s*["\']([a-zA-Z0-9\-_]{20,})["\']', 'Auth Token'),
            (r'bearer\s+([a-zA-Z0-9\-_\.]{20,})', 'Bearer Token'),
        ],
        
        CredentialType.PRIVATE_KEY: [
            (r'-----BEGIN (RSA |DSA )?PRIVATE KEY-----', 'Private Key'),
            (r'-----BEGIN OPENSSH PRIVATE KEY-----', 'SSH Private Key'),
            (r'private_key\s*[=:]\s*["\']([^"\']+)["\']', 'Private Key'),
        ],
        
        CredentialType.DATABASE_URL: [
            (r'(mongodb|postgresql|mysql|redis)://[^:]+:[^@]+@[\w\.\-:]+', 'Database URL with Credentials'),
            (r'jdbc:[^:]+://[^:]+:[^@]+@', 'JDBC Connection String'),
            (r'Server=[^;]+;.*Password=[^;]+', 'SQL Server Connection String'),
        ],
        
        CredentialType.GENERIC_SECRET: [
            (r'secret\s*[=:]\s*["\']([a-zA-Z0-9\-_]{16,})["\']', 'Generic Secret'),
            (r'client[_-]?secret\s*[=:]\s*["\']([a-zA-Z0-9\-_]{16,})["\']', 'Client Secret'),
            (r'encryption[_-]?key\s*[=:]\s*["\']([a-zA-Z0-9\-_]{16,})["\']', 'Encryption Key'),
        ],
    }
    
    # File extensions to scan
    SCANNABLE_EXTENSIONS = {
        '.py', '.js', '.ts', '.java', '.cs', '.go', '.rb', '.php',
        '.yml', '.yaml', '.json', '.xml', '.env', '.config', '.ini',
        '.properties', '.conf', '.sh', '.bash', '.ps1', '.sql'
    }
    
    # Patterns that indicate a finding is likely a false positive
    FALSE_POSITIVE_INDICATORS = [
        'example', 'sample', 'test', 'dummy', 'fake', 'placeholder',
        'your_', 'your-', 'xxx', '***', '...', 'replace', 'change'
    ]
    
    def __init__(self, root_path: str, exclude_dirs: Set[str] = None):
        """
        Initialize the secrets scanner.
        
        Args:
            root_path: Root directory to scan
            exclude_dirs: Directories to exclude (e.g., node_modules, .git)
        """
        self.root_path = Path(root_path)
        self.exclude_dirs = exclude_dirs or {
            '.git', 'node_modules', 'venv', '.venv', '__pycache__',
            'dist', 'build', '.idea', '.vscode'
        }
        self.findings: List[SecretFinding] = []
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned."""
        # Check extension
        if file_path.suffix not in self.SCANNABLE_EXTENSIONS:
            return False
        
        # Check if in excluded directory
        for part in file_path.parts:
            if part in self.exclude_dirs:
                return False
        
        # Check file size (skip very large files)
        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:  # 10 MB
                return False
        except OSError:
            return False
        
        return True
    
    def _is_likely_false_positive(self, line: str, match: str) -> bool:
        """Check if the match is likely a false positive."""
        line_lower = line.lower()
        match_lower = match.lower()
        
        # Check for false positive indicators
        for indicator in self.FALSE_POSITIVE_INDICATORS:
            if indicator in line_lower or indicator in match_lower:
                return True
        
        return False
    
    def _get_severity(self, credential_type: CredentialType) -> str:
        """Determine severity based on credential type."""
        high_severity = {
            CredentialType.PRIVATE_KEY,
            CredentialType.AWS_KEY,
            CredentialType.DATABASE_URL
        }
        
        if credential_type in high_severity:
            return "HIGH"
        elif credential_type == CredentialType.PASSWORD:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def scan_file(self, file_path: Path) -> List[SecretFinding]:
        """
        Scan a single file for secrets.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            List of findings in this file
        """
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # Skip comments (basic detection)
                if line.strip().startswith(('#', '//', '/*', '*', '--')):
                    continue
                
                # Check each pattern
                for cred_type, patterns in self.PATTERNS.items():
                    for pattern, description in patterns:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        
                        for match in matches:
                            matched_text = match.group(0)
                            
                            # Skip likely false positives
                            if self._is_likely_false_positive(line, matched_text):
                                continue
                            
                            # Create finding
                            finding = SecretFinding(
                                file_path=str(file_path.relative_to(self.root_path)),
                                line_number=line_num,
                                credential_type=cred_type,
                                matched_pattern=description,
                                context=line.strip()[:100],  # First 100 chars
                                severity=self._get_severity(cred_type)
                            )
                            
                            findings.append(finding)
                            self.findings.append(finding)
        
        except Exception as e:
            # Skip files that can't be read
            pass
        
        return findings
    
    def scan(self) -> List[SecretFinding]:
        """
        Scan all files in the root path.
        
        Returns:
            List of all findings
        """
        self.findings = []
        
        # Walk directory tree
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and self._should_scan_file(file_path):
                self.scan_file(file_path)
        
        return self.findings
    
    def generate_report(self) -> Dict:
        """
        Generate a summary report of findings.
        
        Returns:
            Report dictionary with statistics and findings
        """
        if not self.findings:
            return {
                'total_findings': 0,
                'files_with_secrets': 0,
                'severity_counts': {},
                'type_counts': {},
                'findings': []
            }
        
        # Count by severity
        severity_counts = {}
        for finding in self.findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
        
        # Count by type
        type_counts = {}
        for finding in self.findings:
            type_name = finding.credential_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        # Count unique files
        unique_files = len(set(f.file_path for f in self.findings))
        
        return {
            'total_findings': len(self.findings),
            'files_with_secrets': unique_files,
            'severity_counts': severity_counts,
            'type_counts': type_counts,
            'findings': [
                {
                    'file': f.file_path,
                    'line': f.line_number,
                    'type': f.credential_type.value,
                    'pattern': f.matched_pattern,
                    'severity': f.severity,
                    'context': f.context
                }
                for f in self.findings
            ]
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def create_demo_files(demo_dir: Path):
    """Create demo files with various types of secrets for testing."""
    demo_dir.mkdir(exist_ok=True)
    
    # Python file with secrets
    (demo_dir / "config.py").write_text("""
# Application Configuration - DO NOT COMMIT
# ⚠️  VULNERABLE: Contains hardcoded credentials (T1552)

# AWS Credentials
aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"
aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Database Connection
db_host = "db.example.com"
db_password = "MySecretPassword123!"
db_url = "postgresql://admin:secretpass@db.example.com:5432/mydb"

# API Keys
stripe_api_key = "sk_live_EXAMPLE_FAKE_KEY_DO_NOT_USE_1234567890"
sendgrid_api_key = "SG.1234567890abcdef.ghijklmnopqrstuvwxyz123456789"

# JWT Secret
jwt_secret = "super-secret-jwt-key-never-share-this"
""")
    
    # JavaScript file with secrets
    (demo_dir / "app.js").write_text("""
// Application configuration
// ⚠️  VULNERABLE: Contains hardcoded credentials (T1552)

const config = {
    apiKey: "AIzaSyD1234567890abcdefghijklmnopqrstuv",
    authDomain: "myapp.firebaseapp.com",
    databaseURL: "https://myapp.firebaseio.com",
    
    // OAuth credentials
    clientId: "123456789-abcdefghijklmnop.apps.googleusercontent.com",
    clientSecret: "GOCSPX-abcdefghijklmnopqrstuvwxyz",
    
    // Database
    mongoUrl: "mongodb://admin:MyPassword123@cluster0.mongodb.net/mydb"
};

// Authentication token
const authToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";
""")
    
    # YAML configuration with secrets
    (demo_dir / "config.yml").write_text("""
# Application Configuration
# ⚠️  VULNERABLE: Contains hardcoded credentials (T1552)

database:
  host: localhost
  port: 5432
  username: admin
  password: "Admin123Password"
  
api:
  key: "pk_test_51H8r2qJ3K4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z9"
  secret: "sk_test_EXAMPLE_FAKE_KEY_DO_NOT_USE_123456"
  
aws:
  access_key: "AKIAIOSFODNN7EXAMPLE"
  secret_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  region: "us-east-1"
""")
    
    # Shell script with secrets
    (demo_dir / "deploy.sh").write_text("""#!/bin/bash
# Deployment script
# ⚠️  VULNERABLE: Contains hardcoded credentials (T1552)

export DATABASE_URL="postgresql://deploy:DeployPass123@prod-db.example.com/app"
export API_TOKEN="ghp_1234567890abcdefghijklmnopqrstuvwxyz"
export SLACK_WEBHOOK="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"

# Deploy application
echo "Deploying with password: MyDeployPassword123"
""")
    
    # Private key file
    (demo_dir / "key.pem").write_text("""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdefghijklmnopqrstuvwxyz
... (truncated for demo)
-----END RSA PRIVATE KEY-----
""")


def demo_scanner():
    """Demonstrate the secrets scanner."""
    print("\n" + "=" * 70)
    print("SCANNING FOR HARDCODED CREDENTIALS (T1552)")
    print("=" * 70)
    
    # Create demo directory and files
    demo_dir = Path("/tmp/demo_secrets_scan")
    create_demo_files(demo_dir)
    
    print(f"\nCreated vulnerable demo files in: {demo_dir}")
    print("These files contain various types of hardcoded secrets...")
    
    # Run scanner
    print("\n🔍 Scanning for secrets...")
    scanner = SecretsScanner(demo_dir)
    findings = scanner.scan()
    
    print(f"\n⚠️  FOUND {len(findings)} POTENTIAL SECRETS!\n")
    
    # Group findings by file
    findings_by_file = {}
    for finding in findings:
        if finding.file_path not in findings_by_file:
            findings_by_file[finding.file_path] = []
        findings_by_file[finding.file_path].append(finding)
    
    # Display findings
    for file_path, file_findings in sorted(findings_by_file.items()):
        print(f"\n📄 {file_path}:")
        for finding in file_findings:
            print(f"   Line {finding.line_number}: [{finding.severity}] {finding.credential_type.value}")
            print(f"      Pattern: {finding.matched_pattern}")
            print(f"      Context: {finding.context}")
    
    # Generate report
    print("\n" + "=" * 70)
    print("SECURITY REPORT")
    print("=" * 70)
    
    report = scanner.generate_report()
    print(f"\nTotal Findings: {report['total_findings']}")
    print(f"Files with Secrets: {report['files_with_secrets']}")
    
    print("\nBy Severity:")
    for severity, count in sorted(report['severity_counts'].items()):
        print(f"  {severity}: {count}")
    
    print("\nBy Type:")
    for cred_type, count in sorted(report['type_counts'].items()):
        print(f"  {cred_type}: {count}")
    
    # Cleanup
    import shutil
    shutil.rmtree(demo_dir)


if __name__ == "__main__":
    print("=" * 70)
    print("MITRE ATT&CK T1552 - Secrets Scanner Demo")
    print("=" * 70)
    print("\nThis tool demonstrates how attackers search for hardcoded credentials")
    print("in source code and configuration files.")
    print("\nWARNING: The demo files contain EXAMPLE credentials only!")
    
    # Run demonstration
    demo_scanner()
    
    # Summary
    print("\n" + "=" * 70)
    print("KEY DEFENSES AGAINST T1552 (Unsecured Credentials):")
    print("=" * 70)
    print("1. ✅ NEVER hardcode credentials in source code")
    print("2. ✅ Use environment variables or secret management systems")
    print("3. ✅ Use tools like git-secrets, truffleHog, or GitGuardian")
    print("4. ✅ Implement pre-commit hooks to scan for secrets")
    print("5. ✅ Rotate credentials regularly")
    print("6. ✅ Use .gitignore to exclude sensitive files")
    print("7. ✅ Implement secrets scanning in CI/CD pipelines")
    print("8. ✅ Use key management services (AWS KMS, Azure Key Vault, etc.)")
    print("9. ✅ Audit code repositories for exposed credentials")
    print("10. ✅ Educate developers about secure credential management")
    print("=" * 70)
