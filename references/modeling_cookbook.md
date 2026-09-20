# Modeling cookbook (modeling_cookbook.md)

> **When to use**: S3 (choose functional forms and assumptions), S4 (write and solve the model), S5 (checks), S7 (comparative statics and sensitivity).
>
> This file is the **technical manual**: the parsimony principle, notation conventions, the functional-form library, solution recipes, comparative-statics techniques, a common-error list,
> and the full usage of `scripts/econ_solve.py`.

---

## 1. The parsimony principle (a hard constraint)

> **Philosophy — simplicity is a virtue, not a compromise.** A beautiful economic model has *few* assumptions and a *simple* form; the reader is an economist, so a long parameter list reads as a crutch, not sophistication. Every functional form and every parameter must justify itself by changing a conclusion or a comparative-static sign — otherwise cut it. Equally, never dress up a toy exercise as a deep contribution, and never hide an approximation or a calibration choice: honesty about what the model *cannot* say is what makes it professional. The goal is a **communicable principle** a researcher or decision-maker can use, not a display of algebra.

| Rule | Ceiling | What to do if you exceed it |
|------|------|------------|
| Number of parameters (excluding normalization constants) | **≤ 5** | Fix one parameter at a benchmark value (e.g. $\alpha=\tfrac12$) or drop a secondary parameter |
| Number of endogenous variables | **≤ 3** | Make a secondary variable exogenous, or solve in two steps |
| Choice variables per agent | **1–2** | Compress dimensions with a composite good (numeraire) |
| State variables | **≤ 1** | Make it static, or introduce dynamics only in S7 |
| Agent types (heterogeneity groups) | **2–3** | Do not use a continuous distribution |
| Length of the model setup (excluding derivations) | **one A4 page** | If it does not fit, the model is too heavy |

**Preference order over functional forms** (if a higher one works, do not use a lower one):

1. **Linear / log-linear** —— most transparent, cleanest comparative-statics signs
2. **Cobb-Douglas** (constant share $\alpha$) —— easy to solve, but it "erases" elasticity-of-substitution effects
3. **Quadratic** ($-\frac{b}{2}x^2$) —— for convex costs and quadratic loss; first-order conditions are linear
4. **CES** (variable elasticity of substitution $\sigma$) —— use only when **the elasticity of substitution is itself the object of study**
5. **General functional forms** $u'(x)$, $F'(\cdot)$ —— use only when **proving a result that must not depend on the functional form**

**The "solvability first" principle**: sacrifice a little realism to keep the closed form. A small solvable model >> a large unsolvable one.

**Three prohibitions**
- Do not introduce a third functional form "to be more realistic"
- Do not mix two preference systems in one model (e.g. quasi-linear here, Cobb-Douglas there)
- Do not use parameters with no economic meaning (e.g. an "adjustment coefficient" without saying what it represents)

---

## 2. Notation conventions

### 2.1 Naming conventions

| Use | Convention | Example |
|------|------|------|
| Endogenous variables (quantity, price, consumption, labour) | Lower-case Roman letters | $x,\ q,\ c,\ p,\ y,\ \ell$ |
| Parameters | Greek letters preferred; Roman letters for intercepts/slopes | $\alpha,\beta,\gamma,\delta,\lambda,\sigma$; $a,b$ |
| Functions | Upper case or sans-serif | $U(\cdot),\ u(\cdot),\ F(\cdot),\ C(\cdot),\ \pi(\cdot)$ |
| Sets / feasible regions | Upper-case upright | $X,\ S,\ \Omega$ |
| Vectors / matrices | Bold | $\mathbf{x},\ \mathbf{A}$ |
| Time subscript | $t,\ t+1$ (or $1,2$) | $x_t$ |
| Agent subscript | $i,\ j,\ -i$ (meaning others) | $x_i,\ x_{-i}$ |
| Optimal value | Star superscript | $x^*,\ p^*,\ u^*$ |
| Exogenous shock / policy variable | $\theta,\ \tau,\ s,\ t$ (tax rate) | $\theta_t$ |
| Multiplier (shadow price) | $\lambda,\ \mu$ | $\lambda\ge 0$ |
| Elasticity | $\eta,\ \sigma$ (with its meaning **fixed**) | $\eta\equiv\frac{\partial x}{\partial p}\frac{p}{x}$ |
| Probability | $\pi$ (**do not** use $p$; keep $p$ for price) | $\pi\in[0,1]$ |
| Discount factor | $\beta$ or $\delta$ (pick only one, and do **not** clash with a production elasticity) | $\beta\in(0,1)$ |

