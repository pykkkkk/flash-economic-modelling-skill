---
name: econ-modeling-flash
description: A fast toolkit for building a small economic model from an observed real-world phenomenon: a 9-step workflow from phenomenon to a compact, defensible, verifiable, audited theoretical model and, optionally, a short LaTeX working paper. For non-specialists, economics/management students and first-time theory writers; it deliberately does not chase top-journal novelty. Use when the user wants to build an economic model, theoretical model, toy or stylized model from a real-world phenomenon; formalize an intuition into assumptions and propositions; set up utility/production/profit maximization, equilibrium, first-order conditions, comparative statics or welfare analysis; explain an observed fact or empirical result with economic theory; or write a small theory paper or working paper. Trigger phrases: economic modeling, theoretical model, build a model, model this phenomenon, formalize an intuition, assumptions and propositions, equilibrium, comparative statics, welfare analysis, short theory paper, working paper.
agent_created: true
---

# Economics Modeling — Flash (econ-modeling-flash)

## Overview

Turn "an observed phenomenon" into "a passable economic model" — **9 steps, bounded, reproducible**.

This skill is for **first-time theory writers, economics/management students, and researchers who want a fast, rigorous scaffold for a small model**.
The *reader* of what you produce is assumed to be economically literate — write for that reader, not for a layperson. Researchers with substantial experience may not need the step-by-step guidance, but the **rigour bar is the same**: the same checks, the same audit, the same honesty about limits.

**Delivery chain**: phenomenon → perspective → assumptions → model & solution → checks → report → extension → expert review → short paper (LaTeX/PDF).

> **Three commitments that define this skill.** (1) **Scientific rigour** — the reader of your output is an economist; never dumb it down, never let it mislead. (2) **Elegance through simplicity** — a beautiful model has few assumptions and a simple form; parameter count is not sophistication. (3) **Practical relevance** — the model must answer a real question and yield a communicable insight, serving research rather than entertainment.

### Three hard constraints (apply throughout; never violate)

| Constraint | Meaning |
|------|---------|
| **Parsimony** | No complicated functional forms; keep the parameter count down (**a baseline model must have ≤ 5 parameters and ≤ 3 endogenous variables**); the model must *look* clean and intuitive — it should fit on one page. A new parameter or assumption must *earn its place* by changing a conclusion or a comparative-static sign; otherwise drop it. |
| **Rigour** | Every assumption, proposition and equation **must be grounded in the literature or in theory** — and the deliverable must state **how** the source supports it (evidence-based modeling, Global Rule 3); the literature must span **both classic foundations and the last ten years**; notation must follow mathematical and economic convention; every solution must be verifiable. After every change, the model must pass the pre-delivery audit. |
| **Practical relevance** | The model must answer a *real* question and yield a *communicable* insight — a management or "life-economics" principle the reader can act on or cite. It serves research, not entertainment: no toy exercises whose only point is to run the solver. State plainly what the model can and cannot tell the reader. |

### What counts as "passing"

A passing model satisfies **all** of: **① assumptions are explicit and defensible; ② the logical chain is complete (assumptions → optimization → equilibrium → propositions); ③ propositions carry sign-level, verifiable implications; ④ it can explain, in one sentence, something about the real world; ⑤ it yields a communicable, decision-relevant insight a reader can use or cite**.
It does *not* require: a new mechanism, new mathematics, or publishability in a top journal.

---

## When to trigger

Load this skill when:

- The user describes a **real phenomenon / policy / puzzling fact** and asks whether economics can explain it, or how to model it
- The user wants to **formalize** an intuition into assumptions, propositions and an equilibrium
- The user needs to set up a utility / production / profit maximization problem, derive first-order conditions, solve for equilibrium, or do comparative statics / welfare analysis
- The user wants a **theoretical framework to match a set of empirical results**
- The user wants to write a **short theory paper / working paper** from scratch
- The user mentions: economic modeling, theoretical model, equilibrium, comparative statics, welfare analysis, assumptions and propositions

**Not applicable**: purely econometric / causal-identification empirical design (use `causal-infer-master` instead); a serious theory paper that needs the full 11-stage heavy workflow (use `pAI-Econ-claude-main` instead).

---

## Global Rules

