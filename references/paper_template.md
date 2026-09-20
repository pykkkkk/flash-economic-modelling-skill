# Short-paper template and LaTeX skeleton (paper_template.md)

> **When to use**: S9 only.

---

## 1. Paper structure (seven sections + appendix)

| Section | Title | Content | Source material | Suggested length |
|----|------|------|---------|---------|
| — | Abstract + keywords | phenomenon → question → model → main results → implications (≤200 words) | everything | half a page |
| 1 | Introduction / phenomenon and background | phenomenon statement, evidence (with sources), why it matters, what this paper does | `S1` | 1–1.5 pages |
| 2 | The economic question | from phenomenon to an analysable economic question; relation to the literature (the gap) | `S1`, `S2` | 1–1.5 pages |
| 3 | Assumptions | assumption list (numbered), the basis and meaning of each, why this simplification | `S3` | 1 page |
| 4 | The model | notation table, environment and timing, individual problems, equilibrium concept | `S4` | 2–3 pages |
| 5 | Solution and results | first-order conditions, closed form, propositions, comparative statics | `S4`, `S7` | 2–3 pages |
| 6 | Discussion | economic meaning of each proposition; policy implications; limitations | `S6`, `S7`, `S8` | 1.5–2 pages |
| — | References | **`[VERIFIED]` entries only** | `S2` | — |
| Appendix | Appendix | full derivations, robustness, heterogeneity, numerical detail | `S4`, `S7` | unlimited |

**Writing discipline**: **present results in the body mainly with figures and compact tables; put detailed results (full derivations, the comparative-statics sign for every parameter, numerical tables) in the appendix.**

---

## 2. LaTeX skeleton (English)

```latex
\documentclass[12pt, a4paper]{article}

\usepackage[margin=1.2in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{microtype}
\usepackage{xcolor}
\definecolor{linkgreen}{RGB}{0,120,100}
\usepackage[colorlinks=true,linkcolor=linkgreen,citecolor=linkgreen,urlcolor=linkgreen]{hyperref}

% Theorem environments
\theoremstyle{plain}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\theoremstyle{definition}
\newtheorem{assumption}{Assumption}
\newtheorem{definition}{Definition}
\theoremstyle{remark}
\newtheorem{remark}{Remark}

\title{<one-sentence statement of the phenomenon>: a simple theoretical framework}
\author{<author>\\ \small \today}
\date{}

\begin{document}
\maketitle

\begin{abstract}
\noindent
<Phenomenon and question.> <The model setup in one sentence.> <Main results.> <Implications.>
\par\vspace{0.5em}
\noindent\textbf{Keywords:} <keyword 1>; <keyword 2>; <keyword 3>\\
\noindent\textbf{JEL codes:} <e.g. D10, I21, H23>
\end{abstract}

\section{Introduction}
\label{sec:intro}
% 1) The phenomenon: let the facts speak, with sources (footnote or parenthetical citation)
% 2) Why it matters
% 3) The gap in the literature (use [VERIFIED] references only)
% 4) What this paper does (model + main findings + contribution)
% 5) Roadmap

\section{The economic question}
\label{sec:question}
% Turn the phenomenon into an analysable question: who chooses what, when, subject to which constraints, and what determines the outcome

\section{Assumptions}
\label{sec:assumptions}
\begin{assumption}[<short name>]
\label{ass:1}
<Normalized statement.>
\end{assumption}
\noindent\textbf{Remark.} <Why this assumption (basis / a simplification for tractability, to be labelled explicitly).>

\section{The model}
\label{sec:model}
\subsection{Notation}
% use a booktabs table: symbol | meaning | type | range | source

\subsection{Environment and timing}
\subsection{Optimization problems}
\begin{equation}
\label{eq:problem}
\max_{x}\ U(x;\theta)\quad \text{s.t.}\quad p\,x \le y
\end{equation}

\subsection{Equilibrium concept}
\begin{definition}[<name>]
\label{def:eq}
<Definition of the equilibrium.>
\end{definition}

\section{Solution and results}
\label{sec:results}
\subsection{First-order conditions and the closed form}
\begin{equation}
\label{eq:foc}
\frac{\partial U}{\partial x}=0
\;\Longrightarrow\;
x^{*}=\frac{y}{2p}
\end{equation}

\subsection{Propositions}
\begin{proposition}[<short name>]
\label{prop:1}
<Content, including the parameter conditions under which it holds.>
\end{proposition}
\begin{proof}[Derivation notes]
<Derivation notes (may point to the appendix).>
\end{proof}
\noindent\textbf{Economic meaning.} <One sentence.>

\subsection{Comparative statics}
% use a table: parameter | partial derivative of the endogenous variable | conditions | economic meaning

\section{Discussion}
\label{sec:discussion}
\subsection{Explaining the phenomenon}
\subsection{Policy implications}
\subsection{Limitations}
% at least 3 specific limitations: unobservable data, omitted general-equilibrium effects, assumed parameter values, static cross-section, etc.

\begin{thebibliography}{99}
% ⚠️ [VERIFIED] references only
\bibitem{akerlof1970} Akerlof, G. A. (1970). The Market for ``Lemons''. \textit{Quarterly Journal of Economics}.
\end{thebibliography}

\appendix
\section{Full derivations}
\section{Robustness and heterogeneity}
\section{Numerical detail and parameter sources}

\end{document}
```

