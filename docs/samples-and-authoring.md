# Samples and Slide Authoring

[Back to the talk](../README.md)

The source deck is [slides/Slides.md](../slides/Slides.md), built with [Marp](https://marp.app/).
The [Pages workflow](../.github/workflows/marp-pages.yml) publishes HTML and PDF together.

## Building and Publishing Slides

Use Node.js 24 LTS for local builds (Marp requires Node.js 18 or newer). PDF export
also requires a supported Chrome/Chromium, Edge, or Firefox installation.
Run these commands from the repository root:

```bash
mkdir -p build
cp -R slides/img slides/themes build/

# HTML and assets, matching the Pages site.
npx --yes @marp-team/marp-cli@4.5.0 --theme-set slides/themes --html -o build/index.html -- slides/Slides.md

# PDF with local images and custom themes.
npx --yes @marp-team/marp-cli@4.5.0 --theme-set slides/themes --html --allow-local-files --pdf -o build/Slides.pdf -- slides/Slides.md
```

The workflow uses the pinned `marpteam/marp-cli:v4.5.0` image, which includes a
browser. Generated `build/` output is ignored by Git.

Pull requests targeting `main`, pushes to `main`, and manual runs build both
formats and upload a downloadable `slides-pdf` workflow artifact. Only runs on
`main` deploy Pages and publish `mitre-attack-for-devs.pdf` in
[GitHub Releases](https://github.com/codebytes/mitre-attack-for-devs/releases).
Configure the repository's Pages source as **GitHub Actions**.

Release tags use `slides-<run-number>-<run-attempt>` and point to the commit that
produced the PDF. Reruns refresh the temporary workflow artifact but create a new
release version rather than overwriting an existing release. Deployment and
release permissions are scoped to their respective jobs; the build is read-only.

## Shared Agent Skills

Use the reusable skills from [codebytes/skills](https://github.com/codebytes/skills)
for slide authoring and review instead of maintaining local copies. Install the
shared Copilot plugin:

```bash
copilot plugin install https://github.com/codebytes/skills
```

| Skill | Use |
| --- | --- |
| [marp-authoring](https://github.com/codebytes/skills/tree/main/skills/marp-authoring) | Edit slide content, speaker notes, and layouts |
| [marp-visuals](https://github.com/codebytes/skills/tree/main/skills/marp-visuals) | Create charts, Mermaid diagrams, and static visual assets |
| [drawio-diagrams](https://github.com/codebytes/skills/tree/main/skills/drawio-diagrams) | Create and validate editable `.drawio.svg` diagrams |
| [pptx-to-marp-theme](https://github.com/codebytes/skills/tree/main/skills/pptx-to-marp-theme) | Extract a Marp theme from a PowerPoint template |
| [marp-slide-review](https://github.com/codebytes/skills/tree/main/skills/marp-slide-review) | Review overflow, clipping, assets, and HTML/PDF rendering |

Follow each installed skill's instructions for its scripts and dependencies; see
the [shared installation guide](https://github.com/codebytes/skills#install) for
other supported hosts. Keep talk-specific conventions in
[the repository instructions](../.github/copilot-instructions.md), themes in
`slides/themes/`, and diagrams and their source specifications in `slides/img/`.

Run `marp-slide-review` before presenting or publishing. Use its structural and
rendered review, inspect every slide, and compare the PDF for clipping and footer
overlap. Keep review artifacts out of source control. The Pages workflow invokes
Marp CLI directly; shared skills are authoring tools, not a CI deployment gate.

The October 2026 security snapshot is dated **26 October 2026**. It covers PHP
and Node.js runtime fixes, with expanded Brotli and eMudhra case studies. Its
speaker notes link to primary advisories and record first-fixed releases,
exposure prerequisites, and the certificate incident's scope. Recheck those
sources before presenting: disclosure is not proof of exploitation, an available
update is not a deployed fix, and a vulnerable component is not necessarily a
supply-chain compromise.

The Techorama 2026 cover and final SpreaView review slide are additive bookends;
keep the original title, feedback, resources, and technical slides intact. Their
styles are slide-scoped, and `paginate: skip` preserves the existing slide
numbers. The cover reuses the template-matched logo and background already in
`slides/themes/techorama/`, without switching themes or adding font binaries.
The supplied review artwork is `slides/img/spreaview-review.png`; preserve its
QR destination and matching text link:
https://spreaview.com/review/0FFUI0XO/DDUQJG5R.

## Motion and Transitions

The deck's motion lives in
[slides/themes/crooked-line-motion.css](../slides/themes/crooked-line-motion.css),
which `custom-default.css` imports. It is CSS only: Marp CLI's bespoke HTML
restarts a slide's CSS animations whenever that slide becomes active.

- **Transitions:** the front matter fades every slide boundary in 250 ms. The
  slide *before* each section divider sets `<!-- _transition: breach -->`,
  because a transition directive applies to the boundary after its slide.
- **Kill-chain morph:** the two "Kill Chain: Expectation vs Reality" slides are
  complete keyframes. Elements with matching `kc-*` classes share a
  `view-transition-name`, so the expected steps morph into the observed path.
  Each name must stay unique within a slide.
- **Entrances:** `mo-*` utility classes read their delay (`--d`), duration
  (`--dur`), and other timing from inline custom properties. The
  `step-cascade` and `response-cascade` slide classes stagger list items and
  table rows.

When adding motion, keep the un-animated style as the finished slide, animate
only inside `screen and (prefers-reduced-motion: no-preference)`, and let every
effect settle within five seconds without looping. Marp reduces transitions to
a fade for reduced-motion viewers, and the print path disables animation, so PDF
pages stay complete. Morphing works best in current Chrome or Edge; other
browsers still show every complete slide.

The data-flow, audit-evidence, defense-in-depth, and OWASP/ATT&CK integration
diagrams have `.mmd` sources beside their static `.svg` outputs in `slides/img/`.
Regenerate them with the installed `marp-visuals` skill's `render-mermaid.mjs`,
following its dependency and browser setup instructions. The deck uses the SVGs
directly; it needs no runtime Mermaid script or diagram generation in CI. Keep
the original embedded draw.io PNG sources intact when changing these replacements.

## Repository Content

This repository provides insights, code samples, and demonstrations for applying the MITRE ATT&CK framework to application development. Topics covered include:

- Understanding the MITRE ATT&CK framework and its 14 tactics
- Adding MITRE ATLAS when threat-modeling AI-enabled application features
- How ATT&CK complements OWASP — vulnerabilities vs. adversary behavior
- Practical code examples mapping ATT&CK techniques to real development scenarios
- Detection and defense patterns for common attack techniques
- Supply chain security, credential access, and data exfiltration defenses
- Building an adversary-informed development workflow

## Code Samples

The `samples/` directory contains educational code samples in three languages, each demonstrating attack techniques and corresponding defenses mapped to ATT&CK technique IDs.

The samples deliberately exclude controls that belong to an identity provider
(credential stuffing, password spray, impossible travel) or to existing tooling
(secret scanning, dependency advisories). Those techniques are worth monitoring,
but reimplementing them inside one application produces a weaker control. Each
language README documents that boundary.

- **[Python](../samples/python/)** — Command injection, unsafe deserialization, bulk export limits, tamper-evident logging, data integrity
- **[.NET/C#](../samples/dotnet/)** — Resource authorization, command injection, file upload validation, session security, tamper-evident logging, secrets management
- **[JavaScript](../samples/javascript/)** — SQL injection, IdP risk signals and step-up, session security, export budgets, dependency policy, data integrity