1. **Every step is a decision point and the user owns the choice.** Steps 1–3 exist to **ask or to identify user input**, not to decide on the user's behalf.
   When the user has not specified something, use `AskUserQuestion` (2–4 concrete options) and **bundle all questions belonging to the same decision point into one round** — do not drip-feed them.
   Only when the user says "you decide" may the model supply a **default recommendation**, explicitly labelled "this is a default and can be changed".
2. **Literature must be verified online; fabrication is forbidden.** Every citation that enters a deliverable must be checked in this session with `WebSearch`/`WebFetch`
   (authors, year, title, journal, volume/issue/pages). Verified items are tagged `[VERIFIED]` with a source; unverifiable items are tagged `[UNVERIFIED]` and
   **must not enter the reference list of the final paper**. Language models produce "very plausible" fake references — internal confidence is not evidence.
3. **Evidence-based modeling (binding principle).** Every **key content item** — each functional form, key assumption, parameter restriction and major modeling choice — must carry **(a)** a **support source** (classic literature / textbook / stylized empirical regularity / axiomatic requirement / a labelled own construction) **and (b)** a **link sentence** stating *how* that source supports it here (source + the property it provides + why this model needs that property).
   **A bare citation is not evidence.** Every `S4_model.md` and `S6_model_report.md` must carry an **evidence table (E-table)**. Full specification, support types and anti-patterns: `references/evidence_based_modeling.md`.
4. **Label the epistemic status honestly.** Strictly distinguish:
   - **Analytical result** (a proof or symbolic derivation exists)
   - **Numerical illustration** (a computation at finite parameter values; not general)
   - **Mechanism sketch** (directional intuition, not proved)
   Never say "we prove" about a numerical result, never say "in general" about a finite parameter grid, never say "robust" about a single parameter value.
5. **When solving fails, degrade — do not force it.** If no closed form exists or it is intractable: try ① simplifying the functional form ② linearizing ③ restricting the parameter domain ④ reducing to two periods / two agents.
   If it is still unsolvable, **tell the user explicitly** and label the model "numerical illustration + local comparative statics". Never fabricate a closed form.
6. **Everything gets written to disk.** Write each step's output to an `S1..S9` file in the working directory, and also give the key conclusions in the reply (the user cannot see raw tool output).
7. **Notation convention beats expressive freedom.** Follow the notation table and naming rules in `references/modeling_cookbook.md`; in one model a symbol may carry **exactly one meaning**.
8. **Deliverables follow the conversation language, not this skill's language.** Everything you *author* — `S1..S9`, the model report, the LaTeX paper, and figure axis labels, titles and legends — must be written in **the language the user is speaking with you**, even though this skill's own documentation and tooling are in English. Translate freely: section headings, table headers, figure labels and the prose around quoted numbers all follow the conversation language, not the language of these files.
   The engine's raw `--out` diagnostics (`S4_cs.md`, `S5_lint.md`, `S7_sim.md`, the `foc` report) are the deliberate exception: they stay verbatim in the engine's language as the **audit trail** for your numbers. Whenever you quote them into a deliverable, render the quoted content in the conversation language and say that the verbatim original is the adjacent raw file.

9. **Audit every change — never a silent revision.** After *any* edit to the model or its deliverables (a new assumption, a recalibration, a corrected formula, a reworded report), re-run the pre-delivery audit (`scripts/audit_model.py`) and the self-test (`scripts/selftest.py`). If the model changed after S8, S8.1 is mandatory *before* you tell the user the revision is "done". A revision that has not been re-audited must never be presented as finished.

10. **Write for an economist, and keep it simple.** The reader of your output knows economics — do not over-explain the basics, but never hide a limitation, an approximation, or a calibration choice. Prefer the *smallest* model that still carries the mechanism: a new parameter or assumption must *earn its place* by changing a conclusion or a comparative-static sign, otherwise drop it. A beautiful model has few assumptions and a simple form; a long parameter list is not sophistication.

---

## The 9-step workflow (plus the conditional **S8.1**)

