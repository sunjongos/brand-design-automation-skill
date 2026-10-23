---
name: brand-design-automation
description: "Create a coherent brand system and derive landing pages, social cards, presentations, and videos with evidence-based QA and channel-safe automation."
license: MIT
---

# Brand Design Automation

Use for a new brand, campaign system, landing page, social carousel, presentation, or short-form video that must share one identity.

## Operating rule

`One Brand Anchor -> many channel adaptations -> human approval.`

Do not call unreviewed output “100% automated.” AI executes; the accountable human selects references, resolves tradeoffs, and approves release.

## Workflow

1. **Frame** — Ask only for missing decision-critical inputs: offer, audience, desired action, channels, constraints, and approver. State assumptions instead of blocking on minor gaps.
2. **Anchor** — Create one `brand-package.json` from [brand-package.schema.json](assets/brand-package.schema.json). Lock promise, voice, palette, type scale, spacing, imagery, CTA, and prohibited claims before channel work.
3. **Prototype** — Build the highest-information artifact first, normally a responsive landing page. For an existing brand, extract the anchor from approved source material instead.
4. **Propagate** — Derive cards, slides, and video from the locked anchor. Adapt hierarchy and pacing to the channel; do not merely resize.
5. **Inspect** — Run `scripts/validate_brand_package.py`. Then use the visual and release gates in [qa-rubric.md](references/qa-rubric.md).
6. **Revise** — Fix the highest-severity failures first. Preserve approved elements. Record each deliberate exception.
7. **Deliver** — Return source files, exports, brand package, QA report, known limitations, and next test.

## Tool routing

- Use code/HTML/CSS for responsive landing pages and deterministic components.
- Use the host image-generation skill for original raster imagery or image edits.
- Use Figma-compatible tooling when editable design-system artifacts are required.
- Use slide tooling for editable decks; use video tooling for timed motion outputs.
- Use browser/computer control only in duplicated project files with least privilege. Never grant blanket permission when scoped approval is available.

For a one-command multi-artifact request, follow [orchestration.md](references/orchestration.md) and maintain a pipeline receipt with `scripts/pipeline_state.py`. The default execution chain is:

`planner -> brand package -> landing -> Figma design -> Canva adaptation -> social -> Figma Slides -> motion/video -> QA -> delivery`

Prefer GPT Astra only when the host exposes it as a callable model. Never pretend that a ChatGPT UI model is connected. Otherwise use the active agent model and record `planner_fallback` in the receipt. Prefer direct Figma MCP for editable systems and Canva MCP for template/social adaptation; both require live write tests. For video use Figma timeline export, then Adobe/video MCP, then deterministic `motion-film`; CapCut is optional and must never be claimed unless its connector is authenticated and tested.

See [workflow.md](references/workflow.md) for artifact-specific production contracts.

## Quality gates

Release only when all apply:

- The same promise, visual tokens, and primary CTA are traceable across every artifact.
- Mobile legibility, keyboard focus, contrast, safe areas, and export dimensions are checked.
- Claims, prices, dates, sources, licenses, and required disclaimers are verified.
- No private data, credentials, patient data, or confidential source material appears in prompts or outputs.
- Regulated work has named legal/medical/compliance approval; absence is a hard stop.
- Facts, assumptions, generated content, and unresolved items are distinguishable.

## World-class loop

Score each iteration with [qa-rubric.md](references/qa-rubric.md). Stop only when:

- no blocker or critical failure remains;
- every dimension is at least 3/5;
- weighted score is at least 85/100;
- the next iteration would be preference-only or lower value than release.

Never improve visual polish by weakening truthfulness, accessibility, privacy, or brand coherence.