### 2.2 Mandatory self-checks (the items lint examines)

- ❌ Using $l$ (lower-case L) as a variable name —— confusable with the digit 1
- ❌ Using $e$ or $E$ for anything other than Euler's number —— confusable with the natural constant, and the solver's `RESERVED` set contains **both** `e` and `E`, so writing `E` in a spec is **silently parsed as 2.718…**. If `E` is the natural letter for your parameter (e.g. enforcement intensity), re-parameterise — for instance use the complementary share `κ = 1 − E` — rather than fighting the collision.
- ❌ $p$ denoting both price and probability
- ❌ $\beta$ denoting both the discount factor and a capital elasticity
- ❌ $\sigma$ denoting both the elasticity of substitution and a standard deviation
- ❌ $t$ denoting both a time subscript and a tax rate
- ❌ Mixed super/subscripts: $p_L$ and $p_l$ treated as the same symbol (**forbidden**)
- ❌ One symbol meaning different things in different sections (S5 treats this as a **substantive problem**)
- ✅ Each symbol carries **exactly one meaning**, and may be used only after it appears in the notation table

---

## 3. Functional-form library

### 3.1 Preferences

| Form | Expression | When to use | Caveat |
|------|-------|------|------|
| Quasi-linear | $u = x_0 + v(x_1)$, $v'>0,\ v''<0$ | Partial equilibrium, no income effects | Income effects are switched off; unsuitable for distributional analysis |
| Cobb-Douglas | $u=x_1^{\alpha}x_2^{1-\alpha}$ | General use; constant expenditure shares | Elasticity of substitution fixed at 1 (quite restrictive) |
| CES | $u=\left(\alpha x_1^{\rho}+(1-\alpha)x_2^{\rho}\right)^{1/\rho}$, $\sigma=\frac{1}{1-\rho}$ | When the elasticity of substitution is the focus | Many parameters; requires $\rho<1$ |
| Log | $u=\ln x_1+\beta\ln x_2$ (= a special case of CD) | Easy to differentiate | — |
| Stone-Geary | $u=(x_1-\bar x_1)^{\alpha}(x_2-\bar x_2)^{1-\alpha}$ | When there is a "subsistence" threshold | One extra parameter |
| Quadratic loss | $U=-\frac{b}{2}(x-x_0)^2$ | Cost of deviation, target setting | Linear first-order conditions |

**Relative status / status externalities (for "rat race" phenomena)**
$u_i = v(c_i) + w\!\left(h_i - \bar h\right)$, where $\bar h$ is the reference-group mean. When $w' > 0$ and $\bar h$ rises with everyone's investment,
the private optimum exceeds the social optimum — the standard characterization of an "arms race / rat race". **When reporting, state clearly whether "relative status" or "absolute level" is doing the work.**

### 3.2 Technology / production

| Form | Expression | When to use | Caveat |
|------|-------|------|------|
| Linear | $Q=aK+bL$ | Simplest; corner solutions are common | Constant returns to scale, corners easy to hit |
| Cobb-Douglas | $Q=AK^{\alpha}L^{\beta}$ | General use | $\alpha+\beta$ determines returns to scale |
| Quadratic cost | $C(q)=\frac{c}{2}q^2$ | Convex costs, interior solutions | Linear marginal cost |
| Fixed cost + linear variable | $C(q)=F+cq$ | Entry, economies of scale | Requires a zero-profit condition |
| CES | $Q=A\left(\alpha K^{\rho}+(1-\alpha)L^{\rho}\right)^{1/\rho}$ | When the elasticity of substitution is the focus | Many parameters |
| Education/health production function | $Q=A\,S^{\gamma}H^{\delta}$ | Input-output | Endogenous-input problem is severe |

### 3.3 Demand and markets

