#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
audit_model.py —— pre-delivery audit for an econ-modeling-flash deliverable
===========================================================================
Purpose: automate the checks that caught real defects during the double-reduction
project. Every check below corresponds to a defect class that actually occurred.

  1. `--lint` / `--solver`   symbol-table completeness + PARAMETER CONSISTENCY
       - every symbol needs meaning / domain / unit / source
       - a parameter's declared value must lie inside its declared domain
       - a parameter valued in a solver spec must exist in the symbol table and agree
         (this is the "one symbol, two values" defect)
  2. `--regress A.json:B.json`   NUMERIC REGRESSION after a revision
       - field-by-field comparison with tolerance; lists every differing key
       - use this to prove "the revision changed nothing numerically" before claiming it
  3. `--scan FILE...`   DELIVERABLE HYGIENE
       - UTF-8 decode failure / U+FFFD / UTF-8-read-as-GBK mojibake
       - Markdown syntax accidentally left inside LaTeX (**bold**, "# heading")
       - \\includegraphics targets that do not exist; \\ref without a matching \\label
       - PDFs (needs pypdf): extract the text and run the same Markdown-residue check
  4. `--claims FILE`   CLAIM SAFETY
       - "passed peer review"-style statements must be marked as simulated
       - numeric results should carry a calibration / illustration qualifier
       - `--require "text"` strings must be present (e.g. a "must not claim" section)

Usage
  <python> audit_model.py --lint spec_lint.json --solver spec_foc.json --solver spec_sim.json \
           --regress old.json:new.json --scan S9_paper.tex --scan figs/ --claims S6.md \
           --require "must not claim" --out audit.md --json-out audit.json

Exit code: 0 when there is no FAIL, 1 when at least one FAIL was recorded.
"""

import argparse
import io
import json
import os
import re
import sys
import traceback
from datetime import datetime

ISSUES = []          # (level, category, message, where)
LEVEL_FAIL, LEVEL_WARN, LEVEL_INFO = "fail", "warn", "info"

NUM_RE = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"

MOJIBAKE = ["鈥", "锛", "銆", "鈽", "鈿", "鐨", "鍑", "鏂", "鎴", "鍏", "锛", "鈭"]

# Binary / image extensions must never be opened as text (a PNG read as UTF-8
# produces a spurious "not valid UTF-8" FAIL). PDFs are handled separately by
# scan_pdf, so they are NOT in this set.
BINARY_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".eps", ".svg"}
# The "no bold text" hint only makes sense for prose deliverables, not for
# data files like .csv / .json / .py.
PROSE_EXTS = {".md", ".markdown", ".txt", ".rst", ".tex", ".ltx", ".sty"}


def add(level, category, message, where=""):
    ISSUES.append((level, category, message, where))


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def read_text(path):
    """Read as UTF-8 strictly. Returns (text, error_message)."""
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            return f.read(), None
    except UnicodeDecodeError as exc:
        return None, "not valid UTF-8: %s" % exc
    except Exception as exc:
        return None, str(exc)


def parse_domain(s):
    """Return (lo, lo_strict, hi, hi_strict) or None when not machine-checkable."""
    if s is None:
        return None
    t = str(s).strip().replace(" ", "").replace("−", "-")
    if not t:
        return None
    m = re.match(r"^([\[\(])(%s),(%s)([\]\)])$" % (NUM_RE, NUM_RE), t)
    if m:
        lo, hi = float(m.group(2)), float(m.group(3))
        return (lo, m.group(1) == "(", hi, m.group(4) == ")")
    m = re.match(r"^(>=|>|≤|<=|<|≤)(%s)$" % NUM_RE, t)
    if m:
        op, val = m.group(1), float(m.group(2))
        if op in (">",):
            return (val, True, None, False)
        if op in (">=",):
            return (val, False, None, False)
        if op in ("<",):
            return (None, False, val, True)
        return (None, False, val, False)
    return None


def in_domain(value, dom):
    if dom is None:
        return None
    lo, ls, hi, hs = dom
    if lo is not None:
        if value < lo or (ls and abs(value - lo) < 1e-15):
            return False
    if hi is not None:
        if value > hi or (hs and abs(value - hi) < 1e-15):
            return False
    return True


def coerce_number(v):
    try:
        if isinstance(v, bool):
            return None
        if isinstance(v, (int, float)):
            return float(v)
        return float(str(v).strip())
    except Exception:
        return None


def walk_numbers(obj, prefix=""):
    """Flatten a JSON object into {dotted.key: float} for numeric leaves."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(walk_numbers(v, "%s.%s" % (prefix, k) if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(walk_numbers(v, "%s[%d]" % (prefix, i)))
    else:
        n = coerce_number(obj) if not isinstance(obj, str) else None
        if n is not None:
            out[prefix] = n
    return out


