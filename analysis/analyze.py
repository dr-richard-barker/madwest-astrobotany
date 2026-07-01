"""
MadWest TREES — canopy growth analysis.

Walks every treatment/plant/frame, measures green-canopy area per frame
(segment_lib), and writes:
  - growth_data.csv             one row per frame
  - ../assets/charts/growth_curves.png
  - ../assets/charts/relative_growth.png
  - ../assets/charts/final_canopy.png

Frames are resized to a fixed width so pixel areas are comparable across
plates. Canopy is reported in kilo-pixels (kpx) at that fixed width.
"""
import os, re, glob, csv
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from segment_lib import segment_canopy

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "raw", "trees_timelapse")
CHARTS = os.path.join(HERE, "..", "assets", "charts")
PROCESSED = os.path.join(HERE, "..", "data", "processed", "trees_growth")
os.makedirs(CHARTS, exist_ok=True)
os.makedirs(PROCESSED, exist_ok=True)
CSV_PATH = os.path.join(PROCESSED, "growth_data.csv")

WIDTH = 700  # fixed analysis width

# TREES launch: Populus tremula host x ectomycorrhizal (ECM) inoculation x flight.
# Folder keys keep the original "Microbe" tag; labels use the accurate ECM naming.
TREATMENTS = {
    "MR_plusMicrobe_flight":  dict(label="+ECM · Flight",  color="#36c97f"),
    "R_minusMicrobe_flight":  dict(label="−ECM · Flight",  color="#5aa9ff"),
    "M_plusMicrobe_control":  dict(label="+ECM · Ground",  color="#1f7a4d"),
    "X_minusMicrobe_control": dict(label="−ECM · Ground",  color="#2f5f8f"),
}

TS = re.compile(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})_(\d{2})_(\d{2})")

def parse_hours(fname):
    m = TS.search(fname)
    if not m:
        return None
    y, mo, d, H, M, S = map(int, m.groups())
    # hours since an arbitrary epoch (2018-01-01); only differences matter
    from datetime import datetime
    return (datetime(y, mo, d, H, M, S) - datetime(2018, 1, 1)).total_seconds() / 3600.0


def canopy_kpx(path):
    bgr = cv2.imread(path)
    if bgr is None:
        return None
    h, w = bgr.shape[:2]
    bgr = cv2.resize(bgr, (WIDTH, int(h * WIDTH / w)))
    _, px = segment_canopy(bgr)
    return px / 1000.0


def main():
    rows = []
    for tkey in TREATMENTS:
        tdir = os.path.join(DATA, tkey)
        plant_dirs = sorted(d for d in glob.glob(tdir + "/*") if os.path.isdir(d))
        for pdir in plant_dirs:
            plant = os.path.basename(pdir)
            # all frames under the plant (direct + nested "<plant> test" early run)
            frames = glob.glob(pdir + "/**/*.jpg", recursive=True)
            series, seen = [], set()
            for fp in frames:
                hrs = parse_hours(os.path.basename(fp))
                if hrs is None or round(hrs, 3) in seen:
                    continue
                kpx = canopy_kpx(fp)
                if kpx is None:
                    continue
                seen.add(round(hrs, 3))
                series.append((hrs, kpx))
            if not series:
                continue
            series.sort()
            t0 = series[0][0]
            base = series[0][1] if series[0][1] > 1 else max(s[1] for s in series[:3]) or 1
            for hrs, kpx in series:
                rows.append(dict(treatment=tkey, plant=plant,
                                 hours=round(hrs - t0, 3),
                                 canopy_kpx=round(kpx, 2),
                                 rel=round(kpx / base, 4) if base else 0))
            print(f"{tkey:24s} {plant:20s} {len(series):3d} frames  "
                  f"canopy {series[0][1]:6.1f} -> {series[-1][1]:6.1f} kpx")

    # write per-frame csv
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["treatment", "plant", "hours", "canopy_kpx", "rel"])
        w.writeheader(); w.writerows(rows)
    print("wrote", CSV_PATH, len(rows), "rows")

    write_summary(rows)
    make_charts(rows)


