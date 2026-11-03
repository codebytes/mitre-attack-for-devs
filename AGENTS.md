# Agent instructions: MITRE ATT&CK for Developers — Beyond OWASP

This repository holds the slides for Chris Ayers' talk **MITRE ATT&CK for Developers**. The deck is published to <https://chris-ayers.com/mitre-attack-for-devs/>.

## Repository layout

- `slides/`: Marp deck, images and diagram sources in `slides/img/`, themes in `slides/themes/` (including `custom-mitre-attack.css` and `crooked-line-motion.css`).
- `samples/dotnet`, `samples/javascript`, `samples/python`: code samples mapped to ATT&CK techniques; `docs/samples-and-authoring.md` explains them and the slide motion rules.
- `test/smoke.test.js`: minimal smoke test (`node --test "test/*.test.js"`).
- `.squad/`, `.ai-team/`, `.ai-team-templates/`: agent-team state and templates. Leave them alone unless the task is about that setup.

## Slides

- Write the deck in Markdown with [Marp](https://marp.app/). `slides/Slides.md` is the source; `build/` is generated output and is never edited or committed.
- Keep the frontmatter at the top of the deck:

  ```yaml
  ---
  marp: true
  theme: custom-default
  ---
  ```

- Store themes in `slides/themes/` and images and diagram sources in `slides/img/`. Prefer theme classes and CSS variables over inline styles.
- Write speaker notes as HTML comments (`<!-- -->`).
- Render locally with the Marp CLI version the Pages workflow uses (v4.5.0):

  ```bash
  npx @marp-team/marp-cli@4.5.0 --theme-set slides/themes --html -o build/index.html -- slides/Slides.md
  npx @marp-team/marp-cli@4.5.0 --theme-set slides/themes --html --pdf --allow-local-files -o build/Slides.pdf -- slides/Slides.md
  ```

- `.github/workflows/marp-pages.yml` builds the HTML deck and `Slides.pdf` and publishes both to GitHub Pages. If you add slide assets outside `slides/img/` and `slides/themes/`, add them to the workflow's copy step.

## Shared skills

Use the shared skills from [codebytes/skills](https://github.com/codebytes/skills) (for Copilot CLI: `copilot plugin install https://github.com/codebytes/skills`). Don't copy their instructions or scripts into this repo.

| Task | Skill |
| --- | --- |
| Write or revise slides, notes, order, or layouts | `marp-authoring` |
| Charts, Mermaid diagrams, or other visuals | `marp-visuals` |
| Editable `.drawio.svg` diagrams (stored in `slides/img/`) | `drawio-diagrams` |
| Check overflow, clipping, and HTML/PDF parity before presenting or publishing | `marp-slide-review` |

Run `marp-slide-review` with structural and rendered checks, inspect every slide, and compare the PDF. Fix overflow without hiding clipped content or shrinking the whole deck, then review again. Keep review output in an ignored `validation-artifacts/` folder, not in source control.

## Talk-specific rules

- Preserve the talk's technical meaning, ATT&CK mappings, speaker notes, and existing visual identity when adjusting layouts.
- Keep slide motion CSS-only in `slides/themes/crooked-line-motion.css` and follow the motion rules in `docs/samples-and-authoring.md`: finished static state, reduced-motion gate, settle within five seconds, complete PDF pages.
- Follow `marp-visuals` for Mermaid initialization when the deck contains inline diagrams; include the Mermaid script once. Pre-rendered diagram images do not need a Mermaid runtime.
- Keep the Pages/PDF pipeline independent of agent skills; it invokes Marp CLI directly and publishes the HTML deck and `Slides.pdf` together.

## README

- Keep the README sections in this order: Slides, Recordings, Resources, Contact.
- When a new recording of the talk is published, add it at the top of `## Recordings` as `- [Event Year](https://www.youtube.com/watch?v=VIDEO_ID)`. When the video's title differs from the talk's, add an em dash and the recorded title after the event. Keep the list newest first.
- The talk also appears on <https://chris-ayers.com/speaking/> (source: `content/speaking.md` in [codebytes/codebytes.github.io](https://github.com/codebytes/codebytes.github.io)); new events and recordings belong there too.

## General

- Keep changes scoped to the request; don't reformat unrelated slides or code.
- Never commit secrets, keys, or connection strings. Demo placeholders must be obviously fake.