# --------------------------------------------------------------------------- #
# check 1: symbol table + parameter consistency
# --------------------------------------------------------------------------- #
def collect_solver_values(spec):
    """Gather name -> (value, where) from the places solver specs keep parameter values."""
    found = {}

    def take(d, where):
        if isinstance(d, dict):
            for k, v in d.items():
                n = coerce_number(v)
                if n is not None:
                    found.setdefault(k, (n, where))

    take(spec.get("params_values") or {}, "params_values")
    take(spec.get("base") or {}, "base")
    take(spec.get("agent_params") or {}, "agent_params")
    cs = spec.get("comparative_statics") or {}
    take(cs.get("evaluate_at") or {}, "comparative_statics.evaluate_at")
    return found


def check_table(lint_spec, solver_specs):
    syms = lint_spec.get("symbols") or []
    if not syms:
        add(LEVEL_FAIL, "table", "the lint spec contains no `symbols` table", "")
        return

    seen = {}
    for s in syms:
        name = str(s.get("sym", "")).strip()
        typ = str(s.get("type", "")).strip().lower()
        if not name:
            add(LEVEL_FAIL, "table", "a symbol entry has no `sym`", "")
            continue
        if name in seen:
            add(LEVEL_FAIL, "table", "duplicate definition of `%s`" % name, "")
        seen[name] = s

        is_param = typ in ("param", "parameter")
        for field in ("meaning", "domain", "unit", "source"):
            if str(s.get(field, "")).strip():
                continue
            if field == "meaning":
                add(LEVEL_FAIL, "table", "`%s` has no `meaning`" % name, name)
            elif field == "source":
                add(LEVEL_FAIL if is_param else LEVEL_WARN, "table",
                    "`%s` has no `source`: state whether the value is estimated, calibrated, "
                    "illustrative, or taken from an institution-side statistic -- "
                    "an institution-side statistic is NOT the model's own parameter" % name, name)
            else:
                add(LEVEL_WARN, "table", "`%s` has no `%s`" % (name, field), name)

        if typ not in ("param", "parameter", "endog", "endogenous", "exog", "exogenous",
                       "derived", "observed", "choice", "state"):
            add(LEVEL_WARN, "table", "`%s` has an unrecognised `type` (%s)" % (name, typ or "?"), name)

        val = coerce_number(s.get("value"))
        if val is not None:
            dom = parse_domain(s.get("domain"))
            if dom is None:
                add(LEVEL_WARN, "table",
                    "`%s`: domain `%s` is not machine-checkable, so value-vs-domain was not verified"
                    % (name, s.get("domain")), name)
            else:
                if in_domain(val, dom) is False:
                    add(LEVEL_FAIL, "table",
                        "`%s` = %g lies OUTSIDE its declared domain `%s`"
                        % (name, val, s.get("domain")), name)

    # cross-check against solver specs
    for path, spec in solver_specs:
        for k, (v, where) in sorted(collect_solver_values(spec).items()):
            if k not in seen:
                add(LEVEL_WARN, "table",
                    "`%s` is valued in %s (%s) but absent from the symbol table"
                    % (k, where, os.path.basename(path)), os.path.basename(path))
                continue
            tv = coerce_number(seen[k].get("value"))
            if tv is None:
                add(LEVEL_INFO, "table",
                    "`%s`: symbol table carries no `value`, so the solver value %g in %s was not compared"
                    % (k, v, where), k)
            elif abs(tv - v) > 1e-9 * max(1.0, abs(tv), abs(v)):
                add(LEVEL_FAIL, "table",
                    "`%s` = %g in the symbol table but %g in %s (%s) -- one symbol, two values"
                    % (k, tv, v, os.path.basename(path), where), os.path.basename(path))

    add(LEVEL_INFO, "table", "symbols checked: %d" % len(seen), "")