| Step | Name | Purpose | Main actions | Output file |
|------|------|------|---------|---------|
| **S1** | Describe the phenomenon | Understand it and map its elements | Verify it online; identify stakeholders and institutional setting; list candidate theories; anticipate the modeling approach | `S1_phenomenon.md` |
| **S2** | Fix the perspective | Choose field and style | Ask "classic or novel explanation"; fix the disciplinary perspective; search classic + frontier work in that field | `S2_perspective.md` |
| **S3** | Core assumptions | Make premises explicit | Normalize the user's assumptions; propose additional candidates; lock in the economic theory | `S3_assumptions.md` |
| **S4** | Build and solve the model | Construct and solve | Apply the **four-step method** (minimize → classic form → relax → extend, see `references/four_step_method.md`); build & solve in Python; annotate each equation's basis with a **link sentence** and fill the **evidence table** (Global Rule 3); prefer fast methods, simplify if hard | `S4_model.md` + `S4_model.py` |
| **S5** | Checks | Guarantee correctness and acceptability | Five hard checks: notation, consistency, solution, boundaries, dimensions | `S5_checks.md` |
| **S6** | Form the report | Deliver the model write-up | Assumptions / parameters / propositions / results / economic interpretation | `S6_model_report.md` |
| **S7** | Extend | Thicken the model | Sensitivity analysis, relaxing/adding assumptions, heterogeneity | `S7_extension.md` + `figs/` |
| **S8** | Expert review | Locate the real standard | 5 reviewers score independently (two rounds), then aggregate + diagnose disagreement | `S8_review.md` |
| **S8.1** | **Re-review after revision** | **Do not let a revision go unverified** | **If the model was changed after S8 (to fix P0/P1 items, to raise the level, or on user request): re-run the same review instrument on the revised version, report the before/after delta per reviewer and per dimension, and check that no new defect was introduced** | `S8.1_review_after_revision.md` |
| **S9** | Write-up | Turn it into a short paper | Compile LaTeX to PDF | `S9_paper.tex` + `S9_paper.pdf` |

> **S8.1 is mandatory, not optional.** Any change to the model after S8 invalidates the S8 verdict — the scores describe the **old** version.
> If the model is revised, you **must** run S8.1 before S9 (or before telling the user the model has reached a given level).
> The only exemption is a purely cosmetic change (typo, formatting) that provably cannot move any dimension; state that exemption explicitly.
> ⚠️ A revision almost always *fixes* the lowest dimension and can therefore *hide* a newly introduced defect — S8.1 exists to catch exactly that.

**The detailed operating manual for each step (question scripts, action lists, self-checks) is in `references/steps.md` — read the relevant section before executing each step.**

### Step highlights

**S1 Describe the phenomenon** — Verify online that the phenomenon exists or assess its credibility (news / policy documents / statistics / case studies), and **always give the source**;
identify stakeholders (who decides, who is affected) and the institutional environment; list 3–5 candidate economic theories; anticipate the family of modeling approaches.
⚠️ Separate "verified public fact", "unverified contextual claim" and "stylized assumption made for tractability" — all three must be labelled distinctly.

**S2 Fix the perspective** — **You must first ask the user: a "classic explanation" or a "novel explanation"?** (This maps onto the four NSFC science-question attributes:
"demand-driven / breaking bottlenecks" and "convergence across disciplines" vs "encouraging exploration / highlighting originality" and "targeting the frontier / taking a distinctive path".)
- Classic explanation → draw mainly on classic theory, with a **conventional** modeling style (textbook setup, expected-direction results)
- Novel explanation → draw mainly on frontier findings, with a **striking** style (counter-intuitive mechanisms, non-standard preferences or information structures)
After fixing the perspective (production & consumption / education / labour / industrial organization / development / public / environmental / health / urban & regional / behavioural / macro / finance / international trade / institutional), search the field's classic views and the last ten years of frontier work, and write both into `S2`.

**S3 Core assumptions** — First **normalize** the user's colloquial premises into assumption statements that can be written into a model;
then **propose additional assumptions** (2–4 candidates at a time, each saying "what this makes more rigorous") for the user to select;
finally lock in **one leading economic theory** (e.g. consumer utility maximization, firm profit maximization, principal–agent, search and matching, game-theoretic equilibrium, externalities/public goods).

**S4 Build and solve the model** — Re-check the perspective and the assumptions → write the model (notation table, timing, equilibrium concept) →
**S4 must follow the four-step method (minimize → classic form → selective relaxation → dimension extension; see `references/four_step_method.md`)**: first add the tightest constraints to reach a solvable baseline, then pair with classic functions; relaxation and extension are done in S7. →
**use `scripts/econ_solve.py` for symbolic solution, comparative statics and numerical verification** → annotate each equation's basis **with a link sentence**, and complete the **evidence table (E-table)** per Global Rule 3 → state the propositions.
If solving is hard, degrade per Global Rule 5 and tell the user.
Default language is Python (use `scripts/econ_solve.py`; interpreter path under "Runtime environment").