| Form | Expression | Note |
|------|-------|------|
| Linear inverse demand | $p = a - bQ$ | Most common; $b$ is the slope (**note**: a smaller $b$ means a larger market) |
| Isoelastic demand | $Q = Ap^{-\eta}$ | Constant elasticity; log-linear and easy to solve |
| Dixit-Stiglitz | $Q=\left(\int q_i^{\rho}\right)^{1/\rho}$ | Monopolistic competition, number of varieties |
| Matching function | $M(u,v)=Au^{\eta}v^{1-\eta}$ | Search frictions; $\theta=v/u$ is market tightness |

### 3.4 Constraints and institutions

| Type | Written as | Use |
|------|------|------|
| Budget constraint | $p_1x_1+p_2x_2 \le y$ | Consumption, education spending |
| Time constraint | $\ell + L = T$ | Labour supply, study time |
| Resource constraint | $c + k' = f(k) + (1-\delta)k$ | Dynamics |
| Rationing / quota | $x \le \bar x$ | Price control, lotteries, ceilings |
| Borrowing constraint | $c_1 \le y_1$ | Development economics, education investment |
| Participation constraint | $U \ge \bar U$ | Principal–agent, contracts |
| Incentive compatibility | $U(\text{truth}) \ge U(\text{lie})$ | Mechanism design, information revelation |

### 3.5 Conventional parameter ranges (must be declared when writing the model)

| Parameter | Convention | Reason |
|------|------|------|
| Discount factor $\beta,\delta$ | $(0,1)$ | Time preference |
| Probability $\pi$ | $[0,1]$ | Domain |
| Production elasticities $\alpha,\beta$ | $(0,1)$; $\alpha+\beta\lessgtr 1$ determines returns to scale | Technology |
| Elasticity of substitution $\sigma$ | $>0$; $\sigma>1$ substitutes, $<1$ complements | Demand |
| Demand slope $b$, cost parameter $c$ | $>0$ | Ensures an interior solution exists |
| Substitution parameter $\rho$ (CES) | $<1$; $\rho\to0$ degenerates to CD | Ensures concavity |

---

## 4. Solution recipes

### 4.1 Equality-constrained optimization (Lagrange)

$$\max_{x}\ f(x)\quad \text{s.t.}\quad g(x)=0
\;\Longrightarrow\;
\mathcal L = f(x) - \lambda g(x),\qquad
\frac{\partial \mathcal L}{\partial x_i}=0,\quad \frac{\partial \mathcal L}{\partial \lambda}=0$$

- If the constraint is an inequality $g(x)\le 0$: use **Kuhn–Tucker**: $\partial\mathcal L/\partial x=0$, $\lambda\ge0$, $g\le0$, $\lambda g = 0$.
- You **must** discuss both cases: $\lambda>0$ (constraint binds) and $\lambda=0$ (it does not).

### 4.2 Unconstrained optimization

$\partial f/\partial x_i = 0$ → solve for $x^*$ → verify the second-order condition:
single variable $f''(x^*)<0$ (maximum); multivariate Hessian $H$ **negative definite** (maximum) / **positive definite** (minimum).

### 4.3 Game-theoretic equilibrium

1. Write each player's optimization problem → best-response function $x_i^*(x_{-i})$
2. Solve the system jointly; for a symmetric equilibrium, guess $x_i=x_j=x$ first to simplify
3. Argue existence and uniqueness: contraction / monotonicity of the best-response map (or at least a numerical check)

### 4.4 Envelope theorem (for the derivative of welfare/value with respect to a parameter)

$$\frac{dV(\theta)}{d\theta}=\frac{\partial \mathcal L}{\partial \theta}\bigg|_{x=x^*}$$
Only a **partial** derivative with respect to the parameter is needed; the change in $x^*$ can be ignored —— the most economical tool in welfare analysis.

### 4.5 Log-linearization (a fast route to comparative statics)

Take logs of both sides of $F(x;\theta)=0$ and totally differentiate: $\dfrac{dx}{x}=\eta_x \dfrac{d\theta}{\theta}$,
where $\eta$ is an elasticity. **Best for multiplicative models** (CD, isoelastic): the sign of the elasticity can be read off directly.

---

## 5. Comparative-statics techniques (the core of S7)

### 5.1 Standard procedure (implicit function theorem / IFT)

Let the equilibrium-condition system for an interior solution be $F(x;\theta)=0$ ($x\in\mathbb R^n$; $\theta$ a parameter):

