# Changelog

All notable changes to this skill are documented here. Versions follow [Semantic Versioning](https://semver.org).

## [1.1.1] - 2026-09-20

### Changed
- Removed all user-specific research references (e.g. "double reduction" / 双减 and the E/R/S taxonomy) from the skill's internal files. The four-step method and the "unified solution-region view" are kept as **general** methodology principles; the user-specific application example has been stripped out so the skill stays domain-neutral.
- `scripts/audit_model.py`: header comment no longer references the user's private project by name.

## [1.1.0] - 2026-09-20

### Added
- Added the **four-step economic modeling method** as the mandatory SOP for S4: `references/four_step_method.md` (minimize → classic form → relax constraints → dimension extension).
  - Step 1–2 are performed inside S4 (solvable baseline under the tightest constraints + textbook-classic form); Step 3–4 share the same logic with S7 (robustness relaxation / dimension extension).
  - `references/steps.md` S4 section gained a "The four-step method" subsection, Action list item 2 and the delivery template gained a "Four-step method log".
  - `SKILL.md` S4 workflow-table row, S4 step highlight, and resource index now reference it.
  - Includes the "unified solution-region view" (corner/interior solution regions after relaxing one assumption in Step 3) to consolidate scattered propositions.

## [1.0.0] - 2026-09-20

### Added
- Initial public release of `econ-modeling-flash`.
- 9-step guided workflow (S1–S9) plus the conditional **S8.1 re-review** step.
- Rigour armor: 7 quality gates (G1–G7), 6 global rules, and a mandatory pre-delivery audit (`scripts/audit_model.py`).
- Engine scripts: `econ_solve.py` (solve / comparative statics / lint / sweeps), `review_score.py` (S8/S8.1 scoring), `audit_model.py` (gate G7), `selftest.py` (55 regression cases).
- Bilingual README (`README.md` English, `README.zh-CN.md` 中文) and a minimalist scientific icon.
- Self-update support: `scripts/update_skill.py` with `check` / `update` subcommands, pulling from GitHub Release tags.
