# Dev log & decisions — MadWest Rocketry × OSDR

A running record of *why* this project looks the way it does: the decisions,
the tangents, the things that didn't work, and the reasoning behind the choices.
Newest work at the bottom. If you're picking this up cold, read this first.

---

## 1 · Project genesis

**Goal:** a one-stop website connecting "MadWest Rocketry" (botanical sounding
rockets — rockets carrying living plant payloads) to **NASA OSDR** (the Open
Science Data Repository for space biology), so a club/classroom flight ends as
open, reusable data rather than a number in a notebook.

**Starting point:** the project folder was **completely empty**. The user said
they'd "started making this website," but nothing was saved here.

**Search for prior work** turned up, in `~/Downloads`:
- `Rockets.oxps` — an XPS print file (not used).
- `DRB ROB3.0 Early Career Investigation application_v2_Jan_2025.docx.html` —
  a **SharePoint online-viewer wrapper** around a Purdue grant application
  (author `barkerrj@purdue.edu`). It was full of auth tokens and viewer
  telemetry, not readable document body. **Decision: did not mine it** — it's
  sensitive (live-ish tokens) and wasn't really the site's source material.

**Decisions made up front (asked the user):**
- Build = **multi-page static site** (not single-page, not a framework).
- First-version focus = **build-guide hub**.

**Initial build:** `index.html`, `build-guide.html`, `osdr-training.html`,
`data-submission.html`, `about.html` + shared `css/styles.css`, `js/main.js`.
Theme = deep-space night sky + botanical green. Every page footer carries a
**"not affiliated with / endorsed by NASA"** disclaimer because the site leans
heavily on NASA/OSDR naming. Placeholders that need the user's real info are
tagged inline with `class="todo"` badges.

---

## 2 · Discovering the real experiment data

The user then pointed at "results" they wanted integrated — timelapse images of
"TREES" growing, with image analysis across treatments.

Found in `~/Downloads`:
`Astro-Rocketry MadWest Rocketry and plants-.../TREES/` plus a sibling
`Reggies Veggies 2/` (gene info, qPCR, flight data, posters — **not** integrated
yet; potential future work).

**The TREES dataset is a clean 2×2 factorial design.** The folder names encode
it cryptically; decoded:

|                  | + Microbe | − Microbe |
|------------------|-----------|-----------|
| Flight (rocket)  | `MR, +M flight` → **MR** | `R, -M rocket` → **R** |
| Ground control   | `M, +M control` → **M**  | `X, -M control` → **X** |

- ~2,628 JPEG timelapse frames, **850 MB**, 13 plants total.
- Plant counts are **uneven**: M=5, MR=4, R=2, X=2.
- Frames are pre-processed `..._result.jpg` images: a backlit gridded agar
  plate, green shoot up top, reddish roots below, a diagonal frosted cover over
  the root half. Filenames carry timestamps:
  `N1-2018-05-29-02_00_48_result.jpg`.

---

## 3 · Tangents & dead-ends in the analysis

This is where most of the real engineering went. Recorded so nobody repeats it.

### 3a · "Move" vs copy the 850 MB
User said "move these results into the folder." **Chose to *copy*, not move** —
keeps the Downloads original as a backup if the pipeline corrupts something.
Trade-off: 850 MB duplicated on disk. Mitigated by `.gitignore` (raw data never
goes to git; only the small derived videos/charts do).

### 3b · Green segmentation — first attempt failed hard
First segmenter used an **HSV green-hue gate** (`H ∈ [33,95]`, with saturation/
value thresholds). Result: **0 canopy pixels on the M and X plates** — which are
the *obviously leafy* ones. Cause: those plates are brightly **backlit and
yellow-green**, pushing leaf hue below the green threshold and blowing out
saturation. A fixed hue gate can't survive the plate-to-plate lighting variance.