1. **Jacobian**: $J \equiv \dfrac{\partial F}{\partial x}$ ($n\times n$)
2. **Total differential**: $J\,\mathrm dx + \dfrac{\partial F}{\partial \theta}\,\mathrm d\theta = 0$
3. **Solve for the derivative**: $\dfrac{\mathrm dx}{\mathrm d\theta} = -J^{-1}\dfrac{\partial F}{\partial \theta}$
4. **Sign it**:
   - The sign of $J$ is often given by the **second-order condition** (e.g. negative definiteness ⇒ the sign of $\det J$ follows from the order)
   - Use **Cramer's rule** to expand until numerator and denominator are both signable
   - Obtain $\dfrac{\mathrm dx}{\mathrm d\theta} = \dfrac{(\pm)}{|J|}$ and write down the **sign and the conditions**

### 5.2 Three techniques for signing

| Technique | How |
|------|------|
| **Use the SOC** | The signs of the principal minors of a negative definite matrix are known ⇒ the denominator's sign is determined |
| **Monotonicity argument** | If $F$ is strictly monotone in $x$ and moves in one direction in $\theta$, the sign can be read off directly |
| **Log differentiation** | In multiplicative models you get the elasticity directly; the sign is immediate |

### 5.3 Reporting convention (**mandatory**)

Do not just write $\partial x^*/\partial \theta > 0$. Write:

> **Corollary 1**: when $\theta > \underline\theta$, $\dfrac{\partial x^*}{\partial\theta}>0$; when $\theta<\underline\theta$ the sign flips.
> **Conditions**: $b>0$, $c>0$ and $a>c$ (which guarantee an interior solution). **Economic meaning**: ……

**A comparative static without conditions is an incomplete comparative static.**

### 5.4 Sensitivity analysis (numerical)

- **One-parameter sweep**: the interval must cover the **critical point where the sign flips**, otherwise nothing is visible
- **Two-parameter heat map**: to show the region of parameter combinations where the conclusion holds
- **Reporting requirement**: the figure must state the benchmark parameter values, the interval covered, and that "this is a numerical illustration, not a general conclusion"

---

## 6. Common-error list (check item by item in S5)

**Setup**
1. The objective contains a variable the optimizer does **not** know (information assumption inconsistent with the optimization)
2. More constraints than variables (over-constrained; usually no solution)
3. Solving for an exogenous variable as if it were endogenous
4. A missing key constraint (e.g. no budget constraint ⇒ unbounded demand)
5. Mutually contradictory assumptions (complete information + unverifiable quality)

**Solution**
6. Deriving only first-order conditions and then claiming a unique equilibrium exists (no SOC, no existence argument)
7. Ignoring corner solutions (treating a negative solution as valid)
8. Differentiation errors: writing $\mathrm d/\mathrm dx$ where $\partial/\partial x$ belongs; dropping a product-rule term
9. Dividing by a term that may be zero (e.g. dividing by $\lambda$) without discussing $\lambda=0$
10. Passing off a numerical solution as a closed form

**Comparative statics**
11. Giving a sign but **not the conditions**
12. Signing by intuition outside the SOC (e.g. "obviously a higher price lowers demand", ignoring income effects)
13. Computing a derivative at a single parameter value and writing it up as a general conclusion

**Notation**
14. One symbol with two meanings ($p$ both price and probability)
15. Parameters and variables sharing a letter
16. A proposition citing a symbol that is not in the notation table
17. Assumption numbers inconsistent with the citations in the text

**Exposition**
18. Dressing up an identity / FOC as a "proposition"
19. "We prove" for numerical results, "in general" for a finite grid, "robust" for a single point
20. A proposition with only its mathematics and no economic meaning

---

## 7. `scripts/econ_solve.py` user manual

> Interpreter: `C:\Users\asus\.workbuddy\binaries\python\envs\default\Scripts\python.exe`
> Script path: `<skill_dir>\scripts\econ_solve.py`
> Every subcommand prints its result to stdout and (optionally) writes it to a file. **On this machine you must write to a file and read it back**.

### 7.1 Common arguments

```
--spec FILE       input JSON spec
--out FILE        write the report to this file (markdown)
--json-out FILE   write the structured result to this file (JSON)
```

### 7.2 `foc` — first-order conditions, closed form, second-order conditions, numerical verification

