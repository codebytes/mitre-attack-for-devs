# Skill: First-Use Acronym Expansion for Security Slide Decks

## Rule

Expand security-specific acronyms on their **first occurrence in visible slide content**, then use the bare acronym for every subsequent occurrence. Do not expand common developer acronyms (API, JSON, SQL, HTTP, HTTPS, URL, CI/CD, OWASP, ATT&CK).

## What counts as "visible slide content"

- Slide body text (bullets, prose, callouts, summary lines)
- Slide headings and titles
- Table cells and column headers

## What does NOT count (skip + do not modify)

| Context | Rule |
|---------|------|
| Speaker notes (`<!-- ... -->`) | Never count, never modify |
| Code blocks (``` ``` ```) | Leave all content untouched |
| Inline code (`` ` ` ``) | Leave untouched |
| Acronym-as-identifier (`CVE-2024-3094`) | Leave untouched |
| Acronym in code comments (`// RBAC:`) | Leave untouched |

## Expansion format

Use natural inline form: `Full Name (ACRONYM)` on first use.

```
SIEM integration                                     ← bare (wrong, first use)
Security Information and Event Management (SIEM) integration  ← ✅ expanded
```

For subsequent uses:
```
- SIEM integration                                   ← ✅ bare is correct after first expansion
```

## Expansion in headings

If the acronym's first visible occurrence is a slide heading, expand it there. If expansion hurts a short iconic title, you may expand on the first body line instead — note the judgment call.

## Multi-acronym same bullet

When two target acronyms appear in the same bullet (e.g., `RCE via SSHd · CVSS 10.0`), expand both inline in that bullet without splitting it:
```
Remote Code Execution (RCE) via SSHd · Common Vulnerability Scoring System (CVSS) 10.0
```

## Acronym allowlist (expand on first use)

| Acronym | Full form |
|---------|-----------|
| SIEM | Security Information and Event Management |
| SBOM | Software Bill of Materials |
| SAST | Static Application Security Testing |
| CVE | Common Vulnerabilities and Exposures |
| CVSS | Common Vulnerability Scoring System |
| RCE | Remote Code Execution |
| C2 | Command and Control |
| RAT | Remote Access Trojan |
| RBAC | Role-Based Access Control |

## Acronyms that stay bare always

API, JSON, SQL, HTTP, HTTPS, URL, HTML, CSS, JS, npm, OS, CI/CD, OWASP, ATT&CK

## Process

1. Grep the deck for each acronym (`\bACRONYM\b`).
2. For each hit, determine: visible slide content, code/note/identifier?
3. The first visible-content hit is the expansion site. All others stay bare.
4. Edit only the expansion site using precise `old_str` context.
5. Re-grep after edits to verify: expanded exactly once, bare thereafter, untouched in code/notes.
6. Run Marp build to validate deck still renders.

## Worked examples from slides/Slides.md (2026-05-11)

### ✅ C2 — line 192 (bullet in SolarWinds kill-chain)
**Before:** `4. 🕸️ **T1071** — C2 via DNS blending`  
**After:** `4. 🕸️ **T1071** — Command and Control (C2) via DNS blending`  
**Line 193 left bare:** `5. 📤 **T1041** — Data exfil over C2 channel`

### ✅ SIEM — line 1018 (Phase 2 bullet in Roadmap slide)
**Before:** `- SIEM integration`  
**After:** `- Security Information and Event Management (SIEM) integration`  
*Earlier SIEM uses on lines 686, 982, 998 were all inside `<!-- ... -->` speaker notes — correctly skipped.*

### ✅ RAT — line 756 (Axios numbered list)
**Before:** `1. **Mar 31**: Maintainer account compromised via RAT malware`  
**After:** `1. **Mar 31**: Maintainer account compromised via Remote Access Trojan (RAT) malware`  
*Lines 759 and 768 left bare. Speaker note line 776 left untouched.*

### ❌ SBOM — no expansion (all occurrences in code blocks)
`sbom.json`, `npm sbom --sbom-format`, `grype sbom:` are CLI literals. No visible prose occurrence. Skip.

### ❌ RBAC — no expansion (all occurrences in code comments and speaker notes)
`// RBAC: App's managed identity...` and `// No API keys! Managed Identity handles auth via RBAC` are code comments. Speaker note mention also skipped.