---

## 3. Compilation options

| Option | Command | When it applies |
|------|------|------|
| **Primary: pdflatex** | `pdflatex -interaction=nonstopmode S9_paper.tex` (run twice) | Standard English-language papers |
| Alternative: xelatex | `xelatex -interaction=nonstopmode S9_paper.tex` | Needed if the text contains non-Latin scripts (then also load `fontspec` and use a suitable font) |
| Non-English text | Use `\documentclass{ctexart}` (Chinese) or an equivalent class and compile with **xelatex** | Only when the user explicitly wants a non-English paper |
| No LaTeX | Output the `.tex` plus `README_compile.md` | **Never fabricate a PDF** |

**Always check after compiling**: lines beginning with `!` in the `.log`; any `Undefined control sequence`;
whether cross-references show `??` (compile once more if so).

---

## 4. Figure and table conventions

### 4.1 Figures

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.75\textwidth]{figs/fig1_sweep_b.pdf}
  \caption{Sensitivity of equilibrium quantity to $b$ (\textbf{parameter sweep}). Benchmark parameters: $a=10,\ c=1$;
  $b$ ranges over $[0.2,2.0]$. The curve is a numerical computation, not a general result.}
  \label{fig:sweep}
\end{figure}
```

**Every figure must include**
- [ ] Axis labels (**with units**)
- [ ] A **figure-type label** in the caption: analytical result / numerical illustration / parameter sweep / mechanism sketch / computational result
- [ ] Benchmark parameter values and the range covered
- [ ] The necessary "not general" qualifier
- [ ] Both PNG (preview/slides) and PDF (for LaTeX)

### 4.2 Tables

```latex
\begin{table}[htbp]
  \centering
  \caption{Comparative statics}
  \begin{tabular}{llll}
    \toprule
    Parameter & $\partial x^{*}/\partial\theta$ & Conditions & Economic meaning \\
    \midrule
    $b$ & $-$ & $b>0,\ a>c$ & The larger the market, the more each firm produces \\
    \bottomrule
  \end{tabular}
\end{table}
```

- Use `booktabs` (`\toprule/\midrule/\bottomrule`), no vertical rules
- The table note should say where the parameter values come from (calibrated / estimated / illustrative)
- Put detailed numerical tables in the appendix

---

## 5. Pre-submission checklist (S9 gate)

**Content**
- [ ] The abstract contains no unproved strong causal claim (e.g. "…… causes ……")
- [ ] Every factual claim in the introduction has a source, or is explicitly labelled "we conjecture"
- [ ] Assumption numbers are cited in the text, and there is no assumption that is "defined but never used"
- [ ] Every proposition has: the parameter conditions under which it holds + proof/derivation notes + economic meaning
- [ ] Every comparative static carries its conditions
- [ ] The limitations section is specific (≥3 items), not boilerplate

**Evidence**
- [ ] **All** references are `[VERIFIED]`; unverified ones deleted
- [ ] Numerical conclusions are labelled by type in the body (numerical illustration / computational sketch)
- [ ] No "we prove" (for numerical results), "in general" (for a finite grid), "robust" (for a single point) anywhere in the paper

**Technical**
- [ ] The notation table is complete; no undefined symbol anywhere
- [ ] Equation numbering is consecutive; no `??` in cross-references
- [ ] Every figure and table has a label and a caption
- [ ] The PDF compiles successfully (non-empty, no errors)

---

## 6. Common rejection reasons (for self-checking)

The most frequent grounds for rejection in economics refereeing practice (check against these after S9 is complete):

1. **Insufficient contribution**: an existing model applied to a new setting, with no new mechanism (corresponds to a low D2)
2. **Conclusion = assumption**: an assumption restated as a proposition (low D3)
3. **Untestable**: core variables unobservable; the prediction conflicts with no conceivable data (low D5)
4. **Technically incomplete**: no existence/uniqueness, no second-order conditions, comparative statics with no conditions (low D4)
5. **Overclaiming**: a local result written up as general policy advice (low D5/D6)
6. **Fabricated literature**: citing a paper that does not exist, or attributing it to the wrong authors (fatal — and this skill has a verification gate specifically to prevent it)
