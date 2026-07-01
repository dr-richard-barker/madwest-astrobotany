# MadWest Rocketry × NASA OSDR

A multi-page static website: a one-stop hub for building **botanical sounding rockets**
(rockets carrying living plant payloads) and contributing the resulting space-biology data
to NASA's [Open Science Data Repository (OSDR)](https://osdr.nasa.gov/).

> 📓 **New here?** Read [DEVLOG.md](DEVLOG.md) first — it records every decision,
> tangent, and dead-end (why segmentation works the way it does, the path bug,
> the codec fix, known limitations), so you don't have to reverse-engineer them.

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Home — the MadWest ↔ OSDR vision and the build → fly → measure → submit loop |
| `results.html` | **Real data** — TREES timelapse videos + image-analysis growth curves + qPCR fold-change |
| `story.html` | **Slideshows** — gravitropism-under-coloured-light assay + the Reggies' Veggies / AstroBotany research story |
| `build-guide.html` | **Centerpiece** — step-by-step build of a botanical sounding rocket |
| `osdr-training.html` | Plain-language training on NASA OSDR open-science / FAIR standards |
| `data-submission.html` | Experiment-to-repository workflow: file structure, metadata, submission |
| `about.html` | The vision, principles, and how to get involved |

## Structure

```
MadWest_Rocket_class/
├── index.html  results.html  story.html  build-guide.html   # the website (served
├── osdr-training.html  data-submission.html  about.html      #  at root -> Pages ready)
├── css/styles.css      # shared theme (deep-space + botanical green)
├── js/main.js          # mobile nav toggle + active-link highlighting
├── js/slideshow.js     # lightweight image-carousel for the Story page
│
├── slides/             # source presentation PDFs (committed; linked for download)
│
├── analysis/           # analysis pipeline (Python)
│   ├── segment_lib.py      # green-canopy segmentation (Excess-Green + glare removal)
│   ├── analyze.py          # per-frame canopy area -> processed CSVs + charts
│   ├── make_timelapse.py   # per-treatment + 2x2 comparison MP4s (H.264)
│   ├── qpcr_analysis.py    # qPCR ΔΔCt fold-change of stress genes -> CSV + chart
│   └── osdr_export.py      # reshape results into an OSDR/ISA submission package
│
├── data/               # research data package (see data/README.md)
│   ├── raw/                       # original sources — GIT-IGNORED (~1 GB)
│   │   ├── trees_timelapse/       # 850 MB growth-arm imagery
│   │   └── reggies_veggies/       # 180 MB molecular arm (flight, qPCR, photos…)
│   └── processed/                 # analysis outputs (committed)
│       ├── trees_growth/          # growth_data.csv + treatment_summary.csv
│       └── reggies_qpcr/          # qpcr_ct_long.csv + qpcr_fold_change.csv
│
├── osdr_submission/    # OSDR/ISA-aligned tables (s_study, a_*, derived) + README
├── asgsr_submission/   # ASGSR abstract + manuscript + figures + checklist
│
├── assets/             # web-facing results (committed)
│   ├── timelapse/      # generated MP4 videos
│   ├── charts/         # growth charts + before/after grid + qPCR fold-change
│   ├── reggies/        # molecular-arm web images (launch, plates, thrust, qPCR)
│   ├── slides/         # rendered slideshow images (gravitropism, reggies_story)
│   └── thumbs/         # video poster(s)
│
├── LICENSE  LICENSE-data           # MIT (code) + CC-BY-4.0 (data)
├── CITATION.cff  .zenodo.json      # citation + Zenodo deposit metadata
├── PUBLISHING.md                   # GitHub + Zenodo release checklist
├── DEVLOG.md                       # decisions, tangents, dead-ends
└── README.md
```

## TREES results pipeline

"TREES" is the **codename of the program's third launch** — *Populus tremula*
(aspen) seedlings ± ectomycorrhizal (ECM) inoculation, flown vs. ground (a 2×2
*ECM × flight* design). The pipeline segments the green canopy in every frame,
tracks its area over time (start → peak → end), and renders comparison videos +
charts. The headline result: the mycorrhizal seedlings **peaked then died back**
— the fungal symbiosis did *not* aid flight survival. Requires `opencv-python`,
`numpy`, `matplotlib`, and `imageio` + `imageio-ffmpeg` (for H.264 export):

```bash
pip install opencv-python numpy matplotlib imageio imageio-ffmpeg openpyxl
cd analysis
python analyze.py          # full re-segmentation -> CSV + charts (~1 min)
python analyze.py charts   # rebuild charts only from the CSV (fast)
python make_timelapse.py   # (re)build the timelapse videos
python qpcr_analysis.py    # qPCR ΔΔCt fold-change -> CSV + chart
python osdr_export.py      # build the OSDR/ISA submission package
```

> **On the data:** classroom-scale (TREES 2–5 plants/group, uneven timelapse
> lengths; qPCR n=4/group) — the Results page presents these as **trends, not
> proof**, and says so. See `DEVLOG.md` for methods, caveats, and the qPCR
> sample-grouping note.

## Run it

It's plain static HTML — just open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8000   # then visit http://localhost:8000
```

## Notes for editing

- Spots that need your real details are tagged inline with an orange **`edit`/`coming soon`**
  badge (search the HTML for `class="todo"`). These include: your organization/safety rules,
  contact links, a model OSDR study to link, and confirming OSDR's current submission process.
- This is an independent **educational** project — **not affiliated with or endorsed by NASA**.
  Always follow the official OSDR portal for current submission requirements and your
  national/local rocketry regulations (e.g. NAR/Tripoli, FAA) for flight.

## Possible next steps

- Downloadable CSV / metadata templates matching the Data Submission structure
- Real photos/diagrams in `assets/`
- A gallery of completed flights and their published OSDR datasets
