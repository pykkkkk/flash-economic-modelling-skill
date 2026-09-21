# Changelog

All notable changes to this skill are documented here. Versions follow [Semantic Versioning](https://semver.org).

## [1.1.2] - 2026-09-21

### Added
- **Evidence-based modeling** as a binding principle (Global Rule 3, gate **G8**): every functional form, key assumption, parameter restriction and major modeling choice must carry a support source **and** a link sentence stating *how* it supports the model. A bare citation is not evidence.
  - New reference `references/evidence_based_modeling.md`: support types (S1 classic / S2 textbook / S3 stylized fact / S4 property requirement / S5 own construction), the "how it supports" link sentence, the required evidence table (E-table), anti-patterns and a checklist.
  - `SKILL.md`: the Rigour constraint and Global Rule 3 rewritten; new gate **G8 Grounding**; resource index and the S4 workflow row/notes updated.
  - `references/steps.md`: the S3 assumption table gained support-type / source / "how it supports" columns; the S4 delivery template gained an **E-table** (`## 3.5`); S4 and S5 self-checks and the S5 audit command gained the evidence check.
  - `references/modeling_cookbook.md`: new §1.1 "Evidence-based modeling".
  - `scripts/audit_model.py`: new `--evidence FILE` check (WARN when a deliverable contains equations but states no basis).
  - `scripts/selftest.py`: new regression cases for the evidence check.
  - `README.md` / `README.zh-CN.md`: gates 7 → 8, G8 row added.

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
