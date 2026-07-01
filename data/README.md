# Data — provenance & dictionary

This folder is the **research data package** for the MadWest Rocketry /
Reggies' Veggies space-biology study. It is organized for open release to
**GitHub** (code + processed data) and **Zenodo** (full archival deposit, incl.
the raw imagery). The study has two arms from the same 2018 flight campaign:

- **TREES** — a timelapse *growth-phenotype* experiment (image analysis).
- **Reggies' Veggies** — the *molecular* experiment (flight telemetry + qPCR).

```
data/
├── raw/                      # original source data — git-ignored (see note)
│   ├── trees_timelapse/      # ~850 MB  timelapse frames (growth arm)
│   └── reggies_veggies/      # ~180 MB  flight + molecular arm
└── processed/                # analysis outputs — COMMITTED to git
    ├── trees_growth/
    │   ├── growth_data.csv         # one row per analysed frame
    │   └── treatment_summary.csv   # per-treatment start/peak/end canopy + die-back (end/peak)
    └── reggies_qpcr/
        ├── qpcr_ct_long.csv        # one row per sample × gene (mean Ct, ΔCt)
        └── qpcr_fold_change.csv    # per treatment × gene ΔΔCt + fold-change
```

> An OSDR/ISA-aligned reshaping of all of the above lives in the top-level
> `osdr_submission/` folder (see its README). Regenerate with
> `python analysis/osdr_export.py`.

> **Git note:** `data/raw/` is in `.gitignore` (~1 GB, too big for git). It is
> documented here and uploaded to **Zenodo directly**. The committed
> `data/processed/` files are small and fully reproducible from the raw data via
> `analysis/` (see the repo README).

---

## The three launches (2018, Cesaroni K1620 motor)

The two arms in this folder come from **different launches** of the same program:

- **Launch 2 — Reggies' Veggies (molecular arm):** *Arabidopsis thaliana* Col-0,
  **three groups** (Flight, Launch-site travel control, Lab ground), assayed by
  qPCR. → `raw/reggies_veggies/`
- **Launch 3 — TREES (growth arm):** *Populus tremula* seedlings, a **2×2**
  design (ectomycorrhizal inoculation ± × flight). → `raw/trees_timelapse/`

(Launch 1, an earlier *Arabidopsis* test that showed earlier flowering and viable
co-flown ECM spores, is described qualitatively in the manuscript; no dataset for
it survives in this folder.)

### TREES 2×2 (launch 3 only)

|                  | + ECM (mycorrhizal) | − ECM |
|------------------|---------------------|-------|
| Flight (rocket)  | **MR**              | **R** |
| Ground control   | **M**               | **X** |

"ECM" = ectomycorrhizal fungal inoculation of the *Populus* host; "Flight" =
flown vs. ground. **Note:** the folder keys say `plusMicrobe`/`minusMicrobe` —
that "microbe" is the ECM fungus; kept as-is to avoid re-touching the raw tree.

---

## `raw/trees_timelapse/` — growth arm (launch 3: *Populus tremula* × ECM)

Backlit gridded agar plates of *Populus tremula* (aspen) seedlings photographed
over ~12 days. Green shoot/canopy (measured), reddish roots, a diagonal frosted
cover over the root half. The experiment tested whether ectomycorrhizal symbiosis
aids flight survival; the analysis found the **mycorrhizal plants die back** (see
the processed summary and the repo README).

```
trees_timelapse/<treatment>/<plant> jpegs/*.jpg
trees_timelapse/<treatment>/<plant> jpegs/<plant> test/*.jpg   # earlier frames
```

- Treatments (`plusMicrobe` = +ECM): `MR_plusMicrobe_flight` (4 plants),
  `R_minusMicrobe_flight` (2), `M_plusMicrobe_control` (5),
  `X_minusMicrobe_control` (2).
- Frame filenames embed a timestamp: `…-YYYY-MM-DD-HH_MM_SS_result.jpg`.
- The nested `<plant> test/` folder holds the **earlier** part of that plant's
  timelapse; the pipeline merges both and de-duplicates by timestamp.