def write_summary(rows):
    """Per-treatment start/end canopy + % change -> treatment_summary.csv."""
    by_t = {k: {} for k in TREATMENTS}
    for r in rows:
        by_t[r["treatment"]].setdefault(r["plant"], []).append((r["hours"], r["canopy_kpx"]))
    out = os.path.join(PROCESSED, "treatment_summary.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["treatment", "label", "n_plants", "mean_imaging_days",
                    "start_canopy_kpx", "peak_canopy_kpx", "end_canopy_kpx",
                    "end_over_peak", "pct_change_start_to_end"])
        for tkey, meta in TREATMENTS.items():
            plants = by_t[tkey]
            if not plants:
                continue
            s_vals, pk_vals, e_vals, day_vals = [], [], [], []
            for ser in plants.values():
                ser.sort()
                s_vals.append(float(np.mean([y for _, y in ser[:3]])))
                pk_vals.append(float(max(y for _, y in ser)))
                e_vals.append(float(np.mean([y for _, y in ser[-3:]])))
                day_vals.append((ser[-1][0] - ser[0][0]) / 24.0)
            s, pk, e = np.mean(s_vals), np.mean(pk_vals), np.mean(e_vals)
            w.writerow([tkey, meta["label"], len(plants), round(np.mean(day_vals), 1),
                        round(s, 2), round(pk, 2), round(e, 2),
                        round(e/pk, 2) if pk else "",
                        round((e/s - 1)*100, 1) if s else ""])
    print("wrote", out)


def rolling_median(ys, win=5):
    n = len(ys); out = []
    h = win // 2
    for i in range(n):
        out.append(float(np.median(ys[max(0, i-h):min(n, i+h+1)])))
    return out


def plant_series(rows, plant, key):
    pts = sorted((r["hours"], r[key]) for r in rows if r["plant"] == plant)
    if not pts:
        return np.array([]), np.array([])
    t = np.array([p[0] for p in pts]) / 24.0          # days
    y = np.array(rolling_median([p[1] for p in pts]))  # smoothed
    return t, y


def grid_mean(plants_xy, step=0.5):
    """Interpolate each plant onto a common grid (no extrapolation), then
    average across plants present. Returns (grid, mean, lo, hi, nmax)."""
    if not plants_xy:
        return None
    tmax = max(t[-1] for t, _ in plants_xy if len(t))
    grid = np.arange(0, tmax + 1e-9, step)
    cols = []
    for t, y in plants_xy:
        if len(t) < 2:
            continue
        vals = np.interp(grid, t, y)
        vals[(grid < t[0]) | (grid > t[-1])] = np.nan  # no extrapolation
        cols.append(vals)
    if not cols:
        return None
    M = np.vstack(cols)
    with np.errstate(all="ignore"):
        mean = np.nanmean(M, axis=0)
        lo = np.nanmin(M, axis=0); hi = np.nanmax(M, axis=0)
        n = np.sum(~np.isnan(M), axis=0)
    ok = n >= 1
    return grid[ok], mean[ok], lo[ok], hi[ok], int(n.max())


def _curve_chart(by_t, key, title, ylabel, fname, hline=None):
    plt.figure(figsize=(8.8, 5.1))
    for tkey, meta in TREATMENTS.items():
        plants = sorted({r["plant"] for r in by_t[tkey]})
        xy = [plant_series(by_t[tkey], p, key) for p in plants]
        xy = [(t, y) for t, y in xy if len(t)]
        # faint individual plant traces
        for t, y in xy:
            plt.plot(t, y, "-", lw=0.8, alpha=0.22, color=meta["color"])
        g = grid_mean(xy)
        if g:
            grid, mean, lo, hi, nmax = g
            plt.fill_between(grid, lo, hi, color=meta["color"], alpha=0.10, lw=0)
            plt.plot(grid, mean, "-", lw=2.6, color=meta["color"],
                     label=f"{meta['label']}  (n={len(xy)})")
    if hline is not None:
        plt.axhline(hline, color="#6f7d9c", ls="--", lw=1)
    style_axes(title, "Days since each plant's first frame", ylabel)
    save(fname)


