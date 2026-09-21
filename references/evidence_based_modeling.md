# Evidence-based modeling (evidence_based_modeling.md)

> **When to use**: S3 (assumptions), S4 (model construction), S5 (checks), S6 (report) — and
> whenever a functional form, a key assumption, a parameter restriction or a major modeling
> choice is introduced or changed.
>
> **One-line rule**: every key content item must carry a **support source** *and* a sentence
> that says **how** that source supports it — a bare citation is not evidence.

---

## 1. What is a "key content item"

An item that changes the model, not mere notation:

- every **functional form** (utility, production, cost, demand, matching, information structure);
- every **key assumption** (timing, information, market structure, agent rationality, boundary);
- every **parameter restriction** (a normalization, a sign restriction, a range);
- every **major modeling choice** (equilibrium concept, horizon, aggregation, dimensionality).

Routine algebraic steps and definitions are **not** key items.

## 2. What counts as a support source

| # | Support type | Use it when | What you must state |
|---|---|---|---|
| **S1** | Classic / canonical literature | a standard model or theorem already establishes the form | the result, and the **property** it provides |
| **S2** | Textbook foundation | the form is standard pedagogy (micro, IO, contract theory, growth) | the textbook anchor |
| **S3** | Stylized empirical regularity / institutional fact | the form encodes a documented fact (decreasing returns, sunk costs, limited liability) | the source **and** the fact |
| **S4** | Axiomatic / property requirement | the model needs a mathematical property (concavity, monotonicity, Inada, single-crossing, supermodularity) | the property and **why it is needed here** |
| **S5** | Author's own construction | no literature anchor exists | label it *"a simplifying assumption made for tractability"* + its checkable implication |

An item with **no** support source must not enter a deliverable unless it is an **S5** own
construction and is **explicitly labelled** as such.

## 3. The "how it supports" requirement (the hard part)

A citation names a source. Evidence **links** the source to *this* form *here*. Write a
**link sentence** of the shape:

```
support = <source>  +  <the property it provides>  +  <why that property is what this model needs>
```

**Rejected — bare citation** vs **accepted — linked**:

- ✗ "Utility is quadratic (Smith, 2019)."
- ✓ "Utility is quadratic: a second-order Taylor approximation of any smooth concave utility
  around the interior optimum — it preserves a participation margin and yields a closed form
  (standard in consumer theory)."
- ✗ "Production is Cobb–Douglas."
- ✓ "Production is Cobb–Douglas because we require constant output elasticity and a closed-form
  factor demand — the textbook baseline for that requirement."
- ✗ "We assume linear demand, following the literature."
- ✓ "Demand is linear so that marginal revenue is linear and the comparative-static sign is
  invariant; this is the standard IO benchmark when the object of interest is the sign, not
  the curvature."

If you cannot write the middle term (the property) or the last term (why we need it), the
citation is decoration — either find the real link or reclassify the item as S5.

## 4. Required deliverable: the evidence table (E-table)

`S4_model.md` and `S6_model_report.md` **must** carry an E-table. One row per **key content
item** (not per equation line):

| # | Item | Form / statement | Support type | Source | How it supports (the link) | Checkable implication |
|---|---|---|---|---|---|---|
| E1 | Utility functional form | $u=\theta q-\tfrac{\gamma}{2}q^{2}$ | S1 + S4 | textbook consumer theory `[VERIFIED]` | concave, closed-form interior solution, keeps the participation margin | linear demand $p=\theta-\gamma q$ (testable) |
| E2 | ... | ... | ... | ... | ... | ... |

- **Source** carries the `[VERIFIED]` tag required by Global Rule 2.
- **Checkable implication** states the form's *over-identification signature* — the observable
  footprint a reader could use to falsify the choice. This is what turns a modelling choice
  into a testable one.

## 5. Interaction with the parsimony principle

Evidence-based modeling and parsimony are complementary, not opposed:

- an item must **earn its place** twice — by **changing a conclusion or a comparative-static
  sign** (parsimony) **and** by **carrying a support source** (this rule);
- a well-anchored form that moves no result is still **cut** (parsimony wins);
- a form that moves a lot but has no basis is still **rejected** (this rule wins).

## 6. Common failure patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| **Citation wall** | many references, no link sentence | write the link for each item |
| **Lens name-dropping** | "following Becker (1964)…" with no property actually used | state the property taken from it |
| **Post-hoc justification** | form picked for tractability, then dressed in a citation | declare it S5 own construction |
| **Unverifiable source** | the citation was never checked | Global Rule 2: verify online or drop it |
| **Orphan parameter** | a parameter with neither source nor role | give it a source, or drop it (parsimony) |

## 7. Checklist (mirrors gate **G8**)

- [ ] every functional form has an E-table row
- [ ] every key assumption has a support type and a source
- [ ] every row has a **link sentence** (how it supports), not a bare citation
- [ ] every parameter restriction is justified
- [ ] all **S5** own constructions are labelled as such and carry a checkable implication
- [ ] all sources are `[VERIFIED]` (Global Rule 2)
