"""
Reshape the processed results into an OSDR/GeneLab-aligned submission package.

NASA OSDR uses the ISA model (Investigation - Study - Assay) with ISA-Tab style
tables: 'Sample Name', 'Characteristics[...]', 'Factor Value[...]',
'Parameter Value[...]', 'Protocol REF'. This writes an *aligned* package (as CSV
for readability) that a curator can finalize into strict ISA-Tab TSV.

Inputs  (data/processed/):
  trees_growth/growth_data.csv         per-frame canopy
  reggies_qpcr/qpcr_ct_long.csv        per sample x gene dCt
  reggies_qpcr/qpcr_fold_change.csv    per treatment x gene fold-change
Outputs (osdr_submission/):
  s_study_madwest.csv                  study-level metadata
  a_trees_growth_phenotype.csv         phenotype assay (one row per plant)
  a_reggies_qpcr_transcription.csv     transcription assay (one row per sample x gene)
  derived_qpcr_fold_change.csv         derived ΔΔCt fold-change summary
  README.md                            how this maps to OSDR / how to finalize

NOT a validated OSDR deposit — confirm current OSDR requirements before submitting.
"""
import os, csv
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PROC = os.path.join(HERE, "..", "data", "processed")
OUT = os.path.join(HERE, "..", "osdr_submission")
os.makedirs(OUT, exist_ok=True)

TREES_LABELS = {
    "MR_plusMicrobe_flight":  ("present", "flight"),
    "R_minusMicrobe_flight":  ("absent",  "flight"),
    "M_plusMicrobe_control":  ("present", "ground control"),
    "X_minusMicrobe_control": ("absent",  "ground control"),
}
QPCR_ORGANISM = "Arabidopsis thaliana"


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---- TREES phenotype assay -------------------------------------------------
def trees_assay():
    rows = read_csv(os.path.join(PROC, "trees_growth", "growth_data.csv"))
    per_plant = defaultdict(list)
    for r in rows:
        per_plant[(r["treatment"], r["plant"])].append((float(r["hours"]), float(r["canopy_kpx"])))
    out = []
    for (trt, plant), ser in sorted(per_plant.items()):
        ser.sort()
        start = sum(y for _, y in ser[:3]) / min(3, len(ser))
        end = sum(y for _, y in ser[-3:]) / min(3, len(ser))
        peak = max(y for _, y in ser)
        dur_days = (ser[-1][0] - ser[0][0]) / 24.0
        ecm, flight = TREES_LABELS[trt]
        sample = f"TREES_{plant.split()[0]}"
        out.append({
            "Sample Name": sample,
            "Characteristics[Organism]": "Populus tremula",
            "Characteristics[Symbiont]": "ectomycorrhizal fungi (species not recorded)",
            "Characteristics[Growth medium]": "agar plate",
            "Factor Value[Ectomycorrhizal inoculation]": ecm,
            "Factor Value[Spaceflight]": flight,
            "Protocol REF": "timelapse imaging; green-canopy image analysis",
            "Parameter Value[Imaging duration]": round(dur_days, 2),
            "Unit[Imaging duration]": "day",
            "Phenotype[Green canopy area, start]": round(start, 2),
            "Phenotype[Green canopy area, peak]": round(peak, 2),
            "Phenotype[Green canopy area, end]": round(end, 2),
            "Unit[Green canopy area]": "kilopixel (700px analysis width)",
            "Derived[End over peak]": round(end / peak, 3) if peak else "",
            "Derived[Canopy change, start to end]": round((end / start - 1) * 100, 1) if start else "",
            "Unit[Canopy change]": "percent",
        })
    return out


# ---- qPCR transcription assay ---------------------------------------------
def qpcr_assay():
    ct = read_csv(os.path.join(PROC, "reggies_qpcr", "qpcr_ct_long.csv"))
    out = []
    for r in ct:
        out.append({
            "Sample Name": f"RV_{r['sample_id']}",
            "Characteristics[Organism]": QPCR_ORGANISM,
            "Characteristics[Genotype]": "Col-0",
            "Factor Value[Spaceflight]": r["treatment"],
            "Protocol REF": "RNA extraction; reverse transcription; qPCR (SYBR)",
            "Parameter Value[Reference gene]": "UBQ10",
            "Assay[Target gene]": r["gene"],
            "Data[Mean Ct]": r["mean_ct"],
            "Data[Reference Ct]": r["ref_ct_UBQ10"],
            "Derived[delta Ct]": r["dCt"],
            "Parameter Value[Technical replicates]": r["n_tech_reps"],
        })
    return out


def write_table(name, rows):
    path = os.path.join(OUT, name)
    if not rows:
        print("skip (no rows):", name); return
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("wrote", os.path.relpath(path, HERE), f"({len(rows)} rows)")


