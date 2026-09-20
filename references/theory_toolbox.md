# Theory toolbox and literature map (theory_toolbox.md)

> **When to use**: S2 (fix perspective and literature), S3 (choose the leading theory), S4 (choose functional forms and solution methods).
>
> ⚠️ **This file is not a citable reference list.** It is a **lead-generation library**: it tells you "which perspective uses which theory, and which theory pairs with which model".
> Any reference that goes into `S2` / `S4` / `S9` **must first be verified online** (authors, year, title, journal, volume/issue/pages) and tagged `[VERIFIED]`.
> The entries here are only **search starting points**; never write down a volume/issue/page you are not sure of.

---

## 1. Perspective overview

| Perspective | Core unit of analysis | Standard modeling framework | Common endogenous variables | Typical form of conclusion |
|------|------------|------------|------------|------------|
| Production & consumption | Representative household / firm | Utility maximization + production function + market clearing | Consumption, price, labour supply | Demand/supply elasticities, comparative-statics signs |
| Economics of education | Household / school / government | Education production function + household investment decision + matching | Education inputs, achievement, admission thresholds | Input-output elasticities, peer effects, policy effects |
| Labour economics | Worker / firm | Labour supply (time allocation) + search and matching + human capital | Labour supply, wage, employment, training | Wage elasticity, participation rate, wage premium |
| Industrial organization | Firm / platform | Oligopoly game (Cournot/Bertrand) + entry + product differentiation | Quantity, price, number of entrants, quality | Equilibrium price, collusion stability, entry effects |
| Development economics | Household / community / government | Dual economy + credit constraints + technology adoption | Investment, migration, technology adoption | Poverty traps, binding constraints |
| Public economics | Government / household | Optimal taxation / public good provision / internalizing externalities | Tax rate, public good level, welfare | Ramsey rule, Samuelson condition |
| Environmental economics | Firm / regulator | Externalities and Pigouvian tax / emissions trading | Emissions, abatement investment, permit price | Prices vs quantities, social cost |
| Health economics | Individual / insurer | Health capital investment + insurance moral hazard | Demand for medical care, insurance coverage | Demand elasticity, size of moral hazard |
| Urban & regional | Household / firm | Monocentric city + agglomeration economies | Land rent, commuting, population density | Rent gradient, agglomeration elasticity |
| Behavioural economics | Individual | Non-standard preferences (present bias, reference dependence, social preferences) | Choice, participation, effort | Direction of deviation from the standard model |
| Macro | Representative agent | Growth (Solow/Romer) + dynamic optimization (Bellman) | Capital, output, growth rate | Steady state, speed of convergence, transition dynamics |
| Finance | Investor / firm | Portfolio choice + asset pricing + corporate finance | Holdings, prices, leverage | Risk premium, pricing kernel |
| International trade | Country / firm | Comparative advantage + monopolistic competition + firm heterogeneity | Trade volume, export decision, factor prices | Gains from trade, selection effect |
| Institutional economics | Player / organization | Transaction costs + property rights + incomplete contracts | Governance structure, investment incentives | Efficiency implications of property-rights allocation |
| Matching & market design | Two-sided / many-sided | Stable matching + mechanism design | Match outcomes, cutoffs | Stability, strategy-proofness |

---

## 2. Phenomenon keywords → candidate theories

Use the phenomenon keywords distilled in S1 to locate candidate theories in the table below (each row gives 2–4 candidates, for the user to choose from in S2).

