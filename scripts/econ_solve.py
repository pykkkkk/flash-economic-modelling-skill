#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
econ_solve.py —— computational engine for the econ-modeling-flash skill
=======================================================================

Subcommands:
  env    print the interpreter and dependency versions (for reproducibility notes)
  foc    first-order conditions / closed form / second-order conditions / numerical verification
  cs     comparative statics (implicit function theorem; symbolic + numerical sign determination)
  sim    numerical sweeps / two-parameter heat maps / CSV export
  lint   notation and assumption-convention check

Dependencies: sympy, numpy, matplotlib (pandas optional)
Every subcommand supports --out (markdown report) and --json-out (structured result).
On this machine PowerShell does not return stdout, so always use --out.

Expression-writing conventions (important)
------------------------------------------
1. Symbol names match the notation table exactly; `q_1` and `q1` are the same symbol (underscores are ignored).
2. **Always write `*` explicitly between symbols**: `2*b*q1`, `b*(q1+q2)`.
   Between a number and a symbol/bracket it may be omitted: `2b` is equivalent to `2*b`.
3. No "guessing" implicit multiplication: a run-together token is split automatically only when it can be
   decomposed entirely into **already-declared symbol names** (with `b`, `q1` declared, `bq1` -> `b*q1`);
   otherwise it is kept as a single symbol and a warning is issued.
   This avoids silent errors such as parsing `q1` as `q*1`.
