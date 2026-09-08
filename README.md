# MITRE ATT&CK for Developers — Beyond OWASP

This repository contains the slide deck, demos, and additional resources for the "MITRE ATT&CK for Developers — Beyond OWASP" talk by Chris Ayers, Principal Software Engineer at Microsoft. The talk bridges the gap between threat intelligence and practical development, showing how to apply adversarial thinking to your code.

## Slides

[View HTML slides](https://chris-ayers.com/mitre-attack-for-devs/) | [Download PDF](https://chris-ayers.com/mitre-attack-for-devs/Slides.pdf)

The source deck is [slides/Slides.md](./slides/Slides.md), built with [Marp](https://marp.app/).
The [Pages workflow](./.github/workflows/marp-pages.yml) publishes HTML and PDF together.

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
[the repository instructions](./.github/copilot-instructions.md), themes in
`slides/themes/`, and diagrams and their source specifications in `slides/img/`.

Run `marp-slide-review` before presenting or publishing. Use its structural and
rendered review, inspect every slide, and compare the PDF for clipping and footer
overlap. Keep review artifacts out of source control. The Pages workflow invokes
Marp CLI directly; shared skills are authoring tools, not a CI deployment gate.

## Repository Content

This repository provides insights, code samples, and demonstrations for applying the MITRE ATT&CK framework to application development. Topics covered include:

- Understanding the MITRE ATT&CK framework and its 14 tactics
- How ATT&CK complements OWASP — vulnerabilities vs. adversary behavior
- Practical code examples mapping ATT&CK techniques to real development scenarios
- Detection and defense patterns for common attack techniques
- Supply chain security, credential access, and data exfiltration defenses
- Building an adversary-informed development workflow

## Code Samples

The `samples/` directory contains educational code samples in three languages, each demonstrating attack techniques and corresponding defenses mapped to ATT&CK technique IDs:

- **[Python](./samples/python/)** — Credential stuffing detection, command injection, unsafe deserialization, tamper-evident logging, data access monitoring, secrets scanning
- **[.NET/C#](./samples/dotnet/)** — Command injection, session security, tamper-evident logging, secrets management, web shell detection
- **[JavaScript](./samples/javascript/)** — SQL injection, session security, credential stuffing detection, supply chain verification, data exfiltration detection, secrets detection

## Resources

- [MITRE ATT&CK Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/)
- [MITRE ATT&CK Techniques](https://attack.mitre.org/techniques/enterprise/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MITRE D3FEND](https://d3fend.mitre.org/)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Connect with Chris Ayers

Feel free to connect with Chris Ayers on social media and visit his blog for more information on security and other topics:

- BlueSky: [@chris-ayers.com](https://bsky.app/profile/chris-ayers.com)
- LinkedIn: [chris-l-ayers](https://linkedin.com/in/chris-l-ayers/)
- Blog: [https://chris-ayers.com/](https://chris-ayers.com/)
- GitHub: [Codebytes](https://github.com/codebytes)
- Mastodon: [@Chrisayers@hachyderm.io](https://hachyderm.io/@Chrisayers)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.