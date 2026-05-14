# Data Dictionary

## Overview
All data files are CSV format with UTF-8 encoding. Each file contains a header row.
All data are derived from publicly available sources documented in `sources.csv`.

---

## device_characteristics.csv

Characteristics of commercially available RR monitoring devices included in the review.

| Column | Type | Description |
|--------|------|-------------|
| device_id | String | Unique device identifier (DEV01–DEV09) |
| device_name | String | Commercial product name |
| manufacturer | String | Manufacturer name |
| country_of_origin | String | Country of manufacturer headquarters |
| measurement_principle | String | Technical measurement method |
| category | String | Technology category for grouping |
| fda_cleared | String | FDA 510(k) clearance status (Yes/No) |
| ce_marked | String | CE marking status (Yes/No) |
| regulatory_class | String | Regulatory risk classification |
| contact_type | String | Contact (requires patient attachment) or Non-contact |
| consumables_required | String | Description of required disposable components |
| emr_integration | String | EMR/HIS integration capability description |
| abnormal_pattern_detection | String | Ability to detect respiratory pattern abnormalities |
| primary_use_countries | String | Countries with documented clinical deployment |
| year_market_entry | Integer | Year of first commercial availability |
| current_status | String | Active, Discontinued, or other status |
| price_estimate_local | Numeric | Price estimate in local currency |
| price_currency | String | Currency of price estimate |
| price_source | String | Source of price information |
| price_note | String | Caveats and context for price estimate |

---

## accuracy_studies.csv

Published accuracy data for each device.

| Column | Type | Description |
|--------|------|-------------|
| study_id | String | Unique study identifier (ACC01–ACC09) |
| device_id | String | Reference to device_characteristics.csv |
| first_author | String | First author surname or source organization |
| year | Integer | Publication year |
| journal | String | Journal or source name |
| doi | String | Digital Object Identifier (if available) |
| pmid | String | PubMed ID (if available) |
| study_design | String | Study design description |
| setting | String | Clinical setting |
| n_patients | Integer/NA | Number of patients |
| n_measurements | Integer/NA | Number of paired measurements |
| reference_standard | String | Reference standard used for comparison |
| bias_bpm | Numeric/NA | Bland-Altman mean bias (breaths/min) |
| loa_lower_bpm | Numeric/NA | Lower 95% limit of agreement (breaths/min) |
| loa_upper_bpm | Numeric/NA | Upper 95% limit of agreement (breaths/min) |
| rmse_bpm | Numeric/NA | Root mean square error (breaths/min) |
| sensitivity | Numeric/NA | Sensitivity for abnormal RR detection |
| specificity | Numeric/NA | Specificity for abnormal RR detection |
| threshold_within_pct | Numeric/NA | Percentage of measurements within defined threshold |
| threshold_definition | String/NA | Definition of accuracy threshold used |
| population | String | Study population description |
| notes | String | Additional context or caveats |

---

## cost_parameters.csv

All cost and model parameters used in the economic analysis.

| Column | Type | Description |
|--------|------|-------------|
| parameter_id | String | Unique parameter identifier |
| parameter_name | String | Human-readable parameter name |
| value | Numeric | Parameter value |
| unit | String | Unit of measurement |
| country | String | Country applicable (or "Global" for model assumptions) |
| year | Integer | Year of data |
| source_type | String | Type of source (Government statistics, Peer-reviewed, Assumption, etc.) |
| source_reference | String | Full source citation |
| doi_or_url | String | DOI or URL for source verification |
| notes | String | Additional context, caveats, sensitivity ranges |

**Important:** Parameters labeled as "Assumption (model parameter)" are explicitly identified as author assumptions. These are subject to sensitivity analysis and should be replaced with institution-specific values when adapting the model.

---

## sources.csv

Complete reference list with verification information.

| Column | Type | Description |
|--------|------|-------------|
| ref_id | String | Unique reference identifier (REF01–REF20) |
| authors | String | Author list |
| year | Integer | Publication year |
| title | String | Title |
| journal | String | Journal or source name |
| volume | String/NA | Volume number |
| pages | String/NA | Page range |
| doi | String/NA | Digital Object Identifier |
| pmid | String/NA | PubMed ID |
| url | String/NA | Direct URL |
| source_type | String | Type (Peer-reviewed, Guideline, Government statistics, etc.) |
| used_for | String | What this source is cited for in the manuscript |

---

## Notes on Data Quality

1. **Price estimates** are from publicly available sources (retail websites, regulatory documents, NICE briefings). Institutional procurement prices may differ significantly.

2. **Accuracy data** come from studies with heterogeneous designs, reference standards, and populations. Direct comparison across devices should be interpreted cautiously.

3. **Cost parameters** from different countries are not directly comparable due to differences in healthcare financing, cost accounting methods, and what is included in "cost" (charges vs. costs vs. reimbursement).

4. **Exchange rates** are approximate and for cross-country reference only. They are explicitly labeled as assumptions in cost_parameters.csv.

5. **EarlySense** data should be interpreted in the context that the company ceased independent operations in 2022. The technology is now owned by Baxter International.