# --------------------------------------------------------------------------- #
# check 2: numeric regression
# --------------------------------------------------------------------------- #
def _is_drive_colon(s, i):
    """True for the colon in `C:\\...` (and for a second path after the separator, `...:C:\\...`)."""
    if s[i + 1:i + 2] not in ("\\", "/"):
        return False
    if not s[i - 1:i].isalpha():
        return False
    if i == 1:
        return True
    return s[i - 2] in "\\/:,;\"'= "


def split_pair(s):
    """Split `OLD:NEW`, ignoring Windows drive-letter colons (there are three colons in a pair)."""
    seps = [i for i, ch in enumerate(s) if ch == ":" and not _is_drive_colon(s, i)]
    if len(seps) != 1:
        return None
    i = seps[0]
    return s[:i], s[i + 1:]


def check_regress(pairs, tol):
    for spec in pairs:
        pair = split_pair(spec)
        if pair is None:
            add(LEVEL_FAIL, "regress",
                "--regress expects OLD.json:NEW.json (a single separating colon), got `%s`" % spec)
            continue
        pa, pb = pair
        try:
            A = json.load(io.open(pa, "r", encoding="utf-8"))
            B = json.load(io.open(pb, "r", encoding="utf-8"))
        except Exception as exc:
            add(LEVEL_FAIL, "regress", "cannot read the pair: %s" % exc, spec)
            continue
        fa, fb = walk_numbers(A), walk_numbers(B)
        keys = sorted(set(fa) | set(fb))
        diffs, only_a, only_b, same = [], [], [], 0
        for k in keys:
            if k in fa and k in fb:
                if abs(fa[k] - fb[k]) <= tol * max(1.0, abs(fa[k]), abs(fb[k])):
                    same += 1
                else:
                    diffs.append((k, fa[k], fb[k]))
            elif k in fa:
                only_a.append(k)
            else:
                only_b.append(k)
        w = "%s -> %s" % (os.path.basename(pa), os.path.basename(pb))
        if diffs:
            for k, a, b in diffs[:20]:
                add(LEVEL_FAIL, "regress", "`%s`: %g -> %g (delta %+.3g)" % (k, a, b, b - a), w)
            if len(diffs) > 20:
                add(LEVEL_FAIL, "regress", "... and %d more differing keys" % (len(diffs) - 20), w)
        if only_a or only_b:
            add(LEVEL_WARN, "regress",
                "keys present in only one file: %s%s"
                % (", ".join(only_a[:10]), (" ; " + ", ".join(only_b[:10])) if only_b else ""), w)
        add(LEVEL_INFO, "regress",
            "%s: %d numeric keys compared, %d identical, %d different"
            % (w, len([k for k in keys if k in fa and k in fb]), same, len(diffs)), w)


# --------------------------------------------------------------------------- #
# check 3: deliverable hygiene
# --------------------------------------------------------------------------- #
def scan_pdf(path):
    try:
        from pypdf import PdfReader
    except Exception:
        add(LEVEL_WARN, "scan",
            "pypdf not available, so the PDF text was NOT checked (a compiled PDF can still "
            "contain raw Markdown markers)", path)
        return
    try:
        r = PdfReader(path)
        txt = "".join((p.extract_text() or "") for p in r.pages)
    except Exception as exc:
        add(LEVEL_WARN, "scan", "could not extract PDF text: %s" % exc, path)
        return
    add(LEVEL_INFO, "scan", "PDF pages: %d, extracted characters: %d" % (len(r.pages), len(txt)), path)
    md = re.findall(r"\*\*[^*\n]{1,80}\*\*", txt)
    if md:
        add(LEVEL_FAIL, "scan",
            "%d literal Markdown bold marker(s) inside the rendered PDF, e.g. %r -- "
            "the source probably mixed Markdown into LaTeX" % (len(md), md[0][:60]), path)
    if "\ufffd" in txt:
        add(LEVEL_FAIL, "scan", "the PDF text contains U+FFFD replacement characters", path)


