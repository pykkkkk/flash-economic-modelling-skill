# Expert review rubric (review_rubric.md)

> **When to use**: S8 only. The "aggregation" at the end of this file is done automatically by `scripts/review_score.py`.
>
> ⚠️ **Nature of this instrument (must accompany every output)**: this is a **simulated** review, a structured self-assessment of the model's own quality.
> It is **not** real peer review. It must not be used to claim "this has passed expert review" or "this reaches journal standard".
> Its only purpose is to let the user form an **undistorted** view of the model's real standard.

---

## 1. Why use 3–5 reviewers plus a rubric

Real peer review contains three mechanisms worth making explicit:

| Mechanism | What happens in practice | How this rubric implements it |
|------|------------|------------|
| **Multiple independent reviewers** | Journals usually send to 2–3 referees; AER-type journals send to 2+ and then the handling editor decides | 5 reviewers with different roles, **blind to each other in round one** |
| **Structured evaluation dimensions** | Journals have explicit review criteria (e.g. *American Journal of Agricultural Economics*: Contribution / Scholarship / Appeal / Originality / Analysis / Illustrations & Length) | 6 weighted dimensions (see §3), each with 0–5 behavioural anchors |
| **Banded decisions, not continuous impressions** | Journals use Reject / Weak R&R / Strong R&R / Accept | 5 bands (A–F), which avoids the "everyone scores 3.5" pile-up |

**Why multiple roles?** A single viewpoint self-assesses with a systematic tilt toward "the dimensions I care about".
Different emphases (theoretical consistency / technique / realism / policy / adversarial) expose defects in different places.

**Why test agreement?** If 5 reviewers give wildly different scores on the same dimension, that dimension's **standard is unclear or the defect is contested** —
which is itself important information and **must not be averaged away**. Interpretation follows
Landis & Koch (1977) for κ bands; for a more conservative reading see Krippendorff's thresholds (κ<0.67 → discount the conclusion; 0.67–0.80 → only tentative conclusions; >0.80 → conclusions may be stated).

---

## 2. The five reviewer roles

| Role | What it attends to | Typical challenge | The most likely reason it gives a low score |
|------|---------|---------|-------------------|
| **R1 Theoretical consistency** | Is the **logical chain** assumptions → optimization → equilibrium → propositions complete and closed? | "Which assumption does this proposition follow from?" "Was A2 ever used?" | Propositions disconnected from assumptions; a key assumption cited but not used in any derivation |
| **R2 Mathematical technique** | Correctness of derivations, second-order conditions, interior/corner cases, the **conditions** under which comparative statics hold | "Were second-order conditions checked?" "Over what parameter range does this sign hold?" | Missing SOC; comparative statics with no conditions; corner solutions never discussed |
| **R3 Empirical/realism fit** | Can the mechanism be mapped to **observable quantities**; can it be falsified by data? | "Which variable is observable?" "What data would overturn this prediction?" | Core variables unobservable; the prediction conflicts with no conceivable data (unfalsifiable) |
| **R4 Policy and welfare** | Normative implications; is the welfare criterion stated; limits to external validity | "Better by what welfare standard?" "How far can this be extrapolated?" | Welfare judgement with no criterion; a local result presented as general policy advice |
| **R5 Adversarial** | Can a **simpler explanation** replace it? What if the assumptions are violated? Is it just restating the phenomenon? | "What does this say beyond a one-line intuition?" "Flip the assumption — does the conclusion change?" | Tautology; conclusion = assumption; no new testable implication |

**R5 must be executed strictly.** It exists to stop the leniency of the first four reviewers from inflating the score.
Its task is not to reject but to **find the cheapest alternative explanation**.

---

## 3. The six weighted dimensions

