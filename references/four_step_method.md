# The Four-Step Economic Modeling Method (optimized)

> **Where it applies**: the standard operating procedure (SOP) for **S4 (Build and solve the model)** in this skill. **Step 1–2 are performed inside S4** (to obtain a solvable baseline model); **Step 3–4 share the same logic with S7 (Extend)** (Step 3 = robustness relaxation in S7; Step 4 = dimension extension in S7).
> **Source**: user-provided modeling methodology, embedded into the skill as the mandatory procedure for S4.

## Overall logic

> **Start from the "tightest constraint", obtain the smallest model that still yields a closed-form solution and signed comparative statics; then relax constraints along one main axis; finally land on the specific setting of the study.**

---

## Step 1 — Minimize: impose the tightest constraints, compress to the smallest solvable case

**Action**: give a complete specification of the four elements — **environment + preferences + technology + information** — and impose the tightest *constraining* assumption on each, compressing the problem to the **smallest model that yields a closed-form solution and signed comparative statics**.

**Typical tight constraints** (use as needed):
- Preferences: single good, separable utility, homogeneous households
- Technology: linear or Cobb-Douglas production/cost
- Information: complete information, no uncertainty
- Market: perfect competition, no frictions
- Time: static one period, no borrowing constraint

**Criterion**: if the model still cannot yield comparative statics, the constraints are not yet tight enough.

> ⚠️ **Key correction**: add *constraining* assumptions to make the model *smaller* — do **not** "propose as many assumptions as possible". The latter only inflates the model.

---

## Step 2 — Take the classic form: use the simplest, most classic functions and variables

**Action**: pair the Step 1 specification with textbook-standard functional forms and a **minimal variable set**.

| Object | Classic choice |
|---|---|
| Utility | Cobb-Douglas / CES / quasi-linear |
| Budget | Linear budget constraint |
| Cost | Linear / quadratic |
| Variables | Keep only the core variables the mechanism requires (usually 1–2 decision variables + 1 policy/price variable) |

**Criterion**: make the mechanism "visible at a glance" — the reader should see where the money comes from and where it goes after one read of the setup.

---

## Step 3 — Relax constraints: keep or drop each according to "whether it flips the sign of the core proposition"

**Action**: relax Step 1's assumptions *one by one* — **not all at once, but selectively**.

**Selection criterion (the single most important rule in this whole flow)**:

| Result after relaxing | Treatment |
|---|---|
| The sign of a core comparative static **flips** | **Keep** the original assumption, or discuss it in a separate section |
| The core conclusion is **qualitatively unchanged**, only the magnitude shifts | **May relax** it, as a robustness check |
| **Irrelevant** to the core mechanism | **Drop** it outright, do not put it in the model |

> ⚠️ **Key correction**: the selection criterion is *not* "whether the assumption literally mentions a core variable". An assumption like "the tutoring market is perfectly competitive" mentions no core variable, yet relaxing it can flip the price effect directly — so it must be kept.

**Goal**: test the **robustness** of the core proposition — "is the conclusion still there?"

---

## Step 4 — Form and dimension extension: answer new questions

**Action**: separate from Step 3, as an independent layer.

| Extension direction | Purpose |
|---|---|
| **Change functional form** | Go from special case to general (e.g. CD → CES, to see the substitution elasticity) |
| **Add independent variables** | Introduce new decision dimensions (time, number of children) |
| **Add heterogeneity** | Income quantiles, ability distribution, age structure |
| **Add dynamics** | Static → two-period / infinite-horizon, to see intertemporal substitution |
| **Add general equilibrium** | From partial to supply-side feedback |

**Goal**: not "test the conclusion" but **"tell more of the story"** — answer new questions the baseline model cannot.

---

## Two general principles

**Principle 1 — Find the main contradiction**
Keep the core / variables of interest as few as possible; the core must stand out. One model is responsible for one mechanism; too many mechanisms is equivalent to none.

**Principle 2 — Keep the form clean**
Reject function forms that are complex for complexity's sake. The value of economics is in *clear mechanisms*, not mathematical detail; if linear suffices, do not go high-dimensional.

---

## Four-step summary table

| Step | One-line positioning | Goal | Relation to neighboring steps |
|---|---|---|---|
| **1 Minimize** | Add the tightest constraints, compress to the smallest | Solvable | Provides the skeleton for 2 |
| **2 Classic form** | Pair with the simplest classic functions and variables | Mechanism visible | Builds on 1, produces the baseline model |
| **3 Relax constraints** | Selectively relax assumptions | **Robustness** | Tests the conclusions of 1–2 |
| **4 Form & dimension extension** | Change form, add dimensions | **New questions** | Opens a separate layer on top of 1–2 |

---

## Mapping onto this skill's workflow

| Four-step | Skill step | Output location |
|---|---|---|
| **Step 1 Minimize** | S3 assumption normalization + S4 opening | `S3_assumptions.md` constraints → `S4_model.md` minimal setup |
| **Step 2 Classic form** | S4 body | `S4_model.md` setup, closed form, propositions |
| **Step 3 Relax constraints (robustness)** | S7 item 3 (relax at least 1) | `S7_extension.md` robustness table |
| **Step 4 Form & dimension extension (new questions)** | S7 items 1/2/4 (comparative statics, numerical sweep, heterogeneity, dynamics / GE) | `S7_extension.md` full text + `figs/` |

> ⚠️ **Unified solution-region view**: when relaxing one assumption in Step 3 splits the solution space, the resulting alternatives (e.g. a corner solution vs an interior solution) are **not several parallel models**, but **distinct solution regions of the same model** under the same set of parameter conditions. Frame them as one family of solutions, so that scattered conclusions unify onto common parameter conditions instead of fragmenting into isolated propositions.

**One-sentence summary**: Step 1 adds *constraints* not assumptions; Step 2 takes the *classic form*; Step 3 selects by *whether the core sign flips*; Step 4 is *layered* with Step 3 (one governs robustness, the other new stories) — together with the two principles of "few and clear mechanisms", this framework directly guides theoretical modeling.