def scan_text_file(path):
    if path.lower().endswith(".pdf"):
        scan_pdf(path)
        return
    txt, err = read_text(path)
    if err:
        add(LEVEL_FAIL, "scan", err, path)
        return
    is_tex = path.lower().endswith((".tex", ".ltx", ".sty"))

    if "\ufffd" in txt:
        add(LEVEL_FAIL, "scan", "contains U+FFFD replacement characters (encoding damage)", path)
    hits = [m for m in MOJIBAKE if m in txt]
    if hits:
        add(LEVEL_WARN, "scan",
            "suspicious sequences %s -- typical of UTF-8 text being read as GBK "
            "(if this came from a console capture, check the file on disk)" % hits[:5], path)

    if is_tex:
        md = re.findall(r"\*\*[^*\n]{1,120}\*\*", txt)
        if md:
            add(LEVEL_FAIL, "scan",
                "%d Markdown bold marker(s) in LaTeX (they print as literal asterisks), e.g. %r; "
                "use \\textbf{...}" % (len(md), md[0][:60]), path)
        ital = re.findall(r"(?<![\\\w])__[^_\n]{1,80}__(?!\w)", txt)
        if ital:
            add(LEVEL_WARN, "scan", "%d Markdown italic marker(s) in LaTeX; use \\emph{...}" % len(ital), path)
        heads = re.findall(r"^\s*#{1,6}\s+\S", txt, re.M)
        if heads:
            add(LEVEL_FAIL, "scan",
                "%d Markdown heading(s) in LaTeX, e.g. %r; use \\section{...}" % (len(heads), heads[0].strip()[:40]), path)
        base = os.path.dirname(os.path.abspath(path))
        for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", txt):
            target = m.group(1).strip()
            cand = [target]
            root, ext = os.path.splitext(target)
            for e in (".pdf", ".png", ".jpg", ".jpeg", ".eps"):
                cand.append(root + e)
            if not any(os.path.exists(os.path.join(base, os.path.normpath(c))) for c in cand):
                add(LEVEL_FAIL, "scan", "\\includegraphics target not found: `%s`" % target, path)
        labels = set(re.findall(r"\\label\{([^}]+)\}", txt))
        for r in re.findall(r"\\ref\{([^}]+)\}", txt):
            if r not in labels:
                add(LEVEL_FAIL, "scan", "\\ref{%s} has no matching \\label" % r, path)
        add(LEVEL_INFO, "scan",
            "LaTeX: %d \\label, %d \\ref, %d \\includegraphics"
            % (len(labels), len(re.findall(r"\\ref\{", txt)), len(re.findall(r"\\includegraphics", txt))), path)
    else:
        if path.lower().endswith(tuple(PROSE_EXTS)):
            md = re.findall(r"\*\*[^*\n]{1,120}\*\*", txt)
            if not md:
                add(LEVEL_WARN, "scan", "no bold text found -- for a report this is unusual, please confirm", path)


# --------------------------------------------------------------------------- #
# check 4: claim safety
# --------------------------------------------------------------------------- #
REVIEW_CLAIMS = ["通过专家评审", "已通过专家评审", "passed peer review", "peer-reviewed",
                 "已达期刊标准", "达到期刊标准"]
SIM_MARKERS = ["模拟", "simulated", "simulation"]
NUMERIC_QUALIFIERS = ["校准", "数值示例", "示例", "illustration", "illustrative", "calibrat", "numerical"]


def check_claims(path, requires):
    txt, err = read_text(path)
    if err:
        add(LEVEL_FAIL, "claims", err, path)
        return
    if any(c in txt for c in REVIEW_CLAIMS):
        ctx_ok = any(m in txt for m in SIM_MARKERS)
        if not ctx_ok:
            add(LEVEL_FAIL, "claims",
                "the text claims expert review / journal standard without any simulation marker; "
                "the review is SIMULATED and must be labelled as such", path)
        else:
            add(LEVEL_INFO, "claims", "review claims are accompanied by a simulation marker", path)
    if re.search(NUM_RE + r"\s*%", txt) and not any(q in txt for q in NUMERIC_QUALIFIERS):
        add(LEVEL_WARN, "claims",
            "numeric percentage results appear without any calibration/illustration qualifier; "
            "a reader may take them as point estimates", path)
    if "不得声称" in txt or "must not claim" in txt:
        add(LEVEL_INFO, "claims", "a 'must not claim' section is present", path)
    else:
        add(LEVEL_WARN, "claims", "no 'must not claim' section found in this deliverable", path)
    for need in requires:
        if need not in txt:
            add(LEVEL_FAIL, "claims", "required text not found: %r" % need, path)
        else:
            add(LEVEL_INFO, "claims", "required text present: %r" % need, path)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(prog="audit_model.py", description="pre-delivery audit")
    ap.add_argument("--lint", help="lint spec JSON holding the symbol table")
    ap.add_argument("--solver", action="append", default=[], help="solver spec JSON holding parameter values")
    ap.add_argument("--regress", action="append", default=[], help="OLD.json:NEW.json")
    ap.add_argument("--scan", action="append", default=[], help="file or directory to scan")
    ap.add_argument("--claims", action="append", default=[], help="deliverable to check for unsafe claims")
    ap.add_argument("--require", action="append", default=[], help="text that must be present in --claims files")
    ap.add_argument("--tol", type=float, default=1e-9, help="numeric regression tolerance (relative)")
    ap.add_argument("--out", help="markdown report")
    ap.add_argument("--json-out", help="JSON result")
    args = ap.parse_args(argv)

    try:
        return run(args)
    except Exception:
        err = traceback.format_exc()
        sys.stderr.write(err)
        if args.out:
            write_text(args.out, "# audit failed to run\n\n```\n%s\n```\n" % err)
        return 2