| Phenomenon keyword | Candidate theories | Common modeling entry point |
|-----------|---------|------------|
| Price control / price cap / ceiling | Excess effective demand, queues and rationing, shadow prices, hidden markets | Supply-demand imbalance + secondary market |
| Supply shock / rising costs | Cost pass-through, incidence determined by elasticities | Partial-equilibrium tax incidence |
| Queueing / lottery / lot allocation | Non-price rationing, opportunity cost, random allocation | Expected utility + rationing constraint |
| Tutoring / shadow education / rat race | Arms race, status externality, human capital investment, prisoner's dilemma | Status competition model + education production function |
| School-district housing / admission thresholds | Capitalization, Tiebout sorting, peer effects | Monocentric city + school-district capitalization |
| Platform commission / two-sided markets | Two-sided pricing, cross-side network externalities | Platform profit maximization (demand on both sides) |
| Monopoly / rising concentration | Market power, entry barriers, markups | Oligopoly / monopolistic competition |
| Asymmetric information / uncertain quality | Adverse selection, signalling, screening | Lemons / Spence signalling |
| Shirking / unobservable effort | Moral hazard, incentive contracts | Principal–agent (hidden action) |
| Commons / congestion / pollution | Externalities, public goods, property rights | Pigouvian tax / Coasean bargaining |
| Policy subsidy / consumption vouchers | Policy incidence, income vs substitution effect | Budget constraint + indifference curves |
| Migration / population flows | Factor mobility, wage convergence, selection | Roy model / spatial equilibrium |
| Technological change / automation | Skill-biased technical change, task displacement | Task-based model (ALM) |
| Time allocation / division of household labour | Time allocation, intra-household bargaining | Becker time allocation / collective model |
| Addiction / habit formation | Rational addiction, habit stock | Dynamic optimization (habit stock) |
| Risk and insurance | Risk sharing, adverse selection, moral hazard | Expected utility + insurance contract |
| Reputation / ratings / certification | Repeated games, reputation mechanisms, signalling cost | Infinitely repeated game |
| Network effects / standards competition | Critical mass, multiple equilibria | Coordination game |
| Scarcity and distributive justice | Allocation rules, welfare functions | Social planner's problem |
| Long-run growth differences | Convergence, technology diffusion, institutional quality | Theoretical counterpart of growth regressions |

---

## 3. Perspective → classic model library

> Each entry gives: **representative optimization problem → key parameters → typical comparative statics → form of output**. Use directly as S4 templates.

### 3.1 Production and consumption

- **Cobb-Douglas utility + budget constraint**
  $\max_{x_1,x_2}\ x_1^{\alpha}x_2^{1-\alpha}$ s.t. $p_1x_1+p_2x_2=y$
  → $x_i^*=\frac{\alpha_i y}{p_i}$; constant expenditure shares (both its strength and its weakness).
- **CES utility** (adjustable elasticity of substitution)
  → demand $x_i^*=\frac{y}{p_i}\cdot\frac{p_i^{1-\sigma}}{\sum_j p_j^{1-\sigma}}$, with $\sigma$ the elasticity of substitution.
- **Cobb-Douglas production + profit maximization**
  $\max_{K,L}\ pAK^{\alpha}L^{\beta}-wL-rK$ → $L^*=\left(\frac{\beta pA}{w}\right)^{\frac{1}{1-\alpha-\beta}}\cdots$ (returns to scale determine whether the solution is finite).
- **Cost minimization → cost function → markup pricing** (common in IO).

### 3.2 Economics of education

- **Education production function**: $Q = f(\text{inputs}; \text{family}, \text{school}, \text{peers})$,
  the identification difficulty is that inputs are endogenous; in a model it is usually written $Q = A\,S^{\gamma}\,H^{\delta}$.
- **Household human-capital investment** (a simplified two-period Ben-Porath version):
  $\max_{I}\ u(c_1)+\beta u(c_2)$ s.t. $c_1+I=y_1$, $c_2=y_2+w\,h(I)$, $h'>0,h''<0$.
- **Status competition / arms race**: $u_i = v(h_i - \bar h)+\cdots$, or put "relative rank" into the utility function
  → gives the classic conclusion of **over-investment** (private optimum > social optimum).
