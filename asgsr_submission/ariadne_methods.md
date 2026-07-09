# Project Ariadne — Methods Appendix
## *Physarum polycephalum* Maze Experiment (2019)

*Working draft for team review before paper submission. Authors: Sophia Zappia, Lizzy Larson,
Brady Nilsson, Hyun-seok Chang, and the MadWest 2019 team.*

---

## A.1 Organism and flight payload

*Physarum polycephalum* cultures were maintained on nutrient medium (see A.3) in petri dishes.
For the flight payload, cultures in sealed dishes were integrated into the sounding-rocket payload
bay alongside standard recovery hardware. The rocket flew on a **Cesaroni K1620** motor; the
payload experienced the full launch profile (high-G boost, ballistic coast, and recovery loads).
On recovery, cultures were returned to the lab and split into three experimental groups (A.2).

## A.2 Post-flight experimental groups

| Group | Treatment | Post-flight handling |
|-------|-----------|----------------------|
| **Baseline** | Ground control — never flew | Maintained in lab throughout |
| **Stress** | Flew in the payload | Cultured separately post-recovery |
| **Hybrid** | Mixed post-flight | Equal portions of Baseline + Stress combined after recovery |

**Hypothesis:** the Stress group will sporulate (preservation response to mechanical/hypergravity
stress); the Hybrid group will first reinforce the plasmodium network before sporulating.

## A.3 Nutrient medium preparation

*Protocol authored by Sophia Zappia and Hyun-seok Chang, June 7, 2019.*

**Recipe (nutrient phytagel):**
- 3 g/L sucrose
- 5 g/L phytagel
- Deionised (DI) water to volume

1. Combine sucrose and phytagel in DI water in an autoclave-safe flask.
2. Autoclave 30 minutes on liquid cycle.
3. Allow to cool until pourable (≈ 55 °C) before dispensing.
4. Pour volumes:
   - Round dishes: ~25 ml
   - Square dishes: ~45 ml
   - Maze plates: ~35 ml (see A.5)
5. Allow to set in BSC; store sealed.

## A.4 Nutrientless medium preparation

*Protocol authored by Sophia Zappia and Hyun-seok Chang, June 4, 2019.*

**Recipe (nutrientless phytagel):**
- 10 g/L phytagel (no sucrose)
- DI water to volume

Oat grains are the sole food source; no nutrients are dissolved in the medium.

1. Combine phytagel in DI water.
2. Autoclave 30 minutes.
3. Pour:
   - Round dishes: ~25 ml
   - Square dishes: ~35 ml
4. Set in BSC.

**Note:** Agar (10 g/L in DI water) can be substituted for phytagel when the melt-and-reuse
property is needed. Phytagel is preferred for maze and bottom-imaging applications because it
sets transparent.

## A.5 Maze pouring protocol

*Protocol authored by Brady Nilsson, Sophia Zappia, and Hyun-seok Chang, June 12, 2019.*

Six 3D-printed maze versions (five maze types; STL files in project archive) were used. All maze
work was performed in a **biological safety cabinet (BSC)** using **aseptic technique**.

1. Place 3D-printed maze insert into a square petri dish inside the BSC.
2. Pour nutrient medium (A.3) or nutrientless medium (A.4) — approximately **35 ml** per maze —
   so that the maze channels are filled to the top of the walls.
3. Allow to air-dry in the BSC for **30–60 minutes** until the surface is no longer glossy.
4. Optional: store lidded in the refrigerator overnight before use.
5. Before seeding: place food oats at designated positions (1 oat at start; 2–3 oats at exit/end
   positions, depending on maze type).

## A.6 *Physarum* propagation (petri dish to petri dish)

*Protocol authored by Lizzy Larson, Hyun-seok Chang, and Sophia Zappia, June 6, 2019.*

1. Arrange **4–5 oat grains in a circle** plus **1 oat in the centre** on fresh medium in the
   destination dish.
2. Cut a **1 cm² piece** of plasmodium from an active source culture (select tissue with
   ≥ 75% visible vein network coverage — avoid thin or sparse areas).
3. Place the inoculum on the **centre oat**.
4. Seal with Parafilm; store in a **dark cabinet** at room temperature.

## A.7 Maze propagation protocol

*Protocol authored by Brady Nilsson, Hyun-seok Chang, and Sophia Zappia, June 12, 2019.*

1. Confirm the maze plate is prepared per A.5 (medium set, oats in place).
2. Cut a **1 cm² plasmodium piece** (≥ 75% vein coverage) from the source culture.
3. Place the inoculum on the **start oat** (single oat at the maze entrance).
4. Exit oats (2–3 oats) should already be in place at the maze exit per A.5.
5. Seal the dish with Parafilm to prevent desiccation.
6. Store in a **dark cabinet** between imaging sessions.

## A.8 Scanner timelapse imaging

*Protocol authored by Hyun-seok Chang and Sophia Zappia, June 12, 2019.*

Flatbed scanner imaging of maze plates (bottom-view timelapse):

1. Place plate **upside-down** on scanner bed (imaging through the bottom of the dish).
   **Note:** Phytagel is required for bottom-imaging because it sets clear; agar is opaque.
2. Scan at **30–60 minute intervals**.
3. Save images to `Pictures/Ariadne/[date]/` folder, named by date-time stamp.
4. Return plate to dark storage between scans.
5. A **parallel flashlapse system** (overhead LED array, camera on timer) captured the petri
   dish cultures at higher temporal resolution for the propagation experiments.

## A.9 Five maze types — design notes

| Maze | Description |
|------|-------------|
| **1** | Basic point-to-point spiral — tests food-finding and maze completion |
| **2** | Two-path routing — tests selection of more efficient route to food |
| **3** | No-solution maze — no path to food; tests response to unsolvable problem |
| **4** | Long-simple vs. short-complex route — tests route-length preference under stress |
| **5** | Multi-food-source network — tests spanning-network efficiency |

All maze STL files and 3D-printer settings are preserved in the project archive.

## A.10 Glossary (from Project A–Z lab glossary, 2019)

| Term | Definition |
|------|-----------|
| **Plasmodium** | The active, motile, multinucleate phase of *Physarum polycephalum*; single cell but macroscopic |
| **Sporulate / Sporulation** | *Physarum*'s survival mode: converting from plasmodium into dry spore bodies when stressed or starved |
| **Phytagel** | Gelling agent that sets clear; preferred over agar for bottom-scanner imaging |
| **Agar** | Alternative gelling agent; opaque when set; can be remelted and reused |
| **BSC** | Biological Safety Cabinet — enclosed bench with HEPA-filtered airflow for aseptic work |
| **Aseptic technique** | Working practices that prevent contamination (wiping surfaces, using sterile tools, working in BSC) |
| **Maze** | 3D-printed labyrinth placed in a petri dish and filled with growth medium |

---

*This methods appendix will be merged into the main manuscript methods section (§2) before
journal submission. All protocols are verbatim from the original 2019 student lab documents.*
