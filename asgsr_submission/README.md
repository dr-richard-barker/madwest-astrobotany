# ASGSR submission package

Everything needed to submit this work to the **American Society for Gravitational
and Space Research (ASGSR)** annual meeting, tailored to its requirements.

## Contents
| File | Purpose |
|------|---------|
| `abstract.txt` | The **abstract** — ASGSR format (title + authors + ≤300-word, text-only body) |
| `manuscript.md` | Full IMRaD manuscript for a poster / proceedings / extended writeup |
| `figures/` | Manuscript figures (TREES growth, qPCR fold-change, gravitropism) |
| `figure_legends.md` | Legends for the figures |
| `authors_and_affiliations.md` | Author list template (designate the presenting author) |
| `cover_letter.md` | Optional cover-letter template |

## ASGSR requirements (verified June 2026) — and how this package meets them
| Requirement | Limit | This package |
|-------------|-------|--------------|
| Title | ≤ 100 words | 21 words ✅ |
| Abstract body | ≤ 300 words (incl. acknowledgments/footnotes) | 247 words ✅ |
| Content | **Text only** — no tables, graphs, or images in the abstract | `abstract.txt` is text-only ✅ (figures live with the manuscript) |
| Authors | Unlimited; **must** mark presenting author | Presenting author indicated ✅ |
| Proceedings | All accepted abstracts are published — no proprietary info | None included ✅ |

## How to submit
1. **Category & timing.** The general deadline (June 14, 2026) has passed. The
   **High School / Middle School call opens August 2026** — that is the right
   track for this team. Watch <https://asgsr.org/> for the dated call.
2. **Portal.** Submissions go through the X-CD system:
   <https://www.xcdsystem.com/asgsr/member/>. Create a profile, choose the
   relevant "ASGSR Abstract Submission," and paste the title, authors, and body
   from `abstract.txt`.
3. **Fill placeholders.** Replace every `[bracketed]` field in `abstract.txt` and
   `authors_and_affiliations.md` (names, school, city/state, presenting author).
4. **Register** to present by the meeting's registration deadline
   (Sept 30 in the 2026 cycle).
5. **Poster/manuscript.** Use `manuscript.md` + `figures/` for the poster or any
   proceedings/extended version. Verify the reference details against the primary
   sources first.

## Before you submit — checklist
- [ ] Confirm the **current** High School call wording, deadline, and word limits
      on asgsr.org (limits can change year to year).
- [ ] Replace all `[bracketed]` author/affiliation placeholders.
- [ ] Mark the presenting author (a student, for the HS category).
- [ ] Re-count the abstract body if you edit it (must stay ≤ 300 words).
- [ ] Verify citations (Toyota 2018; Choi 2019; Willems 2016) against the originals.
- [ ] Confirm all named contributors consent to authorship.

---
Regenerate the figures from source any time with the repository's analysis
scripts (`analysis/analyze.py`, `analysis/qpcr_analysis.py`). Independent
educational project; not affiliated with or endorsed by NASA.
