#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
selftest.py —— econ-modeling-flash engine self-test
==================================================

Purpose: after installation, or after modifying `econ_solve.py` / `review_score.py`,
verify that the parser and solver have not regressed.
Run:
    <python> selftest.py            # exit code 0 when everything passes
    <python> selftest.py --out F    # also write the report to file F

The focus is the **most dangerous class of defect**: an expression silently misparsed
(for example q1 parsed as q*1).
"""

import argparse
import importlib.util
import io
import json
import os
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RESULTS = []


def check_expr(label, got, want):
    """Compare expression strings for mathematical equivalence."""
    import sympy as sp
    try:
        ok = sp.simplify(sp.sympify(got) - sp.sympify(want)) == 0
    except Exception:
        ok = (str(got) == str(want))
    RESULTS.append((ok, label, str(got), str(want)))
    return ok


def check(label, got, want):
    ok = (got == want)
    RESULTS.append((ok, label, str(got), str(want)))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()

    import sympy as sp
    es = load("econ_solve", "econ_solve.py")
    rs = load("review_score", "review_score.py")

    # ---------- 1. expression parsing (guarding against silent misparse) ----------
    parse_cases = [
        # (text, declared symbols, expected sstr)
        ("q1", ["q1"], "q1"),
        ("q2", ["q2"], "q2"),
        ("2bq1", ["b", "q1"], "2*b*q1"),
        ("a - 2bq1 - bq2 - c", ["a", "b", "q1", "q2", "c"], "a - 2*b*q1 - b*q2 - c"),
        ("q_1", ["q1"], "q1"),
        ("2b(q1+q2)", ["b", "q1", "q2"], "2*b*(q1 + q2)"),
        ("bq1", ["b", "q1"], "b*q1"),
        ("abc", ["a", "b", "c"], "a*b*c"),
        ("pi", ["p", "i"], "pi"),
        ("pf_subject", ["pf_subject"], "pf_subject"),
        ("0.5*x", ["x"], "x/2"),
        ("p*K^alpha*L^beta", ["p", "K", "alpha", "L", "beta"], "K**alpha*L**beta*p"),
    ]
    for text, decl, want in parse_cases:
        try:
            syms = es.build_symbols([text] + decl, declared=decl)
            e, _pre = es.parse_math(text, syms, decl)
            check("parse %-22s" % repr(text), sp.sstr(e), want)
        except Exception as exc:
            check("parse %-22s" % repr(text), "ERROR:%s" % str(exc).split("\n")[0], want)

    # ---------- 2. a missing `*` causing a "function call" must be detected and flagged ----------
    syms = es.build_symbols(["a - b(q1+q2)", "a", "b", "q1", "q2"],
                            declared=["a", "b", "q1", "q2"])
    e, _pre = es.parse_math("a - b*q(q1+q2)", syms, ["a", "b", "q1", "q2"])
    check("detect function call from missing *", es.undefined_functions(e), ["q"])
    e2, _ = es.parse_math("u(c)", es.build_symbols(["c"], declared=["c"]), ["c"])
    check("abstract function u(.) is detected", es.undefined_functions(e2), ["u"])
    e3, _ = es.parse_math("ln(x)", es.build_symbols(["ln(x)", "x"], declared=["x"]), ["x"])
    check("standard functions are not false-flagged", es.undefined_functions(e3), [])

    # ---------- 3. Cournot: FOC / SOC / solution ----------
    cournot = {
        "params": ["a", "b", "c"],
        "positive_symbols": ["a", "b", "c"],
        "params_values": {"a": 10, "b": 1, "c": 1},
        "agents": [
            {"name": "f1", "objective": "(a - b*(q1+q2))*q1 - c*q1", "vars": ["q1"]},
            {"name": "f2", "objective": "(a - b*(q1+q2))*q2 - c*q2", "vars": ["q2"]},
        ],
    }
    sy = es.build_system(cournot)
    focs = [e for _, e in sy["focs"]]
    check("Cournot number of FOCs", len(focs), 2)
    check("Cournot SOC f''(q1)", sp.sstr(sp.simplify(sp.diff(sy["agents"][0]["objective"], sy["agents"][0]["vars"][0], 2))), "-2*b")
    sol = sp.solve([sp.Eq(e, 0) for e in focs], sy["endog"], dict=True)
    q = sol[0] if sol else {}
    check("Cournot q1*", sp.sstr(sp.simplify(q.get(sy["endog"][0], sp.nan))), "(a - c)/(3*b)")
    check("Cournot solution value", round(es.eval_point(sp.simplify(q.get(sy["endog"][0], sp.nan)), {"a": 10, "b": 1, "c": 1}) or -999, 6), 3.0)

    # ---------- 4. comparative statics (implicit function theorem) ----------
    F = focs
    J = sp.Matrix([[sp.diff(e, v) for v in sy["endog"]] for e in F])
    dF = sp.Matrix([[sp.diff(e, p) for p in sy["params"]] for e in F])
    dX = sp.simplify((-J.inv() * dF).subs(sol[0])) if sol else None
    check("CS dq1/da", sp.sstr(sp.simplify(dX[0, 0])) if dX is not None else "NA", "1/(3*b)")
    check("CS dq1/dc", sp.sstr(sp.simplify(dX[0, 2])) if dX is not None else "NA", "-1/(3*b)")
    check_expr("CS dq1/db", sp.sstr(sp.simplify(dX[0, 1])) if dX is not None else "NA", "(c - a)/(3*b**2)")

    # ---------- 5. robustness of substitution by symbol name (positive=True must substitute too) ----------
    xpos = sp.Symbol("zeta", positive=True)
    check("eval_point(assumption symbol)", es.eval_point(xpos ** 2, {"zeta": 3.0}), 9.0)
    check("eval_point(missing value)", es.eval_point(xpos * sp.Symbol("w") ** 2, {"zeta": 3.0}), None)

    # ---------- 6. lint atom decomposition ----------
    atoms, unknown = es.scan_text_atoms("2bq_1 + bq_2 + aQ + zz", ["q1", "q2", "p", "a", "b", "c"])
    check("lint atoms", sorted(atoms), ["b", "q1", "q2"])
    check("lint unknown", sorted(unknown), ["aQ", "zz"])

    # ---------- 6b. subscripts and text-macro arguments must be stripped before scanning ----------
    a2, u2 = es.scan_text_atoms(
        "$T_{0i} + h_1 + \\sum_{j} x_j + R_{\\text{agg}} + \\boxed{Q}$",
        ["T", "h", "x", "R", "Q"])
    check("lint atoms after subscript/macro strip", sorted(a2), ["Q", "R", "T", "h", "x"])
    check("lint unknown after subscript/macro strip", sorted(u2), [])

    # ---------- 7. review aggregation ----------
    check("Fleiss kappa perfect agreement", round(rs.fleiss_kappa([[5, 0], [5, 0], [5, 0]], 2), 6), 1.0)
    check("Fleiss kappa total split", round(rs.fleiss_kappa([[3, 2], [2, 3]], 2), 6), -0.2)
    check("band C", rs.judge_band(62.0, rs.DEFAULT_BANDS)[0], "C")
    check("band A", rs.judge_band(90.0, rs.DEFAULT_BANDS)[0], "A")
    check("trimmed mean", rs.trimmed_mean([10, 20, 30, 40, 100]), 30.0)

    # ---------- 8. end-to-end smoke test (foc subcommand writes to disk) ----------
    tmp = tempfile.mkdtemp(prefix="emf_selftest_")
    specf = os.path.join(tmp, "spec.json")
    outf = os.path.join(tmp, "out.md")
    with io.open(specf, "w", encoding="utf-8") as f:
        json.dump(cournot, f)
    rc = es.main(["foc", "--spec", specf, "--out", outf])
    body = io.open(outf, encoding="utf-8").read() if os.path.exists(outf) else ""
    check("foc end-to-end exit code", rc, 0)
    check("foc report contains the closed form", ("3 b" in body) and ("Closed-form solution found" in body), True)
    check("foc report residual passes", "PASS (< 1e-9)" in body, True)

    # ---------- 9. lint must flag E, which the solver reserves for Euler's number ----------
    lspec = {"title": "naming check", "symbols": [
        {"sym": "E", "type": "param", "meaning": "enforcement intensity", "domain": "(0,1)"},
        {"sym": "k", "type": "param", "meaning": "a fine symbol", "domain": ">0"}]}
    lspecf = os.path.join(tmp, "lint_spec.json")
    lintout = os.path.join(tmp, "lint.md")
    with io.open(lspecf, "w", encoding="utf-8") as f:
        json.dump(lspec, f)
    rc2 = es.main(["lint", "--spec", lspecf, "--out", lintout])
    lbody = io.open(lintout, encoding="utf-8").read() if os.path.exists(lintout) else ""
    check("lint end-to-end exit code", rc2, 0)
    check("lint flags E as Euler-confusable", ("`E`" in lbody) and ("Euler" in lbody), True)

    # ---------- 10. audit_model: parameter consistency, regression, hygiene, claims ----------
    am = load("audit_model", "audit_model.py")

    def run_audit(argv):
        """Run audit_model with stdout captured, return (exit_code, json_result)."""
        jf = os.path.join(tempfile.mkdtemp(prefix="emf_audit_"), "audit.json")
        saved = sys.stdout
        sys.stdout = io.StringIO()
        try:
            rc = am.main(list(argv) + ["--json-out", jf])
        finally:
            sys.stdout = saved
        try:
            data = json.load(io.open(jf, encoding="utf-8"))
        except Exception:
            data = {"issues": [], "fail": -1, "warn": -1}
        return rc, data

    def has_fail(data, category=None, needle=None):
        for it in data["issues"]:
            if it["level"] != "fail":
                continue
            if category and it["category"] != category:
                continue
            if needle and needle not in it["message"]:
                continue
            return True
        return False

    lint_ok = {"symbols": [
        {"sym": "kappa", "type": "param", "meaning": "capacity retention", "domain": "(0,1]",
         "unit": "1", "source": "institution-side statistic, calibrated", "value": 0.10},
        {"sym": "mu", "type": "param", "meaning": "relative substitute price", "domain": ">1",
         "unit": "1", "source": "calibrated", "value": 2.0}]}
    f_ok = os.path.join(tmp, "lint_ok.json")
    f_sv = os.path.join(tmp, "solver_ok.json")
    with io.open(f_ok, "w", encoding="utf-8") as f:
        json.dump(lint_ok, f)
    with io.open(f_sv, "w", encoding="utf-8") as f:
        json.dump({"params_values": {"kappa": 0.1, "mu": 2.0}}, f)

    rc, d = run_audit(["--lint", f_ok, "--solver", f_sv])
    check("audit: clean table has no FAIL", d["fail"], 0)

    f_no = os.path.join(tmp, "lint_nosource.json")
    with io.open(f_no, "w", encoding="utf-8") as f:
        json.dump({"symbols": [dict(lint_ok["symbols"][0], source="")]}, f)
    rc, d = run_audit(["--lint", f_no])
    check("audit: missing `source` is flagged", has_fail(d, "table", "source"), True)

    f_dom = os.path.join(tmp, "lint_domain.json")
    with io.open(f_dom, "w", encoding="utf-8") as f:
        json.dump({"symbols": [dict(lint_ok["symbols"][0], value=1.5)]}, f)
    rc, d = run_audit(["--lint", f_dom])
    check("audit: value outside its domain is flagged", has_fail(d, "table", "OUTSIDE"), True)

    f_two = os.path.join(tmp, "solver_two_values.json")
    with io.open(f_two, "w", encoding="utf-8") as f:
        json.dump({"params_values": {"kappa": 0.25, "mu": 2.0}}, f)
    rc, d = run_audit(["--lint", f_ok, "--solver", f_two])
    check("audit: one symbol with two values is flagged", has_fail(d, "table", "two values"), True)

    ra = os.path.join(tmp, "run_a.json")
    rb = os.path.join(tmp, "run_b.json")
    rc_ = os.path.join(tmp, "run_c.json")
    with io.open(ra, "w", encoding="utf-8") as f:
        json.dump({"R": 1.27421, "nested": {"Q": 0.70711}}, f)
    with io.open(rb, "w", encoding="utf-8") as f:
        json.dump({"R": 1.27421, "nested": {"Q": 0.70711}}, f)
    with io.open(rc_, "w", encoding="utf-8") as f:
        json.dump({"R": 1.274211, "nested": {"Q": 0.70711}}, f)
    rc, d = run_audit(["--regress", "%s:%s" % (ra, rb)])
    check("audit: identical runs -> no FAIL", d["fail"], 0)
    check("audit: identical runs -> regression note present",
          any(i["category"] == "regress" for i in d["issues"]), True)
    rc, d = run_audit(["--regress", "%s:%s" % (ra, rc_)])
    check("audit: numeric drift is detected", has_fail(d, "regress"), True)

    tex_bad = os.path.join(tmp, "bad.tex")
    with io.open(tex_bad, "w", encoding="utf-8") as f:
        f.write("\\documentclass{article}\n# Markdown heading\n**bold**\n"
                "\\includegraphics{missing_fig.pdf}\n\\ref{nope}\n")
    rc, d = run_audit(["--scan", tex_bad])
    check("audit: Markdown bold inside LaTeX is flagged", has_fail(d, "scan", "Markdown bold"), True)
    check("audit: Markdown heading inside LaTeX is flagged", has_fail(d, "scan", "Markdown heading"), True)
    check("audit: missing \\includegraphics target is flagged",
          has_fail(d, "scan", "includegraphics target not found"), True)
    check("audit: dangling \\ref is flagged", has_fail(d, "scan", "no matching"), True)

    tex_ok = os.path.join(tmp, "ok.tex")
    with io.open(tex_ok, "w", encoding="utf-8") as f:
        f.write("\\documentclass{article}\n\\begin{document}\n\\section{X}\n"
                "\\textbf{bold}\n\\label{a}\nsee \\ref{a}\n\\end{document}\n")
    rc, d = run_audit(["--scan", tex_ok])
    check("audit: clean LaTeX -> no FAIL", d["fail"], 0)

    damaged = os.path.join(tmp, "damaged.md")
    with io.open(damaged, "w", encoding="utf-8") as f:
        f.write("result: \ufffd damaged\n")
    rc, d = run_audit(["--scan", damaged])
    check("audit: U+FFFD replacement char is flagged", has_fail(d, "scan", "U+FFFD"), True)

    notutf8 = os.path.join(tmp, "not_utf8.md")
    with io.open(notutf8, "wb") as f:
        f.write(b"\xff\xfe\x00bad bytes")
    rc, d = run_audit(["--scan", notutf8])
    check("audit: non-UTF-8 file is flagged", has_fail(d, "scan", "not valid UTF-8"), True)

    c_bad = os.path.join(tmp, "claim_bad.md")
    with io.open(c_bad, "w", encoding="utf-8") as f:
        f.write("\u672c\u6a21\u578b\u5df2\u901a\u8fc7\u4e13\u5bb6\u8bc4\u5ba1\u3002\n")
    rc, d = run_audit(["--claims", c_bad])
    check("audit: unmarked peer-review claim is flagged", has_fail(d, "claims"), True)

    c_ok = os.path.join(tmp, "claim_ok.md")
    with io.open(c_ok, "w", encoding="utf-8") as f:
        f.write("\u672c\u62a5\u544a\u4e3a\u6a21\u62df\u8bc4\u5ba1\uff0c\u4e0d\u662f\u540c\u884c\u8bc4\u8bae\uff1b"
                "\u4e0d\u5f97\u58f0\u79f0\u5df2\u901a\u8fc7\u4e13\u5bb6\u8bc4\u5ba1\u3002\n")
    rc, d = run_audit(["--claims", c_ok, "--require", "\u4e0d\u5f97\u58f0\u79f0"])
    check("audit: labelled simulated review passes", d["fail"], 0)
    rc, d = run_audit(["--claims", c_ok, "--require", "NOT-PRESENT-STRING"])
    check("audit: missing required text is flagged", has_fail(d, "claims"), True)

    # ---------- output ----------
    n_fail = sum(1 for ok, *_ in RESULTS if not ok)
    lines = ["# econ-modeling-flash self-test report", "",
             "- Engine directory: `%s`" % HERE,
             "- Cases: %d | passed: %d | failed: %d" % (len(RESULTS), len(RESULTS) - n_fail, n_fail),
             "", "| Result | Case | Actual | Expected |", "|---|---|---|---|"]
    for ok, label, got, want in RESULTS:
        lines.append("| %s | %s | %s | %s |" % ("PASS" if ok else "**FAIL**", label, got, want))
    lines.append("")
    lines.append("**Conclusion: %s**" % ("all passed" if n_fail == 0 else "failing cases exist; fix them before use"))
    text = "\n".join(lines) + "\n"
    if args.out:
        with io.open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    try:
        sys.stdout.write(text)
    except Exception:
        pass
    return 1 if n_fail else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        sys.exit(main())
    except Exception:
        sys.stderr.write(traceback.format_exc())
        sys.exit(2)
