> 🌐 Language: **English** · [中文](README.zh-CN.md)

<div align="center">

<img src="assets/icon.png" width="150" alt="econ-modeling-flash icon">

# econ-modeling-flash

**From a real-world phenomenon to a defensible economic model — in 9 guided steps.**

*A beginner-friendly, research-grade toolkit for building small economic models.*
*It comes with a built-in rigour armor: seven quality gates, a mandatory pre-delivery audit, and a simulated expert review.*

![Workflow](https://img.shields.io/badge/workflow-9%20steps-2ea44f)
![Quality gates](https://img.shields.io/badge/quality%20gates-7-blue)
![Audit](https://img.shields.io/badge/pre--delivery%20audit-0%20FAIL-orange)
![Self-test](https://img.shields.io/badge/self--test-55%2F55-brightgreen)
![Built with](https://img.shields.io/badge/built%20with-Python%20%C2%B7%20sympy%20%C2%B7%20matplotlib-3776AB)
![Audience](https://img.shields.io/badge/for-students%20%26%20first--time%20theorists-9cf)

</div>

---

## What it is

`econ-modeling-flash` is an agent **skill** that walks you from

> *"Here's something odd I noticed in the world…"*

to

> *"…and here is a small, internally coherent, testable economic model of it."*

— and, if you want, a compiled LaTeX working paper.

It is deliberately **small and honest**. It does not chase top-journal novelty, and it will not pretend a toy model is a breakthrough. What it *does* guarantee is the discipline of a real theory section: **explicit assumptions → a complete logical chain → verifiable propositions → one clear sentence about something real.**

> **The three commitments behind every step**
> 1. **Scientific rigour** — your reader is an economist. Never dumb it down, never let it mislead.
> 2. **Elegance through simplicity** — a beautiful model has *few* assumptions and a *simple* form. A long parameter list is not sophistication.
> 3. **Practical relevance** — the model must answer a real question and yield an insight you can act on or cite. It serves research, not entertainment.

---

## Who it's for

- 🎓 **Students** (economics / management) writing a first theory section, a thesis chapter, or a seminar paper
- 🔬 **Researchers** who want a fast, disciplined scaffold to sanity-check an intuition before investing weeks
- 🧠 **Anyone** who has asked *"can economics explain this?"* and didn't know where to begin

You do **not** need to be a theorist. You need to be curious — and willing to let a gate tell you "no".

---

## Why it's different

Most "AI, build me a model" flows hand you equations and stop. This one hands you equations **and then attacks them** — *before* presenting them as an answer.

| | An ordinary flow | **econ-modeling-flash** |
|---|---|---|
| Assumptions | implicit, in prose | **explicit, numbered, each with a basis + a testability label** |
| Equations | "looks about right" | **basis per equation + independent re-derivation + numerical back-substitution (error < 1e-9)** |
| Claims | confidently stated | **epistemic labels: analytical result · numerical illustration · mechanism sketch** |
| Literature | plausible-looking | **online-verified `[VERIFIED]` only — fabricated citations are blocked** |
| Delivery | "Done!" | **7 gates + a mandatory audit (0 FAIL) before it may be called done** |
| Revisions | silent | **S8.1 re-review: every change is re-scored, every delta reported** |

---

## Quick start

**1 · Install / enable the skill** — drop the `econ-modeling-flash/` folder into your agent's skills directory.

**2 · Smoke-test the engine** *(optional, ~1 s)*

```bash
python scripts/selftest.py     # expected:  Cases: 55 | passed: 55 | failed: 0
```

**3 · Just describe a phenomenon.** For example:

> *"Tutoring prices were capped and the sector shrank ~90%, yet household spending on tutoring went **up**. Can economics explain why?"*

**4 · Answer two questions** — *classic or novel* explanation, and *which field* (education, labour, IO…). The skill takes it from there, **one step at a time**, writing every step to disk.

That's the whole onboarding. No configuration, no hyperparameters, no prior modeling experience required.

---

## The 9-step flow — the heart of the skill

Every project runs the same spine. Each step has a **purpose, a scripted interaction, an action list, and a self-check**; nothing is improvised.

| Step | Name | What happens | Output |
|:---:|---|---|---|
| **S1** | Describe the phenomenon | Verify it online, grade the evidence, map the stakeholders, list candidate theories | `S1_phenomenon.md` |
| **S2** | Fix the perspective | *You choose:* classic vs novel explanation + disciplinary field | `S2_perspective.md` |
| **S3** | Core assumptions | Normalize your premises, propose additions, lock in one leading theory | `S3_assumptions.md` |
| **S4** | Build & solve | Notation table → optimization → equilibrium → **symbolic solve + numerical check** | `S4_model.md` + `.py` |
| **S5** | Checks | Five hard checks: notation · consistency · solution · corners · dimensions **+ the pre-delivery audit** | `S5_checks.md` |
| **S6** | Form the report | Assumptions, parameters, propositions, results, **economic interpretation** | `S6_model_report.md` |
| **S7** | Extend | Comparative statics · sensitivity sweeps · **relax ≥ 1 assumption** · heterogeneity | `S7_extension.md` + `figs/` |
| **S8** | Expert review | 5 reviewers score independently → cross-examine → aggregate + disagreement diagnosis | `S8_review.md` |
| **S8.1** | **Re-review after revision** *(conditional but mandatory)* | Changed the model after S8? The old verdict is stale — re-score and report the delta | `S8.1_review_after_revision.md` |
| **S9** | Write-up | Assemble the short paper and **compile LaTeX → PDF** | `S9_paper.tex` + `.pdf` |

```
 P H E N O M E N O N
        │
        ▼
 [S1]────────[S2]────────[S3]────────[S4]────────[S5]────────[S6]────────[S7]
 describe    perspective  assumptions  build/solve  CHECKS ✅    report      extend
        │                                                            │
        │                                                            ▼
        │                                                     [S8] expert review
        │                                                            │
        │                                      changed the model? ───┤
        │                                                            ▼
        │                                                  [S8.1] re-review
        │                                                            │
        └───────────────────────────────────────────────────────────►▼
                                                          [S9] LaTeX paper → PDF
```

> **S8.1 in one line:** *a revision is not a promotion.* Fixing a defect removes a problem — it does not mean the model got better than it is. S8.1 reports the before/after score for **every** dimension so you can see exactly what changed and what didn't.

---

## Rigour armor — how output quality is protected

This is where the skill earns its keep. Before any deliverable may be called "done", it passes the following.

### The 7 quality gates

| Gate | Question it asks | If it fails |
|:---:|---|---|
| **G1 · Framing** | Is the phenomenon verified? Has the user confirmed the perspective? | Go back to S1/S2 and ask |
| **G2 · Assumption** | Are the assumptions explicit, defensible, mutually consistent, and justified? | Go back to S3 |
| **G3 · Solution** | Are the FOCs back-substituted? Second-order conditions checked? Closed form verified numerically? | Fix, or degrade and disclose |
| **G4 · Consistency** | One symbol = one meaning? Parameters vs variables clean? Dimensions consistent? | Go back to S5 |
| **G5 · Evidence** | Is every reference `[VERIFIED]`? Are numerical results labelled as such? | Verify or delete |
| **G6 · Wording** | Any "we prove" about a number, "in general" about a grid, "robust" about a point? | Rewrite the wording |
| **G7 · Audit** | Did `audit_model.py` return **0 FAIL**? Post-S8 revision re-reviewed? | Run the audit + self-test; **do not finalize** |

### The non-negotiable Global Rules

- **No fabricated citations.** Every reference is verified online this session; unverifiable ones are blocked from the paper.
- **Every equation has a basis** — literature, textbook, institutional fact, or an explicitly labelled "for tractability" assumption.
- **Honest epistemic labels.** Analytical result ≠ numerical illustration ≠ mechanism sketch. Never blurred.
- **Degrade, don't fake.** If no closed form exists, the skill *says so* and reports a numerical illustration instead of inventing a proof.
- **Audit every change.** After *any* edit, the audit and self-test are re-run. A revision that hasn't been re-audited is never called finished.
- **The simulated review is labelled as simulated.** It measures the model's own quality honestly — it never becomes "this passed peer review".

### The tooling behind the armor

| Tool | Role |
|---|---|
| `scripts/econ_solve.py` | symbolic solve · comparative statics · notation lint · sensitivity sweeps & plots |
| `scripts/review_score.py` | S8/S8.1 score aggregation, banding, Fleiss-κ disagreement diagnosis |
| `scripts/audit_model.py` | **pre-delivery audit (gate G7):** symbol-table completeness, parameter consistency, numeric regression after a revision, deliverable hygiene, claim safety |
| `scripts/selftest.py` | **55 regression cases** guarding the parser/solver/reviewer/auditor — *run before first use and after any change* |

### And a paper trail you can audit

Every number is reproducible and traceable:

- ✅ **Reproducible** — solver specs (`spec_*.json`) + a `logs/run.log` for every run
- ✅ **Traceable** — `S9_references_check.md` records, line by line, the verification source (or reason for exclusion) of every citation
- ✅ **Self-critical** — `S8_review.md` ends with a **"what you must not claim"** list, so you never oversell
- ✅ **Regression-checked** — after a revision, the skill greps the old files for stale numbers and un-updated conclusions

---

## What you get

A complete, self-contained project directory:

```
econ_model_<slug>/
├── state.json                     # current step, decisions, resume point
├── S1_phenomenon.md               # …through…
├── S9_paper.tex / S9_paper.pdf    # the short paper (if LaTeX is available)
├── S9_references_check.md         # per-citation verification ledger
├── figs/                          # all figures (PNG + PDF)
└── logs/run.log                   # reproducible run log
```

**Resume any time:** say *"continue"* and the skill reads `state.json`, finds the next step, and re-checks that the previous step's output is complete.

---

## Recommended reading — economics, from zero to modeling

New to economics, or want to build models that actually convince? These are the books this skill leans on, in the order you'd want to read them.

### 🌱 Start here — plain language, no math required

| Book | Author | Why read it |
|---|---|---|
| **Naked Economics** | Charles Wheelan | The clearest "what economists actually think" book. If you read one, read this. |
| **The Undercover Economist** | Tim Harford | Everyday puzzles (coffee prices, supermarket queues) as economics. Great for spotting phenomena to model. |
| **Freakonomics** | Levitt & Dubner | How incentives reshape behaviour. Fun — and a masterclass in finding a question worth formalizing. |

### 📐 The toolkit — how to actually build a model

| Book | Author | Why read it |
|---|---|---|
| **Intermediate Microeconomics: A Modern Approach** | Hal R. Varian | **The single most useful companion to this skill.** Utility, demand, equilibrium, comparative statics — with worked examples. |
| **Game Theory for Applied Economists** | Robert Gibbons | Short, applied, and enough to model strategic situations (bargaining, entry, signalling). |
| **A Course in Microeconomic Theory** | David M. Kreps | The step up: rigorous micro theory for when you want to go deeper than the basics. |

### 🔍 Go further — behaviour, evidence, and the frontier

| Book | Author | Why read it |
|---|---|---|
| **Thinking, Fast and Slow** | Daniel Kahneman | Where standard assumptions about preferences break — a source of "novel" model mechanisms. |
| **Poor Economics** | Banerjee & Duflo | How good questions meet real data. A model of how to think about policy effects. |
| **Mostly Harmless Econometrics** | Angrist & Pischke | For the empirical half: how to tell whether an effect is real (pairs with the `causal-infer-master` skill). |

---

## Boundaries — what it will (and won't) do

**It will:** build a small, internally coherent, defensible, testable theoretical model — and tell you honestly what it can and cannot claim.

**It won't:**

- ✋ **Chase top-journal originality.** It targets *passing*, not *excellence*. 
- ✋ **Run your regressions.** No micro data, no estimation. 
- ✋ **Read the literature for you.** It provides leads and a must-read list; the argument still demands going back to the original papers.
- ✋ **Install software.** It uses only the Python environment already present.
- ✋ **Turn a self-assessment into peer review.** The S8/S8.1 review is *simulated* — structured, honest, and clearly labelled as such.

---

<div align="center">

**Found it useful?** Star the repo ⭐ — and if a gate saved you from an embarrassing mistake, that's the whole point.

*Built for people who want their first model to be an honest one.*

</div>
