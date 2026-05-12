# Fenster — History

## Core Context

- **Project:** A Marp slide deck teaching developers the MITRE ATT&CK framework with code examples.
- **Role:** Code Samples
- **Joined:** 2026-05-11T15:55:39.700Z

## Learnings

- **2026-05-11 — Team update:** mcmanus completed supply-chain case-study research dossier (Shai-Hulud, Notepad++, Axios, SolarWinds, XZ Utils, Log4Shell with narrative arc). Decisions merged: acronym expansion (SIEM, SBOM, SAST, CVE, CVSS, RCE, RAT, C2, RBAC on first use), medieval motif constraints (section intros/Defense in Depth only, no code rewrites), visual theme accent (`.parchment`/`.quest` classes on Techorama base). If touching slide content or code samples, align with these conventions.

---

## 2026-05-12 — Team Notice: Canonical Section Divider Opacity Lock & Reviewer Protocol

**To fenster (and mcmanus):** During Keyser's imagery placement review, the team discovered three opacity-modifier regressions when encoding Marp `![bg opacity:X]` syntax. A canonical opacity reference table has been locked in decisions.md and must be treated as authoritative:

| Slide | Bg Image | Opacity |
|---|---|---|
| Let's Think Like Attackers | `knight-on-horse-gray.png` | `bg right:30% fit` |
| Initial Access & Credential Attacks | `castle-skyline-silhouette.png` | `.2` |
| Persistence & Session Hijacking | `fleur-de-lis-pattern-dark.jpg` | `.2` |
| Credential Access & Secrets | `stone-wall-texture-dark.jpg` | `.15` |
| Defense Evasion & Log Tampering | `stone-wall-texture-dark.jpg` | `.2` |
| Supply Chain Compromise | `techorama-hero-medieval.png` | `.2` |
| Collection & Exfiltration | `castle-skyline-silhouette.png` | `.2` |
| Key Takeaways | `celtic-border-gold.png` | `.08` |

**ACTION:** If you add or modify section-divider imagery or content in future passes, do NOT edit opacity values without updating the canonical table in decisions.md. Failing to do so will trigger regressions identical to what Keyser encountered.

**PRECEDENT:** This project has now invoked its first Reviewer Rejection Lockout (2026-05-12). When an agent produces two consecutive identical regressions despite documentation, a second agent is assigned revision authority instead. Do not assume you will be asked to self-correct on high-stakes visual values like opacity; expect reassignment.