- **Peer effects**: $y_i = \alpha \bar y_{-i} + \beta x_i + \varepsilon_i$ (Manski's reflection problem: identification requires care).
- **School choice / Tiebout**: households sort by willingness to pay for school quality → stratification and capitalization.

### 3.3 Labour

- **Time allocation**: $\max_{c,\ell} u(c,\ell)$ s.t. $c=w(T-\ell)+V$ → labour supply elasticity (income vs substitution effect).
- **Mincer equation**: $\ln w = a + b\,S + c\,X + d\,X^2$ (theoretical counterpart: returns to human capital investment).
- **Search and matching (simplified DMP)**: matching function $M(u,v)=Au^{\eta}v^{1-\eta}$, free-entry condition $c = q(\theta)(J-V)$.
- **Efficiency wages / effort**: $e(w)$, with $w^*$ determined by $\max_w (e(w)(1-w))$.

### 3.4 Industrial organization

- **Cournot duopoly**: $\max_{q_i}(a-b(q_i+q_j))q_i - c q_i$ → $q^*=\frac{a-c}{3b}$ (general $n$: $\frac{a-c}{(n+1)b}$).
- **Bertrand**: homogeneous goods → price equals marginal cost (the Bertrand paradox); differentiated → price above marginal cost.
- **Hotelling linear city**: location choice + price competition → minimum differentiation.
- **Monopolistic competition (Dixit-Stiglitz)**: free entry drives profit to zero; the equilibrium number of varieties depends on fixed cost and the elasticity of substitution.
- **Entry game**: two periods (incumbent commits → potential entrant decides); yields conditions for entry deterrence.

### 3.5 Public / environmental

- **Optimal public good provision (Samuelson condition)**: $\sum_i MRS_i = MRT$.
- **Externalities and Pigouvian tax**: social optimum $\max_x \pi(x) - D(x)$; tax $t = D'(x^*)$.
- **Prices vs quantities (Weitzman)**: under uncertainty, the curvature of marginal benefit/cost decides which instrument is better.
- **Optimal taxation (simplified Ramsey)**: $\max \sum U_i$ s.t. the revenue constraint → $\frac{t_i}{1+t_i} = \frac{1}{\lambda}\cdot\frac{1}{\varepsilon_i}$ (inverse-elasticity rule).

### 3.6 Intra-household

- **Unitary model**: household utility $U(c_1,c_2)$, internal conflict ignored.
- **Collective model**: $\max \mu U_1 + (1-\mu)U_2$, with $\mu$ the bargaining weight — used to analyse how policy changes internal power.

### 3.7 Dynamic (macro / environmental)

- **Two-period saving**: $\max u(c_1)+\beta u(c_2)$ s.t. $c_1+s=y_1$, $c_2=y_2+(1+r)s$ → Euler equation $u'(c_1)=\beta(1+r)u'(c_2)$.
- **Solow**: $\dot k = sAk^{\alpha}-(\delta+n)k$ → steady state $k^*$.
- **Bellman**: $V(k)=\max_{k'}\{u(c)+\beta V(k')\}$ → first-order condition + envelope theorem.

---

## 4. Modeling-approach decision tree

```
How many decision-making agents does the phenomenon involve?
├─ 1 (or representable by a representative agent)
│   ├─ Single period, no strategic interaction → constrained optimization (Lagrange / Kuhn-Tucker)
│   └─ Intertemporal / with a state variable → dynamic optimization (two-period version → Bellman)
├─ 2 or more, whose actions affect each other
│   ├─ Simultaneous moves, complete information → Nash equilibrium (Cournot/Bertrand/Hotelling templates)
│   ├─ Sequential moves → subgame perfect (backward induction)
│   ├─ Asymmetric information → signalling (Spence) / screening / adverse selection / principal–agent
│   └─ Repeated interaction, reputation matters → repeated game (trigger strategies, conditions for cooperation)
└─ Many agents, no strategic interaction but mutual influence
    ├─ Influence through prices → competitive equilibrium / partial equilibrium
    ├─ Influence through externalities → externality model + social planner benchmark
    └─ Influence through matching → stable matching / matching function
```