**S5 Checks** — Five hard checks (details in `references/steps.md`, S5):
① notation follows mathematical and economic convention ② definitions are consistent throughout (does any symbol carry two meanings; are parameters and variables mixed up)
③ the solution is correct (back-substitution + first- and second-order conditions + boundary cases) ④ boundaries and corner solutions ⑤ dimensions and ranges.
**On finding an error → report it to the user and propose a fix; never quietly change a number to hide it.**

**S6 Form the report** — Deliver using `assets/model_report_template.md`: research question / assumptions / parameter table / model setup /
propositions (with proof or derivation notes) / solution / economic interpretation / limitations. Prefer figures and tables; put long derivations in the appendix.

**S7 Extend** — Do at least: ① **symbolic comparative statics** for the key parameters ② **numerical sensitivity** (one-parameter sweeps + two-parameter heat maps)
③ **relax at least 1 assumption** (to see whether conclusions survive) ④ **heterogeneity** (if applicable: split by income / ability / region).
Generate figures with `scripts/econ_solve.py sim` and store them in `figs/`.

**S8 Expert review** — 5 reviewers with different emphases score **independently** (round one blind to each other), then cross-examine and aggregate in round two;
use the 6-dimension weighted table in `references/review_rubric.md` and `scripts/review_score.py` to compute the total, the band and the **disagreement diagnosis**.
The output must include: total score, band, **each reviewer's single most damaging criticism**, and a "what you must not claim" list.

**S8.1 Re-review after revision** — **Trigger**: the model has been changed in any way after S8 (P0/P1 fixes, a "raise it to publishable level" request, a new proposition, a recalibration). Action:
keep the **same reviewer roles, dimensions and weights**, re-score the revised version, and report a **before/after table** (per reviewer total + per dimension mean) plus the change in band;
then run the **regression check**: does the revision contradict anything already written in `S4`–`S7`, and does it leave stale numbers in the old files?
Report the band of the revised version, and state explicitly whether the intended target level was reached.
⚠️ Never let a revision **lower** the reported standard silently: if the new band is the same as the old one, say so — that is the reliability evidence for the band.

**S9 Write-up** — Write the short paper following the LaTeX skeleton in `references/paper_template.md`:
phenomenon → distilling the economic question → assumptions → model → solution and results → interpretation → limitations.
Compile with `pdflatex` twice (for cross-references). If no LaTeX is available locally, output the `.tex` plus compilation instructions — never fabricate a PDF.

---

## Interaction norms

| Situation | What to do |
|------|------|
| The user gives only a one-line phenomenon | Do S1's online verification first, then ask "classic or novel" + "which perspective" in S2 via `AskUserQuestion` |
| The user already has a clear preference | Recognize it, **restate it for confirmation**, skip the repeated question, and move on |
| The user must choose among assumptions / theories / modeling approaches | Use `AskUserQuestion`, ≤ 4 options, each stating the consequence of choosing it |
| The user wants to change perspective or assumptions after S4 | Allowed, but write the change back into `S1`–`S3` and re-check consistency in `S5`; state which downstream conclusions are overturned |
| Solving fails / data missing / phenomenon unverifiable | Stop and tell the user, offer 2–3 options, and wait for their decision |

**Question cadence**: ask everything belonging to the same decision point at once; each step normally needs one round of questions (0–2 questions).
Do not interrogate repeatedly in the name of rigour; when the user clearly wants to move fast, proceed with "default + changeable".

---

## Runtime environment (configured on this machine)

- **Python (isolated environment, prefer this)**: `C:\Users\asus\.workbuddy\binaries\python\envs\default\Scripts\python.exe`
  Installed: numpy / scipy / sympy / matplotlib / pandas.
  If that path does not exist, fall back to `C:\Users\asus\.workbuddy\binaries\python\versions\3.13.12\python.exe`
  and tell the user the plotting/symbolic libraries may need to be installed by them (this skill **does not** install software for the user).