4. Powers use `**` or `^`; the natural logarithm is `ln(x)` or `log(x)`.
5. Function names (exp/log/ln/sqrt/...) must be called with parentheses, not used as symbols.
"""

import argparse
import io
import json
import os
import re
import sys
import traceback
from datetime import datetime

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr,
        standard_transformations,
        convert_xor,
    )
except Exception as exc:  # pragma: no cover
    sys.stderr.write("sympy is required: %s\n" % exc)
    raise

TRANSFORMS = standard_transformations + (convert_xor,)
try:
    from sympy.parsing.sympy_parser import rationalize as _rationalize
    TRANSFORMS = TRANSFORMS + (_rationalize,)
except Exception:
    pass

# Function names: not usable as symbols and excluded from run-together decomposition
FUNC_NAMES = {
    "exp", "log", "ln", "sqrt", "cbrt", "sin", "cos", "tan", "cot", "sec", "csc",
    "asin", "acos", "atan", "sinh", "cosh", "tanh", "abs", "sign", "max", "min",
    "Piecewise", "Rational", "Integer", "Float", "Symbol", "LambertW", "erf",
    "floor", "ceiling", "factorial",
}
RESERVED = FUNC_NAMES | {
    "oo", "pi", "E", "I", "true", "false", "True", "False", "None", "Sum",
    "Integral", "Derivative", "diff", "solve", "beta", "gamma",
}
# Short-name protection: never decompose these even when possible (avoids disasters such as pi -> p*i)
NO_DECOMPOSE = {"pi", "e", "ln", "log", "exp", "max", "min", "abs", "oo", "dx", "dy", "dt"}

LATEX_WHITELIST = {
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta",
    "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma",
    "tau", "upsilon", "phi", "varphi", "chi", "psi", "omega", "Gamma", "Delta",
    "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi", "Omega",
    "text", "mathrm", "mathbf", "frac", "dfrac", "tfrac", "partial", "sum",
    "prod", "int", "infty", "cdot", "times", "div", "le", "leq", "ge", "geq",
    "neq", "approx", "equiv", "to", "Rightarrow", "rightarrow", "leftarrow",
    "left", "right", "big", "Big", "begin", "end", "label", "ref", "tag",
    "quad", "qquad", "space", "arg", "cline", "hline", "toprule", "midrule",
    "bottomrule", "textbf", "emph", "section", "subsection", "caption",
    "centering", "includegraphics", "hspace", "vspace", "par", "noindent",
    "item", "dot", "ldots", "cdots", "operatorname", "underset", "overset",
    "overline", "hat", "bar", "tilde", "star", "prime", "circ", "sim",
    "propto", "asymp", "ll", "gg", "substack", "displaystyle", "limits",
    "nonumber", "notag", "bm", "mathbb", "mathcal", "mathsf", "mathtt",
    "textnormal", "hfill", "protect", "and", "or", "not", "forall", "exists",
    "in", "notin", "subset", "cup", "cap", "emptyset", "nabla", "unlhd",
    "comment", "marginpar", "footnote", "url", "href", "cite", "bibitem",
    "star", "dag", "ddag", "s", "t", "c", "r", "l", "n", "k",
    # common wrappers and relation symbols that are NOT model symbols
    "boxed", "underbrace", "overbrace", "stackrel", "implies", "iff", "colon",
    "mid", "gtrless", "lessgtr", "norm", "mapsto", "xmapsto", "neg", "land", "lor",
    "Longrightarrow", "Longleftrightarrow", "longrightarrow", "longleftarrow",
    "textstyle", "scriptstyle", "binomial", "substack", "argmax", "argmin",
}

FIGS_DEFAULT = "figs"


# ----------------------------------------------------------------------------
# Text -> symbols / expressions
# ----------------------------------------------------------------------------

def norm_name(name):
    """Normalize a symbol name: ignore underscores (q_1 and q1 are the same symbol)."""
    return str(name).replace("_", "").strip()


def _greedy_decompose(tok, declared_norm_map):
    """Greedily decompose a run-together token using declared symbol names; return None on failure."""
    n = len(tok)
    names = sorted(declared_norm_map.keys(), key=len, reverse=True)
    memo = {}

    def go(i):
        if i == n:
            return []
        if i in memo:
            return memo[i]
        for nm in names:
            if tok.startswith(nm, i):
                rest = go(i + len(nm))
                if rest is not None:
                    memo[i] = [nm] + rest
                    return memo[i]
        memo[i] = None
        return None

    parts = go(0)
    if not parts:
        return None
    return [declared_norm_map[p] for p in parts]


def preprocess_expr(text, declared):
    """Safe preprocessing before parsing: decompose only with declared symbols, and insert * after numeric coefficients."""
    declared = [str(d).strip().lstrip("$").rstrip("$").strip() for d in (declared or []) if str(d).strip()]
    declared_norm_map = {}
    for d in declared:
        declared_norm_map.setdefault(norm_name(d), d)
    declared_set = set(declared)

    def _fix_token(m):
        tok = m.group(0)
        if tok in RESERVED or tok in declared_set:
            return tok
        if norm_name(tok) in NO_DECOMPOSE:
            return tok
        norm = norm_name(tok)
        if norm in declared_norm_map:
            return declared_norm_map[norm]
        dec = _greedy_decompose(norm, declared_norm_map)
        if dec and len(dec) > 1:
            return "*".join(dec)
        return tok

    t = re.sub(r"[A-Za-z_][A-Za-z_0-9]*", _fix_token, text)
    # 2b -> 2*b ; 2( -> 2*(   (excluding scientific notation such as 1e-9)
    t = re.sub(r"(?<=[0-9])\s*(?=[A-Za-z_])(?![eE][+-]?[0-9])", "*", t)
    t = re.sub(r"(?<=[0-9])\s*(?=\()", "*", t)
    # )( , )2 , )b  -> insert *
    t = re.sub(r"(?<=\))\s*(?=[(A-Za-z_0-9])", "*", t)
    # A declared symbol followed by ( -> treat as multiplication (an undeclared identifier
    # followed by ( is left alone, so parsing fails and the missing * gets discovered)
    def _before_paren(m):
        name = m.group(1)
        if name in FUNC_NAMES:
            return name + "("
        if name in declared_set or norm_name(name) in declared_norm_map:
            return name + "*("
        return name + "("

    t = re.sub(r"([A-Za-z_][A-Za-z_0-9]*)\s*\(", _before_paren, t)
    return t


def parse_math(text, syms=None, declared=None):
    """Parse an expression; return (expr, preprocessed_text)."""
    declared = declared if declared is not None else list((syms or {}).keys())
    pre = preprocess_expr(text, declared)
    local = {"ln": sp.log, "log": sp.log}
    if syms:
        local.update(syms)
    try:
        expr = parse_expr(pre, local_dict=local, transformations=TRANSFORMS, evaluate=True)
    except Exception as exc:
        raise ValueError(
            "failed to parse expression: %r\n  after preprocessing: %r\n  reason: %s\n"
            "  common causes: a missing `*` between symbols (e.g. b(q1+q2) written instead of b*(q1+q2)); "
            "a symbol name that does not match the notation table; a function name used as a variable." % (text, pre, exc)
        )
    return expr, pre


def collect_tokens(texts):
    toks = set()
    for t in texts:
        for m in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", t or ""):
            if m in RESERVED:
                continue
            toks.add(m)
    return sorted(toks)


def declared_names(spec):
    names = []
    for key in ("params", "endogenous"):
        for n in spec.get(key) or []:
            names.append(str(n))
    for s in spec.get("symbols") or []:
        if isinstance(s, dict) and s.get("sym"):
            names.append(str(s["sym"]))
        elif isinstance(s, str):
            names.append(s)
    for ag in spec.get("agents") or []:
        for n in ag.get("vars") or []:
            names.append(str(n))
    for m in spec.get("_extra_declared") or []:
        names.append(str(m))
    out = []
    for n in names:
        n = n.strip().lstrip("$").rstrip("$").strip()
        if n and n not in out:
            out.append(n)
    return out


def build_symbols(texts, positive=(), declared=()):
    positive = set(positive or ())
    syms = {}
    pool = set(collect_tokens(texts)) | set(declared or ())
    for tok in sorted(pool):
        if norm_name(tok) in NO_DECOMPOSE and tok not in set(declared or ()):
            continue
        syms[tok] = sp.Symbol(tok, positive=True) if tok in positive else sp.Symbol(tok)
    for tok in positive:
        syms.setdefault(tok, sp.Symbol(tok, positive=True))
    return syms


def undefined_functions(expr):
    """Find names parsed as "undefined function calls" (usually a missing `*`, e.g. q(q1+q2))."""
    try:
        from sympy.core.function import AppliedUndef
        names = set()
        for f in expr.atoms(AppliedUndef):
            names.add(str(f.func))
        return sorted(names)
    except Exception:
        return []


def suspicious_symbols(syms, declared):
    """Run-together multi-letter symbols (possibly a missing *): a warning only, never blocking."""
    declared_norm = {norm_name(d) for d in declared}
    out = []
    for name in sorted(syms):
        if name in FUNC_NAMES or name in RESERVED:
            continue
        if norm_name(name) in declared_norm:
            continue
        if re.fullmatch(r"[A-Za-z]{2,}[0-9]*", name):
            out.append(name)
    return out


def best_form(expr):
    """Pick the shortest display form among several rearrangements."""
    cands = [("as-is", expr)]
    for label, fn in (("simplify", lambda z: sp.simplify(z)),
                      ("radsimp", lambda z: sp.radsimp(z)),
                      ("powsimp", lambda z: sp.powsimp(z, force=True)),
                      ("simplify+radsimp", lambda z: sp.radsimp(sp.simplify(z)))):
        try:
            cands.append((label, fn(expr)))
        except Exception:
            pass
    best, best_len, best_label = expr, len(str(expr)), "as-is"
    for label, c in cands:
        s = len(str(c))
        if s < best_len:
            best, best_len, best_label = c, s, label
    return best, (best_label if best_label != "as-is" else None)


def sstr(expr):
    try:
        return sp.sstr(sp.simplify(expr))
    except Exception:
        return sp.sstr(expr)


def sign_mark(expr, point=None):
    try:
        e = sp.simplify(expr)
    except Exception:
        e = expr
    try:
        if e == 0:
            return "0", "identically zero"
        if e.is_positive is True:
            return "+", "determined directly by the sign assumptions"
        if e.is_negative is True:
            return "−", "determined directly by the sign assumptions"
        if e.is_nonnegative is True:
            return "+", "non-negative (may be 0)"
        if e.is_nonpositive is True:
            return "−", "non-positive (may be 0)"
    except Exception:
        pass
    if point:
        num = eval_point(e, point)
        if num is not None:
            if abs(num) < 1e-12:
                return "0", "numerically 0 at this point (possibly a critical point)"
            return ("+" if num > 0 else "−"), "numerical determination (at this point only; not a general result)"
    return "?", "sign undetermined -- additional parameter assumptions required"


def eval_point(expr, point):
    """Substitute numbers by **symbol name** (avoids mismatches between Symbol('a') and Symbol('a', positive=True))."""
    if not point:
        return None
    try:
        subs_map = {}
        for s in expr.free_symbols:
            if s.name in point:
                try:
                    subs_map[s] = sp.Float(float(point[s.name]))
                except Exception:
                    return None
        if not subs_map:
            return None
        sub = expr.subs(subs_map)
        v = complex(sub.evalf())
        if abs(v.imag) > 1e-9:
            return None
        return v.real
    except Exception:
        return None


def ensure_dir(path):
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)


def write_text(path, text):
    ensure_dir(path)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def write_json(path, obj):
    ensure_dir(path)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def load_spec(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_point(spec):
    for key in ("params_values", "agent_params", "base", "evaluate_at"):
        if isinstance(spec.get(key), dict) and spec[key]:
            return {k: float(v) for k, v in spec[key].items()}
    cs = spec.get("comparative_statics") or {}
    if isinstance(cs, dict) and isinstance(cs.get("evaluate_at"), dict) and cs["evaluate_at"]:
        return {k: float(v) for k, v in cs["evaluate_at"].items()}
    return {}


def positive_list(spec):
    out = list(spec.get("positive_symbols") or [])
    cs = spec.get("comparative_statics") or {}
    out += list(cs.get("positive_params") or [])
    seen, res = set(), []
    for s in out:
        if s not in seen:
            seen.add(s)
            res.append(s)
    return res


# ----------------------------------------------------------------------------
# Model assembly
# ----------------------------------------------------------------------------

def build_system(spec):
    declared = declared_names(spec)
    texts = []
    for ag in spec.get("agents") or []:
        texts.append(ag.get("objective", ""))
    for eq in spec.get("equations") or []:
        texts.append(eq)
    texts += list(spec.get("params") or [])
    texts += list(spec.get("endogenous") or [])
    texts += declared

    syms = build_symbols(texts, positive=positive_list(spec), declared=declared)
    decl_set = list(set(declared) | set(syms.keys()))

    echo = []
    agents_out = []
    focs = []

    for ag in spec.get("agents") or []:
        name = ag.get("name", "agent")
        obj, pre = parse_math(ag["objective"], syms, decl_set)
        echo.append((name, ag["objective"], pre, str(obj)))
        vars_ = [syms[v] if v in syms else sp.Symbol(v) for v in ag["vars"]]
        maximize = bool(ag.get("maximize", True))
        ag_focs = [(v, sp.diff(obj, v)) for v in vars_]
        agents_out.append({"name": name, "objective": obj, "vars": vars_,
                           "maximize": maximize, "focs": ag_focs})
        for v, e in ag_focs:
            focs.append(("%s: d/d%s" % (name, v), e))

    for i, eq_text in enumerate(spec.get("equations") or []):
        e, pre = parse_math(eq_text, syms, decl_set)
        echo.append(("eq%d" % (i + 1), eq_text, pre, str(e)))
        if isinstance(e, sp.Equality):
            e = e.lhs - e.rhs
        focs.append(("eq%d" % (i + 1), e))

    endog = spec.get("endogenous")
    if endog:
        endog_syms = [syms[v] if v in syms else sp.Symbol(v) for v in endog]
    else:
        endog_syms = []
        for ag in agents_out:
            for v in ag["vars"]:
                if v not in endog_syms:
                    endog_syms.append(v)

    params = spec.get("params")
    if params:
        param_syms = [syms[p] if p in syms else sp.Symbol(p) for p in params]
    else:
        used = set()
        for _, e in focs:
            used |= e.free_symbols
        for ag in agents_out:
            used |= ag["objective"].free_symbols
        param_syms = sorted([s for s in used if s not in endog_syms], key=lambda z: z.name)

    return {"symbols": syms, "agents": agents_out, "focs": focs, "endog": endog_syms,
            "params": param_syms, "echo": echo, "declared": declared}


def echo_section(L, sysm):
    L.append("## Parse echo (check by hand, to catch a missing `*` that would be misparsed)")
    L.append("")
    L.append("| Input | After preprocessing | Parsed result |")
    L.append("|---|---|---|")
    for label, orig, pre, res in sysm["echo"]:
        L.append("| `%s`: `%s` | `%s` | `%s` |" % (label, orig, pre, res))
    L.append("")
    sus = suspicious_symbols(sysm["symbols"], sysm["declared"])
    if sus:
        L.append("> ⚠️ Run-together multi-letter symbols detected: %s. If you meant multiplication, write `*` explicitly (e.g. `b*q1`)." % ", ".join("`%s`" % s for s in sus))
        L.append("")
    # Inputs parsed as function calls: very likely a missing `*` (e.g. q(q1+q2))
    bad = []
    for nm, _o, _p, res in sysm["echo"]:
        funs = undefined_functions(sp.sympify(res))
        if funs:
            bad.append((nm, ", ".join("`%s`" % f for f in funs)))
    if bad:
        L.append("> ⚠️ **Some input was parsed as a \"function call\"**: %s. If you meant multiplication, write `*(`; "
                 "if you really intend an abstract function such as u(c), note that this engine can only return "
                 "implicit derivatives and cannot deliver an explicit closed-form solution." % "; ".join(
                     "%s -> %s" % (a, b) for a, b in bad))
        L.append("")
    return sus


# ----------------------------------------------------------------------------
# foc
# ----------------------------------------------------------------------------

def cmd_foc(spec, args):
    L, J = [], {}
    L.append("# S4 solution report (foc)")
    L.append("")
    L.append("- Title: %s" % spec.get("title", "(untitled)"))
    L.append("- Generated at: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("")

    sysm = build_system(spec)
    point = get_point(spec)

    L.append("## 0. Notation")
    L.append("")
    L.append("- Endogenous variables: %s" % (", ".join(str(s) for s in sysm["endog"]) or "(none)"))
    L.append("- Parameters: %s" % (", ".join(str(s) for s in sysm["params"]) or "(none)"))
    L.append("")
    J["endogenous"] = [str(s) for s in sysm["endog"]]
    J["params"] = [str(s) for s in sysm["params"]]

    if not sysm["agents"] and not spec.get("equations"):
        L.append("> ⚠️ The spec has neither `agents` nor `equations`; nothing to solve.")
        return finish(L, J, args)

    J["suspicious_symbols"] = echo_section(L, sysm)
    J["agents"] = []

    for ag in sysm["agents"]:
        L.append("## %s" % ag["name"])
        L.append("")
        L.append("**Objective**")
        L.append("")
        L.append("$$ %s\\;\\; %s $$" % ("\\max" if ag["maximize"] else "\\min", sp.latex(ag["objective"])))
        L.append("")
        L.append("**First-order conditions**")
        L.append("")
        for v, e in ag["focs"]:
            L.append("- $\\partial/\\partial %s:\\quad %s = 0$" % (sp.latex(v), sp.latex(sp.simplify(e))))
        L.append("")
        for v, e in ag["focs"]:
            try:
                sol = sp.solve(sp.Eq(e, 0), v, dict=True)
            except Exception as exc:
                sol = []
                L.append("> Solving for %s failed: %s" % (v, exc))
            L.append("- Best response for %s: %s" % (v, sol if sol else "no closed form found"))
        L.append("")

        L.append("**Second-order conditions**")
        L.append("")
        soc = {}
        if len(ag["vars"]) == 1:
            v = ag["vars"][0]
            d2 = sp.simplify(sp.diff(ag["objective"], v, 2))
            sign, why = sign_mark(d2, point)
            need = "−" if ag["maximize"] else "+"
            ok = (sign == need)
            L.append("- $f''(%s) = %s$ -> sign **%s** (%s)" % (v, sp.latex(d2), sign, why))
            L.append("- Criterion: a %s problem requires the second derivative to be %s -> **%s**" % (
                "maximization" if ag["maximize"] else "minimization", need, "satisfied" if ok else "not satisfied / could not be determined"))
            soc = {"expr": str(d2), "sign": sign, "why": why, "satisfied": bool(ok)}
        else:
            H = sp.hessian(ag["objective"], ag["vars"])
            L.append("- Hessian: $%s$" % sp.latex(H))
            minors = []
            for k in range(1, len(ag["vars"]) + 1):
                m = sp.simplify(H[:k, :k].det())
                sign, why = sign_mark(m, point)
                minors.append({"k": k, "det": str(m), "sign": sign})
                L.append("  - Leading principal minor of order %d $= %s$ -> sign **%s**" % (k, sp.latex(m), sign))
            if ag["maximize"]:
                want = ["−"] * len(ag["vars"])
                want_desc = "all negative (Hessian negative definite)"
            else:
                want = ["−" if i % 2 == 0 else "+" for i in range(len(ag["vars"]))]
                want_desc = "alternating − + − ... (Hessian positive definite), expected %s" % "".join(want)
            ok = [m["sign"] for m in minors] == want
            L.append("- Criterion: a %s problem requires %s -> **%s**" % (
                "maximization" if ag["maximize"] else "minimization", want_desc, "satisfied" if ok else "not satisfied / could not be determined"))
            soc = {"hessian": str(H), "minors": minors, "satisfied": bool(ok)}
            if point:
                num = eval_numeric_hessian(ag, point)
                if num is not None:
                    valtxt = ", ".join("%.6g" % x for x in num)
                    L.append("- Hessian eigenvalues at the given parameter point (endogenous variables set to 1): %s" % valtxt)
                    if not all(_is_finite(x) for x in num):
                        L.append("- Numerical criterion (at this point): **cannot be determined** (an eigenvalue is non-finite, "
                                 "usually because some variable is 0 and a power function diverges; check the functional form or use symbolic determination)")
                        soc["numeric_eigenvalues"] = [str(x) for x in num]
                    else:
                        good = all(x < 1e-9 for x in num) if ag["maximize"] else all(x > -1e-9 for x in num)
                        L.append("- Numerical criterion (at this point): **%s**" % ("satisfied" if good else "not satisfied"))
                        soc["numeric_eigenvalues"] = [float(x) for x in num]
        L.append("")
        J["agents"].append({"name": ag["name"], "objective": str(ag["objective"]),
                            "focs": [{"var": str(v), "expr": str(e)} for v, e in ag["focs"]],
                            "soc": soc})

    # Joint solution
    solve_cfg = spec.get("solve") or {}
    tgt_names = solve_cfg.get("for") or [str(s) for s in sysm["endog"]]
    syms = sysm["symbols"]
    tgt_syms = []
    for t in tgt_names:
        tgt_syms.append(syms[t] if t in syms else sp.Symbol(t))

    if solve_cfg.get("use") == "equations" and spec.get("equations"):
        focs_for_solve = [e for nm, e in sysm["focs"] if nm.startswith("eq")]
    else:
        focs_for_solve = [e for _, e in sysm["focs"]]

    L.append("## Joint closed-form solution")
    L.append("")
    solution = None
    if tgt_syms and focs_for_solve:
        try:
            sol_list = sp.solve([sp.Eq(e, 0) for e in focs_for_solve], tgt_syms, dict=True)
        except Exception as exc:
            sol_list = []
            L.append("> solve raised an exception: %s" % exc)
        if sol_list:
            solution = sol_list[0]
            L.append("Closed-form solution found:")
            L.append("")
            for k, v in solution.items():
                disp, how = best_form(v)
                L.append("- $%s^{*} = %s$" % (sp.latex(k), sp.latex(disp)))
                if how:
                    L.append("  - (display form: %s)" % how)
            longest = max((len(str(v)) for v in solution.values()), default=0)
            if longest > 120:
                L.append("")
                L.append("> ⚠️ The closed form is long (at most about %d characters) and hard to read. Suggestions: (1) for multiplicative "
                         "setups (Cobb-Douglas / CES), **take logs before solving** to obtain a linear, compact expression; "
                         "(2) or report only the **signs of the comparative statics** (the `cs` subcommand) instead of the level solution." % longest)
            if len(sol_list) > 1:
                L.append("")
                L.append("> ⚠️ There are %d solution sets; only the first is listed above -- check the others (multiple equilibria are possible)." % len(sol_list))
                for i, s in enumerate(sol_list[1:], 2):
                    L.append("> - Solution %d: %s" % (i, {str(k): sstr(v) for k, v in s.items()}))
        else:
            L.append("**No closed-form solution found** (the first-order conditions were solved simultaneously). Degradation suggestions (try in order):")
            L.append("")
            L.append("1. Simplify the functional form (CES -> Cobb-Douglas, general form -> linear)")
            L.append("2. Reduce to a two-agent / two-period version")
            L.append("3. Linearize locally at the symmetric point or the steady state")
            L.append("4. Fix one parameter (e.g. set alpha = 1/2) to make it solvable")
            L.append("5. Report only a numerical illustration + local comparative statics, **flagged prominently in the report**")
    L.append("")

    L.append("## Numerical back-substitution verification")
    L.append("")
    if not point:
        L.append("> The spec provides no parameter values (`params_values` / `agent_params` / `base`); skipping.")
    else:
        L.append("- Parameter values: `%s`" % json.dumps(point, ensure_ascii=False))
        L.append("")
        # First evaluate the closed form at the parameter point, then substitute everything into the
        # first-order conditions together; only then is the residual a real test
        val_map = dict(point)
        sol_vals = {}
        if solution:
            L.append("**Closed form evaluated at the given parameters**")
            L.append("")
            for k, v in solution.items():
                val = eval_point(v, point)
                sol_vals[str(k)] = val
                feasible = ""
                if val is not None:
                    feasible = " (>0, satisfies the non-negativity constraint)" if val > 0 else (
                        " (=0, corner solution)" if abs(val) < 1e-12 else " (<0, **infeasible solution; check the parameters**)")
                L.append("- $%s^{*} = %s$ %s" % (
                    sp.latex(k), ("%.6g" % val) if val is not None else "cannot be evaluated", feasible))
                if val is not None:
                    val_map[str(k)] = val
            L.append("")
        if not solution:
            L.append("> No closed form, so the first-order conditions still contain endogenous variables. "
                     "To verify numerically, **supply the endogenous variables' values as well** in the spec's `params_values`.")
            L.append("")

        L.append("**First-order-condition residuals** (parameter values and solution substituted in)")
        L.append("")
        max_res, missing = 0.0, set()
        for nm, e in sysm["focs"]:
            r = eval_point(e, val_map)
            if r is None:
                miss = sorted(str(s) for s in e.free_symbols
                              if str(s) not in val_map)
                missing |= set(miss)
                L.append("- %s: cannot be evaluated numerically (missing values: %s)" % (nm, ", ".join(miss) or "?"))
                continue
            max_res = max(max_res, abs(r))
            L.append("- %s: residual = %.3e" % (nm, r))
        L.append("")
        if missing:
            L.append("- ⚠️ The following symbols have no values, so verification cannot be completed: %s" % ", ".join(sorted(missing)))
            L.append("")
        L.append("- **Max first-order-condition residual = %.3e** -> %s" % (
            max_res, "PASS (< 1e-9)" if max_res < 1e-9 and not missing
            else ("FAIL, check the solution or the parameters" if not missing else "could not be fully verified")))
        J["verification"] = {"point": point, "max_abs_foc_residual": max_res,
                             "solution_values": sol_vals,
                             "missing_values": sorted(missing)}

    J["solution"] = {str(k): sstr(v) for k, v in solution.items()} if solution else None
    return finish(L, J, args)


def _is_finite(x):
    try:
        import math
        return math.isfinite(float(x))
    except Exception:
        return False


def eval_numeric_hessian(ag, point):
    """Numerically evaluate the Hessian at a given parameter point (endogenous variables set to 1); return eigenvalues in ascending order."""
    try:
        import numpy as np
        H = sp.hessian(ag["objective"], ag["vars"])
        p = {str(v): 1.0 for v in ag["vars"]}
        p.update(point)
        rows = []
        for i in range(H.rows):
            row = []
            for j in range(H.cols):
                v = eval_point(H[i, j], p)
                if v is None:
                    return None
                row.append(v)
            rows.append(row)
        arr = np.array(rows, dtype=float)
        return np.linalg.eigvalsh(arr)
    except Exception:
        return None


# ----------------------------------------------------------------------------
# cs
# ----------------------------------------------------------------------------

def cmd_cs(spec, args):
    L, J = [], {}
    L.append("# S7 comparative-statics report (cs, implicit function theorem)")
    L.append("")
    L.append("- Title: %s" % spec.get("title", "(untitled)"))
    L.append("- Generated at: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("")

    sysm = build_system(spec)
    cs = spec.get("comparative_statics") or {}
    point = cs.get("evaluate_at") or get_point(spec)
    point = {k: float(v) for k, v in point.items()} if point else {}

    syms = sysm["symbols"]
    endog = [syms[v] if v in syms else sp.Symbol(v)
             for v in (cs.get("endogenous") or [str(s) for s in sysm["endog"]])]
    params = [syms[v] if v in syms else sp.Symbol(v)
              for v in (cs.get("params") or [str(s) for s in sysm["params"]])]

    decl_set = list(set(sysm["declared"]) | set(syms.keys()))
    if cs.get("equations"):
        F = []
        for t in cs["equations"]:
            e, _pre = parse_math(t, syms, decl_set)
            if isinstance(e, sp.Equality):
                e = e.lhs - e.rhs
            F.append(e)
    else:
        F = [e for _, e in sysm["focs"]]

    if not F:
        L.append("> ⚠️ No equilibrium conditions (neither `agents` nor `equations`).")
        return finish(L, J, args)

    echo_section(L, sysm)

    L.append("## 1. Equilibrium-condition system $F(x;\\theta)=0$")
    L.append("")
    for i, e in enumerate(F, 1):
        L.append("- $F_{%d}:\\quad %s = 0$" % (i, sp.latex(sp.simplify(e))))
    L.append("")
    L.append("- Endogenous variables $x$: %s" % ", ".join("$%s$" % sp.latex(s) for s in endog))
    L.append("- Parameters $\\theta$: %s" % ", ".join("$%s$" % sp.latex(s) for s in params))
    L.append("")

    if len(F) != len(endog):
        L.append("> ⚠️ The number of equilibrium conditions (%d) and of endogenous variables (%d) differ, so the Jacobian is "
                 "not square and the implicit function theorem does not apply directly." % (len(F), len(endog)))

    Jm = sp.Matrix([[sp.diff(e, v) for v in endog] for e in F])
    dFdt = sp.Matrix([[sp.diff(e, p) for p in params] for e in F])

    L.append("## 2. Jacobian matrix $J=\\partial F/\\partial x$")
    L.append("")
    L.append("$$ J = %s $$" % sp.latex(sp.simplify(Jm)))
    L.append("")
    if Jm.rows == Jm.cols:
        detJ = sp.simplify(Jm.det())
        signJ, whyJ = sign_mark(detJ, point)
        L.append("- $\\det J = %s$ -> sign **%s** (%s)" % (sp.latex(detJ), signJ, whyJ))
        L.append("- Hint: the second-order conditions (negative/positive definiteness) usually already fix the sign of $\\det J$, which can be used to sign the comparative statics.")
    else:
        L.append("- Not square, so there is no determinant.")
    L.append("")

    L.append("## 3. Comparative statics: $\\mathrm dx/\\mathrm d\\theta = -J^{-1}\\,\\partial F/\\partial\\theta$")
    L.append("")
    results = []
    try:
        dX = -Jm.inv() * dFdt
        L.append("$$ \\frac{\\mathrm dx}{\\mathrm d\\theta} = %s $$" % sp.latex(sp.simplify(dX)))
        L.append("")

        # If the equilibrium has a unique closed form, substitute it so the derivatives contain
        # only parameters (easier to sign and to report)
        dX_use = dX
        subst_note = None
        if len(F) == len(endog):
            try:
                eqs = [sp.Eq(e, 0) for e in F]
                sols = sp.solve(eqs, endog, dict=True)
            except Exception:
                sols = []
            if len(sols) == 1 and sols[0]:
                try:
                    cand = sp.simplify(dX.subs(sols[0]))
                    if cand != dX:
                        dX_use = cand
                        subst_note = sols[0]
                except Exception:
                    pass
        if subst_note:
            L.append("After substituting the equilibrium solution (parameters only, which makes the sign easier to read):")
            L.append("")
            L.append("$$ \\frac{\\mathrm dx^{*}}{\\mathrm d\\theta} = %s $$" % sp.latex(sp.simplify(dX_use)))
            L.append("")
            L.append("> Equilibrium solution substituted in: %s" % ", ".join(
                "$%s^{*}=%s$" % (sp.latex(k), sp.latex(sp.simplify(v))) for k, v in subst_note.items()))
            L.append("")
        elif len(F) == len(endog):
            L.append("> The equilibrium has multiple solutions or no closed form, so the derivatives below are still "
                     "expressed in $x$ (not substituted). Sign determination should then combine the second-order conditions or a numerical point.")
            L.append("")

        L.append("| Parameter $\\theta$ | " + " | ".join("$\\partial %s/\\partial\\theta$" % sp.latex(v) for v in endog) + " |")
        L.append("|---|" + "---|" * len(endog))
        for r in range(len(params)):
            row = ["$%s$" % sp.latex(params[r])]
            for c in range(len(endog)):
                row.append("$%s$" % sp.latex(sp.simplify(dX_use[c, r])))
            L.append("| " + " | ".join(row) + " |")
        L.append("")
        L.append("## 4. Sign determination and conditions")
        L.append("")
        L.append("| Parameter | Endogenous | Sign | Basis | Value (at the given point) |")
        L.append("|---|---|---|---|---|")
        undetermined = []
        for r, p in enumerate(params):
            for c, v in enumerate(endog):
                e = sp.simplify(dX_use[c, r])
                sgn, why = sign_mark(e, point)
                num = eval_point(e, point) if point else None
                L.append("| $%s$ | $%s$ | **%s** | %s | %s |" % (
                    sp.latex(p), sp.latex(v), sgn, why,
                    ("%.6g" % num) if num is not None else "—"))
                if sgn == "?":
                    undetermined.append((str(p), str(v)))
                results.append({"param": str(p), "endog": str(v), "expr": str(e),
                                "sign": sgn, "why": why, "numeric": num})
        L.append("")
        if undetermined:
            L.append("**Undetermined signs** (additional parameter assumptions are needed, or discuss piecewise over parameter regions):")
            L.append("")
            for p, v in undetermined:
                L.append("- $\\partial %s/\\partial %s$" % (v, p))
            L.append("")
            L.append("> Suggested handling: (1) add these parameters to the spec's `positive_params`; "
                     "(2) add sign assumptions for the parameters concerned, or restrict their ranges; "
                     "(3) state it piecewise: \"the sign is + when $\\theta<\\hat\\theta$ and − otherwise\".")
        else:
            n_num = len([r for r in results if "numerical determination" in (r.get("why") or "")])
            if n_num:
                L.append("All signs are determined, but **%d of them only by the numeric value at the given parameter point** -- "
                         "strictly speaking they hold \"at that point\", and becoming a general conclusion requires additional "
                         "parameter assumptions (e.g. declaring the sign of each relevant parameter, or restricting its range)." % n_num)
            else:
                L.append("Every comparative-statics sign is **determined directly** by the parameter assumptions (which is stronger than a numerical determination).")
        L.append("")
        L.append("> ⚠️ Sign determination depends on the declared parameter assumptions. The report **must** state the conditions; a bare sign is not enough.")
    except Exception as exc:
        L.append("> ⚠️ The Jacobian is singular (or not square): **the implicit function theorem does not apply**, so comparative statics cannot be derived by the standard method.")
        L.append(">")
        L.append("> Reason: %s" % exc)
        L.append(">")
        L.append("> Check: (1) a missing equilibrium condition; (2) an exogenous variable listed among the endogenous ones; "
                 "(3) whether the parameter point lies on a singular manifold.")

    J["comparative_statics"] = results
    return finish(L, J, args)


# ----------------------------------------------------------------------------
# sim
# ----------------------------------------------------------------------------

def setup_cjk_font():
    try:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import font_manager, rcParams
        for p in (r"C:/Windows/Fonts/simhei.ttf", r"C:/Windows/Fonts/msyh.ttc",
                  r"C:/Windows/Fonts/simsun.ttc"):
            if os.path.exists(p):
                try:
                    font_manager.fontManager.addfont(p)
                    name = font_manager.FontProperties(fname=p).get_name()
                    rcParams["font.sans-serif"] = [name] + list(rcParams["font.sans-serif"])
                    rcParams["axes.unicode_minus"] = False
                    return name
                except Exception:
                    continue
    except Exception:
        pass
    return None


def cmd_sim(spec, args):
    L, J = [], {}
    L.append("# S7 numerical sensitivity report (sim)")
    L.append("")
    L.append("- Title: %s" % spec.get("title", "(untitled)"))
    L.append("- Generated at: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("")

    try:
        import numpy as np
    except Exception as exc:
        L.append("> numpy is required: %s" % exc)
        return finish(L, J, args)

    cjk_name = setup_cjk_font() if spec.get("cjk_font", True) else None
    L.append("- Non-Latin font fallback: %s" % (cjk_name or "disabled / not found (use ASCII labels if this matters)"))
    L.append("- **Declaration**: everything below is a **numerical illustration**, used to show the direction of a "
             "mechanism. It is neither a general conclusion nor robustness evidence.")
    L.append("")

    base = {k: float(v) for k, v in (spec.get("base") or {}).items()}
    exprs = spec.get("expressions") or {}
    if not exprs:
        L.append("> ⚠️ The spec is missing `expressions`.")
        return finish(L, J, args)

    declared = list(base.keys()) + collect_tokens(list(exprs.values()))
    syms = build_symbols(list(exprs.values()) + declared, declared=declared)

    L.append("## 1. Benchmark parameters and expressions")
    L.append("")
    L.append("- Benchmark parameters: `%s`" % json.dumps(base, ensure_ascii=False))
    L.append("")
    parsed, echoes = {}, []
    for k, v in exprs.items():
        try:
            e, pre = parse_math(v, syms, declared)
            parsed[k] = e
            echoes.append((k, v, pre, str(e)))
            L.append("- `%s = %s`" % (k, v))
        except Exception as exc:
            L.append("> Failed to parse `%s`: %s" % (k, exc))
    L.append("")
    if echoes:
        L.append("Parse echo (check this):")
        L.append("")
        for k, orig, pre, res in echoes:
            L.append("- `%s`: `%s` -> `%s` -> `%s`" % (k, orig, pre, res))
        L.append("")

    L.append("## 2. Benchmark values")
    L.append("")
    base_vals = {}
    for k, e in parsed.items():
        val = eval_point(e, base)
        base_vals[k] = val
        L.append("- %s = %s" % (k, ("%.6g" % val) if val is not None else "cannot be evaluated"))
    L.append("")
    J["base_values"] = base_vals
    J["figures"] = []

    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        L.append("> matplotlib is required to produce figures: %s" % exc)
        plt = None

    for idx, pl in enumerate(spec.get("plots") or [], 1):
        ptype = pl.get("type", "sweep")
        out = pl.get("output") or os.path.join(FIGS_DEFAULT, "fig%d.png" % idx)
        L.append("## 3.%d Figure: %s" % (idx, pl.get("title", out)))
        L.append("")

        if ptype == "sweep":
            vary = pl.get("vary") or []
            if not vary:
                L.append("> Missing `vary`.")
                continue
            v0 = vary[0]
            arr0 = np.linspace(float(v0["range"][0]), float(v0["range"][1]), int(v0["range"][2]))
            series_names = list(pl.get("y") or parsed.keys())
            groups = [None]
            if len(vary) > 1:
                v1 = vary[1]
                arr1 = np.linspace(float(v1["range"][0]), float(v1["range"][1]), int(v1["range"][2]))
                if len(arr1) > 5:
                    arr1 = arr1[np.linspace(0, len(arr1) - 1, 5).round().astype(int)]
                groups = [float(g) for g in arr1]
            fig, ax = (plt.subplots(figsize=(6.4, 4.2), dpi=150) if plt is not None else (None, None))
            data_rows = []
            for g in groups:
                for nm in series_names:
                    e = parsed.get(nm)
                    if e is None:
                        continue
                    ys = []
                    for x in arr0:
                        p = dict(base)
                        p[v0["name"]] = float(x)
                        if g is not None:
                            p[vary[1]["name"]] = float(g)
                        val = eval_point(e, p)
                        ys.append(np.nan if val is None else val)
                    ys = np.array(ys, dtype=float)
                    label = nm if g is None else "%s (%s=%.3g)" % (nm, vary[1]["name"], g)
                    if ax is not None:
                        ax.plot(arr0, ys, linewidth=1.8, label=label)
                    if g is None:
                        finite = np.isfinite(ys)
                        if not finite.any():
                            L.append("- `%s`: cannot be evaluated anywhere in the interval." % nm)
                        else:
                            d = np.diff(ys[finite])
                            trend = "monotonically increasing" if np.all(d > 0) else (
                                "monotonically decreasing" if np.all(d < 0) else "non-monotone (an interior extremum exists)")
                            i_min, i_max = int(np.nanargmin(ys)), int(np.nanargmax(ys))
                            L.append("- `%s`: over %s in [%g, %g] it goes from %.6g to %.6g, %s; "
                                     "minimum %.6g at %s=%.6g, maximum %.6g at %s=%.6g" % (
                                         nm, v0["name"], arr0[0], arr0[-1], ys[0], ys[-1], trend,
                                         np.nanmin(ys), v0["name"], arr0[i_min],
                                         np.nanmax(ys), v0["name"], arr0[i_max]))
                    data_rows.append((g, nm, arr0.copy(), ys.copy()))
            if ax is not None:
                if pl.get("logx"):
                    ax.set_xscale("log")
                if pl.get("logy"):
                    ax.set_yscale("log")
                ax.set_xlabel(pl.get("xlabel", v0["name"]))
                ax.set_ylabel(pl.get("ylabel", ""))
                ax.set_title(pl.get("title", ""))
                ax.grid(alpha=0.3)
                ax.legend(fontsize=8)
                fig.tight_layout()
                ensure_dir(out)
                fig.savefig(out)
                J["figures"].append(out)
                L.append("- Saved: `%s`" % out)
                if pl.get("also_pdf"):
                    pdf = os.path.splitext(out)[0] + ".pdf"
                    fig.savefig(pdf)
                    J["figures"].append(pdf)
                    L.append("- Saved: `%s`" % pdf)
                plt.close(fig)
            if pl.get("csv"):
                csvp = os.path.splitext(out)[0] + ".csv"
                lines = ["group,name,x,y"]
                for g, nm, xs, ys in data_rows:
                    for a, b in zip(xs, ys):
                        lines.append("%s,%s,%.10g,%.10g" % ("" if g is None else "%.10g" % g, nm, a, b))
                write_text(csvp, "\n".join(lines))
                J["figures"].append(csvp)
                L.append("- Saved data: `%s`" % csvp)

        elif ptype == "heatmap":
            xcfg, ycfg = pl.get("x"), pl.get("y")
            e = parsed.get(pl.get("z"))
            if not (xcfg and ycfg and e is not None):
                L.append("> heatmap requires `x`, `y` (each with name/range) and `z` (a key in `expressions`).")
                continue
            xs = np.linspace(float(xcfg["range"][0]), float(xcfg["range"][1]), int(xcfg["range"][2]))
            ys = np.linspace(float(ycfg["range"][0]), float(ycfg["range"][1]), int(ycfg["range"][2]))
            Z = np.zeros((len(ys), len(xs)))
            for i, y in enumerate(ys):
                for j, x in enumerate(xs):
                    p = dict(base)
                    p[xcfg["name"]] = float(x)
                    p[ycfg["name"]] = float(y)
                    val = eval_point(e, p)
                    Z[i, j] = np.nan if val is None else val
            if plt is not None:
                fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=150)
                cf = ax.contourf(xs, ys, Z, levels=20, cmap=pl.get("cmap", "viridis"))
                fig.colorbar(cf, ax=ax, label=pl.get("clabel", pl.get("z")))
                ax.set_xlabel(pl.get("xlabel") or xcfg.get("label", xcfg["name"]))
                ax.set_ylabel(pl.get("ylabel") or ycfg.get("label", ycfg["name"]))
                ax.set_title(pl.get("title", ""))
                fig.tight_layout()
                ensure_dir(out)
                fig.savefig(out)
                J["figures"].append(out)
                L.append("- Saved: `%s`" % out)
                if pl.get("also_pdf"):
                    pdf = os.path.splitext(out)[0] + ".pdf"
                    fig.savefig(pdf)
                    J["figures"].append(pdf)
                    L.append("- Saved: `%s`" % pdf)
                plt.close(fig)
            with np.errstate(all="ignore"):
                L.append("- Z range: %.6g to %.6g" % (np.nanmin(Z), np.nanmax(Z)))
            if pl.get("csv"):
                csvp = os.path.splitext(out)[0] + ".csv"
                lines = ["%s,%s,%s" % (xcfg["name"], ycfg["name"], pl.get("z"))]
                for i, y in enumerate(ys):
                    for j, x in enumerate(xs):
                        lines.append("%.10g,%.10g,%.10g" % (x, y, Z[i, j]))
                write_text(csvp, "\n".join(lines))
                J["figures"].append(csvp)
                L.append("- Saved data: `%s`" % csvp)
        else:
            L.append("> Unsupported plot type: `%s` (supported: `sweep` / `heatmap`)" % ptype)
        L.append("")

    return finish(L, J, args)


# ----------------------------------------------------------------------------
# lint
# ----------------------------------------------------------------------------

def extract_math_spans(path):
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            txt = f.read()
    except Exception:
        return None
    spans = []
    spans += re.findall(r"\$\$(.+?)\$\$", txt, flags=re.S)
    spans += re.findall(r"(?<!\$)\$([^$]+?)\$(?!\$)", txt, flags=re.S)
    spans += re.findall(r"\\\[(.+?)\\\]", txt, flags=re.S)
    return spans


def _base_token(tok):
    """The token with any subscript removed (T_0 -> T, sum_i -> sum); unchanged if it has none."""
    b = re.split(r"[_0-9]", tok, 1)[0]
    return b if b else tok


def scan_text_atoms(text, declared):
    """Extract "symbol atoms" from body text: decompose run-together tokens using declared names; leftover letters are undeclared atoms.

    Two cleaning steps keep the scan from producing spurious "used but not declared" hits:
      1. the arguments of text-like macros are blanked, and brace sub/superscript groups are
         blanked, so `R_{\\text{agg}}` reads as `R` and `T_{0i}` reads as `T` (previously the
         index letters `agg` and `i` were reported as undeclared symbols);
      2. if a token does not resolve as written, it is retried with its subscript removed, so
         `h_1` reads as `h` and `\\sum_{j}` reads as `sum` (whitelisted).
    The retry deliberately happens ONLY after the token as written has failed, so that
    `q_1` is still read as the declared symbol `q1` rather than as `q`.
    """
    declared_norm_map = {}
    for d in declared:
        declared_norm_map.setdefault(norm_name(d), d)
    t = text or ""
    t = re.sub(r"\\(?:text|mathrm|operatorname|textbf|textit|textnormal|mathsf|mathtt)\{[^{}]*\}", " ", t)
    t = re.sub(r"[_^]\{[^{}]*\}", " ", t)
    atoms, unknown = set(), set()
    for m in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", t):
        resolved = False
        for cand in (m, _base_token(m)):
            n = norm_name(cand)
            if cand in FUNC_NAMES or cand in RESERVED:
                resolved = True
                break
            if n in declared_norm_map:
                atoms.add(declared_norm_map[n])
                resolved = True
                break
            if n in NO_DECOMPOSE or n in LATEX_WHITELIST:
                resolved = True
                break
            dec = _greedy_decompose(n, declared_norm_map)
            if dec:
                for d in dec:
                    atoms.add(d)
                resolved = True
                break
        if not resolved:
            unknown.add(m)
    return atoms, unknown


def cmd_lint(spec, args):
    L, J = [], {}
    L.append("# S5 notation and assumption-convention check (lint)")
    L.append("")
    L.append("- Title: %s" % spec.get("title", "(untitled)"))
    L.append("- Generated at: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("")

    syms = spec.get("symbols") or []
    issues = []

    L.append("## 1. Notation table")
    L.append("")
    L.append("| Symbol | Type | Meaning | Domain | Unit |")
    L.append("|---|---|---|---|---|")
    seen = {}
    for s in syms:
        L.append("| `%s` | %s | %s | %s | %s |" % (
            s.get("sym", "?"), s.get("type", "?"), s.get("meaning", ""),
            s.get("domain", "(not stated)"), s.get("unit", "(not stated)")))
        nm = s.get("sym", "")
        if nm in seen:
            issues.append(("high", "duplicate definition", "`%s` appears more than once in the notation table" % nm))
        seen[nm] = s
    L.append("")

    types = {}
    for s in syms:
        types.setdefault(norm_name(s.get("sym", "")), set()).add(s.get("type"))
    for nm, ts in types.items():
        if len(ts) > 1:
            issues.append(("high", "type conflict", "`%s` is declared as both %s" % (nm, " / ".join(sorted(str(t) for t in ts)))))

    L.append("## 2. Naming conventions")
    L.append("")
    naming = []
    for s in syms:
        core = s.get("sym", "").strip().lstrip("$").rstrip("$").strip()
        if core in ("l", "L"):
            naming.append(("medium", "`%s` is easily confused with the digit 1; economics writing convention avoids l as a variable (use the script ell or L_d)" % core))
        if core in ("e", "E"):
            naming.append(("medium", "`%s` is confusable with the natural constant (Euler's number), and the solver itself reserves both `e` and `E`; use another letter" % core))
        if core in ("O", "o"):
            naming.append(("medium", "`%s` is easily confused with the digit 0" % core))
        if core and core[0].isdigit():
            naming.append(("low", "`%s` starts with a digit" % core))
        if re.search(r"[A-Za-z]", core) and re.search(r"[0-9]", core):
            naming.append(("low", "`%s` has a numeric suffix -- confirm it is a subscript (e.g. q1 = q_1) and not a product" % core))
    lower_map = {}
    for s in syms:
        lower_map.setdefault(norm_name(s.get("sym", "")).lower(), set()).add(s.get("sym", ""))
    for k, v in lower_map.items():
        if len(v) > 1:
            naming.append(("high", "%s is treated as one symbol once underscores and case are ignored (%s); use one consistent name" % (
                k, ", ".join(sorted(v)))))
    if naming:
        for sev, msg in naming:
            issues.append((sev, "naming", msg))
            L.append("- [%s] %s" % (sev, msg))
    else:
        L.append("No naming problems found.")
    L.append("")

    L.append("## 3. Domain declarations")
    L.append("")
    dom = []
    for s in syms:
        nm = s.get("sym")
        if s.get("type") == "param" and not s.get("domain"):
            dom.append(("medium", "parameter `%s` has no declared domain (sign determination in comparative statics relies on it)" % nm))
        m = (s.get("meaning") or "") + str(nm or "")
        if ("prob" in m or "chance" in m.lower() or norm_name(str(nm)) == "pi"):
            d = str(s.get("domain", ""))
            if "[0,1]" not in d.replace(" ", "") and "[0, 1]" not in d:
                dom.append(("high", "`%s` looks like a probability; its domain should be declared explicitly as [0,1] (currently: %s)" % (nm, d or "not stated")))
        if s.get("type") == "endogenous" and not s.get("domain"):
            dom.append(("low", "endogenous variable `%s` has no declared domain" % nm))
    if dom:
        for sev, msg in dom:
            issues.append((sev, "domain", msg))
            L.append("- [%s] %s" % (sev, msg))
    else:
        L.append("Domain declarations are complete.")
    L.append("")

    L.append("## 4. Body-text symbol scan")
    L.append("")
    declared = [s.get("sym", "") for s in syms if s.get("sym")]
    tf = spec.get("text_file")
    if tf and os.path.exists(tf):
        spans = extract_math_spans(tf) or []
        L.append("- Scanned file: `%s` (%d math spans)" % (tf, len(spans)))
        L.append("")
        if not spans:
            L.append("> No `$...$` / `$$...$$` / `\\[...\\]` math spans found.")
        all_text = "\n".join(spans)
        atoms, unknown = scan_text_atoms(all_text, declared)
        declared_norm = {norm_name(d): d for d in declared}
        unused = sorted(d for d in declared if norm_name(d) not in {norm_name(a) for a in atoms})
        if unknown:
            issues.append(("high", "used but not declared", "appears in the text but not declared in the notation table: %s" % ", ".join(sorted(unknown))))
            L.append("**Symbols possibly not declared**: %s" % ", ".join("`%s`" % u for u in sorted(unknown)))
            L.append("")
        if unused:
            issues.append(("low", "declared but unused", "declared in the notation table but absent from the text: %s" % ", ".join(unused)))
            L.append("**Declared but absent from the text**: %s" % ", ".join("`%s`" % u for u in unused))
            L.append("")
        L.append("**Declared symbols recognized in the text**: %s" % (
            ", ".join("`%s`" % a for a in sorted(atoms)) or "(none)"))
    else:
        L.append("> No `text_file` provided (or the file does not exist); skipping the body-text scan.")
    L.append("")

    L.append("## 5. Assumption-number consistency")
    L.append("")
    defined = [str(a) for a in (spec.get("assumptions") or [])]
    referenced = [str(a) for a in (spec.get("referenced") or [])]
    L.append("- Defined: %s" % (", ".join(defined) or "(none)"))
    L.append("- Referenced in the text: %s" % (", ".join(referenced) or "(none)"))
    L.append("")
    for r in referenced:
        if r not in defined:
            issues.append(("high", "cites an undefined assumption", "the text cites `%s`, which is not in the assumption list" % r))
    for d in defined:
        if d not in referenced:
            issues.append(("medium", "defined but never cited", "assumption `%s` is never cited after being defined (it may not enter any derivation)" % d))
    L.append("")

    L.append("## 6. Issue summary")
    L.append("")
    if not issues:
        L.append("No issues found.")
    else:
        order = {"high": 0, "medium": 1, "low": 2}
        L.append("| Severity | Category | Description |")
        L.append("|---|---|---|")
        for sev, cat, msg in sorted(issues, key=lambda x: order.get(x[0], 3)):
            L.append("| %s | %s | %s |" % (sev, cat, msg))
        L.append("")
        n_hi = len([i for i in issues if i[0] == "high"])
        n_mid = len([i for i in issues if i[0] == "medium"])
        n_low = len([i for i in issues if i[0] == "low"])
        L.append("**Conclusion**: %d high-severity, %d medium, %d low." % (n_hi, n_mid, n_low))
        L.append("")
        L.append("> ⚠️ High-severity issues exist: **do not proceed to S6** until they are fixed and written back to the upstream files."
                 if n_hi else "> No high-severity issues; proceed to S6 after a manual confirmation.")

    J["issues"] = [{"severity": a, "category": b, "message": c} for a, b, c in issues]
    J["counts"] = {"high": len([i for i in issues if i[0] == "high"]),
                   "medium": len([i for i in issues if i[0] == "medium"]),
                   "low": len([i for i in issues if i[0] == "low"])}
    return finish(L, J, args)


# ----------------------------------------------------------------------------
# env
# ----------------------------------------------------------------------------

def cmd_env(spec, args):
    L = ["# Runtime environment", ""]
    L.append("- Interpreter: `%s`" % sys.executable)
    L.append("- Python: %s" % sys.version.replace("\n", " "))
    for mod in ("numpy", "scipy", "sympy", "matplotlib", "pandas"):
        try:
            m = __import__(mod)
            L.append("- %s: %s" % (mod, getattr(m, "__version__", "?")))
        except Exception as exc:
            L.append("- %s: **missing** (%s)" % (mod, exc))
    L.append("- Non-Latin font fallback: %s" % (setup_cjk_font() or "not found"))
    return finish(L, {}, args)


# ----------------------------------------------------------------------------

def finish(lines, J, args):
    text = "\n".join(lines) + "\n"
    if getattr(args, "out", None):
        write_text(args.out, text)
        text += "\n[written] %s\n" % args.out
    if getattr(args, "json_out", None):
        write_json(args.json_out, J)
        text += "[written] %s\n" % args.json_out
    if getattr(args, "log", None):
        ensure_dir(args.log)
        with io.open(args.log, "a", encoding="utf-8") as f:
            f.write("[%s] %s %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      getattr(args, "cmd", ""), getattr(args, "spec", "") or ""))
    try:
        sys.stdout.write(text)
    except Exception:
        pass
    return 0


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(prog="econ_solve.py", description="computational engine for the econ-modeling-flash skill")
    sub = ap.add_subparsers(dest="cmd")
    for name, helptext in (("foc", "first-order conditions / closed form / second-order conditions / numerical verification"),
                           ("cs", "comparative statics (implicit function theorem)"),
                           ("sim", "numerical sweeps and heat maps"),
                           ("lint", "notation and assumption-convention check"),
                           ("env", "environment self-check")):
        p = sub.add_parser(name, help=helptext)
        if name != "env":
            p.add_argument("--spec", required=True, help="input JSON spec file")
        p.add_argument("--out", help="write a markdown report")
        p.add_argument("--json-out", help="write a JSON result")
        p.add_argument("--log", help="append one line to the run log")
    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help()
        return 1
    args.cmd = args.cmd
    try:
        if args.cmd == "env":
            return cmd_env({}, args)
        spec = load_spec(args.spec)
        return {"foc": cmd_foc, "cs": cmd_cs, "sim": cmd_sim, "lint": cmd_lint}[args.cmd](spec, args)
    except Exception:
        err = traceback.format_exc()
        try:
            sys.stderr.write(err)
        except Exception:
            pass
        if getattr(args, "out", None):
            write_text(args.out, "# run failed\n\n```\n%s\n```\n" % err)
        return 2


if __name__ == "__main__":
    sys.exit(main())
