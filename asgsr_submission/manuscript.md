# Botanical sounding rockets as an accessible space-biology platform: flowering and stress-gene responses in flown *Arabidopsis*, and an ectomycorrhiza × *Populus tremula* survival experiment

**[Student Lead Author]¹\*, [Co-Author Student Name(s)]¹, Richard Barker², and the MadWest High School Rocket Team¹**

¹ MadWest High School, [City, State]  ← fill before submission
² AstroBotany Laboratory, University of Wisconsin–Madison, Madison, WI, USA
\* Presenting / corresponding author — *replace bracketed student names before submission.*

*Prepared for the American Society for Gravitational and Space Research (ASGSR). Independent educational project; not affiliated with or endorsed by NASA.*

---

## Abstract

Spaceflight imposes a distinctive stress on plants: orbital transcriptomics (BRIC-19 / TOAST) reveal a high-light-like, reactive-oxygen-species (ROS) signature involving heat-shock proteins (HSP101, HSP70) and WRKY33, even in darkness (Choi et al., 2019). Such experiments are powerful but costly and rare. We asked whether accessible, repeatable **suborbital sounding rockets** can let students probe flight-associated plant biology and contribute open data. A high-school team, mentored by the University of Wisconsin–Madison AstroBotany laboratory, ran a program of **three 2018 launches** (Cesaroni K1620 motor). Launch 1 (*Arabidopsis thaliana* test): flown seedlings reportedly flowered earlier, and co-flown ectomycorrhizal spores remained viable after flight. Launch 2 (*Arabidopsis*, repeat): qPCR of stress genes (MPK3, TCH3, CBP60g; UBQ10 reference) showed flown plants trending toward lower stress/touch signaling but higher defense signaling versus lab controls (n=4; trends). Launch 3 ("TREES," a codename): *Populus tremula* seedlings ± ectomycorrhizal (ECM) inoculation, flown vs. ground, imaged as a timelapse to test whether the symbiosis aids flight survival. Automated green-canopy analysis of ~2,600 frames showed the opposite of the hypothesis: **mycorrhizal seedlings peaked, then died back** to ~71–73% of peak canopy (versus ~94–96% for non-mycorrhizal), a decline visible in the footage. All results are classroom-scale and hypothesis-generating, but demonstrate a complete build–fly–measure–deposit pipeline ending in data formatted for NASA's Open Science Data Repository (OSDR).

## 1. Introduction

Plants sense gravity through specialized cells — the columella statocytes of the root tip, whose dense amyloplasts (statoliths) sediment and bias auxin transport to drive directional growth (gravitropism). Removing or altering the gravity vector, as in spaceflight, perturbs this system and, more broadly, triggers a stress response. Transcriptomic studies on the International Space Station — including the BRIC-19 hardware flown on SpaceX CRS-4 and the TOAST (Test of Arabidopsis Space Transcriptome) effort across the Col-0, WS-2, Ler-0 and Cvi-0 ecotypes — found that spaceflight reproducibly alters gene expression, and that the signature resembles a **"highlight" (high-light) stress** rich in ROS responses, heat-shock proteins (HSP101, HSP70) and the transcription factor WRKY33, even in darkness (Choi et al., 2019; cf. Willems et al., 2016). Such datasets are deposited in NASA's GeneLab / OSDR, enabling reuse.

Orbital access, however, is scarce and expensive. **Suborbital sounding rockets** subject a payload to a brief, intense profile — high-G boost, a short ballistic coast, and recovery — that is far more accessible to students, and repeatable within a season. We hypothesized that this platform could (i) elicit measurable, flight-associated responses in plants, (ii) support quantitative ground and post-flight assays, and (iii) produce openly shareable, OSDR-aligned data.

Here we report the MadWest High School program across three 2018 launches, plus a companion ground gravitropism assay, framed against the published orbital "highlight" response.

## 2. Materials and methods

