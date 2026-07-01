# OSDR submission package (aligned, not yet validated)

This folder reshapes the processed results into the **ISA model** that NASA OSDR
/ GeneLab uses (Investigation - Study - Assay). Files are CSV for readability;
strict OSDR ISA-Tab is tab-delimited `.txt` — a curator can convert these.

## Files
| File | ISA role | Contents |
|------|----------|----------|
| `s_study_madwest.csv` | Study | Study-level metadata, factors, protocols |
| `a_trees_growth_phenotype.csv` | Assay | TREES growth phenotype, one row per plant (13) |
| `a_reggies_qpcr_transcription.csv` | Assay | qPCR transcription, one row per sample x gene (36) |
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