**Selection principle**: **use a single agent rather than a game, a static model rather than a dynamic one, two agents rather than n agents.**
The marginal information from added complexity is usually far smaller than the risk of failing to solve it.

---

## 5. Literature search and verification procedure (mandatory in S2)

### 5.1 Search-term templates

- Mechanism: `<phenomenon> economic model`, `<phenomenon> theory`, `<phenomenon> mechanism`
- Systematic: `<phenomenon> survey`, `<phenomenon> review of economic studies`
- Positioning: `<theory name> seminal paper`, `<model name> original article`
- Non-English literature: search the regional database for the field (e.g. CNKI for Chinese-language work) using translated keywords
- Preferred sources: NBER / RePEc (IDEAS) / AEA journal pages / NBER Working Papers / official statistics and policy documents

### 5.2 Verification checklist (tick every line; failing any one means `[UNVERIFIED]`)

- [ ] Spelling and order of author names
- [ ] Year
- [ ] **Title matches exactly** (not a plausible-sounding paraphrase)
- [ ] Journal / publisher name
- [ ] Volume, issue, page numbers (or working-paper number)
- [ ] The item really exists (a matching publisher/database record was retrieved)

### 5.3 Hallucination alarms (hitting one of these means verify hard)

- All authors are famous and the title restates your argument very smoothly → most likely fabricated
- The journal fits the topic suspiciously well and the page numbers are round (e.g. 1–20)
- The search only turns up second-hand citations, conference abstracts, or AI-generated pages
- "A working paper from year X" with no findable number
- **Internal confidence is not evidence**: external retrieval is required

### 5.4 Recording format

```
[VERIFIED] Acemoglu, D., & Autor, D. (2011). Skills, Tasks and Technologies: Implications for
Employment and Earnings. Handbook of Labor Economics, 4, 1043–1171. Source: NBER/Elsevier journal page
[UNVERIFIED] <author> (<year>). <title>. <journal>. —— no matching record found; excluded from the paper's references
```

---

## 6. Classic anchor literature (by field, as search starting points)

> The following are **disciplinary anchors**, used to establish "what language this field speaks". **Fill in volume/issue/pages only after verification**; this table provides no unverified page numbers.

**Microeconomic foundations and textbooks**
- Mas-Colell, Whinston & Green, *Microeconomic Theory* (standard graduate textbook)
- Varian, *Microeconomic Analysis* (standard undergraduate/graduate textbook)
- Kreps, *A Course in Microeconomic Theory*

**Consumption and demand**
- Marshall, *Principles of Economics* (demand, elasticity, consumer surplus)
- Hicks, *Value and Capital* (substitution and income effects)
- Becker, "A Theory of the Allocation of Time" (time allocation)
- Lancaster, "A New Approach to Consumer Theory" (demand for characteristics)
- Deaton & Muellbauer, "An Almost Ideal Demand System" (demand systems)

**Production and technology**
- Cobb & Douglas, "A Theory of Production"
- Arrow, Chenery, Minhas & Solow (the CES production function)

**Games and information**
- Nash, "Equilibrium Points in n-Person Games"
- Selten (subgame perfection); Harsanyi (incomplete information)
- Fudenberg & Tirole, *Game Theory*
- Akerlof, "The Market for 'Lemons'" (adverse selection)
- Spence, "Job Market Signaling" (signalling)
- Stiglitz & Weiss, "Credit Rationing in Markets with Imperfect Information"
- Holmström, "Moral Hazard and Observability"; Laffont & Martimort, *The Theory of Incentives*
- Grossman & Hart (incomplete contracts); Hart & Moore (property-rights theory)

**Industrial organization**
- Tirole, *The Theory of Industrial Organization*
- Cournot / Bertrand / Hotelling (oligopoly and location competition)
- Dixit & Stiglitz, "Monopolistic Competition and Optimum Product Diversity"