### 3c · Method bake-off — ExG vs LAB-a*
Compared two approaches on a hard (yellow) plate and an easy (green) one, saving
overlay images to eyeball:
- **LAB `a*` channel** (green = `a < 128`): correctly rejected the yellow
  backlight glow, but **missed blown-out leaf centers** → undercounts canopy.
- **Excess-Green index** (`ExG = 2G − R − B`): captured the **full** canopy
  including bright centers, correctly ignored the reddish roots — but also
  grabbed the **near-white backlight glare** strip at the plate margin.

**Decision: ExG wins on completeness**, then explicitly subtract glare.

### 3d · The glare fix
Key insight: even *yellow* leaves keep a **low blue channel**, whereas backlight
blowout / frost glare is bright in **all** channels (near-white). So:
`canopy = (ExG > 20) AND NOT(min(R,G,B) > 170)`, then morphology + drop tiny
connected components. Verified visually — clean leaf trace, roots & frost
excluded. This is what `segment_lib.py` ships.

### 3e · The Windows path bug (silent data loss)
The QA script built output filenames with `os.path.basename(tr.rstrip("/"))`.
On Windows `glob` returns **backslash** paths, so `rstrip("/")` did nothing,
`basename` returned `""`, and **all four treatments overwrote the same QA file**
— making it look like only one treatment processed. Fix: `os.path.normpath`.
Lesson: never `rstrip("/")` a path on Windows; use `os.path`.

### 3f · Half the frames were "hidden" in nested folders
First full run only saw **1,345 of 2,628** frames, and two plant folders
(`mr1-3`, `m2-2`) produced nothing. Cause: each `<plant> jpegs/` folder contains
a nested `<plant> test/` subfolder holding the **earlier** part of that plant's
timelapse (dates from 2018-05-23, before the direct frames at 05-28+). The glob
only matched direct children.
**Fix:** collect frames recursively and **de-duplicate by timestamp**. This also
*improved the science* — combining the runs gives the full ~12-day growth arc
(small seedling → full canopy) instead of just the mature tail.

### 3g · The sawtooth chart artifact
First growth charts were violently jagged — means spiking between e.g. 3× and
4.5× frame to frame. Cause: **binned-mean over raw points** mixed plants with
very different absolute sizes and uneven time coverage, so the mean jumped as
plants entered/left each time bin. Per-plant frame jitter (condensation, the
plant physically moving) made it worse.
**Fix (current charting):**
1. Smooth each plant with a **rolling median** (tames transient spikes).
2. **Interpolate** each plant onto a common time grid — **no extrapolation**
   beyond its own coverage.
3. Average across plants present at each grid point; show a **min–max band** and
   **faint individual traces** for honesty (small n, real spread).

### 3h · `analyze.py charts` fast path
Re-segmenting all frames takes ~70 s. Added a `python analyze.py charts` mode
that rebuilds charts from the existing `growth_data.csv` in ~1 s, so chart
styling can be iterated without reprocessing imagery.

---

## 4 · Timelapse video tangents