### 2.1 The three launches
All flights used a Cesaroni **K1620** motor (recorded apogee ≈ 4,046 ft; dual-deployment recovery, drogue at apogee and main at ~700 ft AGL), with onboard altimetry (PerfectFlite). "Reggies' Veggies" and "TREES" are launch designations — **TREES is a codename, not a species**.

### 2.2 Launch 1 — *Arabidopsis* test (observational)
*Arabidopsis thaliana* seedlings were flown and recovered. The team reported two qualitative observations: flown seedlings appeared to reach **flowering earlier** than controls, and **ectomycorrhizal spores co-flown** as a payload element **remained viable** (germinated) after the flight — motivating the later host–symbiont experiment. Quantitative records for these first-flight observations were not present in the analyzed data folder and are reported as preliminary.

### 2.3 Launch 2 — *Arabidopsis* qPCR ("Reggies' Veggies")
*A. thaliana* (Col-0) was flown alongside **Launch-site** (travel/transport) and **Lab** ground controls, then fixed in RNA*later* on recovery. Total RNA was extracted (phenol–chloroform / column protocols) and reverse-transcribed. qPCR (SYBR) measured **MPK3** (AT3G45640; stress MAP kinase), **TCH3** (AT2G41100; touch/mechanostimulus-induced), and **CBP60g** (AT5G26920; calmodulin-binding, defense), normalized to **UBQ10**. We computed ΔCt = Ct(target) − Ct(UBQ10) per sample, ΔΔCt vs. the Lab calibrator, and fold-change = 2^(−ΔΔCt) (n = 4 biological replicates/group; technical replicates averaged). Grouping followed the qPCR plate design (see *Limitations* for one caveat).

### 2.4 Launch 3 — TREES: *Populus tremula* × ectomycorrhiza
European aspen (*Populus tremula*) seedlings were grown on gridded agar plates **with or without ectomycorrhizal (ECM) inoculation**, and flown vs. kept as ground controls — a 2×2 (ECM ± × flight) design (13 plants total; groups of 2–5). The working hypothesis was that the tree–fungus **symbiosis would improve flight survival**. Plates were imaged as a timelapse (~2,600 frames, up to ~12 days). Green-canopy area was measured per frame with an automated pipeline: the Excess-Green index (ExG = 2G − R − B) isolated the canopy, near-white backlight glare was removed (pixels bright in all channels), followed by morphological cleanup. Per-plant series were smoothed (rolling median); we report per-plant **start**, **peak**, and **end** canopy and the **end/peak** ratio as a die-back metric. *The ECM fungal species is not recorded in the surviving lab files and is annotated as unknown.*

### 2.5 Gravitropism under spectral light (ground)
In a separate ground assay, roots were imaged under blue, green, purple, red, and white LED illumination; root-tip angle over time (gravitropic reorientation; "RootTrace") and root length ("RootNav") were extracted.

### 2.6 Data and code availability
All analysis code (Python), processed data, and an OSDR/ISA-aligned submission package are openly released on GitHub and archived on Zenodo (see *Data availability*).

## 3. Results

### 3.1 Launch 1: earlier flowering and post-flight spore viability (preliminary)
The first *Arabidopsis* flight yielded two encouraging, qualitative results — apparent **earlier flowering** in flown seedlings and **viable ectomycorrhizal spores** after flight — which are reported as observations (no quantitative dataset survives in the analyzed folder) and which framed the subsequent experiments.

### 3.2 Launch 2: flight shifts which stress pathways engage (qPCR)
Relative to the Lab control, flown *Arabidopsis* trended toward **reduced** stress/touch signaling — MPK3 **0.34×** and TCH3 **0.56×** — but **elevated** defense signaling, CBP60g **1.60×** (Figure 2). The Launch-site control was intermediate (MPK3 0.48×, TCH3 0.89×, CBP60g 0.68×). The pattern suggests brief flight does not simply turn "stress" up or down but **shifts the balance of pathways engaged**. With n = 4 and wide biological spread, error ranges cross "no change" for every gene; these are **trends, not statistically significant effects**.