- The ECM **fungal species is not recorded** in the source files.

## `raw/reggies_veggies/` — molecular arm (launch 2: *Arabidopsis*)

See `raw/reggies_veggies/README.md` for the full breakdown. Summary:

| Subfolder | Contents |
|-----------|----------|
| `flight/` | Altimeter exports (`.pf2`), flight log (`RVFlight1.xlsx`), K1620 thrust curve |
| `molecular/rna_extraction/` | RNA extraction protocols, RNA concentrations, sample tracking |
| `molecular/qpcr_setup/` | Plate design, dilutions, sample status, gene info |
| `molecular/qpcr_results/` | qPCR data (xlsx), instrument exports (eds/edt), amplification plots |
| `molecular/qpcr_analysis/` | Worked qPCR analysis spreadsheets |
| `media_prep/` | Space-media protocols, sample lists, tube spreadsheets |
| `photos/` | 50 launch & lab photographs |
| `reports/` | Project report & timeline documents |

---

## `processed/trees_growth/` — data dictionary

### `growth_data.csv` — one row per analysed timelapse frame
| Column | Type | Description |
|--------|------|-------------|
| `treatment` | string | Treatment key (e.g. `MR_plusMicrobe_flight`) |
| `plant` | string | Plant/replicate folder name |
| `hours` | float | Hours since that plant's first frame |
| `canopy_kpx` | float | Green-canopy area, kilo-pixels at 700 px analysis width |
| `rel` | float | Canopy ÷ that plant's starting canopy (fold-change) |

### `treatment_summary.csv` — one row per treatment
| Column | Description |
|--------|-------------|
| `treatment` | Treatment key |
| `label` | Human-readable label (e.g. `+ECM · Flight`) |
| `n_plants` | Number of plants (replicates) |
| `mean_imaging_days` | Mean per-plant imaging window (days) — differs by group |
| `start_canopy_kpx` | Mean of each plant's first-3-frame canopy |
| `peak_canopy_kpx` | Mean of each plant's maximum canopy |
| `end_canopy_kpx` | Mean of each plant's last-3-frame canopy |
| `end_over_peak` | End ÷ peak — the **die-back** metric (+ECM ≈ 0.71–0.73; −ECM ≈ 0.94–0.96) |
| `pct_change_start_to_end` | Percent change start → end (can hide the die-back) |

### `reggies_qpcr/qpcr_ct_long.csv` — one row per sample × gene
| Column | Description |
|--------|-------------|
| `sample_id` | qPCR sample ID (numeric, from the plate design) |
| `treatment` | Flight / Launch site / Ground (per `Plate design.xlsx`) |
| `gene` | Target gene (MPK3, TCH3, CBP60g) |
| `mean_ct` | Mean Ct across technical replicates |
| `ref_ct_UBQ10` | Mean Ct of the UBQ10 reference for that sample |
| `dCt` | ΔCt = `mean_ct` − `ref_ct_UBQ10` |
| `n_tech_reps` | Technical replicate wells averaged |

### `reggies_qpcr/qpcr_fold_change.csv` — one row per treatment × gene
ΔΔCt vs the lab Ground-control calibrator and `fold_change` = 2^(−ΔΔCt), with a
`fold_lo`/`fold_hi` range from the biological-replicate SD, plus `log2_fold`.

**Caveats:** classroom-scale. TREES (*Populus* × ECM): n = 2–5 per group, and
imaging windows differ by treatment (+ECM ~9 days, −ECM ~6) — a confound for the
die-back comparison; canopy is a 2-D pixel proxy (no cm² calibration); the ECM
fungal species is not recorded. qPCR (*Arabidopsis*): n = 4 per group, error
bands cross "no change" (trends, not significance); sample IDs 22/23 are grouped
per the plate design but labeled differently in the tube-status sheet. Treat
everything as trends, not proof — see `DEVLOG.md`.

## Regenerate processed data
```bash
cd analysis && python analyze.py        # raw frames -> processed CSVs + charts
```