def make_charts(rows):
    by_t = {k: [] for k in TREATMENTS}
    for r in rows:
        by_t[r["treatment"]].append(r)

    _curve_chart(by_t, "canopy_kpx", "Canopy growth by treatment",
                 "Green canopy area (kpx)", "growth_curves.png")
    _curve_chart(by_t, "rel",
                 "Relative canopy growth (each plant normalized to its start)",
                 "Canopy area (× start)", "relative_growth.png", hline=1.0)

    # --- start / peak / end bars: exposes the peak-then-decline (die-back) ---
    labels, starts, peaks, ends, colors, retent = [], [], [], [], [], []
    for tkey, meta in TREATMENTS.items():
        s, pk, e = _group_start_peak_end(by_t[tkey])
        if s is None:
            continue
        labels.append(meta["label"]); colors.append(meta["color"])
        starts.append(s); peaks.append(pk); ends.append(e)
        retent.append(e / pk if pk else 0)

    x = np.arange(len(labels)); w = 0.26
    plt.figure(figsize=(8.8, 5.1))
    plt.bar(x - w, starts, w, label="Start", color="#26324f")
    plt.bar(x, peaks, w, label="Peak", color=colors)
    plt.bar(x + w, ends, w, label="End", color="#7a2f2f")
    for i, (pk, e) in enumerate(zip(peaks, ends)):
        plt.text(i + w, e, f"{retent[i]*100:.0f}% of peak", ha="center",
                 va="bottom", color="#ffb27a", fontsize=8.5)
    plt.xticks(x, labels, fontsize=9)
    style_axes("Canopy start → peak → end: mycorrhizal groups fall back from their peak",
               "", "Green canopy area (kpx)", legend=True)
    save("final_canopy.png")


def _group_start_peak_end(rows):
    """Mean-across-plants of each plant's start(first 3), peak, end(last 3)."""
    plants = {}
    for r in rows:
        plants.setdefault(r["plant"], []).append((r["hours"], r["canopy_kpx"]))
    s_vals, pk_vals, e_vals = [], [], []
    for ser in plants.values():
        ser.sort()
        s_vals.append(np.mean([y for _, y in ser[:3]]))
        pk_vals.append(max(y for _, y in ser))
        e_vals.append(np.mean([y for _, y in ser[-3:]]))
    if not s_vals:
        return None, None, None
    return float(np.mean(s_vals)), float(np.mean(pk_vals)), float(np.mean(e_vals))


def style_axes(title, xlabel, ylabel, legend=True):
    ax = plt.gca()
    ax.set_facecolor("#0f1525")
    plt.gcf().set_facecolor("#0a0e1a")
    for s in ax.spines.values():
        s.set_color("#26324f")
    ax.tick_params(colors="#aab6cf")
    ax.set_title(title, color="#e8edf7", fontsize=12, pad=12)
    ax.set_xlabel(xlabel, color="#aab6cf"); ax.set_ylabel(ylabel, color="#aab6cf")
    ax.grid(True, color="#1a2238", lw=0.8)
    if legend:
        lg = ax.legend(facecolor="#111729", edgecolor="#26324f", labelcolor="#e8edf7", fontsize=9)


def save(name):
    p = os.path.join(CHARTS, name)
    plt.tight_layout(); plt.savefig(p, dpi=130, facecolor="#0a0e1a"); plt.close()
    print("chart ->", p)


def charts_from_csv():
    rows = []
    with open(CSV_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(dict(treatment=r["treatment"], plant=r["plant"],
                             hours=float(r["hours"]), canopy_kpx=float(r["canopy_kpx"]),
                             rel=float(r["rel"])))
    write_summary(rows)
    make_charts(rows)
    print("charts + summary rebuilt from csv")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "charts":
        charts_from_csv()
    else:
        main()
