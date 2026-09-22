# MITRE ATT&CK for Developers — JavaScript/Node.js Samples

Educational samples for a conference talk, mapped to MITRE ATT&CK technique IDs.

## What these samples do and don't cover

These samples deliberately stop at the boundary of the application. Credential
stuffing, password spray, impossible travel, device reputation and MFA are
detected by your **identity provider** — Entra ID Protection, Okta, Auth0,
Cognito — which sees sign-ins across every application and tenant. One
application sees a single slice of that traffic, so a homegrown copy is strictly
worse and usually ends up locking out mobile users who changed cell towers.

**Monitor those techniques. Do not reimplement them.** What is left is the set of
controls no vendor can write for you, because they depend on your object model,
your data volumes, and your interpreters.

## Samples

### 1. SQL Injection (`sql-injection.js`) — T1190
Vulnerable string concatenation versus parameterized queries and input validation.

```bash
node sql-injection.js
```

### 2. Valid Accounts, the application's half (`idp-risk-signals.js`) — T1078
Reads the `acr`, `amr`, `auth_time` and risk claims the IdP already issues, and
decides which of *your* operations demand a stronger credential. Returns an
RFC 9470 step-up challenge rather than a dead end.

```bash
node idp-risk-signals.js
```

### 3. Session Security (`session-security.js`) — T1185, T1550.004
Cryptographically random IDs, rotation on privilege change, and server-side
revocation. Note that it does **not** block on IP change: roaming clients change
address constantly, so that rule logs out real users while a hijacker on the same
network is unaffected.

```bash
node session-security.js
```

### 4. Export Budget (`export-budget.js`) — T1567, T1020
A hard, explainable ceiling on rows and bytes per subject per hour. Each request
is individually authorized and reasonable; the budget catches the accumulation,
which is the actual attack.

```bash
node export-budget.js
```

### 5. Dependency Policy (`dependency-policy.js`) — T1195.001
A CI gate: reviewed lockfile with integrity hashes, `ignore-scripts=true`,
registry signature and provenance verification, and an advisory threshold.
Delegates to `npm audit` rather than reimplementing a typosquat detector —
Shai-Hulud and the Axios compromise both shipped under the *real* package name
through a hijacked maintainer account, so name similarity would have caught neither.

```bash
node dependency-policy.js
```

### 6. Data Integrity (`data-integrity.js`) — T1565
HMAC record signatures over canonical JSON, plus a tamper-evident audit trail and
mass-modification detection.

```bash
node data-integrity.js
```

## Requirements

Node.js 18+. No npm packages — standard library only.

## MITRE ATT&CK techniques covered

| Technique ID | Name | Sample File |
|-------------|------|-------------|
| T1190 | Exploit Public-Facing Application | `sql-injection.js` |
| T1078 | Valid Accounts | `idp-risk-signals.js` |
| T1185 | Browser Session Hijacking | `session-security.js` |
| T1550.004 | Web Session Cookie | `session-security.js` |
| T1567 | Exfiltration Over Web Service | `export-budget.js` |
| T1020 | Automated Exfiltration | `export-budget.js` |
| T1195.001 | Compromise Software Dependencies | `dependency-policy.js` |
| T1565 | Data Manipulation | `data-integrity.js` |

### Covered by your identity provider

| Technique ID | Name | Where it belongs |
|-------------|------|------------------|
| T1110.003 | Password Spraying | IdP sign-in protection |
| T1110.004 | Credential Stuffing | IdP sign-in protection |
| T1078 | Valid Accounts *(sign-in anomalies)* | IdP risk detection |

### Covered by tooling

| Technique ID | Name | Use instead |
|-------------|------|-------------|
| T1552 | Unsecured Credentials | GitHub Secret Scanning + Push Protection, Gitleaks, TruffleHog |

## Security notes

⚠️ **Educational purpose only.** These samples contain intentionally vulnerable
code alongside the defended version. Never ship the vulnerable patterns.

In-memory `Map` state is used throughout for readability. Production counters and
session stores need shared, atomic storage (Redis, a database), because
per-process state resets on deploy and is defeated by spreading calls across
replicas.

## Learning resources

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Node.js Security Best Practices](https://nodejs.org/en/learn/getting-started/security-best-practices)