**spec format**
```json
{
  "title": "Cournot duopoly",
  "params": ["a", "b", "c"],
  "agent_params": {"a": 10, "b": 1, "c": 1},
  "agents": [
    {"name": "Firm 1", "objective": "(a - b*(q1+q2))*q1 - c*q1", "vars": ["q1"], "maximize": true},
    {"name": "Firm 2", "objective": "(a - b*(q1+q2))*q2 - c*q2", "vars": ["q2"], "maximize": true}
  ],
  "solve": {"joint": true, "for": ["q1", "q2"]}
}
```
**Command**
```
python econ_solve.py foc --spec spec_foc.json --out S4_foc_report.md
```
**Output**: each agent's objective, first-order conditions, second-order conditions (Hessian / single-variable $f''$),
the closed form from joint solution, and — after substituting `agent_params` — the **FOC residuals** (should be ≈ 0) and the solution values.

### 7.3 `cs` — comparative statics (implicit function theorem)

**spec format**: shares `params` / `agents` with `foc`; additionally
```json
{
  "comparative_statics": {
    "endogenous": ["q1", "q2"],
    "params": ["a", "b", "c"],
    "evaluate_at": {"a": 10, "b": 1, "c": 1},
    "positive_params": ["a", "b", "c"]
  }
}
```
(You may instead supply the equilibrium-condition system directly as `"equations": ["expr1", "expr2"]`, in place of `agents`.)

**Command**
```
python econ_solve.py cs --spec spec_cs.json --out S7_comparative_statics.md
```
**Output**: the Jacobian $J$, $\partial F/\partial\theta$, the derivative matrix $\mathrm dx/\mathrm d\theta$ as simplified symbolic expressions,
and a **numerical sign determination** at `evaluate_at`. When a sign cannot be determined it states explicitly "sign undetermined (additional assumptions required)".

### 7.4 `sim` — numerical sweeps, heat maps and CSV

**spec format**
```json
{
  "title": "Sensitivity of equilibrium quantity to b",
  "base": {"a": 10.0, "b": 1.0, "c": 1.0},
  "expressions": {"q1": "(a-c)/(3*b)", "Q": "2*(a-c)/(3*b)"},
  "plots": [
    {"type": "sweep", "vary": [{"name": "b", "range": [0.2, 2.0, 60]}],
     "y": ["q1", "Q"], "xlabel": "b", "ylabel": "Quantity",
     "title": "Sensitivity of equilibrium quantity to b", "output": "figs/fig1.png", "also_pdf": true, "csv": true},
    {"type": "heatmap",
     "x": {"name": "b", "range": [0.2, 2.0, 80]},
     "y": {"name": "c", "range": [0.5, 8.0, 80]},
     "z": "Q", "xlabel": "b", "ylabel": "c", "title": "Heat map of total quantity", "output": "figs/fig2.png"}
  ]
}
```
**Command**
```
python econ_solve.py sim --spec spec_sim.json --out S7_sim_report.md
```
**Output**: PNG (optionally PDF) at the given path, optionally CSV, plus a text report (benchmark values, ranges, positions of extremes).
If `vary` has two elements, the second is used as the variable that distinguishes **multiple curves**.
`cjk_font` (default `true`) enables a font fallback for non-Latin axis labels; set it to `false` if your labels are pure ASCII and you want to skip the lookup.

### 7.5 `lint` — notation and assumption-convention check

**spec format**
```json
{
  "title": "Model notation check",
  "symbols": [
    {"sym": "q1", "type": "endogenous", "meaning": "output of firm 1", "domain": ">=0", "unit": "units"},
    {"sym": "a",  "type": "param", "meaning": "demand intercept", "domain": ">0"},
    {"sym": "p",  "type": "endogenous", "meaning": "price", "domain": ">=0"}
  ],
  "assumptions": ["A1", "A2", "A3"],
  "referenced": ["A1", "A3", "A4"],
  "text_file": "S4_model.md"
}
```
**Command**
```
python econ_solve.py lint --spec spec_lint.json --out S5_lint_report.md
```
**Checks**: duplicate symbol definitions / type conflicts / used-but-undeclared (scanning `$...$` math spans in `text_file`) /
declared-but-unused / dangerous names (`l`, `e`, `O`) / subscript-superscript confusion / inconsistent assumption-number citation /
parameters without a declared range / probability-type symbols missing a $[0,1]$ domain.

