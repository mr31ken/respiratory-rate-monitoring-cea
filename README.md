# Automated Respiratory Rate Monitoring in General Hospital Wards: A Deterministic Break-Even Threshold Analysis

[![Concept DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20176682.svg)](https://doi.org/10.5281/zenodo.20176682)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A reproducible, deterministic break-even threshold model comparing manual respiratory rate (RR) counting with five automated monitoring scenarios. For each scenario it calculates the number of unplanned ICU transfers that must be averted for the monitoring cost to be offset, and the fraction of baseline transfers this represents (the required avoidable fraction). Event values from Japan and the UK are used for the primary analyses; Australian and US values, which relate to a different endpoint or cost construct, are reported separately.

This repository contains all data, analysis code, and documentation accompanying the manuscript submitted to the *Journal of Clinical Monitoring and Computing*.

---

## Repository Structure

```
.
├── analysis/           # Python analysis scripts; model_core.py holds the single cost function
├── data/               # Input CSV files with source attribution
├── tables/             # Generated CSV tables (regenerable from analysis/)
├── figures/            # Generated PNG/PDF figures (regenerable from analysis/)
├── supplementary/      # Supplementary materials (S1–S8; markdown source)
├── requirements.txt    # Python dependencies
├── CITATION.cff        # Citation metadata
├── LICENSE             # MIT License
└── README.md
```

---

## Quick Start: Reproduce All Results

Requirements: Python ≥ 3.9.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Regenerate all figures and tables from source data
cd analysis
python 05_generate_all.py
```

This regenerates every figure (`figures/fig1_*.png` through `fig6_*.png`) and every table (`tables/table1_*.csv` through `table8_*.csv`) deterministically from `data/`. All cost and break-even calculations use the single function in `analysis/model_core.py`.

---

## Adapt the Model to Your Institution

General cost and clinical parameters are stored as plain CSV in `data/cost_parameters.csv`; device-specific costs (prices, consumables and device-related staff time) are defined in the `DEVICES` dictionary in `analysis/model_core.py`. To run the model with local data:

1. Edit values in `data/cost_parameters.csv` (each row contains a value, source citation, and "Published" / "Assumption" classification) and, for device costs, `DEVICES` in `analysis/model_core.py`.
2. Re-run `python analysis/05_generate_all.py`.
3. Inspect `tables/table4_breakeven_analysis.csv` (break-even thresholds and required avoidable fractions) and the regenerated figures. To use your own baseline unplanned ICU transfer rate, edit `RATE01`; the required avoidable fraction is the break-even threshold divided by that rate.

The data dictionary (`data/DATA_DICTIONARY.md`) defines every variable.

---

## Data Provenance

- Input CSVs in `data/` cite primary sources (NICE MIBs, FDA 510(k) summaries, peer-reviewed clinical validation studies, MHLW/NHS/AIHW/CMS government statistics, manufacturer disclosures).
- Parameters are explicitly classified as **Published** (cited source) or **Assumption** (model parameter requiring sensitivity testing); see Supplementary S1.
- Values were checked against primary sources by the corresponding author (full citation list provided in the manuscript reference list).

---

## Reporting Standard

Reporting follows the **Consolidated Health Economic Evaluation Reporting Standards 2022 (CHEERS 2022)**. The completed 28-item checklist is in Supplementary S8.

---

## Citation

If you use this repository or adapt the model, please cite:

> Saito K, Kishimoto K, Ishizuka N, Kusuda K, Kuroda T. *Automated Respiratory Rate Monitoring in General Hospital Wards: A Deterministic Break-Even Threshold Analysis.* Submitted to the *Journal of Clinical Monitoring and Computing*; manuscript under peer review (revised version). Repository archive: Zenodo, concept DOI [10.5281/zenodo.20176682](https://doi.org/10.5281/zenodo.20176682) (stable identifier resolving to the latest archived release). The journal DOI of the published article will be added upon acceptance.

Machine-readable citation metadata is in `CITATION.cff`.

---

## License

The code in `analysis/` and the documentation in this repository are released under the **MIT License** (see `LICENSE`).

CSV data files in `data/` aggregate publicly available statistics and published values; original sources retain their respective licenses and are cited within each row.

---

## Conflict of Interest

The author(s) declare no conflicts of interest. No device manufacturer was involved in study design, data collection, analysis, interpretation, or manuscript preparation.

---

## AI-Assisted Development

A large language model (Anthropic Claude) was used to assist with text drafting and Python code development. During revision, Claude and a second LLM (OpenAI Codex) were also used to cross-check the revised text against primary sources, and discrepancies they identified were verified against the primary sources by the authors before any change was made. No images or figures were generated by AI. The authors assume full responsibility for the content.

---

## Contact

For questions about the model or to request data corrections, please open an issue on GitHub.
