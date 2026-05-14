# Economic Evaluation of Automated Respiratory Rate Monitoring in General Hospital Wards: A Deterministic Cost-Minimization and Break-Even Modeling Study

## Authors
Kenichi Saito¹,²

¹ Center for Medical DX Education and Research, Graduate School of Medicine, Kyoto University, Kyoto, Japan
² Graduate School of Medicine, Osaka Metropolitan University, Osaka, Japan

**Corresponding author:** Kenichi Saito, Center for Medical DX Education and Research, Graduate School of Medicine, Kyoto University, 53 Kawahara-cho, Shogoin, Sakyo-ku, Kyoto 606-8507, Japan. Tel: +81-75-751-4836. E-mail: mr31ken@kuhp.kyoto-u.ac.jp. ORCID: [0000-0003-2301-706X](https://orcid.org/0000-0003-2301-706X).

## Target Journal
Journal of Clinical Monitoring and Computing (Springer)

Word count: ~4,800 (main text, excluding abstract, references, tables, and figure legends)
Display items: 6 figures, 3 tables (main text) + 4 supplementary tables

---

## Abstract

**Purpose:** To develop a reproducible break-even model determining the conditions under which automated respiratory rate (RR) monitoring achieves cost-neutrality on general hospital wards, across four national healthcare systems.

**Methods:** A deterministic decision-analytic model (hospital perspective, 1-year horizon, CHEERS 2022-compliant) compared manual RR counting with six automated monitoring scenarios. Model parameters—device accuracy, costs, and adverse event costs from Japan, UK, Australia, and USA—were identified through comprehensive searches of PubMed, NICE Evidence, FDA 510(k), and government statistics (2010–2025). Nine devices across five technology categories were identified. Costs were converted to Japanese yen at 2024 mid-year exchange rates. One-way sensitivity, multi-way scenario, and cross-country break-even analyses were performed.

**Results:** Manual RR counting cost ¥350/patient-day (Japan base case). Incremental costs of automated monitoring ranged from ¥106 (radar) to ¥1,900 (capnography) per patient-day. Non-contact sensors required avoidance of only 0.24–1.3 deterioration events per 1,000 patient-days for cost-neutrality, depending on national adverse event cost (¥476,000–¥1,605,000). Even under worst-case assumptions, the break-even threshold (5.93/1,000 patient-days) remained within published ward deterioration rates (2–10/1,000 patient-days). Adverse event cost and device unit cost were the dominant parameters.

**Conclusions:** Break-even thresholds for automated RR monitoring are clinically achievable on wards with moderate-to-high deterioration rates. This study provides a threshold analysis framework—not a definitive cost-effectiveness conclusion—that hospitals can adapt with local data. All model parameters and analysis code are publicly available.

**Keywords:** respiratory rate; continuous monitoring; cost-minimization analysis; break-even analysis; patient deterioration; health economic modeling

---

## Introduction

Respiratory rate (RR) has been recognized as a sensitive physiological indicator of clinical deterioration, with changes in RR often preceding derangements in heart rate, blood pressure, and consciousness by hours to days [1, 2]. The National Early Warning Score 2 (NEWS2), widely adopted across the UK National Health Service and internationally, assigns RR a maximum weighting of 3 points—equal to other critical parameters including SpO₂, systolic blood pressure, pulse rate, and level of consciousness—making it one of the most heavily weighted components [1]. Despite this clinical importance, RR remains the least accurately and most inconsistently measured vital sign in hospital practice [2].

The fundamental problem is measurement fidelity. Multiple studies have demonstrated that manually recorded RR values exhibit systematic biases including digit preference (clustering at values of 18 and 20 breaths/min), estimation rather than timed counting, and frequent omission [3, 4]. A systematic review by Kallioinen et al. identified five distinct sources of inaccuracy in manual RR measurement: the awareness effect (patient altering breathing when observed), short counting intervals, digit preference, inter-observer variability, and documentation errors [3]. These measurement deficiencies directly compromise the effectiveness of early warning score systems, as inaccurate RR values distort score calculations and may delay clinical escalation [5].

Automated RR monitoring technologies have emerged across multiple technological platforms, from non-contact radar sensors to wearable patches and extensions of existing bedside monitoring equipment. Clinical evidence supporting their deployment is growing: the Dartmouth-Hitchcock Medical Center surveillance monitoring program demonstrated a 48% reduction in ICU transfers on a 36-bed unit over 21 months [6], and a subsequent 10-year review of 111,488 monitored discharges reported zero deaths from opioid-induced respiratory depression [7]. However, translating this evidence into adoption decisions requires an economic framework that accounts for substantial variation in device costs, accuracy characteristics, consumable requirements, staff time implications, and adverse event costs across healthcare systems.

Existing economic analyses are limited in scope. Blike et al. estimated operating margin impacts from the single-institution Dartmouth-Hitchcock program [8], while the NICE Medtech Innovation Briefings for EarlySense [9] and RespiraSense [10] provided device-specific assessments without cross-technology or cross-country comparison. No published study has constructed a unified, reproducible economic model that compares multiple monitoring technologies across diverse healthcare systems using explicitly documented and sensitivity-tested parameters.

The purpose of this study is to develop a unified, multi-technology, cross-country economic model with transparent and reproducible parameters. Specifically, we aim to: (1) construct a transparent, deterministic cost-minimization and break-even model comparing manual RR counting with six automated monitoring scenarios from the hospital perspective; (2) parameterize this model using device accuracy and cost data identified through comprehensive literature search; and (3) evaluate the robustness of break-even thresholds through sensitivity analysis, multi-way scenario analysis, and cross-country comparisons across Japan, UK, Australia, and USA. This study provides a threshold analysis framework—identifying the conditions under which device adoption achieves cost-neutrality—rather than a definitive cost-effectiveness conclusion, since the clinical effectiveness of automated monitoring (i.e., the actual rate of adverse event avoidance) has not been established in randomized trials.

## Methods

### Study Design and Reporting

This study is a health economic modeling study that constructs a deterministic decision-analytic cost-minimization and break-even model for automated respiratory rate monitoring in general hospital wards. The primary analysis is a threshold analysis: rather than estimating the actual cost-effectiveness of device adoption (which would require empirical data on event reduction rates), we calculate the break-even thresholds at which each monitoring scenario achieves cost-neutrality compared with manual counting. The study follows the Consolidated Health Economic Evaluation Reporting Standards 2022 (CHEERS 2022) checklist [11]; a completed 28-item checklist is provided in Supplementary S7.

To parameterize the model, we conducted a comprehensive literature search to identify: (a) commercially available automated RR monitoring devices suitable for general ward deployment, (b) published accuracy data for these devices (Bland-Altman bias and limits of agreement), and (c) cost parameters including device prices, consumable costs, staff time, and adverse event costs from multiple national healthcare systems. The literature search was designed to inform model inputs rather than to produce a formal systematic review; accordingly, no systematic review protocol was registered.

### Literature Search and Data Sources

We searched the following databases from January 2010 to March 2025:

1. **PubMed/MEDLINE** (https://pubmed.ncbi.nlm.nih.gov/): ("respiratory rate" OR "breathing rate" OR "respiration rate") AND ("monitoring" OR "continuous" OR "automated" OR "wearable" OR "contactless") AND ("accuracy" OR "validation" OR "Bland-Altman" OR "limits of agreement" OR "cost" OR "cost-effectiveness" OR "general ward" OR "medical-surgical ward" OR "step-down"). Additional searches with specific device and manufacturer names (Masimo, Nellcor, EarlySense, Neteera, RespiraSense, Capnostream, Guardian M10, Equivital) were performed iteratively.

2. **NICE Evidence Search** (https://www.evidence.nhs.uk/): Including Medtech Innovation Briefings (MIBs), technology appraisals, and clinical guidelines related to respiratory rate monitoring or patient deterioration.

3. **FDA 510(k) database** (https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm): Searched for respiratory rate monitoring devices cleared since 2010, extracting accuracy data from 510(k) summaries where available.

4. **PMDA (Japan) device approval database** (https://www.pmda.go.jp/english/review-services/reviews/approved-information/devices/0001.html): Searched for corresponding Japanese regulatory approvals.

5. **Government cost statistics and grey literature:** NHS National Cost Collection data, government statistical publications from Japan (MHLW), UK (NHS England), Australia (AIHW), and USA (CMS/SCCM), and manufacturer regulatory submissions.

Citation lists of included studies and relevant systematic reviews [3, 12] were hand-searched for additional references.

### Device Identification and Data Extraction

We identified devices meeting the following criteria: (1) commercially available automated/continuous RR monitoring device suitable for adult general ward use; (2) regulatory clearance in at least one jurisdiction (FDA, CE, PMDA); (3) not exclusively for neonatal/pediatric or ICU-only settings. For each device, we extracted: manufacturer, measurement principle, regulatory status, contact type, consumable requirements, EMR integration capability, and publicly available pricing.

For accuracy data, we extracted Bland-Altman bias and 95% limits of agreement (or 98.9% LoA where 95% was not reported, noted accordingly), RMSE, and sensitivity/specificity against a defined reference standard. Conference abstracts were generally excluded unless they provided unique comparative data from large datasets (Kelley et al. [13]: the only multi-technology impedance comparison from 23,243 paired observations). No formal risk-of-bias assessment using standardized tools (e.g., QUADAS-2) was performed; however, we conducted a qualitative assessment of methodological limitations for each study, evaluating sample size adequacy, clinical setting representativeness, reference standard validity, and statistical reporting completeness. These assessments are documented in Table 2, enabling readers to weigh the strength of evidence for each device.

### Cost-Effectiveness Model

**Structure:** A deterministic decision-analytic model comparing manual RR counting (standard care) with six automated monitoring scenarios: (1) under-mattress sensor, (2) bedside monitor with impedance RR, (3) capnography, (4) wearable patch, (5) radar sensor, and (6) pulse-oximetry-derived RR with notification system.

**Perspective and time horizon:** Hospital perspective (direct costs borne by the hospital for monitoring equipment, consumables, maintenance, and staff time; excludes societal costs, patient out-of-pocket costs, and downstream outpatient care); 1-year time horizon (chosen because device procurement and ward-level cost accounting in acute care settings typically operate on annual budget cycles, and because the clinical evidence base [6, 7] reports outcomes over periods of months to years without time-preference discounting). No discounting was applied given the 1-year horizon.

**Base-case parameters (Japan):** All model input parameters, their values, sources, and sensitivity ranges are presented in Table 1 and in the supplementary data file (data/cost_parameters.csv). Key base-case assumptions: 30-bed ward, 90% occupancy (9,855 patient-days/year), standard monitoring frequency of 4.5 observations/patient-day [5], manual RR counting time of 80 seconds/observation (60-second count + 20-second documentation; sensitivity range 60–120 seconds), nurse full-cost hourly rate of ¥3,500 (includes salary, social insurance, and institutional overhead; sensitivity range ¥2,800–¥4,200).

Device costs were derived from published sources where available: EarlySense £35,000/10 beds (NICE MIB49 [9]); RespiraSense £35/patch (NICE MIB299 [10]); Masimo Rad-G €795 (retail); Nihon Kohden PVM-4000 ¥1,350,000 (press release). Where published prices were unavailable (Neteera, Guardian M10), costs were estimated as model assumptions and clearly flagged in the parameter table (Supplementary S2).

**Model equations:** The cost model is defined by the following equations:

*Equation 1 — Manual counting cost per patient-day:*
C_manual = (t_obs / 3600) × w_nurse × f_obs

where t_obs = observation time per measurement (seconds), w_nurse = nurse hourly cost (¥/hour), and f_obs = monitoring frequency (observations/patient-day).

*Equation 2 — Device scenario cost per patient-day:*
C_device_i = D_i / (B × O × 365) + M_i + S_i + L_i

where D_i = annualized device capital cost for scenario i (purchase price / useful life), B = number of beds, O = occupancy rate, M_i = maintenance cost per patient-day, S_i = consumable/supply cost per patient-day, and L_i = device-related staff time cost per patient-day.

*Equation 3 — Incremental cost per patient-day:*
ΔC_i = C_device_i − C_manual

*Equation 4 — Break-even threshold (events per year):*
BE_i = (ΔC_i × B × O × 365) / C_AE

where C_AE = cost per adverse event (country-specific). The break-even threshold represents the minimum number of deterioration events that must be avoided annually for the device scenario to achieve cost-neutrality.

**Outcomes:** (1) Incremental cost per patient-day for each device scenario versus manual counting; (2) break-even threshold expressed as the number of adverse events (deterioration episodes requiring ICU transfer or equivalent) that must be avoided to achieve cost-neutrality (Equation 4).

**Adverse event costs** were drawn from four national sources with explicit derivations (Supplementary S4):
- Japan: ¥476,420/event (3 additional ICU days at ¥96,970/day [15] + 5 additional ward days at ¥37,102/day [15]; this is a highly conservative floor estimate based solely on 診療報酬 reimbursement points, as the actual operating cost of ICU care in Japan averages approximately ¥197,277/bed-day [16], more than double the reimbursement rate; additional costs for procedures, pharmaceuticals, and imaging are excluded)
- UK: £7,368/event (3 ICU days × £1,881/day + 5 ward days × £345/day [17]; 2020/21 NCC data via Parliament Written Question 165361)
- Australia: A$14,134/event (Curtis et al. [18]; controlled for length-of-stay and AR-DRG; 929 deterioration episodes)
- USA: $10,700/event (operating margin impact per ICU transfer avoided; Blike et al. [8]; 31,993 patients over 3.5 years)

**Currency, price year, and conversion:** All costs are reported in the original currency of the source data and converted to Japanese yen (¥) for the model using 2024 mid-year exchange rates: USD/JPY 150, GBP/JPY 190, AUD/JPY 100, EUR/JPY 160 (sensitivity ±15%). Cost data derive from the following price years: Japan bed-day costs (2021 fiscal year [15]); UK critical care and ward costs (2020/21 financial year [17]); Australian deterioration episode costs (2017–2019 [18]); US operating margin data (2019–2022 [8]). Device prices reflect the publication year of the cited source (2016–2024; Supplementary S2). No inflation adjustment was applied across price years, as the primary output is a break-even threshold (ratio of incremental cost to adverse event cost) rather than an absolute monetary value; modest differences in price year denominators largely cancel in ratio calculations. Exchange rate sensitivity (±15%) is tested in the sensitivity analysis.

**Sensitivity analysis:** One-way sensitivity analysis was performed on nine key parameters with clinically plausible ranges (Table 1). Parameters and ranges were determined a priori. Adverse event cost was varied from ¥300,000 to ¥2,000,000 to capture cross-country variation and within-country uncertainty. Multi-way scenario analysis was performed by simultaneously setting all assumption parameters to their best-case and worst-case values to assess model robustness under extreme conditions.

We deliberately elected not to perform probabilistic sensitivity analysis (PSA) with Monte Carlo simulation. PSA is the recommended approach for characterizing joint parameter uncertainty in health economic models when empirical distributions can be assigned to each input parameter [11]. However, for PSA to be informative, each parameter requires a defensible probability distribution derived from empirical data. For several key parameters in our model—device procurement prices (subject to institutional negotiation, not sampling variability), nurse time allocation (workflow-dependent, not stochastically distributed), and adverse event costs (derived from heterogeneous national accounting methodologies)—no such empirical distributions exist. Assigning arbitrary distributions (e.g., gamma, beta, log-normal) to these parameters would give a false impression of statistical precision where none is warranted, potentially misleading decision-makers into over-interpreting confidence intervals that reflect distributional assumptions rather than genuine uncertainty. Our approach—combining one-way sensitivity analysis (identifying influential parameters) with multi-way scenario analysis (stress-testing simultaneous worst-case conditions)—provides a more transparent and decision-relevant characterization of uncertainty.

### Model Validation

Model validation was performed through the following approaches:

**Face validity:** The model structure, parameter values, and output ranges were reviewed for clinical and economic plausibility. Base-case manual counting cost (¥350/patient-day) and device incremental costs (¥106–¥1,900/patient-day) are consistent with published estimates from NICE technology assessments [9, 10] and the Dartmouth-Hitchcock financial analysis [8].

**Extreme value testing:** All parameters were individually set to extreme boundary values to verify that model outputs responded in the expected direction and magnitude. For example, setting adverse event cost to ¥0 correctly yielded infinite break-even thresholds (device never pays for itself through event avoidance alone), while setting device cost to ¥0 correctly yielded negative incremental costs (device scenario cheaper than manual counting).

**Cross-validation:** Break-even thresholds were compared against external benchmarks. Our base-case threshold for pulse-oximetry monitoring (0.24–0.81 events/1,000 patient-days) is consistent with the Dartmouth-Hitchcock observed reduction of 2.7 events/1,000 patient-days [6], which substantially exceeds our threshold—suggesting that the model's break-even estimates are conservative relative to observed real-world outcomes.

**Internal consistency:** All figures and tables are programmatically generated from source CSV files, eliminating transcription errors between data inputs and reported results. The complete analysis code is available for independent verification (see Data Availability).

### Use of AI-Assisted Tools

A large language model (LLM; Anthropic Claude) was used during the drafting and iterative revision of this manuscript, including assistance with literature organization, text drafting, and Python code development for analysis scripts. All factual claims, numerical values, and citations were independently verified against primary sources by the author; corrections are documented in Supplementary S1. All figures were generated programmatically using Python (matplotlib) from the author's data and analysis scripts—no generative AI was used to create any images or figures. The author assumes full responsibility for the accuracy of all content.

### Reproducibility and Data Availability

All data inputs, analysis scripts (Python 3.x), and generated outputs are publicly available in the project repository at https://github.com/mr31ken/respiratory-rate-monitoring-cea. Analyses use pandas, numpy, matplotlib, and scipy. All figures and tables are programmatically generated from the input CSV files. The complete parameter set is provided in machine-readable format (data/cost_parameters.csv) to enable institutional adaptation with local cost data. A snapshot of the repository (release v1.0.1-jcmc-submission) is archived at Zenodo with DOI [10.5281/zenodo.20176683](https://doi.org/10.5281/zenodo.20176683).

## Results

An overview of the study design, data sources, and analytical framework is presented in Figure 1.

### Technology Landscape: Identified Devices and Accuracy Characteristics

The literature search identified 26 primary sources used to parameterize the model, comprising peer-reviewed clinical validation studies (n=8), health technology assessments and regulatory documents (n=7), government cost statistics (n=5), and other published sources (n=6). We identified nine commercially available devices from seven manufacturers across five technology categories (Supplementary Table S1). These devices represent the current landscape of automated RR monitoring options for general ward deployment and provide the technological context for the cost-effectiveness model.

**Regulatory status:** Seven of nine devices hold FDA 510(k) clearance, and all nine are CE-marked. Regarding Japanese regulatory status, the Nihon Kohden PVM-4000 series holds PMDA approval as a general medical device (一般医療機器) for the Japanese market; the Masimo Rad-G and Capnostream 35 are available in Japan through authorized distributors but formal PMDA device approval numbers were not identified in our search; the remaining devices (Neteera, Guardian M10, RespiraSense, Equivital) do not currently hold PMDA approval. The Vitalthings Guardian M10 achieved CE MDR Class IIb certification in 2024 but has not yet received FDA or PMDA clearance as of this writing [19]. The EarlySense under-mattress sensor, while widely cited in the literature, is no longer independently available; EarlySense's contact-free monitoring technology and intellectual property were acquired by Hillrom (now Baxter International) in February 2021 [20].

**Accuracy data (Figure 2; Table 2):** Accuracy data were available for seven of nine devices, derived from eight studies or regulatory assessments. Direct comparison across devices is fundamentally limited by heterogeneity in reference standards (capnography, respiratory inductance plethysmography, manual counting, ECG-derived RR), patient populations, clinical settings, and statistical reporting conventions (95% vs. 98.9% LoA) (Table 2; Supplementary S5 and S8). Device-by-device accuracy findings are detailed in Supplementary S8; key results are summarized here.

Limits of agreement (LoA) ranged from ±1.1 breaths/min (radar-based Guardian M10 vs. respiratory inductance plethysmography [19]) to >±6 breaths/min (thoracic impedance vs. capnography across multiple studies [12–14]). Pulse-oximetry-derived RR showed intermediate LoA of ±3.1–4.0 breaths/min against capnography [21]. For context, manual nurse-documented RR showed LoA of −13.5 to +12.3 against capnography [14], illustrating the magnitude of the baseline measurement problem.

**Accuracy data were not incorporated into the cost model as differential detection probabilities.** This deliberate methodological choice reflects two constraints: (1) no published study has quantified the relationship between RR measurement accuracy (Bland-Altman LoA) and the probability of detecting clinical deterioration; and (2) the heterogeneity in reference standards renders cross-device accuracy comparisons unreliable for modeling purposes. The accuracy data are therefore presented as a technology assessment to inform device selection, not as a model input. Future studies establishing accuracy-to-detection probability functions would enable incorporation of differential accuracy into economic models.

### Cost-Effectiveness Model Results

#### Model Input Parameters (Table 1)

Table 1 presents the complete parameter set used in the cost-effectiveness model. Parameters are classified as "Published" (with source citation) or "Assumption" (model parameters requiring sensitivity testing). All parameters are available in machine-readable format in the supplementary CSV file.

| Parameter | Base case | Range | Source |
|-----------|-----------|-------|--------|
| Ward size | 30 beds | 20–50 | Assumption |
| Occupancy | 90% | 75–95% | Assumption |
| Monitoring frequency | 4.5/patient-day | 2–8 | Pankhurst 2022 [5] |
| Manual counting time | 80 sec/obs | 60–120 | Assumption (60s count + 20s doc) |
| Nurse hourly cost (Japan) | ¥3,500 | ¥2,800–4,200 | Assumption (salary + overhead) |
| General ward bed-day (Japan) | ¥37,102 | — | MHLW 2021 [15] |
| ICU bed-day (Japan) | ¥96,970 | — | 診療報酬 2024 [15] |
| Adverse event cost (Japan, conservative) | ¥476,420 | ¥300,000–2,000,000 | Derived (see S4) |
| Adverse event cost (UK, 2020/21 NCC) | £7,368 | — | Parliament WQ 165361 [17] |
| Adverse event cost (Australia) | A$14,134 | — | Curtis 2021 [18] |
| Adverse event cost (USA) | $10,700 | — | Blike 2025 [8] |
| Device useful life (monitor) | 7 years | 5–10 | Assumption |
| Maintenance rate | 8%/year | 5–12% | Assumption |
| Exchange rates (JPY) | ¥150/USD, ¥190/GBP, ¥100/AUD | ±15% | Approximate 2024 mid-year |

*Note: Costs are expressed in the price year of the original source (2019–2024) and converted to ¥ at 2024 mid-year rates. No inflation adjustment across price years (see Methods: Currency, price year, and conversion).*

#### Per-Patient-Day Costs (Figure 3; Supplementary Table S2)

In the Japan base case, manual RR counting at 4.5 observations/patient-day costs ¥350/patient-day in nurse time alone. Automated monitoring scenarios ranged from ¥456 (radar sensor) to ¥2,250 (capnography) per patient-day, yielding incremental costs of ¥106 to ¥1,900 versus manual counting.

The cost structure differs markedly across technologies. For capnography, consumables (disposable sampling lines at ~¥1,500/day) dominate. For bedside monitors, device depreciation is the primary cost driver. Non-contact sensors (radar, under-mattress) have lower per-patient-day costs because they require no consumables and minimal staff interaction. Wearable patches occupy an intermediate position, with patch replacement costs (~¥950/day) partially offset by the absence of capital equipment.

#### Break-Even Analysis (Figure 4; Table 3)

The economic viability of automated monitoring depends critically on the cost attributed to each adverse event avoided. Using the under-mattress sensor (incremental cost ¥389/patient-day) as the representative non-contact scenario:

- **Japan (bed-day calculation):** With a conservative per-event cost of ¥476,420 (derivation: 3 ICU days × ¥96,970 + 5 ward days × ¥37,102, from MHLW reimbursement data [15]), break-even requires avoidance of 8.0 events/year (0.81 per 1,000 patient-days).

- **Japan (including procedures):** At ¥1,000,000/event (a mid-range estimate incorporating procedures and drugs), break-even drops to 3.8 events/year (0.39 per 1,000 patient-days).

- **UK (2020/21 NCC):** Using £7,368/event [17] (¥1,399,920 at assumed exchange rate; 3 critical care days × £1,881 + 5 ward days × £345), break-even is 2.7 events/year (0.28 per 1,000 patient-days).

- **Australia (Curtis et al.):** Using A$14,134/event [18] (¥1,413,400 at assumed exchange rate), break-even is 2.7 events/year (0.28 per 1,000 patient-days).

- **USA (Blike et al.):** Using $10,700 operating margin impact per ICU transfer avoided [8] (¥1,605,000), break-even is 2.4 events/year (0.24 per 1,000 patient-days).

For context, general medical wards typically report deterioration event rates of 2–10 per 1,000 patient-days depending on case mix and definitions [18, 22]. Post-surgical wards and units with high opioid use have higher rates. Thus, the break-even threshold is plausibly achievable in most acute care settings, particularly with targeted deployment.

#### Sensitivity Analysis (Figure 5; Supplementary Table S3)

One-way sensitivity analysis identified the cost per adverse event and device unit cost as the most influential parameters on the break-even threshold. Over the tested ranges:

- **Adverse event cost** (¥300,000–¥2,000,000): Break-even ranged from 2.7 to 18.1 events/year.
- **Device cost per bed** (¥400,000–¥1,000,000): Break-even ranged from 7.9 to 16.5 events/year.
- **Nurse hourly cost** (¥2,800–¥4,200): Modest impact, as higher nurse costs make manual counting more expensive, slightly favoring device adoption.
- **Monitoring frequency** (2–8 observations/day): Higher manual frequency increases manual cost, improving the device's relative economics.

The model was relatively insensitive to maintenance rate, device useful life, and occupancy rate within tested ranges.

#### Multi-Way Scenario Analysis (Figure 6; Supplementary Table S4)

To assess model robustness under simultaneous parameter variation, we constructed three multi-way scenarios: a best case (all assumption parameters set to values favoring device adoption), a base case (30-bed ward, 90% occupancy, nurse cost ¥3,500/hr, 80-second manual counting time, 4.5 observations/day, device cost ¥700,000/bed, 7-year useful life, 8% maintenance, 5 min/patient-day device staff time, adverse event cost ¥476,420), and a worst case (all assumption parameters simultaneously set to values disfavoring adoption). In the best-case scenario (high nurse cost ¥4,200/hr, long manual counting time 120s, high monitoring frequency 6/day, cheap device ¥400,000, long life 10 years, low maintenance 5%, minimal device staff time 1 min/pd, high adverse event cost ¥2,000,000), the incremental cost of automated monitoring was actually negative (−¥337/patient-day), indicating that under optimistic but plausible conditions, the device scenario is less expensive than manual counting even before accounting for adverse event avoidance.

In the base case, break-even required avoidance of 1.16 events per 1,000 patient-days. In the worst-case scenario (low nurse cost ¥2,800/hr, short counting time 60s, low frequency 2/day, expensive device ¥1,000,000, short life 5 years, high maintenance 12%, high device staff time 8 min/pd, low adverse event cost ¥300,000), the break-even threshold rose to 5.93 events per 1,000 patient-days. Crucially, even this worst-case threshold falls within the published range of deterioration event rates (2–10 per 1,000 patient-days [18, 22]), suggesting that cost-neutrality is achievable even under pessimistic parameter combinations for wards with moderate-to-high clinical acuity.

## Discussion

### Principal Findings

This threshold analysis yields three principal findings. First, the per-patient-day cost of automated RR monitoring is modest (¥106–¥1,900 above manual counting in the Japan base case), placing the economic question firmly in the domain of adverse event avoidance rather than measurement cost savings. Second, break-even thresholds are clinically plausible across all four national healthcare systems examined (0.24–1.3 deterioration events per 1,000 patient-days for non-contact sensors), and even worst-case multi-way scenario analysis yields thresholds within published deterioration rate ranges. These thresholds represent the conditions under which device adoption achieves cost-neutrality; whether devices actually deliver this level of event avoidance in a given institution remains an empirical question that our model cannot answer. Third, the technology landscape reveals wide accuracy variation (LoA ranging from ±1.1 breaths/min for radar to >±6 breaths/min for impedance), which has important implications for clinical deployment decisions even though accuracy differences were not directly incorporated into the cost model.

### Comparison with Prior Economic Analyses

The Dartmouth-Hitchcock Medical Center program provides the most extensive body of evidence for the economic and clinical impact of continuous monitoring on general wards. Taenzer et al. reported a before-and-after study on a single 36-bed orthopedic unit over approximately 21 months, in which pulse-oximetry surveillance was associated with a 48% reduction in ICU transfers (5.6 to 2.9 per 1,000 patient-days) and a 65% reduction in rescue events [6]. Separately, McGrath et al. conducted a 10-year retrospective review (December 2007 to November 2017) encompassing 111,488 discharges on monitored units, finding zero deaths or severe morbidity from opioid-induced respiratory depression while surveillance monitoring was in active use; three deaths occurred on unmonitored units during the implementation rollout period [7]. The financial analysis by Blike et al. evaluated 31,993 patients over 3.5 years, estimating approximately $10,700 in operating margin improvement per ICU transfer avoided and $5,500 per rescue event avoided, projecting annual savings of ~$759,000 for 200 monitored beds [8].

Our model extends this evidence base in three ways. First, we compare six device scenarios rather than a single technology, revealing that cost structures differ markedly (consumable-dominated vs. capital-dominated). Second, by incorporating adverse event costs from four national systems, we demonstrate that the economic case is robust across healthcare contexts with very different cost structures. Third, by providing all parameters in machine-readable format with explicit sensitivity ranges, we enable institutional adaptation—a feature absent from prior analyses.

The $10,700 per ICU transfer avoided estimated by Blike et al. [8] is broadly consistent with the Australian estimate of A$14,134 per deterioration episode by Curtis et al. [18] when accounting for healthcare system cost differences. Our model's break-even thresholds (0.24–1.3 events per 1,000 patient-days for non-contact sensors) are conservative compared to published deterioration rates. Curtis et al. reported that approximately 1,600 of 71,000 admissions (2.3%) experienced clinical deterioration within 72 hours [18], suggesting that even modest detection improvements could exceed break-even.

### Practical Implications for Hospital Decision-Making

The cost-effectiveness framework presented here is designed for institutional adaptation. Hospitals considering automated RR monitoring should:

1. **Estimate their baseline deterioration rate** using existing rapid response team or code blue data.
2. **Calculate facility-specific adverse event costs** using institutional cost accounting rather than published averages.
3. **Prioritize deployment** in units with the highest event rates (post-surgical, respiratory, high-opioid-use wards) rather than pursuing universal deployment.
4. **Consider the total value proposition**, including nurse time reallocation, alarm management burden, and EMR integration requirements, not merely device purchase cost.

### Technology Selection Considerations

No single technology is optimal for all settings. Capnography provides the richest waveform analysis (apnea detection, EtCO₂ trend), but carries the highest consumable cost and requires nasal cannula tolerance, limiting general ward applicability. Radar-based non-contact sensors (e.g., Guardian M10) demonstrated the narrowest LoA in a hospital validation study [19] with zero patient burden, but have limited commercial track records and single-center validation data. Under-mattress sensors represent a mature technology category with the strongest clinical outcome evidence (via the Dartmouth-Hitchcock studies [6, 7]), though the original EarlySense product is no longer independently available. Pulse-oximetry-derived RR (Medtronic Nellcor CNRRS, Masimo RRa/RRp) leverages existing monitoring infrastructure, making it an economically attractive option for hospitals already using compatible pulse oximeters; however, LoA against capnography were ±3–4 breaths/min in hospitalized patients [21].

### Limitations

Several limitations warrant emphasis.

First, the literature search and data extraction were conducted by a single investigator. As this study is a health economic modeling analysis, not a formal systematic review, the formal dual-reviewer methodology was not applied, and selection bias in device and study identification cannot be excluded. However, the primary objective was not to produce an exhaustive evidence synthesis, but to identify representative accuracy and cost parameters for constructing a practical economic framework. The comprehensive search across multiple databases (PubMed, NICE, FDA, PMDA, government statistics), iterative manufacturer-specific searches, and citation tracking mitigate—but do not eliminate—this limitation.

Second, the cost model is deterministic. As detailed in Methods, we deliberately did not perform probabilistic sensitivity analysis because the distributional assumptions for key parameters lack empirical basis; presenting Monte Carlo-derived confidence intervals would imply a statistical precision that the underlying data do not support. The multi-way scenario analysis, by stress-testing simultaneous worst-case parameter combinations, provides decision-makers with a more transparent and actionable characterization of model uncertainty than would artificially narrow confidence bands.

Third, accuracy data across devices are not directly comparable because studies used different reference standards (capnography, respiratory inductance plethysmography, manual counting, ECG-derived RR), patient populations, clinical settings, and statistical reporting conventions (95% vs 98.9% LoA). The absence of head-to-head comparative trials is a significant gap. Accuracy differences were not directly incorporated into the cost model as differential detection probabilities, because no study has quantified the relationship between RR measurement accuracy and deterioration detection rates.

Fourth, the model values nurse time savings at the full hourly cost rate, but this does not represent a direct cash release (i.e., reduced staffing or payroll). In practice, nursing staff will continue bedside visits for other vital signs, medication administration, and clinical assessment. The modeled savings are best understood as an **opportunity cost**: the economic value of time that becomes available for reallocation to higher-value clinical activities. This reallocation may include more frequent assessment of complex patients, earlier identification of non-respiratory clinical changes, or enhanced patient communication—tasks that automated monitoring cannot replace and that are central to nursing professional value. Our valuation at the full nurse hourly cost therefore represents an upper bound on the opportunity cost; the actual realized value depends on how effectively institutions redeploy the freed time. Hospitals should interpret the manual counting cost offset as a framework for workflow optimization rather than a guaranteed budget reduction.

Fifth, the model does not capture potential costs of alarm fatigue from continuous monitoring systems, which could partially offset benefits through increased nursing workload for alarm adjudication.

Sixth, published device prices represent list or retail prices that may differ substantially from institutional procurement costs; prices for two devices (Neteera, Guardian M10) were unavailable and were estimated.

Regarding cost parameters, our Japanese adverse event estimate of ¥96,970/ICU-day relies on 診療報酬 (medical fee schedule) reimbursement points, which substantially understate actual resource consumption. Published hospital cost accounting data indicate that the actual operating cost of ICU care in Japan averages approximately ¥197,277/bed-day [16], more than double the reimbursement rate. Our conservative use of reimbursement-based costs biases the model against device adoption; had we used actual operating costs, the economic case for automated monitoring would be substantially stronger. UK cost data are derived from the 2020/21 National Cost Collection [17]; the most granular data (HRG-level critical care costs, 2023/24 NCC) are published via Power BI dashboards and not yet available as citable tabulated values. The Dartmouth-Hitchcock evidence, while compelling, derives from a single academic institution with an established patient safety culture, and generalizability to other settings requires verification.

Kelley et al. [13] is a conference abstract rather than a peer-reviewed full publication, and the impedance data from that source should be interpreted with this caveat. The Guardian M10 validation [19] was conducted during daytime in 32 patients with a median monitoring duration of 42 minutes, and performance during overnight monitoring or in patients with irregular breathing patterns remains to be demonstrated.

### Research Priorities

Three research priorities emerge from this analysis. First, pragmatic comparative effectiveness trials comparing automated monitoring with usual care in general wards, with cost as a primary or co-primary outcome, are needed. The Dartmouth-Hitchcock before-and-after design [6] provides suggestive evidence, but randomized or stepped-wedge cluster designs would provide stronger causal inference. Second, head-to-head accuracy comparisons of different monitoring technologies using consistent reference standards (preferably respiratory inductance plethysmography rather than manual counting) would enable more confident technology selection and allow accuracy to be incorporated into cost-effectiveness models as differential detection probabilities. Third, implementation science studies examining alarm management strategies, nurse acceptance, and workflow integration are essential for translating monitoring capability into clinical outcome improvement.

## Conclusions

This study constructed a deterministic cost-minimization and break-even model comparing manual respiratory rate counting with six automated monitoring scenarios across four national healthcare systems, and demonstrated that break-even thresholds (0.24–5.93 avoided deterioration events per 1,000 patient-days) are clinically achievable on general wards with moderate-to-high acuity. The economic case for device adoption rests on avoidance of downstream deterioration costs; whether devices actually deliver the required event reduction in specific institutional contexts remains to be established through prospective comparative studies. Hospitals considering automated RR monitoring should use this openly available framework—with institution-specific deterioration rates, adverse event costs, and device procurement prices—to perform local threshold analyses before adoption decisions.

---

## Declarations

**Funding:** This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

**Conflicts of interest:** The author declares no conflicts of interest. No device manufacturer was involved in study design, data collection, analysis, interpretation, or manuscript preparation.

**Ethics approval:** Not applicable. This study used only published aggregate data and did not involve human participants, human tissue, or animals.

**Consent to participate:** Not applicable.

**Author contributions:** Kenichi Saito: Conceptualization, methodology, data curation, formal analysis, software, validation, visualization, writing—original draft, writing—review and editing.

**Data availability:** The complete dataset, analysis code (Python 3.x), and data dictionary supporting this study are publicly available at https://github.com/mr31ken/respiratory-rate-monitoring-cea. An archived snapshot (release v1.0.1-jcmc-submission) is deposited at Zenodo with DOI [10.5281/zenodo.20176683](https://doi.org/10.5281/zenodo.20176683). The repository contains: (1) all input CSV files with source attribution; (2) Python scripts that programmatically generate all figures and tables; (3) complete parameter sets in machine-readable format for institutional adaptation. No patient-level data were used; all inputs derive from published aggregate statistics.

---

## References

[1] Royal College of Physicians. National Early Warning Score (NEWS) 2. London: RCP; 2017. Available from: https://www.rcp.ac.uk/media/a4ibkkbf/news2-final-report_0_0.pdf

[2] Cretikos MA, Bellomo R, Hillman K, et al. Respiratory rate: the neglected vital sign. Med J Aust. 2008;188:657-659.

[3] Kallioinen N, Hill A, Horswill MS, et al. Sources of inaccuracy in the measurement of adult patients' respiratory rate. J Clin Nurs. 2021;30:1485-1499. doi:10.1111/jocn.15714

[4] Philip KEJ, Pack E, Cambiano V, et al. The accuracy of respiratory rate assessment by doctors in a London teaching hospital: a cross-sectional study. J Clin Monit Comput. 2015;29:455-460. doi:10.1007/s10877-014-9621-0

[5] Pankhurst T, Sapey E, Stanley B, et al. Evaluation of NEWS2 response thresholds in a retrospective observational study from a UK acute hospital. BMJ Open. 2022;12:e054027. doi:10.1136/bmjopen-2021-054027

[6] Taenzer AH, Pyke JB, McGrath SP, Blike GT. Impact of pulse oximetry surveillance on rescue events and intensive care unit transfers. Anesthesiology. 2010;112:282-287. doi:10.1097/ALN.0b013e3181ca7a9b

[7] McGrath SP, McGovern KM, Perreard IM, Huang V, Moss LB, Blike GT. Inpatient respiratory arrest associated with sedative and analgesic medications: impact of continuous monitoring on patient mortality and severe morbidity. J Patient Saf. 2020;16(4):e351-e356. doi:10.1097/PTS.0000000000000809

[8] Blike G, McGrath S, Perreard I, McGovern K. Estimating the financial impact of surveillance monitoring in the general care setting. J Patient Saf. 2025;21(8):e169-e175. doi:10.1097/PTS.0000000000001392

[9] NICE. EarlySense for heart and respiratory monitoring and predicting patient deterioration. Medtech innovation briefing MIB49. London: NICE; 2016.

[10] NICE. RespiraSense for continuously monitoring respiratory rate. Medtech innovation briefing MIB299. London: NICE; 2022.

[11] Husereau D, Drummond M, Augustovski F, et al. Consolidated Health Economic Evaluation Reporting Standards 2022 (CHEERS 2022) statement: updated reporting guidance for health economic evaluations. BMJ. 2022;376:e067975. doi:10.1136/bmj-2021-067975

[12] van Loon K, Breteler MJM, van Wolfwinkel L, et al. Accuracy of remote continuous respiratory rate monitoring technologies intended for low care clinical settings: a prospective observational study. Can J Anesth. 2018;65:1324-1332. doi:10.1007/s12630-018-1214-z

[13] Kelley SD, Mestek ML, Bergese SD, et al. Comparison of respiration rate derived from pulse oximetry and transthoracic impedance vs capnography. Eur J Anaesthesiol. 2014;31(Suppl 52):30-31. [Conference abstract]

[14] Lee MM, et al. Assessment of respiratory rate monitoring in the emergency department. J Am Coll Emerg Physicians Open. 2024. PMC11077426.

[15] Ministry of Health, Labour and Welfare (Japan). 社会医療診療行為別統計 2021年. Available from: https://www.mhlw.go.jp/toukei/saikin/hw/sinryo/tyosa21/dl/gaikyou2021.pdf

[16] Hayata E, Takeuchi M, Kamei Y, et al. Cost analysis of ICU care in Japan: a nationwide survey. J Intensive Care. 2019;7:44. doi:10.1186/s40560-019-0396-y

[17] UK Parliament. Written Question 165361: Hospital Beds Costs (2020/21 NCC data). March 2023. Available from: https://www.theyworkforyou.com/wrans/?id=2023-03-14.165361.h

[18] Curtis K, Sivabalan P, Bedford DS, et al. Treatment costs associated with inpatient clinical deterioration. Resuscitation. 2021;166:49-54. doi:10.1016/j.resuscitation.2021.07.022

[19] Toften S, Kjellstadli JT, Kværness J, et al. Contactless and continuous monitoring of respiratory rate in a hospital ward: a clinical validation study. Front Physiol. 2024;15:1502413. doi:10.3389/fphys.2024.1502413

[20] Hillrom (Baxter). Hillrom announces acquisition of contact-free continuous monitoring technology from EarlySense. Press release. February 2021.

[21] Bergese SD, Mestek ML, Kelley SD, et al. Multicenter study validating accuracy of a continuous respiratory rate measurement derived from pulse oximetry: a comparison with capnography. Anesth Analg. 2017;124:1153-1159. doi:10.1213/ANE.0000000000001852

[22] Vlayen A, et al. Exploring unplanned ICU admissions: a systematic review. Acta Clin Belg. 2012;67:350-360.

[23] NICE. Acutely ill adults in hospital: recognising and responding to deterioration. Clinical guideline CG50. London: NICE; 2007.

[24] Subbe CP, Kinsella S. Continuous monitoring of respiratory rate in emergency admissions: evaluation of the RespiraSense sensor in acute care. Sensors. 2018;18:2700. doi:10.3390/s18082700

[25] US Food and Drug Administration. 510(k) Premarket Notification K212143: Neteera 130H/131H. September 2022. Available from: https://www.accessdata.fda.gov/cdrh_docs/pdf21/K212143.pdf

---

## Figure Legends

**Figure 1.** Study overview. Schematic representation of the study design showing the literature search strategy, model construction, and analytical framework. The model compares manual respiratory rate counting with six automated monitoring scenarios, parameterized using data from four national healthcare systems.

**Figure 2.** Accuracy of automated respiratory rate monitoring devices: Bland-Altman bias (circles) and 95% limits of agreement (horizontal bars) versus reference standards. Red dashed lines indicate the ±3 breaths/min clinical acceptance threshold. Where 98.9% LoA are reported (van Loon et al. [12]), this is noted. Only studies reporting Bland-Altman statistics or equivalent are shown. Detailed accuracy metrics including sample sizes, settings, and reference standard for each study are provided in Table 2.

**Figure 3.** Per-patient-day cost comparison of manual respiratory rate counting versus automated monitoring scenarios. Stacked bars show cost components: device depreciation, maintenance, consumables, and staff time. Japan base case: 30-bed ward, 90% occupancy, nurse cost ¥3,500/hour.

**Figure 4.** Break-even analysis showing the number of adverse events (deterioration episodes) that must be avoided per 1,000 patient-days for each device scenario to achieve cost-neutrality, across five adverse event cost assumptions derived from Japan, UK, Australia, and USA data.

**Figure 5.** Tornado diagram for one-way sensitivity analysis of the under-mattress sensor scenario (Japan). Bars represent the change in break-even threshold (adverse events avoided per year) when each parameter is varied across its plausible range. Parameters classified as "Assumption" in Table 1 are marked with an asterisk.

**Figure 6.** Multi-way scenario analysis showing break-even thresholds when all assumption parameters are simultaneously varied. Best case: all parameters set to values favoring device adoption; worst case: all parameters set to values disfavoring adoption. Orange dashed lines indicate the published range of deterioration events (2–10 per 1,000 patient-days [18, 22]).

---

## Tables

**Table 1.** Complete model input parameters with values, ranges, sources, and source classification (Published/Assumption). Available as supplementary CSV (data/cost_parameters.csv).

**Table 2.** Summary of published accuracy data for automated RR monitoring devices, including reference standard, sample size, and Bland-Altman parameters where available. Studies are grouped by technology category. Methodological limitations (sample size, setting, reference standard) are noted for each entry (see tables/table2_accuracy_summary.csv).

**Table 3.** Break-even analysis: adverse events avoided to achieve cost-neutrality, by device scenario and national adverse event cost (see tables/table4_breakeven_analysis.csv).
