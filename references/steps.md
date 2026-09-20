# The 9-step operating manual (steps.md)

> Read this file's relevant section before executing a step. Each step gives: **purpose / question script / action list / delivery template / self-check / common traps**.
> General conventions are in `SKILL.md` (Global Rules and interaction norms); notation and functional forms in `modeling_cookbook.md`; theories and literature in `theory_toolbox.md`.

---

## S0 — Kick-off (not one of the 9 steps, but always done)

**Actions**
1. Classify the user: phenomenon only / already has assumptions / has a half-finished model / wants only one step (e.g. just comparative statics).
   —— If the user wants only one step, **do not force the 9 steps**; do that step and state what was skipped.
2. Create or locate the working directory (see the output layout in `SKILL.md`) and write `state.json`:
   ```json
   {"slug":"tutor_ban","current_step":1,"completed_steps":[],
    "decisions":{"phenomenon":"","perspective":"","style":"","theory":"","assumptions":[]},
    "pending":[],"python":"C:\\Users\\asus\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\python.exe"}
   ```
3. Print a progress banner: `[S1/9] Describe the phenomenon`, so the user can follow along.
4. **Fix the output language** (Global Rule 8). Record in `state.json` the language the user is speaking, and use it for **every authored file** — step documents, report section headings, table headers, and figure axis labels, titles and legends. A Chinese-speaking user gets Chinese `S1..S9` and Chinese figures even though this manual is in English. The engine's raw `--out` reports remain in English as the audit trail; anything you quote from them into a deliverable is rendered in the user's language.

**Self-check**: directory created, `state.json` written, output language fixed, the user knows what is coming next.

---

## S1 — Describe the phenomenon

**Purpose**: turn the user's "phenomenon" into a workable object of study — **does it really exist? who is inside it? which theory might explain it?**

### Question script (restate + key clarifications, at most 2 questions)

```
Let me restate your phenomenon first — please confirm or correct:
① The phenomenon (one sentence, observable, with a time/space scope):
② Who is affected, who knows what, who decides:
③ The outcome variable you care about:
④ Roughly when this started and how large it is:
```
If the user has already given enough, **do not read this out mechanically** — just restate and confirm.

### Action list

1. **Online verification** (mandatory; at least 2 searches, using both general and field-specific terms)
   - Search news, policy documents, statistical releases, case studies, academic abstracts, to confirm the phenomenon exists and its magnitude.
   - **Record the source**: title + institution + year + URL. Write it into the "evidence table" in `S1`.