- **Solver engine**: `scripts/econ_solve.py` (symbolic solution / comparative statics / numerical sweeps and plots / notation lint)
- **Review tool**: `scripts/review_score.py` (score aggregation, banding, reviewer disagreement and agreement coefficient)
- **Self-test**: `scripts/selftest.py` (verifies the parser, solver, reviewer and auditor have not regressed; **run it before first use and after any change to the scripts**)
- **Pre-delivery audit**: `scripts/audit_model.py` (symbol-table completeness, parameter consistency, numeric regression after a revision, deliverable hygiene, claim safety, evidence-based grounding `--evidence`; **run it as gates G7 + G8 before you call the model "done"**)
- **PowerShell note**: on this machine `bash` is broken, so use the PowerShell tool for commands; PowerShell does not return stdout,
  so **write results to a UTF-8 file and read them back**, or have the script write its own report to a file.

**Expression-writing conventions (must be communicated to the user when the model is first written in S4)**

| Rule | Explanation |
|------|------|
| Symbol names match the notation table | `q_1` and `q1` are the same symbol (underscores are ignored) |
| **Explicit `*` between symbols** | Write `2*b*q1`, `b*(q1+q2)`; between a number and a symbol/bracket the `*` may be omitted (`2b` = `2*b`) |
| No guessing-based implicit multiplication | A run-together token is split only if it can be decomposed **entirely into already-declared symbol names** (with `b`, `q1` declared, `bq1` → `b*q1`); otherwise it stays a single symbol and a warning is issued. **This prevents the fatal error of silently parsing `q1` as `q*1`** |
| Powers and functions | Powers use `**` or `^`; logarithms use `ln(x)`/`log(x)`; function names need parentheses |
| Abstract functions | Inputs such as `u(c)` or `F(K,L)` are recognized as function calls and **flagged in the report**; in that case only implicit derivatives are available |

---

## Output layout

By default create `econ_model_<slug>/` under the current working directory (e.g. `econ_model_tutor_ban/`);
if the user specifies a directory, use theirs; if continuing work inside an existing project directory, keep using that directory.

```
econ_model_<slug>/
├── state.json              # current step, completed steps, key decisions (perspective/style/assumptions/theory), pending
├── S1_phenomenon.md
├── S2_perspective.md
├── S3_assumptions.md
├── S4_model.md             # notation table, model setup, propositions, annotated bases
├── S4_model.py             # reproducible solution script (from an econ_solve.py spec, or hand-written)
├── S5_checks.md
├── S6_model_report.md
├── S7_extension.md
├── S8_review.md
├── S8.1_review_after_revision.md   # only if the model was changed after S8 (mandatory then)
├── S9_paper.tex
├── S9_paper.pdf            # if pdflatex is available
├── S9_references_check.md  # one line per reference: verification source or reason for exclusion
├── figs/                   # all figures (PNG; also PDF when used in the paper)
└── logs/run.log            # script run log
```

**Resuming**: when the user says "continue", read `state.json` first to locate the next step, and re-check that the previous step's output is complete.

---

## Quality gates (self-check before ending each step)

| Gate | Checkpoint | If it fails |
|------|-------|--------------|
| **G1 Framing gate** | Is the phenomenon verified? Has the user confirmed the perspective and style (classic/novel)? | Go back to S1/S2 and ask |
| **G2 Assumption gate** | Are the assumptions explicit, defensible and mutually consistent? Does each have a basis? | Go back to S3 and add or remove |
| **G3 Solution gate** | Are the FOCs back-substituted? Are second-order conditions checked? Is the closed form verified by numerical sampling? | Fix it; if unfixable, degrade and say so |
| **G4 Consistency gate** | Does each symbol have one meaning? Are parameters and variables mixed up? Are dimensions consistent? | Go back to S5, fix, and write back upstream |
| **G5 Evidence gate** | Is every reference `[VERIFIED]`? Are numerical conclusions labelled "numerical illustration"? | Verify or delete the citation/conclusion |
| **G6 Wording gate** | Any "we prove" about numerical results, "in general" about a finite grid, "robust" about a single point? | Rewrite the wording |
| **G7 Audit gate** | Has `scripts/audit_model.py` been run and returned **0 FAIL**? Are solver values consistent with the symbol table (no "one symbol, two values")? Did a post-S8 revision re-run S8.1? | Run the audit + self-test; do not finalize until 0 FAIL |
| **G8 Grounding gate** (evidence-based modeling) | Does every functional form / key assumption / parameter restriction have a support source **and** a link sentence saying *how* it supports? Is the E-table present and complete? Are own constructions labelled? (Check: `audit_model.py --evidence S4_model.md S6_model_report.md`) | Go back to S3/S4, write the missing links or drop the unjustified item |