def write_text(path, text):
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def run(args):
    del ISSUES[:]           # reset module-level state, so repeated invocations do not accumulate
    if not any([args.lint, args.solver, args.regress, args.scan, args.claims]):
        add(LEVEL_WARN, "audit", "nothing to do: pass at least one of --lint / --solver / --regress / --scan / --claims")

    # 1) table + parameter consistency
    if args.lint or args.solver:
        lint_spec = {}
        if args.lint:
            try:
                lint_spec = json.load(io.open(args.lint, "r", encoding="utf-8"))
            except Exception as exc:
                add(LEVEL_FAIL, "table", "cannot read the lint spec: %s" % exc, args.lint)
        solver_specs = []
        for p in args.solver:
            try:
                solver_specs.append((p, json.load(io.open(p, "r", encoding="utf-8"))))
            except Exception as exc:
                add(LEVEL_FAIL, "table", "cannot read %s: %s" % (p, exc), p)
        if lint_spec:
            check_table(lint_spec, solver_specs)

    # 2) numeric regression
    if args.regress:
        check_regress(args.regress, args.tol)

    # 3) hygiene scan
    targets = []
    for t in args.scan:
        if os.path.isdir(t):
            for root, dirs, files in os.walk(t):
                dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
                for f in sorted(files):
                    if os.path.splitext(f)[1].lower() in BINARY_EXTS:
                        continue
                    targets.append(os.path.join(root, f))
        elif os.path.exists(t):
            targets.append(t)
        else:
            add(LEVEL_FAIL, "scan", "path not found: %s" % t)
    for t in targets:
        scan_text_file(t)

    # 4) claims
    for c in args.claims:
        check_claims(c, args.require)

    # report
    fails = [i for i in ISSUES if i[0] == LEVEL_FAIL]
    warns = [i for i in ISSUES if i[0] == LEVEL_WARN]
    L = ["# Pre-delivery audit", "",
         "- Generated at: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         "- Checks run: table=%s regress=%s scan=%d file(s) claims=%d file(s)"
         % (bool(args.lint or args.solver), bool(args.regress), len(targets), len(args.claims)),
         "",
         "- **FAIL: %d | WARN: %d | INFO: %d**" % (len(fails), len(warns),
                                                  len([i for i in ISSUES if i[0] == LEVEL_INFO])),
         "",
         "> FAIL items block delivery: they correspond to defect classes that have actually "
         "occurred in practice (silent misparse, one symbol with two values, a value outside its "
         "domain, Markdown left inside LaTeX, an over-claimed review).", ""]
    for lvl, title in ((LEVEL_FAIL, "FAIL (must fix)"), (LEVEL_WARN, "WARN (read and decide)"),
                       (LEVEL_INFO, "INFO")):
        rows = [i for i in ISSUES if i[0] == lvl]
        if not rows:
            continue
        L.append("## %s" % title)
        L.append("")
        L.append("| Category | Where | Message |")
        L.append("|---|---|---|")
        for _, cat, msg, where in rows:
            L.append("| %s | %s | %s |" % (cat, where or "-", msg))
        L.append("")

    text = "\n".join(L) + "\n"
    if args.out:
        write_text(args.out, text)
    if args.json_out:
        write_text(args.json_out, json.dumps(
            {"issues": [{"level": l, "category": c, "message": m, "where": w} for l, c, m, w in ISSUES],
             "fail": len(fails), "warn": len(warns)}, ensure_ascii=False, indent=2))
    try:
        sys.stdout.write(text)
    except Exception:
        pass
    return 1 if fails else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
