# End-to-end orchestration

## Completion contract

“Automated” means every requested stage produces either a verified artifact or a named blocked receipt. A plan alone is not completion.

## Stages

1. `planner` — resolve callable provider. Use Astra only when actually exposed; otherwise record the active model as fallback.
2. `brand_anchor` — write and validate `brand-package.json`.
3. `landing` — generate a responsive implementation and test mobile, keyboard, and error states.
4. `figma_design` — create/session a Figma file, write incrementally with `use_figma`, return every node ID, and inspect screenshots.
5. `social` — derive channel-native frames from the same promise, CTA, and tokens.
6. `slides` — call Figma Slides with a self-contained brief; retain editable claim URLs.
7. `video` — route in order: Figma timeline/MP4, Adobe quick cut/resize, deterministic motion-film. Produce 16:9 and 9:16; a CapCut path is optional only when connected.
8. `qa` — validate tokens, contrast, privacy, rights, claims, responsive behavior, screenshots, and video frames.
9. `delivery` — provide editable sources, final exports, URLs, receipt, limitations, and approver state.

## Failure handling

- Retry only after classifying the error: auth, permission, schema, rate, transient, or design defect.
- Never silently skip a stage. Mark it `blocked`, record evidence and fallback, and continue only if the fallback preserves the requested outcome.
- Authentication is a user boundary. Return the exact reconnect requirement; do not claim a connector works.
- External writes use project-specific files and least privilege.

## Receipt

Create with:

```bash
python3 scripts/pipeline_state.py init run.json --brand "Brand name"
python3 scripts/pipeline_state.py set run.json planner passed --artifact active-model --note planner_fallback
python3 scripts/pipeline_state.py set run.json figma_design passed --artifact https://figma.com/design/...
python3 scripts/pipeline_state.py check run.json
```

`check` succeeds only when all nine stages pass. `--allow-blocked` is diagnostic only and must not be presented as full completion.