def write_study():
    fields = [
        ("Study Identifier", "MADWEST-2018"),
        ("Study Title", "MadWest Rocketry botanical sounding-rocket program: Arabidopsis spaceflight stress-gene expression and a Populus tremula x ectomycorrhiza survival experiment"),
        ("Study Description", "A high-school sounding-rocket program (2018, motor K1620) across three launches. Launch 1 (Arabidopsis test): flown seedlings showed earlier flowering, and co-flown ectomycorrhizal spores remained viable after flight. Launch 2 (Arabidopsis, repeat): flown vs. launch-site and lab controls, assayed by qPCR for stress-response genes (MPK3, TCH3, CBP60g) normalized to UBQ10 -- the 'Reggies' Veggies' molecular arm. Launch 3 ('TREES', codename): Populus tremula seedlings +/- ectomycorrhizal (ECM) inoculation, flown vs. ground, imaged as a timelapse to test whether the fungal symbiosis aids flight survival; green-canopy image analysis instead showed the mycorrhizal groups peaking then declining (die-back)."),
        ("Study Organism", "Arabidopsis thaliana (launches 1-2); Populus tremula (launch 3)"),
        ("Study Factor Name", "Spaceflight; Ectomycorrhizal inoculation"),
        ("Study Factor Type", "experimental factor; experimental factor"),
        ("Study Assay Measurement Type", "growth phenotype (timelapse image analysis); transcription profiling (qPCR)"),
        ("Study Protocol Name", "timelapse imaging; green-canopy image analysis; RNA extraction; qPCR; delta-delta-Ct analysis"),
        ("Study Person (Role)", "TODO - add PI / contributors (see CITATION.cff)"),
        ("Study Public Release Date", "TODO"),
        ("Comment[Caveats]", "Classroom-scale. TREES (Populus) n=2-5/group with UNEVEN imaging windows (+ECM tracked ~9 d, -ECM ~6 d) -- the die-back is clearest in the longer-tracked +ECM plants. qPCR n=4/group, trends only. ECM fungal species not recorded in the source. See DEVLOG.md."),
        ("Comment[Affiliation with NASA]", "None - independent educational project; not affiliated with or endorsed by NASA."),
    ]
    path = os.path.join(OUT, "s_study_madwest.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["Field", "Value"]); w.writerows(fields)
    print("wrote", os.path.relpath(path, HERE))


def write_readme(n_trees, n_qpcr):
    txt = f"""# OSDR submission package (aligned, not yet validated)

This folder reshapes the processed results into the **ISA model** that NASA OSDR
/ GeneLab uses (Investigation - Study - Assay). Files are CSV for readability;
strict OSDR ISA-Tab is tab-delimited `.txt` — a curator can convert these.

## Files
| File | ISA role | Contents |
|------|----------|----------|
| `s_study_madwest.csv` | Study | Study-level metadata, factors, protocols |
| `a_trees_growth_phenotype.csv` | Assay | TREES growth phenotype, one row per plant ({n_trees}) |
| `a_reggies_qpcr_transcription.csv` | Assay | qPCR transcription, one row per sample x gene ({n_qpcr}) |
| `derived_qpcr_fold_change.csv` | Derived | ΔΔCt fold-change per treatment x gene |

## Column conventions
`Sample Name`, `Characteristics[...]` (intrinsic properties), `Factor Value[...]`
(the experimental variables), `Parameter Value[...]` (protocol parameters),
`Protocol REF`, plus `Data[...]`/`Phenotype[...]`/`Derived[...]` for measurements.

## Before submitting to OSDR
1. Confirm the **current** OSDR submission format & requirements at
   https://osdr.nasa.gov/ (the process is set by NASA and changes).
2. Fill the `TODO` fields in `s_study_madwest.csv` (people, release date) and the
   TREES organism (species).
3. Convert CSV -> ISA-Tab TSV and add the investigation file (`i_*.txt`) if the
   current OSDR workflow requires full ISA-Tab.
4. Attach the raw data (imagery, qPCR exports) per OSDR's raw-data policy.

Independent educational project; not affiliated with or endorsed by NASA.
"""
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("wrote", os.path.relpath(os.path.join(OUT, "README.md"), HERE))


def copy_fold_change():
    src = os.path.join(PROC, "reggies_qpcr", "qpcr_fold_change.csv")
    rows = read_csv(src)
    write_table("derived_qpcr_fold_change.csv", rows)


if __name__ == "__main__":
    trees = trees_assay()
    qpcr = qpcr_assay()
    write_study()
    write_table("a_trees_growth_phenotype.csv", trees)
    write_table("a_reggies_qpcr_transcription.csv", qpcr)
    copy_fold_change()
    write_readme(len(trees), len(qpcr))
    print("OSDR package ->", os.path.relpath(OUT, HERE))