**Human capital and labour**
- Becker, *Human Capital*; Mincer, *Schooling, Experience, and Earnings*
- Ben-Porath, "The Production of Human Capital and the Life Cycle of Earnings"
- Mortensen & Pissarides, "Job Creation and Job Destruction in the Theory of Unemployment"
- Autor, Levy & Murnane, "The Skill Content of Recent Technological Change"
- Acemoglu & Autor, "Skills, Tasks and Technologies"

**Economics of education**
- Hanushek (survey of education production functions)
- Lazear, "Educational Production"
- Epple & Romano, "Competition between Private and Public Schools, Vouchers, and Peer-Group Effects"
- Hoxby, "Does Competition among Public Schools Benefit Students and Taxpayers?"
- Manski, "Identification of Endogenous Social Effects" (the identification problem in peer effects)
- Shadow education: Bray, *The Shadow Education System*; Dang & Rogers' survey of private tutoring

**Public economics and taxation**
- Samuelson, "The Pure Theory of Public Expenditure"
- Ramsey, "A Contribution to the Theory of Taxation"
- Mirrlees, "An Exploration in the Theory of Optimum Income Taxation"
- Atkinson & Stiglitz, "The Design of Tax Structure: Direct versus Indirect Taxation"
- Tiebout, "A Pure Theory of Local Expenditures"; Oates, *Fiscal Federalism*

**Environment**
- Hardin, "The Tragedy of the Commons"; Ostrom, *Governing the Commons*
- Weitzman, "Prices vs. Quantities"
- Nordhaus, work on the social cost of carbon

**Urban and spatial**
- Alonso / Muth / Mills (monocentric city models)
- Krugman, "Increasing Returns and Economic Geography"; Fujita, Krugman & Venables, *The Spatial Economy*

**Behavioural**
- Kahneman & Tversky, "Prospect Theory"
- Rabin, "Psychology and Economics"; DellaVigna, "Psychology and Economics: Evidence from the Field"
- O'Donoghue & Rabin (present bias and self-control)

**Macro and growth**
- Solow, "A Contribution to the Theory of Economic Growth"
- Romer, "Endogenous Technological Change"; Aghion & Howitt (creative destruction)
- Kydland & Prescott, "Time to Build and Aggregate Fluctuations"
- Acemoglu, "Directed Technical Change"

**Finance**
- Markowitz (portfolio choice); Sharpe / Lintner (CAPM)
- Black & Scholes (option pricing); Fama & French (factors)
- Grossman & Stiglitz, "On the Impossibility of Informationally Efficient Markets"

**Trade**
- Ricardo, *On the Principles of Political Economy and Taxation* (comparative advantage)
- Krugman (new trade theory); Melitz, "The Impact of Trade on Intra-Industry Reallocations…" (firm heterogeneity)

**Institutions**
- Coase, "The Nature of the Firm"; Coase, "The Problem of Social Cost"
- North, *Institutions, Institutional Change and Economic Performance*
- Acemoglu, Johnson & Robinson, "The Colonial Origins of Comparative Development"

**Health**
- Arrow, "Uncertainty and the Welfare Economics of Medical Care"
- Grossman, "On the Concept of Health Capital and the Demand for Health"

**Matching and market design**
- Gale & Shapley, "College Admissions and the Stability of Marriage"
- Roth & Sotomayor, *Two-Sided Matching*
- Abdulkadiroğlu & Sönmez (school choice mechanisms)

**Method and topic positioning (for S2 / S8)**
- Whetten, "What Constitutes a Theoretical Contribution?" (the four elements of a theoretical contribution: What / How / Why / Who-Where-When)
- Sutton & Staw, "What Theory is Not" (what does **not** count as theory: citations are not theory, data are not theory, lists are not theory)
- Corley & Gioia, "Building Theory about Theory Building" (the two-dimensional originality × usefulness framework)
- Ellison, "Evolving Standards for Academic Publishing: A q-r Theory" (how refereeing standards at top journals evolve: $q$ is the importance of the idea, $r$ the craftsmanship)
- Card & DellaVigna, "Nine Facts about Top Journals in Economics" (factual background on submission and acceptance trends)
