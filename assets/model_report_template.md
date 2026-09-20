# Model report template (model_report_template.md)

> **When to use**: S6. Copy this template to `<output_dir>/S6_model_report.md` and fill it in section by section.
> This is the **main report** delivered to the user — the paper (S9) is its normalized rewrite.
> Filling rules: leave no `<>` placeholders; never write "to be added"; every symbol must already be defined in the notation table in §2 of this file before it is used.

---

# <Model name>: model report

**Date**: <YYYY-MM-DD>
**Explanation style**: classic / novel  |  **Perspective**: <…>
**One-sentence model**: <state in plain words, without mathematics, what this model does>
**Epistemic status**: this report is a **theoretical model**, containing no data estimation and no causal identification. All numerical values are **illustrative computations**, not general conclusions.

---

## 1. Research question

### 1.1 The phenomenon
<Phenomenon statement: one sentence + time/space scope.>

### 1.2 Evidence
| # | Fact | Source (institution/title/year) | URL | Status |
|---|------|---------------------|-----|------|
| 1 | | | | verified / unverified / stylized |

### 1.3 From phenomenon to economic question
<Rewrite the phenomenon as an analysable question: who chooses what, when, subject to which constraints, and what determines the outcome.>

> **Research question**: <one sentence, of the form "Under … constraints, how does an increase in … change the equilibrium …?">

### 1.4 Relation to existing research
<Where this model stands and which gap it fills. Use [VERIFIED] references only.>

---

## 2. Notation table

| Symbol | Meaning | Type | Range | Unit | Source |
|------|------|------|---------|------|------|
| $x$ | <…> | endogenous | ≥0 | | — |
| $p$ | <…> | endogenous | ≥0 | | — |
| $a$ | <…> | parameter | >0 | | illustrative value |
| $\beta$ | <…> | parameter | (0,1) | | calibrated from literature |

**Number of parameters**: <n> (limit 5)  |  **Number of endogenous variables**: <n> (limit 3)

---

## 3. Assumptions

| # | Assumption (normalized statement) | Mathematical content | Type | Testability | Basis |
|---|---------------|---------|------|---------|------|
| A1 | <…> | <…> | preference | not testable | <literature [VERIFIED] / institutional fact / simplifying assumption for tractability> |
| A2 | <…> | <…> | market structure | partly testable | |

**Leading theory**: <utility maximization / Nash equilibrium / principal–agent / …>

**Assumption conflict check**: <no conflict / handled — explain how>

**Assumptions dropped and why**: <…>

---

## 4. Model setup

### 4.1 Environment and timing
<1–4 steps: who knows what, and does what, when.>

### 4.2 Individual problem
$$
\max_{x}\ U(x;\theta)\quad\text{s.t.}\quad \text{<constraint>}
$$
<Basis for each expression: literature / textbook / own construction (labelled)>

### 4.3 Equilibrium concept
> **Definition (<equilibrium name>)**: <definition of the equilibrium.>

### 4.4 Equilibrium conditions
$$
F(x^{*};\theta)=0
$$

---

## 5. Solution and results

### 5.1 First-order conditions
$$
\frac{\partial U}{\partial x}=0 \;\Longrightarrow\; \text{<FOC expression>}
$$

### 5.2 Closed-form solution
$$
x^{*}=\text{<solution>},\qquad p^{*}=\text{<solution>}
$$
<If a numerical solution or a degraded treatment was used, say so explicitly here: which degradation, why, and which conclusions it affects.>

### 5.3 Second-order conditions and boundaries
<SOC conclusion (Hessian negative definite / $f''<0$); interior/corner discussion; the parameter region in which the solution is feasible.>

### 5.4 Numerical verification
- Script: `<path>`
- Parameters: <values>
- FOC residual: <order of magnitude; should be < 1e-9>
- Verdict: <pass / fail>

---

## 6. Propositions

> **Proposition 1 (<short name>).** <Content, including the parameter conditions under which it holds.>
> *Proof/derivation notes*: <…>
> *Economic meaning*: <one plain sentence.>
> *Testable implication*: <if it maps to an observable quantity, state it; otherwise write "this one cannot be tested directly">

> **Proposition 2 (<short name>).** …
>
> **Corollary 1 (<short name>).** …

**Number of propositions**: <2–4>. Identities and first-order conditions are not presented as propositions.

---

## 7. Comparative statics

| Parameter | Effect on endogenous variables | Conditions | Economic meaning |
|------|---------------|---------|---------|
| $a$ | $\partial x^{*}/\partial a > 0$ | $b>0$ | <…> |

**Numerical sensitivity** (figure type: **parameter sweep**; parameter range: <…>)
![<caption>](figs/<file>.png)

---

## 8. Economic interpretation

### 8.1 Mechanism
<Explain the mechanism in 2–3 plain paragraphs: what changed → whose optimal choice changed → what happened after aggregation.>

### 8.2 Explaining the phenomenon
<Can the mechanism explain the phenomenon in §1.1? Which part can it explain? Which part can it not? >

### 8.3 Policy implications
<State cautiously; say which welfare criterion it relies on and which effects are ignored.>

---

## 9. Limitations and boundaries

1. **Technical limitations**: <…>
2. **Cost of the assumptions**: <relaxing which assumption would change the conclusions.>
3. **Extrapolation boundary**: <the range to which the conclusions apply.>
4. **Factors not modelled**: <general-equilibrium effects, dynamics, heterogeneity, information changes, etc.>
5. **Epistemic status**: <which conclusions are proved and which are only mechanism sketches.>

---

## 10. Reproducibility notes

- Interpreter: `C:\Users\asus\.workbuddy\binaries\python\envs\default\Scripts\python.exe`
- Scripts: `S4_model.py`, `econ_solve.py` (commands in §5.4 and §7)
- Log: `logs/run.log`
- Figures: `figs/`