**Sources** (cite these when writing the report):
- The six *AJAE* refereeing criteria (Contribution / Scholarship / Appeal / Originality / Analysis / Illustrations & Length)
- Whetten (1989) four elements of a theoretical contribution (What / How / Why / Who–Where–When)
- Sutton & Staw (1995) "what theory is not" (citations, data, lists and variable names are not theory)
- Corley & Gioia (2011) two-dimensional view of theoretical contribution (originality × usefulness)
- Ellison (2002) the $q$–$r$ framework ($q$ = importance of the idea, $r$ = craftsmanship)
- The NSFC's four science-question attributes (used for the positioning judgement in D1)

| Dimension | Weight | Source | 5 (best practice) | 3 (basically adequate) | 1 (serious defect) |
|------|-----|---------|---------------|---------------|---------------|
| **D1 Question and positioning** | 15 | AJAE *Contribution/Appeal*; Whetten *Why* | Question is clear, substantively important, and precisely matched to a gap in the literature | Question is clear but the importance argument is ordinary | Question is vague or purely fictional |
| **D2 Originality** | 20 | AJAE *Originality*; Corley & Gioia; NSFC attributes | A counter-intuitive mechanism or a genuinely new combination, with an explicit statement of what is new | A new application of a classic framework | Merely restating an existing model |
| **D3 Assumptions and logical rigour** | 20 | Whetten *What/How*; Sutton & Staw | Assumptions explicit, mutually consistent, all grounded, logical chain closed | Main assumptions grounded, a few left undeveloped | Assumptions implicit or conflicting, or conclusion = assumption |
| **D4 Technical correctness** | 20 | AJAE *Analysis/Scholarship*; Ellison's $r$ | Derivations correct, SOCs verified, closed form obtained or degradation explicitly stated | Derivations correct but boundary discussion thin | Derivations wrong or the solution does not hold |
| **D5 Explanatory power and testability** | 15 | AJAE *Analysis*; Manski-style falsifiability | Observable implications and explicit falsification conditions are given | Qualitative interpretation but no clear testing design | Cannot be mapped to any observable data |
| **D6 Exposition and parsimony** | 10 | AJAE *Illustrations & Length*; Ellison's $r$ | ≤5 parameters, ≤3 variables, notation conventional, figures and tables clear | Slightly over-complex but readable | Chaotic notation or excessive clutter |

> **Sub-questions inside one dimension** (added after a real review, 2026-09-19). Two dimensions bundle two
> distinct questions. Reviewers who answer *different* ones produce a large range that looks like a standards
> dispute but is really a question mismatch:
> - **D3** = (a) *grounding* — is each assumption explicit, grounded and mutually consistent? (b) *closure* —
>   is there enough distance between assumptions and conclusions (no "conclusion = assumption")?
> - **D5** = (a) *falsifiability* — can the mechanism be mapped to observables and overturned by data?
>   (b) *welfare criterion* — for a policy paper, is a welfare standard stated?
>
> So when a dimension's range is ≥ 2, **first check whether the reviewers were scoring different sub-questions**.
> If they were, record the split explicitly (which sub-question each side scored, and which you adopt) instead of
> reporting one averaged number as if it were a single contested question.

**Weighted total (out of 100)**
$$\text{Score}=100\times\sum_{d=1}^{6} w_d\cdot\frac{s_d}{5},\qquad \sum w_d = 1$$

**Score anchors (0–5; force discrimination)**

| Score | Meaning |
|----|------|
| 5 | Best practice for this dimension (top-tier among published work) |
| 4 | Clearly adequate, only negligible problems |
| 3 | Basically adequate but with clear room for improvement |
| 2 | A definite defect that must be corrected before proceeding |
| 1 | A serious defect undermining the validity of the conclusions |
| 0 | Entirely missing or entirely wrong |

> **Anti-clustering rule**: if a reviewer scores all 6 dimensions within [3,4], they must re-score and identify at least one
> concrete piece of evidence for a score "below 3" or "equal to 5". **All 3s and 4s is equivalent to giving no assessment.**

---

## 4. The two-round procedure

### Round one: independent scoring (**no communication**)

