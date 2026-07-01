"""
Reggies' Veggies qPCR analysis — ΔΔCt fold-change of stress genes.

Parses the Applied Biosystems "Results" exports (per-well Ct), maps each numeric
sample ID to its treatment via the plate design, and computes, for each target
gene relative to the UBQ10 reference:

    ΔCt   = Ct(gene)  − Ct(UBQ10)            per biological sample
    ΔΔCt  = mean ΔCt(treatment) − mean ΔCt(calibrator)
    fold  = 2^(−ΔΔCt)                         relative to Ground-control calibrator

Outputs -> data/processed/reggies_qpcr/:
    qpcr_ct_long.csv         one row per sample × gene (mean Ct, ΔCt)
    qpcr_fold_change.csv     one row per treatment × gene (ΔΔCt, fold, range)
And a chart -> assets/charts/qpcr_fold_change.png

NOTE on grouping: per `Plate design.xlsx` the samples split into FLIGHT,
LAUNCH SITE (travel control), GROUND (lab control, calibrator). The upstream
tube-status sheet labels IDs 22 & 23 as "ground control" rather than launch
site — a documented inconsistency. We follow the plate design (how the qPCR was
actually laid out) and flag it. This affects only the launch-site group; the
Flight-vs-control comparison is unaffected (13/15/17/18 are Flight in both).
"""
import os, re, glob
import numpy as np
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RV = os.path.join(HERE, "..", "data", "raw", "reggies_veggies", "molecular", "qpcr_results")
OUTDIR = os.path.join(HERE, "..", "data", "processed", "reggies_qpcr")
CHARTS = os.path.join(HERE, "..", "assets", "charts")
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

REFERENCE = "UBQ10"
TARGETS = ["MPK3", "TCH3", "CBP60g"]

# sample ID -> treatment (from Plate design.xlsx); GROUND is the calibrator.
SAMPLE_GROUP = {
    "13": "Flight", "15": "Flight", "17": "Flight", "18": "Flight",
    "22": "Launch site", "23": "Launch site", "24": "Launch site", "25": "Launch site",
    "5": "Ground", "6": "Ground", "20": "Ground", "21": "Ground",
}
CALIBRATOR = "Ground"
GROUP_ORDER = ["Ground", "Launch site", "Flight"]
GROUP_COLOR = {"Ground": "#2f5f8f", "Launch site": "#5aa9ff", "Flight": "#36c97f"}

# the two complementary instrument exports (no sample overlap)
DATA_FILES = [
    os.path.join(RV, "Sophia Template 1_data.xlsx"),       # 13,15,20,21,24,25
    os.path.join(RV, "Data", "Sophia Template 2_data.xlsx"),  # 5,6,17,18,22,23
]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower()) if s is not None else ""


def read_wells(path):
    """Yield (sample_id, gene, ct_float) from a Results sheet."""
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Results"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = next(i for i, r in enumerate(rows)
               if "well" in [norm(c) for c in r] and "targetname" in [norm(c) for c in r])
    H = [norm(c) for c in rows[hdr]]
    ci_sample, ci_gene = H.index("samplename"), H.index("targetname")
    ci_ct = H.index("c")  # the bare Ct column ("Cт" normalizes to "c")
    for r in rows[hdr + 1:]:
        if not any(x is not None for x in r):
            continue
        sid = str(r[ci_sample]).strip() if r[ci_sample] is not None else ""
        sid = sid[:-2] if sid.endswith(".0") else sid       # "20.0" -> "20"
        gene = str(r[ci_gene]).strip() if r[ci_gene] is not None else ""
        ct = r[ci_ct]
        if sid not in SAMPLE_GROUP or gene not in (TARGETS + [REFERENCE]):
            continue
        try:
            ctf = float(ct)
        except (TypeError, ValueError):
            continue                                          # undetermined / blank
        if ctf <= 0 or ctf > 40:
            continue
        yield sid, gene, ctf