2. **Grade the evidence** (the three categories must be labelled separately — this is the skill's core honesty requirement)

   | Category | Meaning | Handling |
   |------|------|------|
   | **Verified fact** | Public information retrieved in this session supports it | Cite the source |
   | **Unverified context** | Plausible but not findable | Write "we conjecture…" or phrase it as a hypothetical setting |
   | **Stylized assumption** | A deliberate departure from reality for tractability | Write "for tractability we assume…" |
   | **Possibly false** | Evidence contradicts it | **Must not motivate the model**; rewrite the phenomenon or change direction |

3. **Stakeholders and environment**: list 2–5 agents (households/firms/government/platforms/schools/hospitals…),
   and for each write its **objective, available actions, information, constraints**. This step directly determines whether what follows is a "single-agent decision problem" or a "game".
4. **Candidate theories**: list 3–5 economic theories that might explain the phenomenon, one line each as "theory → predicted direction".
   See the "phenomenon keyword → candidate theory" index in `theory_toolbox.md`.
5. **Anticipate the modeling approach**: offer 2–3 candidates (partial-equilibrium single-agent optimization / oligopoly game / principal–agent / search and matching / general equilibrium / dynamic optimization /
   heterogeneous agents), and state the cost of each (more parameters? harder to solve?).

### Delivery template (`S1_phenomenon.md`)

```markdown
# S1 Describe the phenomenon
## 1. Phenomenon statement (one sentence)
## 2. Evidence table
| # | Fact | Source (institution/title/year) | URL | Verification status |
## 3. Stakeholders and environment
| Agent | Objective | Available actions | Information | Key constraints |
## 4. Candidate theories (3–5)
| Theory | Proponent/year | Prediction for this phenomenon | Status of basis |
## 5. Candidate modeling approaches
| Approach | Pros | Cost | Data/parameters needed |
## 6. Open questions (handed to S2)
```

### Self-check
- [ ] The phenomenon is observable, has a time/space scope, and is not "everyone feels that…"
- [ ] The evidence table has ≥ 2 verified sources, each with its category labelled
- [ ] No "possibly false" claim was used to motivate the model
- [ ] ≥ 3 candidate theories (otherwise S2's multiple-choice question has no options)

### Common traps
- Mistaking a policy's **stated objective** for its **effect** (a policy saying it will reduce burden ≠ the burden fell).
- Treating a "contested empirical fact" as established fact (search first; the controversy itself can be written up as the phenomenon).
- A phenomenon that is too broad ("China's education problem") → narrow it to **one measurable outcome variable** (e.g. "household spending on academic private tutoring").

---

## S2 — Fix the perspective

**Purpose**: fix the **disciplinary perspective** and the **explanation style**. The output of this step sets the stylistic baseline for everything after it.

### Question script (`AskUserQuestion`, two questions at once)

**Question 1: explanation style**
| Option | Meaning | Consequence |
|------|------|------|
| Classic explanation (recommended for beginners) | Use mature theory to give a conventional explanation | Direction of conclusions largely predictable, low risk, low novelty |
| Novel explanation | Emphasize counter-intuitive mechanisms / frontier findings | More striking, but easier for reviewers to challenge; needs stronger argument |
| Both | Do the classic version first, then layer a novel mechanism on top | About 1.5× the work, but often the best route |

**Question 2: disciplinary perspective** (offer 3–4 relevant options based on the phenomenon; do not list all)
Production & consumption / Education / Labour / Industrial organization / Development / Public / Environmental /
Health / Urban & regional / Behavioural / Macro / Finance / International trade / Institutional

> Style ↔ science-question attribute mapping (for reference; from the NSFC four-attribute classification reform):
> - Classic explanation ≈ "demand-driven / breaking bottlenecks" (the problem comes from real demand; solving a known hard problem)
> - Novel explanation ≈ "encouraging exploration / highlighting originality" or "targeting the frontier / taking a distinctive path"
> - Cross-disciplinary borrowing ≈ "convergence across disciplines"

### Action list
1. Read out the user's choices and **restate them for confirmation** (write them into `state.json.decisions`).
2. Load `theory_toolbox.md` and take **3–5 classic foundational works + 2–4 works from the last decade** for that perspective.
3. **Verify each reference online** (authors/year/title/journal/volume-issue-pages), tagging `[VERIFIED]` or `[UNVERIFIED]`.
   ⚠️ Unverified items **must not** enter the body of S2's "must-read list"; they may only sit in a "pending verification" column.
4. Write a "style baseline statement": one sentence on what kind of explanation this model pursues —
   e.g. "This model is a **classic explanation**: it characterizes tutoring demand within the standard consumer utility-maximization framework and introduces no new preference structure."

### Delivery template (`S2_perspective.md`)

```markdown
# S2 Perspective and positioning
## 1. User choices
- Explanation style: classic / novel / both
- Disciplinary perspective:
- Style baseline statement (one sentence):
## 2. The core analytical framework of this field
(2–4 paragraphs: what this perspective usually cares about, the standard modeling recipe, the variables commonly used)
## 3. Classic foundational literature (all verified)
| Reference | Contribution | Relation to this phenomenon | Verification |
## 4. Frontier work of the last decade (all verified)
| Reference | What is new | Relation to this phenomenon | Verification |
## 5. Where this model stands (one sentence)
## 6. Pending-verification references (must not enter the paper's reference list)
```

### Self-check
- [ ] The style (classic/novel) was confirmed by the **user**, not chosen by the model
- [ ] Both classic and frontier references are present, and **each carries a verification tag and a source**
- [ ] The "style baseline statement" is written, and all later steps align to it

### Common traps
- Choosing "novel explanation" but still using the most standard setup → the label does not match the content; S8 will dock the originality score.
- Giving references by title only, or citing something that looks authoritative but cannot be retrieved (**verify first**).
- A perspective spanning too many fields (education *and* finance *and* environment) → narrow to 1–2.

---

## S3 — Core assumptions

**Purpose**: make the premises **explicit and normalized**, add the assumptions that make the model more rigorous, and finally lock in one leading theory.

### Question script (two rounds, which can be merged into one message)

**Round 1: normalize the existing assumptions** (the model drafts these; the user confirms)
Rewrite the user's colloquial premises into standard form, giving the "mathematical content" of each:

| User's original wording | Normalized assumption | Mathematical content |
|------|------|------|
| "Parents all want their kids in a good school" | A1 Households have monotone preferences over school quality | $u = u(c, q)$, $\partial u/\partial q > 0$ |
| "The tutor said the price will not go up" | A2 The supply price is exogenous and constant | $p$ is a constant, $p_{t+1}=p_t$ |

**Round 2: propose additional assumptions** (`AskUserQuestion`, 2–4 candidates, multi-select allowed)
For each, state "what becomes rigorous if we add it" and "what hole is left if we don't". For example:

- Candidate A: **Complete information** (parents know the true quality) → without it, signalling/reputation must be introduced and the model gets complicated
- Candidate B: **Binding budget constraint** (income $y$ is finite; education spending crowds out other consumption) → without it, demand is unbounded and the result is meaningless
- Candidate C: **Market clearing with flexible prices** → without it, only partial equilibrium is possible
- Candidate D: **Homogeneous agents** (do a representative agent first; leave heterogeneity to S7) → without it, distributional assumptions plus numerical solution are needed

### Action list
1. Number the assumptions **A1, A2, …** (every later step cites the same numbers and must not change their meaning).
2. For each assumption, annotate: **type** (preference / technology / information / market structure / institutional constraint) + **testability** (testable / partly testable / not testable) + **basis**.
3. Lock in **one leading economic theory** (user-confirmed, or give a default and mark it changeable):
   utility maximization / profit maximization / cost minimization / principal–agent / signalling game / search and matching / oligopoly competition /
   externalities and public goods / intra-household bargaining / Ramsey optimal taxation / dynamic optimization (Bellman) / heterogeneous agents.
4. **Consistency scan**: assumptions must not conflict. Build a "conflict matrix" marking what breaks if each is violated.
5. If an assumption the user proposes would make the model unsolvable, **say so explicitly** and offer a solvable substitute (this is one of the skill's core services).

### Delivery template (`S3_assumptions.md`)

```markdown
# S3 Core assumptions
## 1. Leading theory
## 2. Assumption list
| # | Assumption (normalized) | Mathematical content | Type | Testability | Basis | New/existing |
| A1 | ... | ... | preference | not testable | literature [VERIFIED] | existing |
## 3. Assumption conflict check
| Assumption pair | Conflict? | Consequence if violated | Handling |
## 4. Assumptions dropped and why
## 5. The resulting model skeleton (agents / timing / choice variables / constraints / equilibrium concept)
```

### Self-check
- [ ] Every assumption can be written as a mathematical condition, or has a clear institutional basis
- [ ] No internal conflicts; conflicting items resolved or dropped
- [ ] The user confirmed the added assumptions (the model did not add them unilaterally)
- [ ] Parameters ≤ 5 and endogenous variables ≤ 3 (the parsimony constraint); exceeding it requires justification
- [ ] **Simplicity check (principle 1):** each added assumption *earns its place* — it changes a conclusion or a comparative-static sign. An assumption that only adds notation without moving any result should be dropped; a beautiful model is the smallest one that still carries the mechanism.

### Common traps
- An assumption like "parents are rational", which is not operational → it must be converted into a condition that can be written into a utility function.
- Adding assumptions to be "more realistic" → parameter explosion, S4 cannot solve it, and S8 docks the parsimony score.
- So many assumptions that no equilibrium exists (e.g. complete information + free entry + fixed prices).

---

## S4 — Build and solve the model

**Purpose**: write the model and solve it, with **every equation grounded in the literature or in theory**.

### The four-step method (mandatory SOP for S4)

S4's modeling and solving **must** follow the "four-step method" (full method in `references/four_step_method.md`). Key points:

- **Step 1 Minimize**: impose the **tightest constraining** assumption on each of the four elements — environment / preferences / technology / information — compressing the model to the smallest scale that still yields a closed-form solution and signed comparative statics. ⚠️ Add *constraints* to make the model *smaller* — do **not** "propose many assumptions".
- **Step 2 Classic form**: pair the Step 1 specification with textbook-standard functions (Cobb-Douglas / CES / quasi-linear utility + linear budget + linear/quadratic cost) and a **minimal variable set** (1–2 decision variables + 1 policy/price variable); the mechanism must be "visible at a glance".
- **Step 3 Relax constraints (robustness)**: performed in **S7**. Relax Step 1's assumptions one by one; **keep only the assumptions whose relaxation would flip a core comparative-static sign**; those that change only magnitude may be relaxed as robustness; those irrelevant to the core mechanism are dropped.
- **Step 4 Form & dimension extension (new questions)**: performed in **S7**, layered separately from Step 3 — change functional form (CD→CES for substitution elasticity), add independent variables, add heterogeneity, add dynamics, add general equilibrium, to "tell more of the story" rather than to test the conclusion.

**Criterion**: if Step 1 still cannot yield comparative statics, the constraints are not yet tight enough (not "too few assumptions"). The baseline model must satisfy parsimony (≤5 parameters, ≤3 endogenous variables).

### Action list

1. **Re-check gate** (do this first; do not enter S4 if it fails): are the perspective and assumptions still reasonable? Is S2's style baseline respected?
2. **The four-part model write-up** (this implements **Step 2 Classic form** on top of the **Step 1** minimized setup — see the "The four-step method" subsection above)
   - **Notation table** (before the equations): symbol | meaning | type (parameter/endogenous/exogenous) | range | unit
   - **Environment and timing**: who knows what and does what, when (1–4 steps)
   - **Individual problems**: $\max/\min$ objective + constraints (annotate the basis of each expression)
   - **Equilibrium concept and definition**: e.g. "competitive equilibrium", "Nash equilibrium (pure strategy)", "subgame perfect", "constrained optimum"
3. **Symbolic solution**: prefer an analytical solution. Use `scripts/econ_solve.py` (tool usage in `modeling_cookbook.md`):
   - First-order conditions and closed form: `econ_solve.py foc --spec spec.json`
   - Comparative statics (implicit function theorem): `econ_solve.py cs --spec spec.json`
   - Notation check: `econ_solve.py lint --spec spec.json`
4. **Interior vs corner**: does the solution lie inside the feasible region? Any corner solution must be discussed separately (S5 checks this).
5. **Second-order conditions**: verify max/min (Hessian negative/positive definite, or $f''<0$ in one variable). **Never skip this.**
6. **Numerical sampling check**: draw 3–5 parameter sets at random, substitute the closed form back into the constraints and FOCs; the error should be < 1e-9.
   (`econ_solve.py foc --verify` does this.)
7. **Degradation strategy** (when solving fails, try in order and tell the user which one was used):
   ① simplify the functional form (log → linear, general CES → Cobb-Douglas)
   ② a two-agent, two-period version
   ③ local linearization (first-order expansion at the steady state / symmetric point)
   ④ parameter restriction (e.g. set $\alpha=\frac12$) to make it solvable
   ⑤ give up the closed form → report only a numerical illustration + local comparative statics, and **flag this prominently**
8. **Turn results into propositions**: write each result as a Proposition with "proof/derivation notes" and "one sentence of economic meaning".
   Include only **non-trivial** results; **do not** dress up identities or first-order conditions as propositions.

### Delivery template (`S4_model.md`)

```markdown
# S4 Model construction and solution
## 0. Re-check (perspective/assumptions/style)
## 1. Notation table
## 1.5 Four-step method log (Step 1 Minimize → Step 2 Classic form)
| Step | What this model does | Criterion met? |
|------|----------------------|----------------|
| Step 1 Minimize | Tightest constraining assumptions listed (one each for environment/preferences/technology/information) | Closed form + signed comparative statics obtained |
| Step 2 Classic form | Standard functions and minimal variable set chosen | Mechanism visible at a glance |
| (Step 3 / 4 → see S7) | — | — |
## 2. Environment and timing
## 3. Individual optimization problems (basis per equation)
| Eq. | Formula | Basis |
| (1) | max_{x} U(x) = ... | standard utility maximization, see [VERIFIED] reference |
## 4. Equilibrium definition
## 5. Solution
### 5.1 First-order conditions
### 5.2 Closed-form solution
### 5.3 Second-order conditions
### 5.4 Interior/corner discussion
### 5.5 Numerical verification (script command and output summary)
## 6. Propositions
**Proposition 1** (...). *Proof/derivation notes*: … *Economic meaning*: …
## 7. Solution tooling and reproducibility (script path, parameters, log)
## 8. Unresolved technical issues (disclosed honestly)
```

### Self-check
- [ ] The notation table is complete; each symbol has exactly one meaning
- [ ] Every equation has a stated basis (literature / textbook / own construction + label)
- [ ] Second-order conditions checked; corner solutions discussed or ruled out
- [ ] The closed form is verified by numerical back-substitution (state the order of magnitude of the error)
- [ ] Propositions are separated from identities; 2–4 propositions
- [ ] Any degradation was disclosed explicitly in `## 8` and in the reply to the user

### Common traps
- Treating "the sign of the comparative static" as the conclusion without stating the parameter region where it holds (**always give the region**).
- Deriving FOCs and then claiming a unique equilibrium exists (second-order conditions and an existence argument are still needed).
- Trying to brute-force a general functional form → getting stuck; instead retreat to a solvable form first.
- Writing a numerical result as "we prove".

---

## S5 — Checks

**Purpose**: guarantee **correctness** and **academic acceptability**. This step adds nothing new; it only finds faults.

### Five hard checks (write a conclusion per item, not just "no problems")

| Check | How | Typical problems |
|------|---------|---------|
| **① Notation convention** | Against the notation table in `modeling_cookbook.md`: Greek letters for parameters, Roman letters for variables; subscripts used consistently; no $l$ (confusable with 1); no $e$ for anything but Euler's number | Parameters and variables sharing a letter; one letter meaning different things in different equations |
| **② Consistency** | Build a table of all symbols; check that each definition is unique, that assumption numbers are cited consistently, and that every symbol in the propositions appears in the notation table | A2's meaning silently changed in S4; a proposition citing an undefined symbol |
| **③ Correctness of the solution** | (a) substitute the closed form back into the FOCs (error < 1e-9); (b) re-check second-order conditions; (c) compare against 3–5 random numerical draws; (d) degenerate cases (special parameter values) — does it reduce to a known result? | A dropped term, a wrong derivative, writing $d/dx$ where $\partial/\partial x$ is meant |
| **④ Boundaries and corners** | Check the solution's feasibility across parameter regions; find the critical parameters where the interior solution fails | Negative prices, negative quantities, probabilities > 1 |
| **⑤ Dimensions and ranges** | Both sides of each equation have the same dimensions; parameter ranges are compatible with their economic meaning (e.g. $0<\beta<1$) | A probability parameter left unconstrained; elasticity confused with a level |

### Action list
1. Produce `S5_checks.md`, giving **conclusion + evidence** per item (which equation, which parameter, which command's output).
2. **If an error is found**: report it to the user → propose a fix (which equation changes, which propositions are affected) → **wait for the user's confirmation, or fix it and write back to S3/S4**.
   ⚠️ Never "quietly change a number" to make things look better.
3. **If the issue is local** (a typo, an algebraic slip that changes no direction of any conclusion): fix it directly, write back to the upstream file, and log the fix in `S5`.
4. **If the issue is substantive** (a sign is overturned, a proposition fails): stop per the gate protocol and tell the user, offering:
   ① go back to S3 and change an assumption ② go back to S4 and change the setup ③ weaken the proposition ④ accept it as a "boundary condition" and disclose it.
5. **Pre-delivery audit (gate G7).** Before you close S5, run `scripts/audit_model.py --lint spec_lint.json --solver <solver specs> --scan <deliverables> --claims <report>` and confirm **0 FAIL**. A non-zero FAIL means a defect class that has actually occurred in practice (a value outside its domain, one symbol with two values, Markdown left inside LaTeX, an over-claimed review); treat it like any other check failure — fix, write back, do not proceed to S6.

### Delivery template (`S5_checks.md`)

```markdown
# S5 Check report
## 1. Summary of conclusions
| Check | Conclusion | Severity |
| ① Notation | pass / N issues | low/medium/high |
## 2. Detail per item (problem → location → fix → impact)
## 3. Fix log (including upstream files written back to)
## 4. Failed items and disposition (user-confirmed)
## 5. Verdict: proceed to S6 / return to S3 / return to S4
```

### Self-check
- [ ] All five checks carry **concrete evidence**, not "no problems found"
- [ ] All fixes were written back to the upstream files (S3/S4) — not only into S5
- [ ] The disposition of substantive issues was confirmed by the user

### Common traps
- Checking your own work: the check must **re-derive independently** (ignore S4's steps; re-derive from the assumptions and then compare).
- Checking only the algebra and not the economics (e.g. a negative price elasticity read as "demand rises with price").

---

## S6 — Form the report

**Purpose**: explain the model clearly and deliver it to the user (it is also the raw material for S9).

### Action list
1. Copy `assets/model_report_template.md` and fill it in section by section.
2. Required content: research question (phenomenon → question) / assumptions (with bases) / parameter table (symbol, meaning, value, source, calibrated or not) /
   model setup / propositions (with derivation notes) / solution / **economic interpretation** (one plain paragraph per proposition plus its real-world meaning) / limitations.
   The interpretation must include, for each proposition, **one line a manager, policymaker or reader could act on or cite** — the model exists to produce a communicable principle, not just a solved system.
3. **Classify every parameter source**: `calibrated from literature` / `estimated` / `illustrative value`. Illustrative values must be labelled explicitly.
4. Wording discipline (per Global Rule 4): for analytical results say "the proposition gives…"; for numerical results say "computed at parameter values $X$…".
5. **Practical-relevance check (principle 3).** Before S6 is "done", state in one sentence what a real decision-maker should take away, and confirm the model is answering a *real* question rather than exercising the solver. If the takeaway is only "the math works", the model is under-specified — revisit S1/S2.
6. If plotting is available locally, use `econ_solve.py sim` to produce 1–2 mechanism figures for the body; put the rest in S7.

### Delivery template
See `assets/model_report_template.md` (8 sections: abstract / research question / assumptions / parameters / model / propositions and results / economic interpretation / limitations and boundaries).

### Self-check
- [ ] No undefined symbol anywhere in the report
- [ ] Every parameter has a source and a value
- [ ] Every proposition has "one sentence of economic meaning"
- [ ] The limitations section has at least 3 items (writing no limitations is unprofessional)

---

## S7 — Extend

**Purpose**: move the model from "it runs" to "it holds up". Complete all 4 of the following.

### Action list (in order)

1. **Symbolic comparative statics**: for each key parameter derive $\partial x^*/\partial \theta$, giving the **sign and the parameter region where it holds**.
   Compute with `econ_solve.py cs`, and help simplification by declaring sign assumptions (e.g. `positive=True`).
   Organize the output as a table: parameter | endogenous variable | expected sign | conditions | economic meaning.
2. **Numerical sensitivity**: one-parameter sweeps (one figure with several curves) + at least one two-parameter heat map or contour plot.
   Command: `econ_solve.py sim --spec spec_sim.json` (writes PNG + optional PDF into `figs/`).
3. **Relax an assumption** (**at least 1 is mandatory**): pick the "hardest" assumption from the S3 list (usually homogeneity, complete information, exogenous price,
   a non-binding budget) and relax it to see which propositions change sign. Write a "robustness table": conclusion | under the original assumption | after relaxing | robust?
4. **Heterogeneity** (if applicable): replace the representative agent with 2–3 types (high/middle/low income; high/low ability) and
   check whether the **direction of between-group differences** matches the phenomenon. 2–3 groups suffice; do not use a continuous distribution (unless genuinely necessary).
5. **Counterfactual / institutional comparison** (optional, adds a lot): with policy vs without, tax vs subsidy, closed vs open — compare welfare.

### Delivery template (`S7_extension.md`)

```markdown
# S7 Extension
## 1. Comparative statics master table
## 2. Numerical sensitivity (with figure paths and parameter ranges)
## 3. Robustness: relaxing assumptions
| Proposition | Sign under original setup | Sign after relaxing | Robust? | Note |
## 4. Heterogeneity analysis
## 5. Counterfactual/policy comparison (optional)
## 6. Conclusions overturned or weakened (disclosed honestly)
## 7. What could be done next but is not done here (left to the reader / future research)
```

### Self-check
- [ ] Every comparative static carries **conditions**, not an unconditional claim
- [ ] At least 1 assumption relaxed, with weakened conclusions reported faithfully
- [ ] Every figure has: axis labels (with units), parameter values, and a figure-type label (numerical illustration / parameter sweep / mechanism sketch)
- [ ] Figures exported as both PNG and PDF (PDF for the paper)

### Common traps
- A sensitivity analysis that moves one parameter by 5% and shows nothing → the sweep range must cover the critical point where the conclusion flips.
- The conclusion flips after relaxing an assumption but this is not reported → violates Global Rule 4.
- Writing a "numerical illustration" into a proposition as "a general conclusion".

---

## S8 — Expert review

**Purpose**: let the user know **what standard this model actually reaches professionally**, to prevent false beliefs. **Do not** turn this into "universal praise".

### Action list
1. Load `references/review_rubric.md` and score using its **5 reviewer roles × 6 dimensions**.
2. **Round one: independent scoring.** Each of the 5 reviewers gives 6 dimension scores (0–5), a total, and **their single most damaging criticism**;
   every reviewer must attach "evidence citations" to their scores — citing specific equation numbers / assumption numbers / paragraphs. **Vague scoring is prohibited.**
3. **Round two: cross-examination.** Circulate the 5 score sheets, let each reviewer revise 1–2 of their own dimensions with reasons;
   record the before/after difference — this is the core data for the disagreement diagnosis.
4. Aggregate with `scripts/review_score.py`:
   - mean/sd per dimension, weighted total (per reviewer), overall score (mean + median + trimmed mean)
   - **disagreement index** = (max − min)/mean, and the inter-reviewer agreement coefficient (Fleiss κ, interpreted via Landis & Koch 1977)
   - the band conclusion and a submission recommendation
5. Output the **"what you must not claim" list** — the single most important deliverable of this step:
   e.g. "must not claim this model explains the national effect of the burden-reduction policy", "must not claim it has passed peer review", "numerical results are not robustness evidence".

### Delivery template (`S8_review.md`)

```markdown
# S8 Expert review
## 0. Object under review (file list + one-sentence model)
## 1. Round one: independent scoring
### Reviewer R1 | Theoretical consistency
| Dimension | Score (0-5) | Evidence (equation/assumption number) |
……(R1–R5)
## 2. Round two: cross-examination and revision
| Reviewer | Dimension | Old score | Revised | Reason |
## 3. Aggregation
| Dimension | Weight | Mean | SD |
Total: X.X/100 (mean / median / trimmed mean)
Disagreement index: 0.XX  |  Fleiss κ = 0.XX (agreement: moderate/substantial…)
## 4. Band and positioning
(A/B/C/D/F —— see the banding table in review_rubric.md)
## 5. The five most damaging criticisms (one per reviewer)
## 6. Revision priority list (P0/P1/P2)
## 7. The "what you must not claim" list
```

### Self-check
- [ ] The 5 reviewers score **independently**, not one person repeated five times (different roles, attentive to different defects)
- [ ] Every score has a concrete evidence citation
- [ ] **Disagreement** is reported; the mean is not used to mask it
- [ ] A band conclusion plus a "must not claim" list are present
- [ ] It is stated explicitly that this is a simulated review, not real peer review

### Common traps
- All scores landing in 3–4 (no discrimination) → force separation: make R5, the adversarial reviewer, strict.
- Reporting only the total and not the disagreement → defeats the purpose of this step.
- Writing the simulated review up as "has passed expert review".
- A dimension with range ≥ 2 while every reviewer sounds reasonable → check whether they are scoring **different
  sub-questions** of that dimension (D3: grounding vs. closure; D5: falsifiability vs. welfare criterion — see
  `review_rubric.md` §3). Record the split; do not average two different questions into one number.
- Round two coming out **net higher** than round one → this is the expected direction when the author also plays
  the reviewers. Report **both** rounds and set the final position at the **boundary between the two bands**
  (e.g. "lower edge of B, crossing the B/C line") rather than adopting the higher round; disclose the net change
  in the limitations section. If the second round does not move the band at all, say so — that is the reliability
  evidence for the band.

> **If the model is changed after this step, S8.1 is mandatory** (see below): the scores here describe the model as it stood when it was scored, and a revision makes them stale.

---

## S8.1 — Re-review after revision

**Purpose**: a revision makes the S8 verdict **stale**. S8.1 exists so that "we fixed the P0 items" is never asserted without evidence, and so that a fix does not hide a newly introduced defect.

**Trigger (mandatory)**: any change to the model after S8 has been scored —
- fixing S8's P0/P1 items;
- a request to raise the model to a target level ("make it publishable", "reach the standard of a thesis theory section");
- a new proposition, a recalibration, a corrected formula, or a changed notation that alters a number.

**Exemption (must be stated explicitly)**: a purely cosmetic change (typo, formatting, reordering) that provably cannot move any of the six dimensions. Say so and name the change; do not silently skip S8.1.

### Action list
1. **Freeze the version.** Copy the S8-scored files or record their hashes, so the "before" state is auditable.
2. **Reuse the identical instrument**: same 5 reviewer roles, same 6 dimensions, same weights, same bands (`references/review_rubric.md`). A different rubric makes the delta meaningless.
3. **Re-score the revised version**, keeping every score bound to a location. Reuse the previous spec file as the template so the comparison is like-for-like.
4. **Report the delta in two tables**:
   - per reviewer: old total → new total → change;
   - per dimension: old mean → new mean → change, with a one-line reason for each move (e.g. "D5 +0.6: the identification identity now converts an unobservable parameter into an observable one").
5. **Run the regression check** (this is the part unique to S8.1):
   - Does the revision **contradict** anything already written in `S4`–`S7`? Grep the old files for the numbers and statements the revision changed.
   - Are there **stale numbers** left in earlier deliverables? Old figures, old tables, old abstracts are the usual culprits.
   - Did the revision **introduce** a new defect? Look specifically at the dimension that was *not* the target of the fix (fixes tend to be local; damage tends to be elsewhere).
6. **State whether the intended target was reached**, with the band as the evidence — and if the target was expressed qualitatively ("publishable in a management journal"), translate it into the rubric's band language and say plainly whether it was met.
7. **Update the downstream artifacts**: `state.json` (completed steps, headline results), the file index, and the "what you must not claim" list if the revision changed what may be claimed.

### Delivery template (`S8.1_review_after_revision.md`)

```markdown
# S8.1 Re-review after revision
## 0. What changed since S8 (file-by-file, one line each) + verification evidence
## 1. Scores: revised version (same 5 roles × 6 dimensions)
## 2. Delta table (per reviewer, per dimension, with the reason for each move)
## 3. Aggregation (mean/median/trimmed mean, band, kappa) — old vs new
## 4. Regression check
   - contradictions with S4–S7:
   - stale numbers in earlier deliverables:
   - new defects introduced:
## 5. Did the revision reach the target level? (band as evidence)
## 6. What may now be claimed / what still may not
```

### Self-check
- [ ] Same roles, dimensions, weights and bands as the original S8
- [ ] Every score still carries a location reference
- [ ] The delta is reported for **every** dimension, including those that did not move
- [ ] At least one item in the regression check was actually executed (grep / re-run), not merely asserted
- [ ] "Target reached" is stated with a band, not with an adjective
- [ ] `state.json` and the file index are updated

### Common traps
- Re-scoring with a *softer* rubric after a revision → the delta is meaningless. Reuse the original spec file.
- Reporting only the dimensions that improved → report all six; a dimension that fell is the most informative line in the table.
- Calling a revision "done" because the script ran → S8.1 is about the **model**, not about the script exiting 0.
- Fixing the weakest dimension and thereby inflating the total → check that the new total is consistent with the per-dimension moves (weighted sum), not just with the narrative.
- Letting S9 start on the pre-revision text → after S8.1, the numbered deliverables must reflect the revised model, or the paper will cite retracted numbers.

---

## S9 — Write-up (short paper / working paper)

**Purpose**: integrate the first 8 steps into a readable short paper, compiled by LaTeX to PDF.

### Action list
1. Load `references/paper_template.md` and use its LaTeX skeleton.
2. Paper structure (fixed seven sections + appendix):
   ① phenomenon and background → ② distilling the economic question → ③ assumptions → ④ model construction →
   ⑤ solution and results (including comparative statics) → ⑥ interpretation (including policy implications and limitations) → references; the appendix holds full derivations and robustness.
3. **Present results in the body mainly with figures and compact tables; put detailed results (derivations, signs for all parameter variations, numerical tables) in the appendix.**
4. **Reference gate**: only `[VERIFIED]` references may enter `thebibliography`; delete anything unverified,
   and produce `S9_references_check.md` recording each entry's verification source or the reason for exclusion.
5. **Wording gate**: check the whole text for "we prove" describing a numerical result, "generally" describing a finite grid, "robust" describing a single point.
6. **Audit gate (G7) before you finalize.** Run `scripts/audit_model.py` over the symbol table, the solver specs and the deliverables; the paper must reach **0 FAIL** (Markdown-in-LaTeX, dangling `\ref`, an over-claimed review, and a `must not claim` section are all checked here). Do not call the paper "done" until it is clean.
7. Compile: `pdflatex -interaction=nonstopmode S9_paper.tex` twice (for cross-references);
   check the `.log` for lines starting with `!`; on success confirm the PDF exists.
7. If no pdflatex is available: output the `.tex` plus `README_compile.md`, and **never fabricate a PDF**.
8. Use `present_files` to show the PDF/`.tex` and the key figures.

### Delivery template
See `references/paper_template.md` (full preamble, theorem environments, figure/table conventions, pre-submission checklist).

### Self-check
- [ ] All seven sections present, each with substantive content (not just headings)
- [ ] All references `[VERIFIED]`
- [ ] Numerical conclusions are labelled by type in the body (numerical illustration / computational sketch)
- [ ] A limitations section exists and is specific
- [ ] The PDF really compiles (not empty and not erroring)

### Common traps
- Pasting the S6 report straight into the paper (a report may be colloquial; a paper may not).
- A summary containing strong causal claims that were never proved.
- Figures without axis units; tables without a note on where parameter values come from.

---

## Appendix: the "user-interaction map" for the whole workflow

| Step | Must interact with the user? | Form of interaction | Decisions the user makes |
|------|------------------|---------|--------------|
| S1 | Yes | Restate for confirmation + clarify | Is the phenomenon described accurately |
| S2 | **Yes (key decision point)** | `AskUserQuestion` ×2 | Classic/novel + disciplinary perspective |
| S3 | **Yes (key decision point)** | `AskUserQuestion` | Select additional assumptions + confirm the leading theory |
| S4 | Conditional | Only if solving fails or degradation is needed | Whether to accept the simplification |
| S5 | Conditional | Only when a substantive error is found | Change assumptions / change setup / weaken propositions |
| S6 | No | Deliver directly | — |
| S7 | No (optional confirmation) | Deliver + ask whether to go deeper | Whether to continue |
| S8 | No | Deliver directly | — |
| S9 | Conditional | Confirm paper language/length/whether to compile a PDF | Form of delivery |
