# Brand Design Automation Skill

A reusable AgentSkill for turning one approved **Brand Anchor** into coherent landing pages, social carousels, presentations, and videos.

It treats automation as a controlled production system:

`strategy -> brand anchor -> prototype -> channel adaptation -> QA -> human approval`

## Why it exists

Many AI design workflows optimize for the first attractive image. This skill optimizes for a complete, traceable system: the same promise, proof, voice, visual tokens, and CTA across formats—without sacrificing accessibility, truth, privacy, or rights.

## Features

- Lean cross-tool workflow; no vendor lock-in
- Machine-readable brand package and JSON Schema
- Landing page, social, presentation, video, and interactive-promotion contracts
- Weighted 100-point QA rubric and severity model
- Hard release gates for privacy, rights, claims, and regulated review
- Dependency-free deterministic validator with tests
- Explicit stop rule for iterative quality improvement
- Auditable ten-stage automation receipt; blocked stages cannot masquerade as completion
- Direct Figma MCP, Canva MCP, and Figma Slides paths with verified video fallbacks

## Install

```bash
git clone https://github.com/sunjongos/brand-design-automation-skill.git
cp -R brand-design-automation-skill ~/.agents/skills/brand-design-automation
```

For OpenClaw workspaces, place it under `skills/brand-design-automation`.

## Validate

```bash
python3 scripts/validate_brand_package.py assets/brand-package.example.json
python3 -m unittest discover -s tests -v
```

## Usage

Ask the agent to create a coordinated brand campaign, for example:

> Build a brand system and derive a responsive landing page, ten social cards, an editable presentation, and 16:9 plus 9:16 videos. Run the brand QA loop before release.

The agent creates a `brand-package.json` first, then derives and verifies channel outputs from it.

For a full run, it also keeps a machine-readable receipt across planner, anchor, landing, Figma, Canva, social, slides, video, QA, and delivery. Astra, Canva, and CapCut are used only when the host actually exposes authenticated connectors; supported fallbacks preserve the output contract without misrepresenting provider availability.

## Safety

- Never place credentials, confidential material, patient data, or other private data into design prompts.
- Use least-privilege automation in duplicated project files.
- Verify claims, dates, prices, licenses, releases, and required disclaimers.
- Regulated work requires a named qualified approver.

## Repository layout

```text
SKILL.md                          Skill instructions
assets/brand-package.schema.json Machine-readable contract
assets/brand-package.example.json Example package
references/workflow.md           Artifact production contracts
references/qa-rubric.md          Release rubric and iteration loop
references/orchestration.md      End-to-end MCP workflow and failure policy
scripts/validate_brand_package.py Dependency-free validator
scripts/pipeline_state.py         Auditable stage receipt
tests/                            Regression tests
```

## License

MIT