def main():
    # collect per-well Ct -> mean Ct per (sample, gene)
    wells = {}
    for f in DATA_FILES:
        if not os.path.exists(f):
            print("MISSING", f); continue
        for sid, gene, ct in read_wells(f):
            wells.setdefault((sid, gene), []).append(ct)

    mean_ct = {k: float(np.mean(v)) for k, v in wells.items()}

    # ΔCt per sample x target
    long_rows = []
    dct = {}  # (sample, gene) -> dCt
    for sid in SAMPLE_GROUP:
        ref = mean_ct.get((sid, REFERENCE))
        if ref is None:
            continue
        for gene in TARGETS:
            ct = mean_ct.get((sid, gene))
            if ct is None:
                continue
            d = ct - ref
            dct[(sid, gene)] = d
            long_rows.append((sid, SAMPLE_GROUP[sid], gene,
                              round(mean_ct.get((sid, gene)), 3),
                              round(ref, 3), round(d, 3),
                              len(wells.get((sid, gene), []))))

    # write long table
    long_path = os.path.join(OUTDIR, "qpcr_ct_long.csv")
    with open(long_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("sample_id,treatment,gene,mean_ct,ref_ct_UBQ10,dCt,n_tech_reps\n")
        for row in sorted(long_rows, key=lambda r: (GROUP_ORDER.index(r[1]), r[2], r[0])):
            fh.write(",".join(str(x) for x in row) + "\n")
    print("wrote", long_path, len(long_rows), "rows")

    # mean ΔCt per (treatment, gene) across biological reps
    grp = {}
    for (sid, gene), d in dct.items():
        grp.setdefault((SAMPLE_GROUP[sid], gene), []).append(d)

    fold_rows = []
    for gene in TARGETS:
        cal = grp.get((CALIBRATOR, gene), [])
        cal_mean = float(np.mean(cal)) if cal else None
        for trt in GROUP_ORDER:
            vals = grp.get((trt, gene), [])
            if not vals or cal_mean is None:
                continue
            mdct = float(np.mean(vals)); sdct = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            ddct = mdct - cal_mean
            fold = 2 ** (-ddct)
            # propagate biological SD of ΔCt into a fold range
            fold_lo = 2 ** (-(ddct + sdct)); fold_hi = 2 ** (-(ddct - sdct))
            fold_rows.append(dict(gene=gene, treatment=trt, n=len(vals),
                                  mean_dCt=round(mdct, 3), ddCt=round(ddct, 3),
                                  fold=round(fold, 3), fold_lo=round(fold_lo, 3),
                                  fold_hi=round(fold_hi, 3),
                                  log2fold=round(-ddct, 3)))

    fold_path = os.path.join(OUTDIR, "qpcr_fold_change.csv")
    with open(fold_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("gene,treatment,n_bio_reps,mean_dCt,ddCt,fold_change,fold_lo,fold_hi,log2_fold\n")
        for r in fold_rows:
            fh.write(f"{r['gene']},{r['treatment']},{r['n']},{r['mean_dCt']},"
                     f"{r['ddCt']},{r['fold']},{r['fold_lo']},{r['fold_hi']},{r['log2fold']}\n")
    print("wrote", fold_path, len(fold_rows), "rows")

    for r in fold_rows:
        print(f"  {r['gene']:8s} {r['treatment']:12s} n={r['n']}  "
              f"fold={r['fold']:.2f}  log2={r['log2fold']:+.2f}")

    make_chart(fold_rows)


def make_chart(fold_rows):
    fig, ax = plt.subplots(figsize=(8.8, 5.1))
    genes = TARGETS
    x = np.arange(len(genes))
    width = 0.26
    plotted = [g for g in GROUP_ORDER if g != CALIBRATOR]  # bars vs calibrator
    for i, trt in enumerate(plotted):
        ys, los, his = [], [], []
        for g in genes:
            rec = next((r for r in fold_rows if r["gene"] == g and r["treatment"] == trt), None)
            ys.append(rec["log2fold"] if rec else 0)
            los.append((rec["log2fold"] - np.log2(rec["fold_lo"])) if rec else 0)
            his.append((np.log2(rec["fold_hi"]) - rec["log2fold"]) if rec else 0)
        off = (i - (len(plotted) - 1) / 2) * width
        ax.bar(x + off, ys, width, label=f"{trt} vs {CALIBRATOR}",
               color=GROUP_COLOR[trt], yerr=[np.abs(los), np.abs(his)],
               capsize=4, ecolor="#aab6cf")
    ax.axhline(0, color="#6f7d9c", lw=1)
    ax.set_xticks(x); ax.set_xticklabels(genes)
    ax.set_facecolor("#0f1525"); fig.set_facecolor("#0a0e1a")
    for s in ax.spines.values():
        s.set_color("#26324f")
    ax.tick_params(colors="#aab6cf")
    ax.set_title("qPCR stress-gene response — log2 fold-change vs lab ground control",
                 color="#e8edf7", fontsize=12, pad=12)
    ax.set_ylabel("log2 fold-change  (0 = no change)", color="#aab6cf")
    ax.set_xlabel("Target gene (normalized to UBQ10)", color="#aab6cf")
    ax.grid(True, axis="y", color="#1a2238", lw=0.8)
    ax.legend(facecolor="#111729", edgecolor="#26324f", labelcolor="#e8edf7", fontsize=9)
    out = os.path.join(CHARTS, "qpcr_fold_change.png")
    fig.tight_layout(); fig.savefig(out, dpi=130, facecolor="#0a0e1a"); plt.close(fig)
    print("chart ->", out)


if __name__ == "__main__":
    main()