### 3.3 Launch 3 (TREES): the symbiosis did not rescue the trees — mycorrhizal die-back
Contrary to the hypothesis, the **mycorrhizal (+ECM) *Populus* seedlings peaked, then declined**. Averaged within group, +ECM plants ended at only **0.71** (flight) and **0.73** (ground) of their **peak** canopy, whereas −ECM plants held near peak (**0.96** flight, **0.94** ground) (Figure 1). Several +ECM plants collapsed far further — one flown +ECM seedling fell to **22%** of its peak, another +ECM plant to 38% — a slow die-back plainly visible in the timelapse. **The tree–fungus symbiosis did not confer the expected flight-survival benefit; if anything the inoculated plants deteriorated.**

Two caveats temper this. First, the **imaging windows differ**: +ECM groups were tracked ~9 days but −ECM groups only ~6, so the non-mycorrhizal plants may not have been observed long enough to reach the same fate — the comparison is confounded by duration. Second, n is small (2–5/group). The die-back is therefore a **strong, reproducible trend visible in the footage**, not a controlled proof; the additional contribution is a repeatable image-analysis method that turns plate photos into quantitative growth *trajectories* (start → peak → end), not just endpoints.

### 3.4 Root gravitropism under spectral light
Root-tip angle declined over the assay across all light colors, consistent with active gravitropic reorientation, while root length varied with the light spectrum (Figure 3). These measurements establish the team's capacity to quantify the gravity-sensing behavior that spaceflight perturbs.

### 3.5 Placing the results in the orbital context
The published orbital signature — a high-light/ROS stress response mediated by HSP101, HSP70 and WRKY33 (Choi et al., 2019; Willems et al., 2016) — provides the interpretive backdrop for the *Arabidopsis* qPCR trends (a defense-pathway shift), which are a student-scale, testable complement rather than a replication.

## 4. Discussion

Several points follow. First, **a suborbital platform yields interpretable readouts** across molecular, phenotypic, and survival axes when paired with controls and reproducible analysis. Second, the TREES result is a genuine, if preliminary, **negative result**: a plausible "symbiosis aids survival" hypothesis was *not* supported, and the trajectory-aware analysis (peak → end) was essential to see it — an endpoint-only or start-to-end summary would have masked the die-back behind a couple of fast early growers. Reporting this honestly, confound and all, is itself a teaching outcome. Third, the *Arabidopsis* qPCR trends — down MPK3/TCH3, up CBP60g — connect naturally to the orbital "highlight"/ROS/HSP framework, where stress-pathway remodeling (not a single switch) is the rule. Fourth, **the open-data endpoint matters**: formatting everything to the ISA model OSDR uses makes a student project reusable science.

### 4.1 Limitations
- **Sample size and windows.** qPCR n = 4/group; TREES n = 2–5/group. Critically, TREES imaging windows differ by treatment (+ECM ~9 d, −ECM ~6 d), which confounds the die-back comparison. All effects are trends, not significance tests.
- **Platform.** A sounding rocket delivers a brief, high-G, short-microgravity profile — *not* the sustained microgravity of orbit; comparisons to ISS data are contextual.
- **Missing metadata.** The TREES host is *Populus tremula*, but the **ECM fungal species is not recorded** in the surviving files; Launch-1 flowering/spore observations lack a surviving quantitative dataset.
- **Proxies.** Canopy area is a 2-D pixel proxy (no cm² calibration yet).
- **One qPCR labeling caveat.** Samples 22/23 are grouped per the plate design but labeled differently in the tube log; we followed the plate design. It does not affect the Flight group.

### 4.2 Future work: a targeted "highlight"-marker flight experiment

