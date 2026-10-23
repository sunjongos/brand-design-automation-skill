# End-to-end orchestration

## Completion contract

“Automated” means every requested stage produces either a verified artifact or a named blocked receipt. A plan alone is not completion.

## Stages

1. `planner` — resolve callable provider. Use Astra only when actually exposed; otherwise record the active model as fallback.
2. `brand_anchor` — write and validate `brand-package.json`.
3. `landing` — generate a responsive implementation and test mobile, keyboard, and error states.
4. `figma_design` — create/session a Figma file, write incrementally with `use_figma`, return every node ID, and inspect screenshots.
5. `canva` — verify live authentication, select an approved Brand Kit when available, then create editable template/social adaptations. Never replace Figma source-of-truth tokens silently.
6. `social` — derive channel-native frames from the same promise, CTA, and tokens.
7. `slides` — call Figma Slides with a self-contained brief; retain editable claim URLs.
8. `video` — the active capable model writes the edit decision list, scene code, captions, transitions, and safe-area adaptations. Render with deterministic motion-film + FFmpeg and run frame QA. Produce 16:9 and 9:16. Figma/Adobe may accelerate; CapCut is optional only when connected.
9. `qa` — validate tokens, contrast, privacy, rights, claims, responsive behavior, screenshots, and video frames.
10. `delivery` — provide editable sources, final exports, URLs, receipt, limitations, and approver state.

## Failure handling

- Retry only after classifying the error: auth, permission, schema, rate, transient, or design defect.
- Never silently skip a stage. Mark it `blocked`, record evidence and fallback, and continue only if the fallback preserves the requested outcome.
- Authentication is a user boundary. Return the exact reconnect requirement; do not claim a connector works.
- External writes use project-specific files and least privilege.
- A remote generative-video failure does not block editing when source assets and the local motion-film/FFmpeg path are available. Record the local render, probe output, and QA report as evidence.

## Receipt

Create with:

```bash
python3 scripts/pipeline_state.py init run.json --brand "Brand name"
python3 scripts/pipeline_state.py set run.json planner passed --artifact active-model --note planner_fallback
python3 scripts/pipeline_state.py set run.json figma_design passed --artifact https://figma.com/design/...
python3 scripts/pipeline_state.py check run.json
```

`check` succeeds only when all ten stages pass. `--allow-blocked` is diagnostic only and must not be presented as full completion.
