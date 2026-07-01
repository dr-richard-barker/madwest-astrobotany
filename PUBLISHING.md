# Publishing checklist — GitHub + Zenodo

How to take this repo public and mint a citable DOI. Two destinations, different
jobs:

- **GitHub** = code + website + processed data + docs (the ~1 GB raw imagery is
  git-ignored).
- **Zenodo** = the archival deposit with a DOI. Because the raw data is
  git-ignored, the usual GitHub-release→Zenodo hook will **not** capture it —
  so the raw data package is uploaded to Zenodo **directly** (see Track B).

---

## Before you publish — fill the placeholders

- [ ] `CITATION.cff` — replace the `TODO` author block with real names (+ ORCID).
- [ ] `.zenodo.json` — replace the `creators` placeholder (format `Family, Given`).
- [ ] `LICENSE` — confirm the copyright holder line (currently
      "MadWest Rocketry contributors", 2026).
- [ ] Website `class="todo"` spots — org/safety rules, contact links, model OSDR
      study, confirm OSDR's current submission process.
- [ ] Decide: is the molecular (qPCR) arm analyzed yet, or released as raw-only?
      Say so in the Zenodo description either way.

Licensing is already set: **MIT** for code (`LICENSE`), **CC-BY-4.0** for data
(`LICENSE-data`).

---

## Track A — GitHub

1. [ ] `git init && git add . && git commit -m "Initial public release"`
       (`.gitignore` already excludes `data/raw/` and `*.eds/*.edt`.)
2. [ ] Create the GitHub repo and `git push`.
3. [ ] Confirm the repo size is sane (should be tens of MB — mostly the
       committed videos/charts, NOT the raw imagery). If it's ~1 GB, the
       `.gitignore` didn't take — check `git status` before the first commit.
4. [ ] (Optional) Enable **GitHub Pages** from the repo root to serve the site.
       The site lives at the root (`index.html`, etc.), so Pages works with no
       config. Landing page: `index.html`; results: `results.html`.
5. [ ] Add the repo URL to `CITATION.cff` (`repository-code:`) and the
       `related_identifiers` in `.zenodo.json`.

## Track B — Zenodo (the data + DOI)

The raw imagery is the actual research data and belongs on Zenodo (50 GB/record
limit, well above our ~1 GB).

1. [ ] Build the raw-data archive (kept out of git):
       ```bash
       # from the repo root
       zip -r madwest_raw_data.zip data/raw
       # or split if your uploader prefers smaller parts
       ```
2. [ ] At https://zenodo.org → **New upload**:
   - [ ] Upload `madwest_raw_data.zip` **and** a copy of `data/processed/`.
   - [ ] Upload type: **Dataset**. Access: **Open**. License: **CC-BY-4.0**.
   - [ ] Paste title/description/keywords from `.zenodo.json`.
   - [ ] Add the real creators/affiliations/ORCIDs.
   - [ ] Under *Related identifiers*, link the GitHub repo URL ("is supplemented
         by").
3. [ ] **Publish** → Zenodo mints the DOI.
4. [ ] Put the DOI back into `CITATION.cff` (`doi:`) and the README badge, then
       push that update to GitHub.

### Alternative: automated GitHub→Zenodo (code snapshot only)
If you also want Zenodo to archive each GitHub *release* automatically, enable
the repo in your Zenodo "GitHub" settings and cut a release. ⚠️ This captures
only git-tracked files — **the raw imagery will be missing** — so still do Track
B for the data, or reference the data deposit from the release.

---

## Note on NASA OSDR

OSDR is a separate destination from Zenodo, with its own submission process set
by NASA. The growth data here is *formatted toward* OSDR conventions but not yet
submitted — confirm current requirements at https://osdr.nasa.gov/ before
attempting an OSDR deposit. See the website's Data Submission page.
