# Project Context

- **Owner:** Chris Ayers (clayers@gmail.com)
- **Project:** MITRE ATT&CK for Developers — deep-dive research into ATT&CK framework, Marp slide decks, and multi-language code samples (Python, .NET, JavaScript) showing attack techniques and defenses
- **Stack:** Marp (Markdown slides), Python, .NET/C#, JavaScript, Mermaid diagrams
- **Created:** 2026-02-22

## Learnings

### Audit Session 2026-02-22: Accuracy Deep Dive

1. **MITRE ATT&CK Technique Precision**
   - All 40+ technique IDs in this project are correctly identified and mapped
   - T1059.006 (Python deserialization) is correct classification; don't confuse with T1203
   - Defensive code patterns follow best practices (allowlists, proper encoding, cryptographic integrity)

2. **Code Sample Quality Standards**
   - Vulnerable code must be actually exploitable (this project achieves this)
   - Defended code must properly mitigate (verified for all 12 reviewed samples)
   - Multi-language consistency matters (Python, .NET, JavaScript implementations are aligned)

3. **OWASP vs ATT&CK Distinction**
   - This is a common teaching confusion: vulnerabilities (OWASP) vs techniques (ATT&CK)
   - Students need explicit clarification that a vulnerability can enable multiple techniques
   - Current slides conflate the two; needs educator note for teaching clarity

4. **Coverage Gaps Are Minor**
   - 60% technique coverage with code samples is solid
   - Missing samples (T1078, T1110, T1565) are nice-to-have, not critical
   - Scope of credential stuffing (T1110.004) vs brute force (T1110) should be documented

5. **Defensive Pattern Validation**
   - Input validation: Allowlist approach is correct (reject first, allow known)
   - Process execution: ArgumentList + shell=false is the secure pattern
   - Session security: Fingerprinting + rotation + anomaly detection are complementary
   - Logging: Hash chains with sequence numbers properly detect tampering/deletion

6. **Documentation Consistency**
   - READMEs are accurate and match actual files
   - Technique descriptions in README match their code samples
   - No misleading or outdated information found

<!-- Append new learnings below. Each entry is something lasting about the project. -->