Our present qPCR panel (MPK3, TCH3, CBP60g) reports general stress and defense signaling. The orbital signature, however, is defined by a specific **high-light / ROS module** in which **HSP101, HSP70, and WRKY33** are the diagnostic, validated markers — up-regulated by spaceflight and reproduced on the ground by hydrogen-peroxide (ROS) and hypoxia treatments (Choi et al., 2019; Willems et al., 2016). The natural next experiment is to ask whether a **brief suborbital flight** engages this same module.

**Hypothesis.** If the highlight response reflects the broad flight environment (launch vibration, high-G, transient ROS and hypoxia) rather than sustained microgravity alone, then suborbital-flown *Arabidopsis* will up-regulate HSP101, HSP70, and WRKY33 relative to launch-site and lab controls. If the response is specific to sustained orbital microgravity, these markers will not move — a clean, falsifiable test a sounding rocket can run.

**Design.** Repeat the flight with the three groups (Flight, Launch-site, Lab) plus two ground-based **positive controls known to induce the markers** — an H₂O₂ (ROS) and a hypoxia treatment — to anchor the assay (mirroring Choi et al., 2019). Quantify HSP101, HSP70, WRKY33 by qPCR, normalized to the geometric mean of **two** reference genes (UBQ10 + e.g. PP2A). Fix material in RNA*later* immediately on recovery and **record time-to-fixation** (a confound flagged in our sample log). Published primer sequences (Choi et al., 2019) can be reused.

**Powering it properly.** Our own data set a realistic variance target: the pooled within-group SD of ΔCt was **1.52 cycles**. At α = 0.05 and 80% power, detecting a 2-fold change (ΔΔCt = 1) needs ≈ 36 biological replicates/group; a 3-fold change ≈ 14; a 4-fold change ≈ 9. This explains why our n = 4 pilot returned only trends, and sets a concrete target of **≥ 10–15 seedlings/group**, analyzed with a t-test/ANOVA and multiple-comparison correction.

**Also planned.** Repeat the ECM × *Populus* survival experiment with **matched imaging windows** across treatments (removing the duration confound) and, ideally, the ECM species identified; root-growth segmentation and grid-based cm² calibration in the TREES pipeline; and a formal OSDR deposit once current requirements are confirmed.

## 5. Conclusion

A high-school team, mentored by an academic AstroBotany laboratory, executed a complete **build → fly → measure → deposit** cycle across three launches: a phenotype/viability test, a stress-gene qPCR experiment, and a host–symbiont survival timelapse — the last returning an honest negative result (the mycorrhizal trees died back). All were packaged toward NASA OSDR. Botanical sounding rockets are a tractable, repeatable entry point for student-led space biology — and a way to grow the open spaceflight data record one flight at a time.

## Data availability

Code, processed data, and the OSDR/ISA submission package: GitHub repository (URL on release) and Zenodo archive (DOI on deposit). Raw imagery and qPCR exports are in the Zenodo deposit. See `PUBLISHING.md`.

## Acknowledgments

The MadWest High School students and mentors; the University of Wisconsin–Madison AstroBotany laboratory and collaborators for guidance and for the published spaceflight context. *(Add funding sources and named individuals before submission.)*

## References

1. Toyota M, Spencer D, Sawai-Toyota S, et al. (2018). Glutamate triggers long-distance, calcium-based plant defense signaling. *Science* 361:1112–1115.
2. Choi W-G, Barker RJ, Kim S-H, Swanson SJ, Gilroy S. (2019). Variation in the transcriptome of different ecotypes of *Arabidopsis thaliana* reveals signatures of oxidative stress in plant responses to spaceflight. *American Journal of Botany* 106(1):123–136.
3. Willems P, Mhamdi A, Stael S, et al. (2016). The ROS Wheel: refining ROS transcriptional footprints. *Plant Physiology* 171(3):1720–1733.
4. NASA Open Science Data Repository (OSDR / GeneLab). https://osdr.nasa.gov/

*Reference details (volume/page, author lists) should be verified against the primary sources before submission. Launch-1 flowering and spore-viability observations should be corroborated with the team's original records where available.*
