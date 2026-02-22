# Work Routing

How to decide who handles what.

## Routing Table

| Work Type | Route To | Examples |
|-----------|----------|----------|
| Research strategy, scope, prioritization | Kobayashi | What tactics to cover, content structure, trade-offs |
| ATT&CK tactics/techniques, threat modeling | Fenster | Technique deep-dives, adversary behavior, detection strategies |
| Slide decks, Marp content, diagrams | McManus | New slides, Mermaid diagrams, visual layouts, speaker notes |
| Code samples (Python, .NET, JS) | Hockney | Attack/defense demos, sample code, vulnerability examples |
| Code review | Kobayashi | Review PRs, check quality, suggest improvements |
| Testing & validation | Keaton | Verify code samples, technique accuracy, edge cases |
| Scope & priorities | Kobayashi | What to build next, trade-offs, decisions |
| Session logging | Scribe | Automatic — never needs routing |

## Issue Routing

| Label | Action | Who |
|-------|--------|-----|
| `squad` | Triage: analyze issue, assign `squad:{member}` label | Kobayashi |
| `squad:{name}` | Pick up issue and complete the work | Named member |

## Rules

1. **Eager by default** — spawn all agents who could usefully start work, including anticipatory downstream work.
2. **Scribe always runs** after substantial work, always as `mode: "background"`. Never blocks.
3. **Quick facts → coordinator answers directly.** Don't spawn an agent for "what tactic is T1059?"
4. **When two agents could handle it**, pick the one whose domain is the primary concern.
5. **"Team, ..." → fan-out.** Spawn all relevant agents in parallel as `mode: "background"`.
6. **Anticipate downstream work.** If research is being done, spawn McManus to draft slides simultaneously.
7. **Security research → Fenster.** ATT&CK-specific questions always go to the security researcher first.
8. **Code + security overlap → Fenster + Hockney together.** When a task involves both technique analysis and code samples.
