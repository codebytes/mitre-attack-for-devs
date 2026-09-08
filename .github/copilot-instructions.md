# Shared Skills

Use the canonical skills from [codebytes/skills](https://github.com/codebytes/skills)
for reusable slide workflows. Do not vendor or maintain copies of their skill
instructions, scripts, or dependencies in this repository.

Install the shared Copilot plugin when needed:

```bash
copilot plugin install https://github.com/codebytes/skills
```

For other hosts, follow the [shared installation guide](https://github.com/codebytes/skills#install).
Use the relevant installed skill before working on a deck:

| Task | Skill |
| --- | --- |
| Create or revise slide content, notes, order, or layouts | [marp-authoring](https://github.com/codebytes/skills/tree/main/skills/marp-authoring) |
| Generate charts, Mermaid diagrams, or static visuals | [marp-visuals](https://github.com/codebytes/skills/tree/main/skills/marp-visuals) |
| Create or validate editable draw.io diagrams | [drawio-diagrams](https://github.com/codebytes/skills/tree/main/skills/drawio-diagrams) |
| Adapt a PowerPoint template into a Marp theme | [pptx-to-marp-theme](https://github.com/codebytes/skills/tree/main/skills/pptx-to-marp-theme) |
| Review overflow, clipping, assets, and HTML/PDF parity | [marp-slide-review](https://github.com/codebytes/skills/tree/main/skills/marp-slide-review) |

Follow the installed skill's current setup and command instructions rather than
assuming a local script path. Keep this file focused on talk-specific conventions.

# Repository Conventions

- Write all slide decks in Markdown using [Marp](https://marp.app/).
- Include the required frontmatter:

  ```yaml
  ---
  marp: true
  theme: custom-default
  ---
  ```

- Store decks in `slides/`, themes in `slides/themes/`, and images and diagram
  source files in `slides/img/`.
- Use HTML comments (`<!-- -->`) for speaker notes.
- Preserve the talk's technical meaning, ATT&CK mappings, speaker notes, and
  existing visual identity when adjusting layouts.
- Follow `marp-visuals` for Mermaid initialization when a deck contains inline
  diagrams; include the required Mermaid script once. Pre-rendered diagram
  images do not need a Mermaid runtime.
- Use the Marp CLI version pinned in `.github/workflows/marp-pages.yml` for local
  exports and review. Supply `--theme-set slides/themes --html`, and enable
  `--allow-local-files` for PDF exports that use local images.
- Run `marp-slide-review` before presenting or publishing: perform structural
  and rendered checks, inspect every slide, and compare PDF output. Fix overflow
  without hiding clipped content or shrinking the whole deck, then repeat the
  review on the updated render.
- Keep generated exports and review evidence out of source control. Use `build/`
  for local publishing output and ignored `validation-artifacts/` or the session
  artifact directory for review output.
- Keep the Pages/PDF pipeline independent of agent skills; it invokes Marp CLI
  directly and publishes the HTML deck and `Slides.pdf` together.