Each reviewer outputs:
1. Scores on the 6 dimensions (0–5)
2. The weighted total
3. **Their single most damaging criticism** (must cite a specific location: equation number / assumption number / proposition number)
4. A one-sentence overall verdict

**Format**
```markdown
### R2 Mathematical technique — round one
| Dimension | Score | Evidence (location reference) |
| D1 | 4 | Phenomenon and model clearly matched, see S1 §2 evidence table |
| D4 | 2 | The comparative static in Proposition 2 has no conditions, see equation (7) in S4 |
Weighted total: XX.X / 100
Most damaging criticism: the sign in Proposition 2 holds only when a>c, and the model never states that region (S4 §6).
Overall: the technical route is right, but boundary conditions are under-discussed.
```

### Round two: cross-examination and revision

1. Circulate the 5 score sheets among each other (mimicking a journal's "multiple reports")
2. Each reviewer may revise **at most 2 dimensions**, and must state the reason ("having read R1's point that A2 is unused, I lower D3")
3. Record the before/after differences — this is the core data for the **disagreement diagnosis**
4. If the 5 reviewers disagree strongly on a dimension (range ≥ 3), discuss it separately and mark that dimension "standard unclear or defect contested"

---

## 5. Aggregation and banding

Aggregation is done by `scripts/review_score.py`, which outputs:

| Output | Meaning |
|-------|------|
| Mean ± SD per dimension | The degree of consensus on each dimension |
| Weighted total per reviewer | How lenient or strict each reviewer is |
| Overall score | **Mean / median / trimmed mean (drop the highest and lowest)** — report all three |
| Disagreement index | $(\max-\min)/\text{mean}$; if > 0.25 the source of disagreement must be explained |
| Cross-reviewer agreement | Fleiss $\kappa$ (6 dimensions × 5 reviewers, 6 categories) |
| Band | A–F (table below) |
| Decision recommendation | Accept / Strong R&R / Weak R&R / Reject (borrowed from the AJAE four-way scheme) |

**Interpreting agreement** (Landis & Koch 1977)

| $\kappa$ | Reading | How this rubric handles it |
|----------|------|------------|
| < 0.00 | Poor | Report "reviewer standards have not converged"; look only at disagreement, not at the mean |
| 0.00–0.20 | Slight | As above |
| 0.21–0.40 | Fair | Report the mean but flag prominently that "consensus is weak" |
| 0.41–0.60 | Moderate | Report normally, with the disputed items attached |
| 0.61–0.80 | Substantial | Report normally |
| 0.81–1.00 | Almost perfect | Report normally; consensus may be emphasized |

> Additional note: under Krippendorff's more conservative thresholds, conclusions should be discounted when $\kappa<0.67$, and only tentative conclusions are allowed in the range $0.67$–$0.80$.

> **Small-sample caution**: this rubric has only **6 rated dimensions**, so κ is unstable in small samples (it is also sensitive to whether scores cluster in a few categories).
> Treat κ as a **rough indication of agreement** only, not as a statistical test result; to judge disagreement, prioritize
> "dimensions with range ≥ 2" and the disagreement index $(\max-\min)/\text{mean}$.

**Banding criteria**

| Band | Score | Meaning | How the user should use it |
|------|------|------|--------------|
| **A** | 85–100 | At the standard of a submittable working paper: the mechanism has an articulable marginal contribution | Can serve as a working paper; real peer review is still needed |
| **B** | 70–84 | **Adequate**: internally coherent, conclusions correct, with testable implications, but limited originality | A thesis chapter / a strong course paper; strengthen D2 before submitting |
| **C** | 55–69 | Near the pass line: usable as a proposal or coursework, with 1–2 structural weaknesses | Strengthen via S7 before writing it up |
| **D** | 40–54 | A structural defect (insufficient assumptions / problems in the solution / untestable) | Go back to S3/S4 and rebuild |
| **E** | 25–39 | The model basically does not hold but the direction is salvageable | Go back to S1/S2 and re-position |
| **F** | 0–24 | Internally contradictory, unsolvable with no valid degradation, or merely restating the phenomenon | Start over |

**The four-way decision mapping (matching the table above)**: A → *Accept / Strong R&R*; B → *Strong R&R*;
C → *Weak R&R*; D and below → *Reject*.

---

## 6. The five mandatory outputs

Whatever the scores, the S8 output **must** contain these five items:

1. **Overall score and band** (with all three of mean/median/trimmed mean)
2. **Agreement diagnosis** (Fleiss κ with its reading; if consensus is weak, say so explicitly)
3. **Each reviewer's single most damaging criticism** (5 items, each citing a specific location)
4. **Revision priority list**: P0 (conclusions do not hold unless fixed) / P1 (affects persuasiveness) / P2 (polish)
5. **The "what you must not claim" list** — the most important deliverable of this step

### The "what you must not claim" template

```markdown
## What you must not claim
- ❌ Do not claim the model "explains" the <outcome> of <phenomenon> — the model offers only a **possible** mechanism,
     with no estimation or testing of any kind (no data, no identification).
- ❌ Do not claim the conclusions hold "in general" — Proposition X holds only within <parameter region>.
- ❌ Do not claim the numerical result is "robust" — it is one numerical illustration at <parameter values>.
- ❌ Do not claim "this has passed expert review" — this report is a simulated review, not peer review.
- ❌ Do not claim the policy recommendation is ready for implementation — the welfare judgement relies on <welfare criterion> and ignores <omitted general-equilibrium effects>.
- ✅ You may say: the model shows that "if <assumption> holds, then <mechanism> leads to <directional result>",
     and it yields the empirically testable implication <specific implication>.
```

---

## 7. Objectivity mechanisms (so scoring does not become self-praise)

| Mechanism | How |
|------|------|
| **Independent scoring** | Round one's 5 sheets are mutually invisible (when generating them, **do not** produce all 5 at once and let them see each other) |
| **Evidence binding** | Every score must cite a specific location (equation / assumption / proposition number); a score without a citation is void |
| **Anchor reference** | Behavioural descriptions for 0–5 are provided (§3), to avoid "I feel like a 3.5" |
| **Mandatory low score** | Each reviewer must identify at least one sub-standard item; R5 must supply an alternative explanation |
| **Refuse averaging** | Report min/max/range; dimensions with range ≥ 3 get separate discussion |
| **Keep the right to fail** | D/F bands are allowed; never inflate scores to "make the user happy" |
| **Reverse test** | If the total is ≥ 85, R5 must additionally answer: "If this model were rejected, what would most likely be the reason?" |

**The most dangerous practice**: bunching scores in the 70–80 range to make the user feel good. That defeats S8's only purpose —
to stop the user from **forming a false picture**.

---

## 8. Citation anchors (may be cited when writing the S8 report; each must first be verified)

| Use | Literature anchor |
|------|---------|
| Six refereeing criteria | *American Journal of Agricultural Economics*, Refereeing Criteria (Contribution / Scholarship / Appeal / Originality / Analysis / Illustrations and Length) |
| Four elements of a theoretical contribution | Whetten, "What Constitutes a Theoretical Contribution?" (AMR) |
| What theory is not | Sutton & Staw, "What Theory is Not" (ASQ) |
| Two-dimensional framework of theoretical contribution | Corley & Gioia, "Building Theory about Theory Building" (AMR) |
| Evolution of refereeing standards ($q$–$r$) | Ellison, "Evolving Standards for Academic Publishing: A q-r Theory" (JPE) |
| Facts about submission and acceptance at top journals | Card & DellaVigna, "Nine Facts about Top Journals in Economics" (JEL) |
| Agreement-coefficient bands | Landis & Koch (κ bands); Krippendorff (more conservative thresholds) |
| Topic positioning | NSFC four science-question attributes for classified review (encouraging exploration / highlighting originality; targeting the frontier / taking a distinctive path; demand-driven / breaking bottlenecks; common-good oriented / convergence across disciplines) |