### 7.6 `env` — environment self-check

```
python econ_solve.py env --out env.md
```
Prints the interpreter path and the numpy/scipy/sympy/matplotlib/pandas versions (for the reproducibility notes).

---

## 8. Result-reporting conventions

### 8.1 How to write a proposition

```
**Proposition 1 (the critical condition for substitution).** There exists a unique threshold $\hat\theta$ such that
for $\theta>\hat\theta$, $x^*$ decreases in $\theta$.
*Derivation notes*: totally differentiating the first-order condition gives $\mathrm dx/\mathrm d\theta = -(\partial F/\partial\theta)/(\partial F/\partial x)$;
by the second-order condition $\partial F/\partial x<0$, so the sign is determined by $\partial F/\partial\theta$; solving $\partial F/\partial\theta=0$ gives $\hat\theta$.
*Economic meaning*: once …… exceeds the threshold, ……, so policy …….
```
- Include only **non-trivial** results (2–4 propositions)
- Every proposition must be paired with one sentence of "economic meaning"
- Identities and first-order conditions are **not** dressed up as propositions

### 8.2 Table conventions

- Parameter table: symbol | meaning | value/range | source (calibrated/estimated/illustrative) | unit
- Comparative statics table: parameter | $\partial x^*/\partial\theta$ | conditions | economic meaning
- Robustness table: conclusion | benchmark setup | sign after relaxing | robust?

### 8.3 Relaxation triage (before deriving a new closed form)

When the user asks you to "relax assumption X" (imperfect competition, imperfect substitution, risk aversion, dynamics...), **do not start deriving a new model**. First run this three-question triage:

1. **Is it a reparametrization?** Write the relaxed primitive and ask whether the old model is recovered by a change of variable. If yes, say so explicitly, give the mapping, and note that **every proposition survives** — only magnitudes change. This is a stronger and more useful answer than a re-derivation.
   *Worked example*: replacing perfect substitution with "one unit of the substitute delivers $\lambda$ effective units" gives $h^{d}=B(\mu/\lambda)^{-\varepsilon}$, i.e. the old model with $\tilde\mu\equiv\mu/\lambda$. So all closed forms are preserved verbatim under $\mu\to\tilde\mu$.
2. **Which direction does each object move, and is it monotone?** Never claim the relaxed version "strengthens the result" without checking every derived object. In the example above, $R$ rises in $\tilde\mu$ (effect amplified) **but** the sign threshold $\varepsilon^{*}$ is **non-monotone** in $\lambda$ — so "relaxing A6 widens the region where the result holds" would be false. **Compute the direction; do not assume it.**
3. **Does the relaxed version now generate a feature of the data the old one could not?** If it still cannot, say so and name what else is needed.
   *Worked example*: the $\lambda$ form still corners (the household buys only the cheaper-per-effective-unit good), so it cannot produce the pre-policy coexistence of both goods seen in survey data. Coexistence requires an **intrinsic** demand term for the substitute: with $\Phi(a+\lambda n)+\Psi(n)$ and $\Psi(n)=D^{1/\eta}\frac{\eta}{\eta-1}n^{(\eta-1)/\eta}$, the pre-policy first-order condition gives $n_0=D(\mu-\lambda)^{-\eta}$, so coexistence holds **iff $\mu>\lambda$**. State the condition; do not calibrate what the data do not pin down.

**Report all three answers.** A relaxation that only reports (1) is marketing, not analysis; a relaxation that reports (2) honestly — including the direction that hurts the paper — is what makes a referee trust the rest.

> **Corollary for the write-up**: if a relaxation is a reparametrization, put it in the main text as a **proposition** (it shows economy of structure), and keep the extra symbol out of the benchmark parameter table so parsimony is not damaged.

### 8.4 Figure conventions
- Axes must have labels (**with units**)
- **Labels, titles and legends follow the conversation language** (Global Rule 8), not the language of this manual. The engine takes them from the spec, so put the translated strings in `xlabel` / `ylabel` / `title` / `clabel` and set `"cjk_font": true` when the labels contain non-Latin script
- The caption must contain: the figure-type label (numerical illustration / parameter sweep / mechanism sketch) + parameter values + a "not general" qualifier
- Figures used in the paper should be exported as both PNG and PDF
