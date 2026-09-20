# Changelog

All notable changes to this skill are documented here. Versions follow [Semantic Versioning](https://semver.org).

## [1.0.0] - 2026-09-20

### Added
- Initial public release of `econ-modeling-flash`.
- 9-step guided workflow (S1–S9) plus the conditional **S8.1 re-review** step.
- Rigour armor: 7 quality gates (G1–G7), 6 global rules, and a mandatory pre-delivery audit (`scripts/audit_model.py`).
- Engine scripts: `econ_solve.py` (solve / comparative statics / lint / sweeps), `review_score.py` (S8/S8.1 scoring), `audit_model.py` (gate G7), `selftest.py` (55 regression cases).
- Bilingual README (`README.md` English, `README.zh-CN.md` 中文) and a minimalist scientific icon.
- Self-update support: `scripts/update_skill.py` with `check` / `update` subcommands, pulling from GitHub Release tags.