### 4a · Codec problem
Browsers need **H.264** in `<video>`. OpenCV's `VideoWriter` can't reliably
write H.264 without a system ffmpeg, and there was **no ffmpeg on PATH** (the
`convert` found was Windows' disk utility, not ImageMagick).
**Fix:** `pip install imageio-ffmpeg` — it ships a static ffmpeg binary. Write
via `imageio` with `codec=libx264` + `-pix_fmt yuv420p` (the pixel format that
actually plays in browsers; without it Safari/Chrome may show black).

### 4b · Syncing four plants of different lengths
The 2×2 montage resamples each plant to a fixed **N_SYNC = 220** output frames by
index, so all four "grow together" on screen regardless of original frame count.
**Known imperfection:** because each plant spans a different real duration, the
burned-in **day counters are not synchronized** across tiles. Chose to label each
tile with *its own* elapsed day rather than fake a shared clock. Acceptable for a
visual comparison; noted on the Results page too.

---

## 5 · Key decisions at a glance

| Decision | Choice | Why |
|----------|--------|-----|
| Site type | Multi-page static | User pick; easy to host, no build step |
| NASA branding | Disclaimer in every footer | Site leans on NASA/OSDR names |
| Raw 850 MB data | Copy in, git-ignore | Keep backup; don't bloat git |
| Canopy segmentation | ExG + glare removal | Only method robust to lighting variance |
| Frame collection | Recursive + dedupe | Nested `test/` folders hold early growth |
| Treatment averaging | Interp to grid + band | Kills the sawtooth; honest about spread |
| Growth metric | Canopy area (px) + relative | Px proxy; relative controls plate scale |
| Video codec | libx264 via imageio-ffmpeg | No system ffmpeg; browsers need H.264 |
| Charts altitude | Trends, not proof | n = 2–5/group; said plainly on the page |

---

## 6 · Known limitations (be honest about these)

- **Small sample:** 2–5 plants per treatment; the −Microbe groups (n=2) were
  also imaged for a **shorter window** (~6–7 days vs ~12 for +Microbe).
- **Canopy is a 2-D pixel proxy**, not biomass. No scale calibration yet, so
  areas are in kilo-pixels at a fixed analysis width, not cm².
- **Neighboring plates** occasionally peek into frame edges; not masked out.
- The montage day-counters are per-tile, not a shared clock (see 4b).
- `Reggies Veggies 2/` (gene info, qPCR, flight data) is **not** integrated.

---

## 7 · Reproduce / regenerate

```bash
pip install opencv-python numpy matplotlib imageio imageio-ffmpeg
cd analysis
python analyze.py          # segment all frames -> growth_data.csv + charts (~1 min)
python analyze.py charts   # rebuild charts only from the CSV (fast)
python make_timelapse.py   # per-treatment + 2x2 comparison MP4s
```
Outputs → `assets/charts/`, `assets/timelapse/`, `assets/thumbs/`.

---

## 8 · Candidate next steps

- **Root-growth analysis** — roots are clearly visible; segment them too.
- **Scale calibration** from the printed grid → report real cm² instead of px.
- More qPCR replicates to move the gene trends past "trend" toward significance.
- Fill the `class="todo"` placeholders (org/safety rules, contact links, a model
  OSDR study to mirror, confirm OSDR's current submission process).

> Done since first written: ✅ qPCR ΔΔCt analysis (§10) · ✅ OSDR/ISA export (§11).

---

## 9 · Reorg for GitHub + Zenodo + Reggies' Veggies integration

Restructured the repo into a **research compendium** and integrated the second
experiment arm, in preparation for public release.

### Decisions
- **Site stays at repo root** (not moved into `site/`). Reason: zero-config
  GitHub Pages, and it avoids rewriting relative paths in 6 HTML files.
- **`data/` split into `raw/` + `processed/`.** `data/trees/` → moved (fast,
  same-volume `mv`) to `data/raw/trees_timelapse/`. Updated the `DATA` constant
  in `analyze.py` and `make_timelapse.py` to match. Processed outputs now write
  to `data/processed/trees_growth/` (added `treatment_summary.csv` alongside the
  per-frame CSV).
- **Reggies' Veggies integrated** from the messy original (`Photos!`, smart
  quotes, duplicate root copies) into clean subfolders under
  `data/raw/reggies_veggies/`: `flight/`, `molecular/{rna_extraction,qpcr_setup,
  qpcr_results,qpcr_analysis}/`, `media_prep/`, `photos/`, `reports/`. Copied
  (not moved) verbatim; redundant top-level duplicate docs were not carried over
  (canonical copies live in subfolders). Renamed `Media!` → `protocols`.
- **Licensing (user pick):** MIT for code (`LICENSE`), CC-BY-4.0 for data
  (`LICENSE-data`).
- **Authors:** placeholders in `CITATION.cff` / `.zenodo.json` (user will fill).

### The two-destinations gotcha (important)
Raw imagery is ~1 GB, so it's **git-ignored**. That means the usual
**GitHub-release → Zenodo** webhook would archive a deposit with **no data**.
Resolution documented in `PUBLISHING.md`: push code+processed+site to GitHub;
upload the raw-data package to **Zenodo directly** (50 GB/record limit). Don't
rely on the GH hook for the data.

### Encoding bug (Windows)
`treatment_summary.csv` crashed writing the `−`/`·` characters in treatment
labels — Python's default CSV encoding on Windows is cp1252. Fix: open all CSV
reads/writes with `encoding="utf-8"`. Also made `analyze.py charts` rewrite the
summary (not just the charts) so the fast path stays consistent.

### Website integration
Added a **"molecular arm — Reggies' Veggies"** section to `results.html`: launch
photo, lab-plates photo, the K1620 thrust curve, the qPCR gene table, and an
amplification plot. Small web copies live in `assets/reggies/` (committed);
originals stay in the git-ignored raw tree. Framed honestly: raw data included,
qPCR analysis still pending.

### New files
`LICENSE`, `LICENSE-data`, `CITATION.cff`, `.zenodo.json`, `.gitattributes`,
`PUBLISHING.md`, `data/README.md` (data dictionary), and
`data/raw/reggies_veggies/README.md`. Updated `.gitignore` (`data/raw/` +
`*.eds`/`*.edt`).

---

## 10 · qPCR ΔΔCt analysis (Reggies' Veggies molecular arm)

Computed gene-expression fold-changes from the raw qPCR exports.

### Decoding the data
- Per-well **Ct** lives in the Applied Biosystems `Results` sheets (`Sophia
  Template 1/2_data.xlsx`). Header row is offset (row 8); the Ct column header is
  a mangled "Cт" — normalized headers (letters only) to find it (`c`).
- **Genes:** MPK3, TCH3, CBP60g (targets) + **UBQ10** (reference).
- **Sample IDs → treatment** came from `Plate design.xlsx`: FLIGHT (13,15,17,18),
  LAUNCH SITE (22,23,24,25), GROUND/lab control (5,6,20,21). Two complementary
  exports (Template 1 & 2) together cover all 12 samples with no overlap.

### The 22/23 discrepancy (flagged, not hidden)
`Plate design.xlsx` puts IDs **22 & 23** under "Launch site", but the upstream
`SAMPLE STATUS` tube table labels them "ground control" (`2CL1`,`2CL4`). Followed
the **plate design** (it's how the qPCR was physically laid out and analyzed) and
flagged it in the code, the data dictionary, and on the website. Doesn't touch
the Flight group (13/15/17/18 = Flight in both sources).

### Method
ΔCt = Ct(gene) − Ct(UBQ10) per sample → mean ΔCt per treatment → ΔΔCt vs the
lab-ground calibrator → fold = 2^(−ΔΔCt). Biological-replicate SD propagated into
a fold range. `analysis/qpcr_analysis.py`.

### Result (n=4/group, vs lab ground)
MPK3 ↓ in flight (0.34×), TCH3 ↓ (0.56×), CBP60g ↑ (1.60×). **Error bars cross
zero for every gene** — presented as trends, not significance. Honest framing on
the Results page and in the data dictionary.

### Gotcha
Same Windows cp1252 CSV-encoding trap as §9 — wrote all qPCR CSVs `utf-8`.

---

## 11 · OSDR / ISA export

`analysis/osdr_export.py` reshapes the processed results into NASA OSDR's **ISA
model** (Investigation–Study–Assay), written to `osdr_submission/`:
- `s_study_madwest.csv` — study metadata, factors, protocols (TODO: people, dates).
- `a_trees_growth_phenotype.csv` — phenotype assay, one row per plant, with
  `Factor Value[Spaceflight]` / `Factor Value[Microbe inoculation]`.
- `a_reggies_qpcr_transcription.csv` — transcription assay, one row per sample ×
  gene, with ΔCt.
- `derived_qpcr_fold_change.csv` — the ΔΔCt summary.

Used ISA-Tab column conventions (`Sample Name`, `Characteristics[...]`,
`Factor Value[...]`, `Parameter Value[...]`, `Protocol REF`). Written as CSV for
readability; the package README explains converting to strict ISA-Tab TSV.
**Deliberately not claimed as a validated OSDR deposit** — the export README and
the website both say to confirm OSDR's current requirements first. TREES organism
left as `species TODO` (the TREES arm species isn't documented in the source).

---

## 12 · Slideshows, the AstroBotany story, and the ASGSR manuscript

Added two presentation decks to the site and produced a conference submission.

### Decks → web slideshows
Two source PDFs (`MadWest_Gravitropism_RootAssay_summer_2016.pdf`, 4 pp;
`MadWest DR5_Venus.pdf`, 29 pp — the Read tool mis-reported 112). **No poppler**
on the box, so the Read tool can't render PDFs; installed **`pypdfium2`**
(self-contained PDFium, no external deps) to render pages → JPGs at 1600px into
`assets/slides/{gravitropism,reggies_story}/`. Source PDFs committed under
`slides/` (11.5 MB total — acceptable, and needed so the Story page's download
links work on GitHub Pages). Built a small dependency-free carousel
(`js/slideshow.js` + CSS): stage, prev/next, counter, captions, thumbnails,
keyboard. New `story.html`, linked in every nav after "Results".

### Reading the decks for accuracy
Rendered legible contact sheets and read the science slides. The DR5_Venus deck
is the **UW–Madison AstroBotany lab** story (GCaMP calcium imaging per Toyota et
al. 2018; the BRIC-19 / TOAST spaceflight transcriptome across 4 ecotypes; the
"highlight"/ROS stress response via HSP101/HSP70/WRKY33 per Choi et al. 2019 and
Willems et al. 2016; GeneLab/OSDR deposition). Captioned the slides I could
confidently identify. **Care taken** to frame the orbital spaceflight work as the
lab's *published background*, not the high-school team's own result — the team's
contributions are the suborbital payloads + ground assays.

### ASGSR submission
Looked up the **actual** ASGSR rules (web): abstract is **text-only**, title
≤100 words, body ≤300 words (incl. acknowledgments), unlimited authors, mark the
presenting author, submitted via the X-CD portal. The general 2026 deadline
(June 14) has passed, but the **High School / Middle School call opens Aug 2026**
— the right target for this team. Built `asgsr_submission/`:
- `abstract.txt` — verified programmatically: **title 21 words, body 247 words**.
- `manuscript.md` — full IMRaD, honest limitations, refs (Toyota/Choi/Willems +
  OSDR), placeholders for authors/affiliations.
- `figures/` (copied charts + gravitropism slides), `figure_legends.md`,
  `authors_and_affiliations.md`, `cover_letter.md`, `README.md` (requirements
  table + step-by-step submission + checklist).

Honesty throughout: every result restated as a trend (qPCR n=4, TREES n=2–5),
sounding-rocket ≠ sustained-microgravity caveat stated, TREES species left as
`TODO`, the 22/23 grouping caveat carried into the manuscript.

### 12a · Concrete "highlight"-marker follow-up (manuscript §4.2)
Expanded the manuscript's future-work into a specified, falsifiable experiment:
assay the orbital highlight markers **HSP101, HSP70, WRKY33** (the ROS/heat-shock
module validated in Choi et al. 2019 via H₂O₂ and hypoxia) on suborbital-flown
material, with H₂O₂ + hypoxia positive controls and a two-reference-gene
normalization. Made it **data-driven**: computed the pooled within-group ΔCt SD
from our own qPCR (**1.52 cycles**) → power-based targets of ~36 / 14 / 9 reps per
group to detect 2- / 3- / 4-fold changes, which explains why the n=4 pilot only
gave trends and sets a concrete ≥10–15/group goal.

---

## 13 · MAJOR CORRECTION — TREES is a launch codename (Populus × ECM), not "tree seedlings"

A user correction overturned a core assumption. Recording it prominently because
earlier sections (§2, §9–§11) were written under the wrong understanding.

### What was wrong
- **"TREES" is the codename of the program's *third launch*, not a species.** The
  host organism is **_Populus tremula_** (European aspen).
- The **"microbe" (±M) factor is ectomycorrhizal (ECM) fungal inoculation.** The
  hypothesis was that the tree–fungus **symbiosis would help the tree survive
  flight.**
- The program is **three launches**, not two arms of one:
  1. *Arabidopsis* test — earlier flowering; co-flown **ECM spores stayed viable**.
  2. *Arabidopsis* repeat — the **qPCR** samples (Reggies' Veggies, launches Feb
     17 & 24 2018 per the timeline doc).
  3. **TREES** — *Populus tremula* × ECM survival experiment (imaged May–Jun 2018).
- My earlier headline — "+Microbe·Flight gained the most canopy (+57%)" — was
  **misleading**. Trajectory analysis (end ÷ peak) shows the **mycorrhizal plants
  peaked then died back**: +ECM end/peak ≈ 0.71 (flight) / 0.73 (ground), vs.
  −ECM ≈ 0.96 / 0.94. Several +ECM plants collapsed (mr1-2 → 22% of peak, m2-2 →
  38%). The start→end metric hid this behind a few fast early growers. **The
  symbiosis did NOT aid survival** — the opposite of the hypothesis.

### Did the folder have the species? (user asked)
Searched every docx/xlsx (and the slide PDFs) in `data/raw` + the Downloads
source. **No** mention of Populus, mycorrhiza, ECM, spore, or a fungal species —
the surviving files document only the *Arabidopsis* qPCR launches. So: host =
*Populus tremula* (from the user); **ECM fungal species = unknown / not recorded**
(flagged as TODO everywhere). The Reggies report did confirm the K1620 flight
(apogee 4046 ft, dual-deploy) and gene loci (TCH3 AT2G41100, MPK3 AT3G45640,
CBP60G AT5G26920).

### What changed
- **`analyze.py`**: labels → `±ECM`; replaced the start-vs-end bar chart with a
  **start → peak → end** chart (title: "mycorrhizal groups fall back from their
  peak"); `treatment_summary.csv` now carries `peak_canopy_kpx`, `end_over_peak`
  (die-back), and `mean_imaging_days`.
- **`osdr_export.py`**: organism → *Populus tremula*; `Characteristics[Symbiont]`
  = ECM (species not recorded); factor → `Ectomycorrhizal inoculation`; added
  peak + end/peak to the phenotype assay; study metadata rewritten for 3 launches.
- **`results.html`**: added a "three launches" strip; rewrote the TREES section
  (Populus × ECM survival hypothesis) and the headline finding (die-back, not
  growth); relabelled ±ECM throughout.
- **Manuscript + abstract**: retitled and rewritten around the 3 launches; TREES
  result is now an honest **negative result** (symbiosis didn't rescue; die-back),
  with the uneven-imaging-window confound stated. Abstract re-verified: title 29 /
  body 251 words. Figure 1 legend → die-back.
- **Docs/metadata**: `README.md`, `data/README.md`, `data/raw/reggies_veggies/
  README.md`, `CITATION.cff`, `.zenodo.json` all corrected; added keywords
  *Populus tremula*, ectomycorrhiza, plant-fungal symbiosis.

### Key caveat introduced
The die-back comparison is **confounded by imaging duration** (+ECM tracked ~9 d,
−ECM ~6 d) — so the −ECM plants may simply not have been watched long enough. The
die-back is a strong, visible trend, not a controlled proof. Future work: repeat
with **matched imaging windows** and the ECM species identified.
