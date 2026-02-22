# Decision: ATT&CK Research Document Complete

**Date:** 2025-02-21  
**Author:** Fenster  
**Status:** Complete

## Summary

Created comprehensive ATT&CK research document at `.ai-team/agents/fenster/attack-research.md` to serve as the authoritative reference for developers building ATT&CK-aware applications.

## Document Structure

### 1. The 14 ATT&CK Tactics — Developer Relevance
- All 14 tactics (TA0043 through TA0040)
- Each includes: tactic ID, description, why developers should care (2-3 sentences), and top 3 relevant techniques with defenses
- Focus on application-layer concerns and developer-controllable mitigations

### 2. Developer-Centric Technique Deep Dives
- 15 high-priority techniques analyzed in depth: T1190, T1059, T1078, T1195, T1552, T1070, T1110, T1567, T1499, T1565, T1098, T1134, T1505.003, T1021, T1213
- Each technique includes 4-5 sentences covering: what it is, how attackers use it, how developers defend
- Emphasizes practical, code-level defenses

### 3. OWASP Top 10 2025 → ATT&CK Mapping
- Complete table mapping all 10 OWASP categories to relevant ATT&CK techniques
- Bridges vulnerability-focused (OWASP) and adversary-focused (ATT&CK) perspectives
- Enables developers to understand attack techniques through familiar OWASP lens

### 4. Modern Attack Chains
- 5 realistic multi-stage attack scenarios demonstrating technique chaining
- Scenarios: Supply Chain to Persistence, Initial Access to Data Breach, Credential Stuffing to Lateral Movement, File Upload to Web Shell, API Abuse to Mass Exfiltration
- Each chain shows 7-8 sequential techniques with T-codes

### 5. MITRE D3FEND Mappings
- 20 defensive techniques mapped to D3FEND IDs
- Links defensive patterns to techniques they mitigate
- Provides standardized vocabulary for defensive measures

### 6. Emerging Techniques (2024-2026)
- 5 emerging attack areas: AI/ML Security, Cloud-Native Attacks, API-Specific Attacks, Container/Orchestration Risks, CI/CD Pipeline Targeting
- Each area analyzed for 2-3 sentences with ATT&CK technique analogies
- Future-focused content for modern development practices

## Key Design Decisions

1. **Developer-first language**: Avoided security jargon, used practical code examples and familiar vulnerability types (IDOR, ReDoS, etc.)
2. **Actionable defenses**: Every technique includes concrete defensive measures developers can implement
3. **OWASP bridge**: Mapped ATT&CK to OWASP Top 10 2025 to leverage existing developer knowledge
4. **Technique prioritization**: Focused on application-layer techniques developers can actually mitigate in code
5. **Modern context**: Emphasized microservices, cloud, containers, and CI/CD—reflecting current development practices

## Coverage Analysis

- **Complete**: All 14 tactics covered
- **Deep dives**: 15 priority techniques analyzed
- **Mappings**: OWASP, D3FEND, attack chains provided
- **Forward-looking**: Emerging techniques section for 2024-2026 threats

## Usage

This document serves as:
- Reference for slide content development (McManus)
- Source material for code examples (Hockney)
- Threat modeling input (all team members)
- Training material foundation for developer security education

## Next Steps

- McManus can extract key points for slides
- Hockney can reference defensive patterns for code examples
- Keaton can use attack chains for test scenario development
- Document should be updated quarterly as ATT&CK framework evolves