When a gate fails, **tell the user explicitly** — do not let it pass silently.

---

## Resource index

| File | When to load |
|------|---------|
| `references/steps.md` | **Before executing each step**, read that step's subsection (question script, action list, delivery template) |
| `references/four_step_method.md` | **S4** (+ S7): the four-step economic modeling method (minimize → classic form → relax constraints → dimension extension), the mandatory SOP for S4 |
| `references/evidence_based_modeling.md` | **S3, S4, S5, S6**: the binding evidence-based modeling principle — support types, the "how it supports" link sentence, the E-table, anti-patterns (gate G8) |
| `references/theory_toolbox.md` | S2, S3, S4: perspective → theory → classic model → must-read literature map; modeling-approach selection |
| `references/modeling_cookbook.md` | S3, S4, S5: functional-form library, solution recipes, comparative-statics techniques, **notation conventions**, **the parsimony principle**, common-error list |
| `references/review_rubric.md` | S8 / S8.1: reviewer roles, 6-dimension weighted scoring table, banding criteria, disagreement and agreement handling |
| `references/paper_template.md` | S9: short-paper structure, LaTeX skeleton, figure/table and equation conventions, pre-submission checklist |
| `assets/model_report_template.md` | S6: the model-report delivery template |
| `scripts/econ_solve.py` | S4, S5, S7: symbolic solution / comparative statics / numerical sweeps and plots / notation lint |
| `scripts/review_score.py` | S8 / S8.1: score aggregation, banding, disagreement diagnosis |
| `scripts/audit_model.py` | Gates G7 + G8 / every revision: symbol-table completeness, parameter consistency, numeric regression, deliverable hygiene, claim safety, evidence-based grounding (`--evidence`) |
| `scripts/selftest.py` | **Before first use**, or after changing the scripts: verifies parsing/solving/review/audit computation have not regressed (57 cases) |
| `scripts/update_skill.py` | Updating the skill: `check` compares the local `VERSION` with the latest GitHub Release; `update` backs up and syncs (source of truth: Release tags) |

---

## Updating this skill

This skill can update itself from its GitHub Release tags. Two subcommands ship in `scripts/update_skill.py` (Python standard library only — no extra dependencies):

```bash
python scripts/update_skill.py check    # compare local VERSION with the latest GitHub Release
python scripts/update_skill.py update   # back up the current skill, then download and sync the latest Release
```

Conventions:
- The single source of truth for the version is the `VERSION` file at the skill root; `CHANGELOG.md` records every change.
- Updates are pulled from **GitHub Release tags** (stable, reversible) — never from a moving branch.
- On every activation of this skill, run `check` first (silent, non-destructive) so you are told when a newer release exists.
- `update` writes a timestamped backup to `../_backups/econ-modeling-flash_<timestamp>/` before overwriting, so you can always roll back.
- **After `update`, restart the session** for the new code to take effect.

---

## Known boundaries (must be communicated to the user)

- This skill targets **passing**, not **excellence**: it produces a small theoretical model that is internally coherent, defensible and testable.
  It does not guarantee originality and does not assess journal-level contribution (that needs the heavy workflow of `pAI-Econ-claude-main`).
- **No empirical estimation**: it does not obtain the user's micro data and does not run regressions; if the user needs causal identification, redirect to `causal-infer-master`.
- **It does not substitute for reading the literature**: `theory_toolbox.md` offers leads and a must-read list; the actual argument still requires the user to go back to the original papers.
- **It does not install software**: it only uses the environment already present; missing libraries must be installed by the user.
- **The S8 review is simulated**: it is a structured self-assessment of the model's own quality, not a real peer-review outcome,
  and must not be used to claim "this has passed expert review". **The same applies to S8.1** — a re-review measures the *change* honestly, it does not turn a self-assessment into peer review.
- **A revision is not a promotion**: fixing the P0 items raises the score because the defects are gone, not because the instrument became generous. S8.1 must report the before/after delta so the user can see how much of the gain came from the fix and how much from the author's own leniency.
