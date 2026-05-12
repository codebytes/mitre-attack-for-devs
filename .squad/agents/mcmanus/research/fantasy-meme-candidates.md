# Fantasy Meme Candidates for MITRE ATT&CK for Developers

**Date:** 2026-05-11T17:43:21-04:00  
**Researcher:** McManus  
**Requested by:** Chris Ayers

## Research scope

Looked for medieval, fantasy, D&D, wizard, dragon, rogue, Skyrim, and Lord of the Rings meme formats that can work as text-only Marp slides. Priority went to formats that:

- Work without embedded images or copyrighted stills.
- Teach a real MITRE ATT&CK or secure-development concept.
- Fit a professional developer/security conference.
- Add variety beyond the current Drake choice, galaxy-brain maturity ladder, and "How it started vs How it's going" consequence comparison.

## Source notes

- Know Your Meme pages were the most useful definitive sources for established formats.
- Reddit top pages were checked, but accessible pages mostly exposed subreddit metadata/rules rather than a reliable ranked post corpus. Useful takeaway: r/dndmemes explicitly values legible, understandable, strongly D&D-relevant humor and flags overdone topics/formats, which supports keeping any D&D references simple and text-first.

## Candidate shortlist

| Meme format | Source URL | Text-format viable? | Proposed slide title | What it teaches (ATT&CK concept) | Fit score (1-5) | Notes |
|---|---|---:|---|---|---:|---|
| One Does Not Simply | https://knowyourmeme.com/memes/one-does-not-simply-walk-into-mordor | Yes — pure snowclone headline | One Does Not Simply Patch Production | Patch exposure is a campaign, not a single deploy; maps to T1190 Exploit Public-Facing Application and vulnerability management | 5 | Strongest fit. Recognizable, dry, already fantasy-coded, and naturally expresses "harder than it sounds." |
| You Shall Not Pass | https://knowyourmeme.com/memes/you-shall-not-pass | Yes — gatekeeper phrase with bullet list | You Shall Not Pass: Guard Clauses That Matter | Preventing initial access and privilege misuse with authN/authZ, input validation, rate limits; maps to T1190, T1078, T1110 | 5 | Excellent castle-gate metaphor. Use as control checklist, not just catchphrase. |
| Skyrim Skill Tree / Sneak 100 | https://knowyourmeme.com/memes/skyrim-skill-tree | Yes — `SNEAK 100`/`SPEECH 100` stat cards | SNEAK 100: Living Off the Land | Attackers blend into normal tooling/logs; maps to T1059 Command and Scripting Interpreter, T1070 Indicator Removal, valid admin activity | 5 | Adds a "badge/stat unlock" joke shape distinct from current memes. Great for detection section. |
| Alignment Chart | https://knowyourmeme.com/memes/alignment-charts | Yes — markdown 3x3 table | Deployment Security Alignment Chart | Different release/security behaviors; maps to secure SDLC, supply-chain risk, secrets handling, and response readiness | 4 | Very text/table-friendly. Risk: nine cells may be dense; keep labels short. |
| I Cast Fireball | https://knowyourmeme.com/photos/2640732-dungeons-and-dragons | Yes — dialogue/script format | I Cast Fireball at the Input Field | Command execution as the "universal solution" attackers abuse; maps to T1059 and injection/RCE prevention | 4 | Good D&D wizard reference. Keep it dry: "The parser did not ask for feelings." Avoid murderhobo tone. |
| Roll Initiative | https://knowyourmeme.com/photos/2755144-dungeons-and-dragons | Yes — incident trigger line | Roll Initiative: When the Alert Is Real | Detection-to-response transition; maps to SIEM triage, incident response, T1071 C2, T1041 exfiltration | 4 | Useful for practical implementation or response slide. Less visually specific, but developers understand the escalation cue. |
| I Took an Arrow in the Knee | https://knowyourmeme.com/memes/i-took-an-arrow-in-the-knee | Yes — snowclone | I Used to Ship Secrets Like That | Developer behavior changes after a real incident; maps to T1552 Unsecured Credentials and secrets management | 3 | Recognizable but older and noted as oversaturated. Use only if intentionally nostalgic. |
| Fus Ro Dah | https://knowyourmeme.com/memes/fus-ro-dah | Mostly — shout phrase plus before/after bullets | Fus Ro Dah: When One Bad Input Moves the Whole Stack | Blast-radius thinking; maps to T1059/RCE and lateral movement containment | 3 | Fun but more sound-effect than teaching format. Could feel goofy unless restrained. |

## Top 3 recommendations

### 1. One Does Not Simply

Best for a patching or exposed-service slide. It gives a dry, immediate punchline: fixing T1190 is not "just deploy a patch"; it requires inventory, prioritization, rollout, validation, and monitoring.

````markdown
---

<!-- _class: parchment -->

# One Does Not Simply Patch Production

> "It's just one CVE."

| The council says | The keep actually needs |
|---|---|
| Patch the gate | Know which gates exist |
| Restart the service | Prove the caravan still runs |
| Close the ticket | Watch for sappers already inside |

**ATT&CK lens:** T1190 — Exploit Public-Facing Application

<!-- Speaker note: The joke is that patching is not a button. For developers, the real work is asset inventory, safe rollout, compensating controls, and post-patch detection. -->
````

### 2. Skyrim Skill Tree / SNEAK 100

Best for living-off-the-land and detection. It turns attacker stealth into a simple stat-card format and reinforces that "normal-looking" commands are exactly what defenders need to understand.

````markdown
---

<!-- _class: parchment -->

# SNEAK 100: Living Off the Land

```text
PowerShell ran from a service account at 02:13
curl posted 48 MB to an unknown host
audit log cleared five minutes later

             SNEAK 100
```

**ATT&CK lens:** T1059 command execution + T1070 log tampering + T1071 C2

<!-- Speaker note: The attacker is not always wearing a black cloak. Sometimes they look like the build agent, the admin shell, or yesterday's maintenance job. -->
````

### 3. You Shall Not Pass

Best for guardrails and practical implementation. It uses the castle gate vocabulary directly and can teach concrete controls without feeling like another comparison meme.

````markdown
---

<!-- _class: parchment -->

# You Shall Not Pass

The gate is not a vibe. It is a control surface.

- No token? **401.**
- Wrong role? **403.**
- Weird payload? **Rejected before business logic.**
- Too many guesses? **Rate-limited and logged.**
- Valid account from impossible travel? **Challenge it.**

**ATT&CK lens:** T1078 valid accounts, T1110 brute force, T1190 exposed app exploitation

<!-- Speaker note: This is where the medieval frame earns its keep: gates are useful because they force explicit decisions. Every ambiguous pass becomes an attack path. -->
````

## Formats considered but not recommended

- Distracted Boyfriend — explicitly excluded; overused and dating-coded.
- This Is Fine — explicitly excluded; overused.
- Generic dragon-hoard image macros — often image-dependent and can drift goofy.
- "It's Magic. I Ain't Gotta Explain Shit" — sourced via the D&D page, but profanity and hand-wavy tone are wrong for this deck.
- Fus Ro Dah — viable as a backup, but the punchline is more sound effect than security lesson.
