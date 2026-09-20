#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
review_score.py —— S8 expert-review score aggregation and disagreement diagnosis
=================================================================================

Input : a reviewer-score JSON file (see the schema below)
Output: weighted totals, band, inter-reviewer agreement (Fleiss kappa), disagreement
        diagnosis, and an optional markdown report

spec schema
-----------
{
  "title": "Model review aggregation",
  "scale_max": 5,
  "weights": {"D1": 0.15, "D2": 0.20, "D3": 0.20, "D4": 0.20, "D5": 0.15, "D6": 0.10},
  "dimensions": {
     "D1": "Question and positioning", "D2": "Originality",
     "D3": "Assumptions and logical rigour", "D4": "Technical correctness",
     "D5": "Explanatory power and testability", "D6": "Exposition and parsimony"
  },
  "reviewers": [
    {"name": "R1 Theoretical consistency",
     "scores": {"D1": 4, "D2": 3, "D3": 4, "D4": 3, "D5": 3, "D6": 4},
     "evidence": {"D4": "Proposition 2 gives no conditions (eq. (7) in S4)"},
     "fatal": "..."}
  ],
  "bands": [ ... optional, custom bands ],
  "reference_band": true
}

Agreement is read off the kappa bands of Landis & Koch (1977); see Krippendorff for
more conservative thresholds.
"""

import argparse
import io
import json
import os
import sys
import traceback
from datetime import datetime

DEFAULT_BANDS = [
    (85, 100, "A", "At the standard of a submittable working paper: the mechanism has an articulable marginal contribution", "Accept / Strong R&R"),
    (70, 84, "B", "Adequate: internally coherent, correct conclusions, testable implications, but limited originality", "Strong R&R"),
    (55, 69, "C", "Near the pass line: usable as a proposal or coursework, with 1-2 structural weaknesses", "Weak R&R"),
    (40, 54, "D", "A structural defect; go back to S3/S4 and rebuild", "Reject"),
    (25, 39, "E", "The model basically does not hold but the direction is salvageable; go back to S1/S2 and re-position", "Reject"),
    (0, 24, "F", "Internally contradictory, unsolvable with no valid degradation, or merely restating the phenomenon", "Reject"),
]

KAPPA_BANDS = [
    (-1.01, 0.00, "Poor (no agreement)"),
    (0.00, 0.20, "Slight (very weak)"),
    (0.21, 0.40, "Fair (weak)"),
    (0.41, 0.60, "Moderate"),
    (0.61, 0.80, "Substantial"),
    (0.81, 1.01, "Almost perfect"),
]


def read_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_text(path, text):
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def mean(xs):
    return sum(xs) / float(len(xs)) if xs else 0.0


def stdev(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return 0.0
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def trimmed_mean(xs, k=1):
    s = sorted(xs)
    if len(s) <= 2 * k:
        return mean(xs)
    return mean(s[k:len(s) - k])


def fleiss_kappa(table, n_cat):
    """table: rows = rated items, columns = categories; entries = number of raters choosing that category."""
    n_items = len(table)
    if n_items == 0:
        return None
    n_raters = sum(table[0])
    if n_raters < 2:
        return None
    P = []
    for row in table:
        s = sum(v * (v - 1) for v in row)
        P.append(s / float(n_raters * (n_raters - 1)))
    Pbar = mean(P)
    col = [sum(table[i][j] for i in range(n_items)) / float(n_items * n_raters)
           for j in range(n_cat)]
    Pe = sum(p * p for p in col)
    if abs(1.0 - Pe) < 1e-12:
        # Degenerate case: every reviewer gave the same category on every item, so the
        # chance-agreement rate is 1 and kappa is normally undefined. Convention: if the
        # observed agreement is also 1 (perfect agreement) report kappa = 1; otherwise
        # the coefficient cannot be determined.
        return 1.0 if Pbar >= 1.0 - 1e-12 else None
    return (Pbar - Pe) / (1.0 - Pe)


def judge_band(score, bands):
    for lo, hi, grade, desc, decision in bands:
        if lo <= score <= hi:
            return grade, desc, decision
    return "?", "outside the band range", "—"


def kappa_band(k):
    if k is None:
        return "not computable"
    for lo, hi, label in KAPPA_BANDS:
        if lo <= k < hi:
            return label
    return "?"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="review_score.py", description="S8 review score aggregation")
    ap.add_argument("--spec", required=True, help="input JSON file")
    ap.add_argument("--out", help="write a markdown report")
    ap.add_argument("--json-out", help="write a JSON result")
    args = ap.parse_args(argv)

    try:
        spec = read_json(args.spec)
    except Exception as exc:
        sys.stderr.write("read failed: %s\n" % exc)
        return 1

    try:
        return run(spec, args)
    except Exception:
        err = traceback.format_exc()
        sys.stderr.write(err)
        if args.out:
            write_text(args.out, "# run failed\n\n```\n%s\n```\n" % err)
        return 2


def run(spec, args):
    L, J = [], {}
    smax = float(spec.get("scale_max", 5))
    weights = spec.get("weights") or {}
    dims = spec.get("dimensions") or {}
    reviewers = spec.get("reviewers") or []
    bands = [tuple(b) for b in (spec.get("bands") or DEFAULT_BANDS)]
    if not dims:
        dims = {k: k for k in weights}
    dim_keys = list(weights.keys()) or list(dims.keys())
    wsum = sum(weights.get(k, 0) for k in dim_keys)
    if abs(wsum - 1.0) > 1e-6 and wsum > 0:
        weights = {k: weights.get(k, 0) / wsum for k in dim_keys}

    L.append("# S8 expert review — aggregated report")
    L.append("")
    L.append("- Title: %s" % spec.get("title", "(untitled)"))
    L.append("- Generated at: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("- Scale: 0-%d per dimension" % int(smax))
    L.append("")
    L.append("> ⚠️ **Nature of this instrument**: this report is a **simulated** review aggregation, intended to give the author "
             "an undistorted view of the model's real standard. It is **not** peer review, and must not be used to claim "
             "\"this has passed expert review\".")
    L.append("")

    if not reviewers:
        L.append("> ⚠️ No reviewer data (`reviewers` is empty).")
        return dump(L, J, args)

    # ---- weights and dimensions ----
    L.append("## 1. Dimension weights")
    L.append("")
    L.append("| Dimension | Name | Weight |")
    L.append("|---|---|---|")
    for k in dim_keys:
        L.append("| %s | %s | %.0f%% |" % (k, dims.get(k, k), 100 * weights.get(k, 0)))
    L.append("")

    # ---- per-reviewer totals ----
    L.append("## 2. Scores and weighted totals by reviewer")
    L.append("")
    L.append("| Reviewer | " + " | ".join(dims.get(k, k) for k in dim_keys) + " | Weighted total |")
    L.append("|---|" + "---|" * (len(dim_keys) + 1))
    totals, per_dim = {}, {k: [] for k in dim_keys}
    for r in reviewers:
        name = r.get("name", "?")
        sc = r.get("scores") or {}
        row, tot = [], 0.0
        missing = []
        for k in dim_keys:
            v = sc.get(k)
            if v is None:
                missing.append(k)
                v = float("nan")
            else:
                v = float(v)
                per_dim[k].append(v)
            row.append(v)
            if v == v:  # not nan
                tot += weights.get(k, 0) * v / smax
        totals[name] = 100.0 * tot
        L.append("| %s | %s | **%.1f** |" % (
            name, " | ".join(("—" if v != v else "%g" % v) for v in row), totals[name]))
        if missing:
            L.append("")
            L.append("> ⚠️ Reviewer \"%s\" is missing dimension scores: %s" % (name, ", ".join(missing)))
    L.append("")

    # ---- evidence binding check ----
    L.append("## 3. Evidence binding check")
    L.append("")
    L.append("> Rule: every score should carry a specific location reference (equation / assumption / proposition number). "
             "A reviewer with no evidence citations should be treated as providing insufficient evidence and sent back for re-scoring.")
    L.append("")
    L.append("| Reviewer | Dimensions with evidence | Gaps |")
    L.append("|---|---|---|")
    for r in reviewers:
        name = r.get("name", "?")
        ev = r.get("evidence") or {}
        gaps = [k for k in dim_keys if k not in ev]
        L.append("| %s | %s | %s |" % (
            name, ", ".join(sorted(ev.keys())) or "(none)", ", ".join(gaps) or "none"))
    L.append("")

    # ---- dimension statistics ----
    L.append("## 4. Per-dimension statistics and disagreement")
    L.append("")
    L.append("| Dimension | Name | Mean | SD | Min | Max | Range | Reviewer pairs at range>=2 |")
    L.append("|---|---|---|---|---|---|---|---|")
    disagreements = []
    for k in dim_keys:
        vs = [v for v in per_dim[k] if v == v]
        if not vs:
            continue
        rng = max(vs) - min(vs)
        pairs = []
        for r in reviewers:
            nm = r.get("name", "?")
            v = (r.get("scores") or {}).get(k)
            if v is not None and (float(v) == min(vs) or float(v) == max(vs)):
                pairs.append("%s(%g)" % (nm.split()[0], float(v)))
        L.append("| %s | %s | %.2f | %.2f | %g | %g | %g | %s |" % (
            k, dims.get(k, k), mean(vs), stdev(vs), min(vs), max(vs), rng,
            " / ".join(pairs) if rng >= 2 else "—"))
        if rng >= 2:
            disagreements.append((k, dims.get(k, k), rng))
    L.append("")
    if disagreements:
        L.append("**Dimensions needing separate discussion** (range >= 2, meaning the standard is unclear or the defect is contested):")
        L.append("")
        for k, nm, rng in disagreements:
            L.append("- %s (%s), range %g" % (nm, k, rng))
        L.append("")
        L.append("> Such dimensions **should not be masked by the mean**: record the source of disagreement in the S8 report, "
                 "and state which side you adopt and why.")
    else:
        L.append("Every dimension has a range < 2, so disagreement between reviewers is small.")
    L.append("")

    # ---- agreement coefficient ----
    L.append("## 5. Inter-reviewer agreement (Fleiss kappa)")
    L.append("")
    n_cat = int(smax) + 1
    table = []
    for k in dim_keys:
        row = [0] * n_cat
        for r in reviewers:
            v = (r.get("scores") or {}).get(k)
            if v is None:
                continue
            idx = int(round(float(v)))
            if 0 <= idx < n_cat:
                row[idx] += 1
        if sum(row) >= 2:
            table.append(row)
    kappa = fleiss_kappa(table, n_cat)
    klabel = kappa_band(kappa)
    if kappa is None:
        L.append("> Kappa cannot be computed (needs >=2 reviewers and some variation in the scores).")
    else:
        L.append("- Reviewers: %d | rated dimensions: %d | categories: %d" % (
            len(reviewers), len(table), n_cat))
        L.append("- **Fleiss kappa = %.3f** -> %s" % (kappa, klabel))
        L.append("- Reading based on Landis & Koch (1977). Under Krippendorff's more conservative thresholds, "
                 "conclusions should be discounted when kappa < 0.67, and only tentative conclusions are allowed in 0.67-0.80.")
        if kappa < 0.41:
            L.append("")
            L.append("> ⚠️ **Weak consensus**: do not look at the mean alone. Report the disagreement itself as a finding -- "
                     "it means the evaluation standard for this dimension has not converged, or the model is genuinely contested there.")
    L.append("")

    # ---- overall score ----
    tv = list(totals.values())
    overall_mean = mean(tv)
    overall_median = median(tv)
    overall_trimmed = trimmed_mean(tv, 1)
    disp = ((max(tv) - min(tv)) / overall_mean) if overall_mean > 0 else 0.0

    L.append("## 6. Overall score")
    L.append("")
    L.append("- Mean: **%.1f** / 100" % overall_mean)
    L.append("- Median: %.1f" % overall_median)
    L.append("- Trimmed mean (drop the highest and lowest): %.1f" % overall_trimmed)
    L.append("- Score range: [%.1f, %.1f] | disagreement index (max-min)/mean = **%.2f**" % (
        min(tv), max(tv), disp))
    if disp > 0.25:
        L.append("")
        L.append("> ⚠️ Disagreement index > 0.25: reviewers differ substantially on the model's overall standard. "
                 "Prefer the **median** and explain the source of the disagreement.")
    L.append("")

    grade, desc, decision = judge_band(overall_median, bands)
    L.append("## 7. Band and submission recommendation")
    L.append("")
    L.append("> Banded on the **median %.1f** (the median is more robust to extreme scores than the mean)." % overall_median)
    L.append("")
    L.append("- Band: **%s**" % grade)
    L.append("- Meaning: %s" % desc)
    L.append("- Recommendation: **%s**" % decision)
    L.append("")

    if overall_median >= 85:
        L.append("> Because this reaches band A, the following must be answered (R5, the adversarial reviewer): "
                 "\"If this model were rejected, what would most likely be the reason?\"")
        L.append("")

    L.append("## 8. Banding criteria (used in this round)")
    L.append("")
    L.append("| Band | Score range | Meaning | Decision |")
    L.append("|---|---|---|---|")
    for lo, hi, g, d, dec in bands:
        mark = " <-**this round**" if g == grade else ""
        L.append("| %s | %g-%g | %s | %s%s |" % (g, lo, hi, d, dec, mark))
    L.append("")

    J.update({
        "totals": totals,
        "overall": {"mean": overall_mean, "median": overall_median,
                    "trimmed_mean": overall_trimmed,
                    "min": min(tv), "max": max(tv), "dispersion": disp},
        "dimension_stats": {k: {"mean": mean([v for v in per_dim[k] if v == v]),
                                "sd": stdev([v for v in per_dim[k] if v == v]),
                                "min": min([v for v in per_dim[k] if v == v], default=None),
                                "max": max([v for v in per_dim[k] if v == v], default=None)}
                            for k in dim_keys if per_dim[k]},
        "fleiss_kappa": kappa,
        "kappa_band": klabel,
        "grade": grade,
        "decision": decision,
        "disputed_dimensions": [{"dim": k, "name": nm, "range": r} for k, nm, r in disagreements],
    })
    return dump(L, J, args)


def dump(L, J, args):
    text = "\n".join(L) + "\n"
    if getattr(args, "out", None):
        write_text(args.out, text)
        text += "\n[written] %s\n" % args.out
    if getattr(args, "json_out", None):
        write_text(args.json_out, json.dumps(J, ensure_ascii=False, indent=2, default=str))
        text += "[written] %s\n" % args.json_out
    try:
        sys.stdout.write(text)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
