# Supplementary Materials

## Economic Evaluation of Automated Respiratory Rate Monitoring in General Hospital Wards: A Deterministic Cost-Minimization and Break-Even Modeling Study

---

## S1. Fact-Check Summary and Corrections from Prior Draft Documents

This study was preceded by two preliminary reports generated through LLM-assisted literature review. Prior to constructing the current analysis, all key factual claims were independently verified against primary sources. This supplement documents the verification process and all corrections applied.

### Critical Corrections (Issues Identified in Revision)

| Original Claim (v1 manuscript) | Correction | Impact |
|-------------------------------|-----------|--------|
| "Capnography bias 0.0, LoA ±1.0 [20]" | **Removed.** Bergese 2017 [20] validates pulse-ox-derived RR (Nellcor CNRRS), not capnography itself. The cited bias/LoA values do not appear in [20]. Primary source for these values was not identified despite systematic search. | Accuracy summary in Abstract and Results rewritten |
| "Thoracic impedance bias −2.2, LoA −6.5 to +2.0 [20]" | **Removed.** These values do not appear in Bergese 2017. Replaced with verified data: van Loon 2018: IPG bias −1.9, 98.9% LoA −13.1 to +9.2 [12]; Lee 2024: impedance bias 0.2, LoA −6.2 to +6.6 [13] | Two independent sources now cited for impedance |
| "Over 10 years and 32,000 patients, 50% ICU reduction + zero OIRD deaths [6]" | **Split into 3 correctly attributed studies.** Taenzer 2010 [6]: ~21 months, single unit, 48% ICU reduction. McGrath 2021 [7]: 10 years, 111,488 monitored discharges, zero OIRD deaths. Blike 2025 [8]: 3.5 years, 31,993 patients, financial analysis. | Discussion section rewritten with correct attributions |
| Guardian M10 "bias near zero, LoA ±1.2" | **Refined.** Toften 2024 [18] reports: stationary bias 0.1, LoA −1.09 to +1.19; mobile bias 0.0, LoA −1.07 to +1.07 (32 patients, 1,112/1,119 paired measurements). | Values updated to verified precision |

### Verified Claims (Unchanged)
| Claim | Source | Verification Status |
|-------|--------|-------------------|
| Masimo Rad-G price €795 (ex-VAT) | DocCheckShop.eu | **Verified** |
| NEWS2 score-based escalation thresholds | RCP NEWS2 report [1] | **Verified** |
| NICE CG50: minimum 12-hourly monitoring | NICE CG50 [22] | **Verified** |
| Australian deterioration cost A$14,134/episode | Curtis et al. 2021 [17] | **Verified** (n=929, PMID: 34314776) |
| Taenzer 2010: ICU transfers 5.6→2.9/1000 pt-days | Taenzer et al. [6] | **Verified** (48% reduction, ~21-month before-after) |
| Guardian M10 MDR Class IIb certification | Vitalthings/Toften 2024 [18] | **Verified** (PMID: 39665054) |
| Neteera 510(k) FDA clearance | FDA K212143 [24] | **Verified** (cleared September 2022) |
| MHLW 2021: 3,710.2 points/day inpatient | MHLW statistics [14] | **Verified** |
| Blike 2025: $10,700/ICU transfer avoided | J Patient Saf 2025 [8] | **Verified** (31,993 patients, 3.5 years) |

### Other Corrected/Clarified Claims
| Original Claim | Correction |
|----------------|-----------|
| EarlySense as current product | **Corrected**: EarlySense's contact-free monitoring technology and IP were acquired by Hillrom (now Baxter) in February 2021 [19]. No claim is made regarding the current corporate status of EarlySense Ltd., as verifiable public records are limited. |
| "72% of recorded RR were inaccurate" (DOCX draft) | **Clarified**: Philip et al. 2015 [4] is a perception survey (72% of doctors rated RR records as only "sometimes accurate"), not a direct accuracy measurement. |
| UK critical care £1,173/bed-day | **Verified but outdated**: From 2012-13 NHS reference costs [16]. Acknowledged as limitation. |
| Neteera "95% accuracy rate" | **Partially verified**: Website claims 95%; FDA 510(k) data show ~93%. Discrepancy noted. |
| Blike et al. 2025 citation | **Corrected**: Full citation: Blike G, McGrath S, Perreard I, McGovern K. J Patient Saf. 2025;21(8):e169-e175. https://doi.org/10.1097/PTS.0000000000001392 |

---

## S2. Model Assumptions and Parameter Sources

All model parameters are documented in `data/cost_parameters.csv` with source attribution. Parameters are classified as:
- **Published**: Value derived directly from a cited source (peer-reviewed, government, or regulatory)
- **Assumption**: Author-determined value requiring sensitivity testing

### Explicitly Assumed Parameters (flagged for sensitivity analysis)

1. **Manual RR counting time (80 seconds)**: Composed of 60 seconds observation + 20 seconds documentation. Literature reports range from 60 seconds (timing only) to 180 seconds (including preparation and recording). Sensitivity range: 60–120 seconds.

2. **Nurse hourly cost (¥3,500 Japan)**: Approximated from average nursing salary with overhead. Japanese nursing salary data from MHLW suggest base hourly rates of ¥2,500–3,000; the ¥3,500 figure includes estimated social insurance and indirect costs. Sensitivity range: ¥2,800–4,200.

3. **Device staff time (2–10 min/patient-day)**: Represents time for alarm management, device checking, and documentation. Highly variable in practice and depends on alarm algorithm tuning.

4. **Radar sensor price (¥500,000/bed)**: The Vitalthings Guardian M10 price is not publicly disclosed. ¥500,000 is a conservative estimate based on comparable medical radar devices. Sensitivity range: ¥400,000–¥1,000,000.

5. **Exchange rates**: USD/JPY 150, GBP/JPY 190, AUD/JPY 100, EUR/JPY 160. Approximate 2024 values; sensitivity ±15%.

### Device Prices: Source Classification

| Device | Price | Source | Classification |
|--------|-------|--------|---------------|
| Masimo Rad-G | €795 | DocCheckShop.eu retail | Published (retail) |
| EarlySense (10-bed) | £35,000 | NICE MIB49 [9] | Published (HTA) |
| RespiraSense (per patch) | £35 | NICE MIB299 [10] | Published (HTA) |
| Nihon Kohden PVM-4000 | ¥1,350,000 | Press release | Published (manufacturer) |
| Capnostream 35 | $3,000–6,000 | Third-party retailers | Published (range) |
| Neteera 130H/131H | Not disclosed | — | **Assumption** |
| Guardian M10 | Not disclosed | — | **Assumption** |
| Equivital eq02+ | €1,944 | Mindtecstore retail | Published (retail) |

---

## S3. Detailed Break-Even Calculations

The break-even formula is:

```
Break-even events/year = (Incremental cost/patient-day × Patient-days/year) / Cost per adverse event
```

Where:
- Incremental cost = Total device scenario cost − Manual counting cost (per patient-day)
- Patient-days/year = Ward beds × Occupancy × 365
- Cost per adverse event = Country-specific estimate from published sources

### Example (Under-mattress sensor, Japan, conservative estimate):
- Incremental cost: ¥388.9/patient-day
- Patient-days/year: 30 × 0.90 × 365 = 9,855
- Adverse event cost (Japan, bed-day): ¥96,970 × 3 + ¥37,102 × 5 = ¥476,420
- Break-even: (388.9 × 9,855) / 476,420 = **8.0 events/year** (0.81 per 1,000 patient-days)

### Cross-country break-even comparison (under-mattress sensor):

| Country | Adverse event cost (local) | In JPY | Break-even (events/year) | Per 1,000 pt-days |
|---------|--------------------------|--------|------------------------|-------------------|
| Japan (conservative) | ¥476,420 | ¥476,420 | 8.0 | 0.81 |
| Japan (mid-range) | ¥1,000,000 | ¥1,000,000 | 3.8 | 0.39 |
| Australia | A$14,134 | ¥1,413,400 | 2.7 | 0.28 |
| USA | $10,700 | ¥1,605,000 | 2.4 | 0.24 |
| UK (2020/21 NCC) | £7,368 | ¥1,399,920 | 2.7 | 0.28 |

---

## S4. Adverse Event Cost Derivation by Country

### Japan
- ICU bed-day: ¥96,970 (特定集中治療室管理料 categories 3-4: 9,697 points × 10 yen/point [14])
- General ward bed-day: ¥37,102 (MHLW 2021 national average: 3,710.2 points × 10 [14])
- Base estimate: 3 additional ICU days + 5 additional ward days = ¥476,420
- This is a **highly conservative floor estimate**: it includes only 診療報酬 (medical fee schedule) reimbursement points and excludes procedure costs, pharmaceutical costs, imaging, and laboratory tests associated with managing the deterioration event
- **Important**: The reimbursement-based ICU bed-day cost of ¥96,970 substantially understates actual resource consumption. A recent nationwide cohort study using bottom-up cost accounting (1,453,929 ICU patients across fiscal years 2018–2022) estimated the mean ICU cost at ¥197,277/patient-day [15], more than double the reimbursement rate. Substituting this bottom-up figure for the reimbursement-based ICU rate yields an alternative base-case adverse event estimate of approximately ¥777,000 (3 × ¥197,277 + 5 × ¥37,102), substantially lowering break-even thresholds.
- Sensitivity range: ¥300,000 (minimal deterioration with rapid recovery) to ¥2,000,000 (including ICU procedures, ventilation, drugs, extended stay)

### United Kingdom
- Critical care bed-day: £1,881 (2020/21 NCC data, via Parliament Written Question 165361 [16])
- General ward bed-day: £345 (2020/21 NCC, acute clinical setting maintenance cost excl. diagnosis/treatment [16])
- Estimate: 3 × £1,881 + 5 × £345 = £7,368
- **Note**: Updated from 2012-13 reference costs (£1,173 critical care, £273 excess bed-day) used in the preliminary draft. The most granular data (HRG-level critical care costs XC01-XC07, 2023/24 NCC) are published via NHS England Power BI dashboards but not yet available as citable tabulated per-day values.

### Australia
- Per-episode incremental cost: A$14,134 (Curtis et al. 2021 [17])
- This is the most methodologically robust estimate in our analysis: derived from 929 deterioration episodes among 71,000 admissions, controlled for length-of-stay and AR-DRG using multivariate regression
- Includes all treatment cost differences, not limited to bed-day fees

### USA
- Operating margin impact per ICU transfer avoided: $10,700 (Blike et al. 2025 [8])
- Operating margin impact per rescue event avoided: $5,500 [8]
- These represent financial impact on hospital operations (revenue minus cost), not total healthcare cost
- Derived from 31,993 patients over 3.5 years at Dartmouth-Hitchcock Medical Center
- Note: Direct cost comparisons with other countries should be interpreted cautiously due to differences in cost accounting methods

---

## S5. Accuracy Data Quality Notes

### Reference Standard Heterogeneity
A critical limitation in comparing accuracy across devices is the use of different reference standards:

| Reference Standard | Used by | Strengths | Limitations |
|-------------------|---------|-----------|-------------|
| Capnography | [20], [12], [13] | Gold standard for RR; breath-by-breath | Requires nasal cannula; patient cooperation |
| Respiratory inductance plethysmography (RIP) | [18] | Non-invasive; validated against pneumotachograph | Requires calibrated bands; body position-dependent |
| Manual counting | [10], [13] | Universal availability | Known to be inaccurate (LoA −13.5 to +12.3 vs capnography [13]) |
| ECG-derived | [10] | Available from existing monitoring | Algorithm-dependent; not a true gold standard |
| Standard monitoring (unspecified) | [9] | As used clinically | Varies by institution |

Studies using manual counting as reference may underestimate device accuracy, as the reference itself introduces substantial measurement error [3, 13].

### Statistical Reporting Heterogeneity
- Most studies report 95% LoA (bias ± 1.96 × SD)
- Van Loon et al. [12] reports 98.9% LoA (bias ± 2.63 × SD with repeated-measures correction)
- EarlySense studies [9] report percentage accuracy (aRE within threshold) rather than Bland-Altman metrics
- Neteera [24] reports percentage within 10% or 2 bpm

These reporting differences preclude a formal meta-analysis and require caution in cross-device comparisons.

---

## S6. Reproducibility Statement

All analyses in this paper are fully reproducible. The complete repository includes:
- `data/`: All input data with documented sources (CSV format with source attribution)
- `data/DATA_DICTIONARY.md`: Complete variable definitions for all data files
- `analysis/`: Python scripts that generate all figures and tables
- `supplementary/`: This document

To reproduce:
```bash
cd analysis/
pip install pandas numpy matplotlib scipy
python 05_generate_all.py
```

All intermediate outputs are regenerated from source data. No manual data manipulation is performed outside the documented scripts. Parameters classified as "Assumption" in `data/cost_parameters.csv` are explicitly flagged and tested in sensitivity analysis.

---

## S8. Device-by-Device Accuracy Data (Detail)

This section provides detailed accuracy findings for each device category, supplementing the summary in the main text (Results: Technology Landscape).

### Radar-based non-contact sensors
The Vitalthings Guardian M10 was validated against respiratory inductance plethysmography (Nox T3s) in 32 emergency ward patients (1,112 paired measurements). Bland-Altman analysis showed bias of 0.1 breaths/min (stationary) and 0.0 breaths/min (mobile), with 95% LoA of −1.09 to +1.19 and −1.07 to +1.07 breaths/min, respectively [18]. This represents the narrowest LoA among devices evaluated in a hospital setting.

### Pulse-oximetry-derived RR
The Medtronic Nellcor Continuous RR (CNRRS) was validated against clinician-overscored capnography in a multicenter study of 79 subjects (23,243 paired observations). Overall bias was 0.18 breaths/min with 95% LoA of −3.06 to +3.42 (RMSD 1.35 breaths/min). Among 53 hospitalized patients, bias was 0.07 breaths/min with wider LoA of −3.84 to +3.97 [20]. For the Masimo Rad-G (pulse-oximetry plethysmographic RR), peer-reviewed adult-ward accuracy data (Bland-Altman bias, limits of agreement, or sensitivity/specificity) were not identified within the scope of our literature search.

### Thoracic impedance
Transthoracic impedance (TTI) showed the poorest agreement across multiple studies. Van Loon et al. reported impedance plethysmography (IPG) bias of −1.9 breaths/min with 98.9% LoA of −13.1 to +9.2 in 20 PACU patients [12]; notably, these are 98.9% LoA (using ±2.63×SD with repeated-measures correction), and 95% LoA would be somewhat narrower. In a recent ED study, telemetry-based impedance showed bias of 0.2 breaths/min but LoA of −6.2 to +6.6 against capnography [13]. In the same study, manual nurse-documented RR showed bias of −0.6 with LoA of −13.5 to +12.3 against capnography, illustrating the magnitude of manual measurement error [13].

### Wearable patches
For RespiraSense, NICE MIB299 reported mean bias of −0.41 breaths/min versus ECG-derived RR with 95% LoA of −3.9 to +3.1 [10]. Against nurse manual counting, the agreement was wider (mean bias −0.58, LoA −5.5 to +4.3), with 20% of intervals showing differences exceeding 3 breaths/min [10]. The Equivital chest belt has primarily been validated in non-clinical exercise and occupational settings rather than in adult hospital wards; peer-reviewed ward-based accuracy data within the scope of this review were not identified.

### Under-mattress sensors
For EarlySense, NICE MIB49 summarized accuracy rates from manufacturer-submitted studies rather than Bland-Altman metrics: adult sleep lab accuracy 93.1%, ICU accuracy 82% versus end-tidal CO₂, and 75% versus manual counting [9]. The varying definitions of "accuracy" across these source studies preclude direct comparison with Bland-Altman data from other devices.

### Non-contact radar (Neteera)
The Neteera 130H/131H received FDA 510(k) clearance with reported accuracy of approximately 93% (within 10% or 2 breaths/min of reference) based on clinical validation in ~170 subjects [24]. The manufacturer's website claims 95% accuracy; the basis for this discrepancy is unclear.

---

## S9. Supplementary Tables (Moved from Main Text)

### Supplementary Table S1. Device Characteristics

Characteristics of commercially available automated respiratory rate monitoring devices identified through literature search (PubMed, NICE Evidence, FDA 510(k), PMDA, manufacturer documentation). Full machine-readable data: `tables/table1_device_comparison.csv`.

| Device | Manufacturer | Measurement principle | Category | Contact type | FDA cleared | CE marked | EMR integration | Abnormal pattern detection | Price (local) | Status |
|--------|--------------|----------------------|----------|--------------|-------------|-----------|-----------------|---------------------------|---------------|--------|
| Rad-G (RRp) | Masimo | PPG-derived RR (plethysmography) | Pulse-ox derived | Finger clip | Yes | Yes | Limited | No (rate only) | €795 | Active |
| Patient SafetyNet + Rad-97 | Masimo | PPG-derived RR + SpO₂ + alarm notification | Pulse-ox derived + notification | Finger clip | Yes | Yes | Yes (HL7/ADT) | Limited (rate trend + threshold) | NR (USD) | Active |
| PVM-4000 series | Nihon Kohden | Thoracic impedance via ECG | Bedside monitor (impedance) | ECG electrodes | Yes (510k) | Yes | Yes (HL7 Gateway) | Limited (rate alarm) | ¥1,350,000 | Active |
| Capnostream 35 | Medtronic | Sidestream capnography (EtCO₂) + SpO₂ | Capnography | Nasal cannula/mask | Yes | Yes | Yes (Vital Sync) | Yes (apnea; EtCO₂ waveform) | $3,000–6,000 | Active |
| EarlySense System 2.0 | Baxter/Hillrom | Piezoelectric under-mattress (ballistocardiography) | Non-contact (under-mattress) | Non-contact | Yes | Yes | Partial | Yes (apnea; bed-exit) | £35,000/10 beds | Discontinued (acquired Feb 2021) |
| Neteera 130H/131H | Neteera | Sub-THz micro-radar (122–123 GHz) | Non-contact (radar) | Non-contact | Yes (K212143, 2022) | Yes (CE MDR) | Partial | Limited | NR | Active |
| Guardian M10 | Vitalthings | Ultra-wideband radar (7.29 GHz) | Non-contact (radar) | Non-contact | No (as of 2024) | Yes (CE MDR Class IIb) | Yes | Yes (waveform; continuous trend) | NR | Active (early commercialization) |
| RespiraSense | PMD Solutions | Piezoelectric chest/abdomen patch | Wearable patch | Adhesive patch | No | Yes | Yes (Bluetooth) | Yes (waveform; motion-tolerant) | £35/patch | Active |
| eq02+ LifeMonitor | Equivital (Hidalgo) | Respiratory inductive plethysmography + ECG | Wearable chest belt | Chest belt | Yes | Yes | Limited | Limited | €1,944 | Active |

*NR = not publicly reported. PPG = photoplethysmography. EtCO₂ = end-tidal CO₂. Status reflects market availability as of March 2025.*

---

### Supplementary Table S2. Per-Patient-Day Cost Comparison (Japan Base Case)

Per-patient-day cost decomposition for manual respiratory rate counting versus five automated monitoring scenarios. Japan base case: 30-bed ward, 90% occupancy, nurse hourly cost ¥3,500, 4.5 observations/patient-day. Full machine-readable data: `tables/table3_cost_per_patient_day.csv`.

| Scenario | Device depreciation (¥/pd) | Maintenance (¥/pd) | Consumables (¥/pd) | Staff time (¥/pd) | Total (¥/pd) | Incremental vs manual (¥/pd) | Annual total (¥) | Staff time (min/pd) |
|----------|---------------------------:|-------------------:|-------------------:|------------------:|-------------:|------------------------------:|------------------:|--------------------:|
| Manual (standard care) | 0.0 | 0.0 | 0.0 | 350.0 | 350.0 | — | 3,449,250 | 6.0 |
| Radar sensor (Guardian M10-type) | 339.2 | 121.8 | 0.0 | 116.7 | 455.9 | +105.9 | 4,492,607 | 2.0 |
| Under-mattress (EarlySense-type) | 563.9 | 274.7 | 0.0 | 175.0 | 738.9 | +388.9 | 7,282,125 | 3.0 |
| Wearable patch (RespiraSense-type) | 0.0 | 0.0 | 950.0 | 291.7 | 1,241.7 | +891.7 | 12,236,625 | 5.0 |
| Bedside monitor (impedance RR) | 915.9 | 328.8 | 200.0 | 233.3 | 1,349.2 | +999.2 | 13,296,214 | 4.0 |
| Capnography (Capnostream-type) | 457.9 | 164.4 | 1,500.0 | 291.7 | 2,249.6 | +1,899.6 | 22,169,732 | 5.0 |

*Sorted by total cost. Device depreciation = (purchase price + installation) / (useful life × beds × occupancy × 365). Annual total = total per-patient-day × ward patient-days/year (9,855).*

---

### Supplementary Table S3. One-Way Sensitivity Analysis (Under-Mattress Sensor, Japan)

Effect of varying each parameter (one at a time) across its plausible range on the incremental cost (¥/patient-day) and break-even threshold (events/year). Base case: 30-bed ward, 90% occupancy, Japan adverse event cost ¥476,420. Full machine-readable data: `tables/table5_sensitivity.csv`.

| Parameter | Base value | Low | High | Incremental cost at low (¥/pd) | Incremental cost at high (¥/pd) | Break-even at low (events/yr) | Break-even at high (events/yr) |
|-----------|-----------:|----:|-----:|-------------------------------:|--------------------------------:|------------------------------:|-------------------------------:|
| Nurse hourly cost (¥) | 3,500 | 2,800 | 4,200 | 585.9 | 515.9 | 12.1 | 10.7 |
| Manual obs time (sec) | 80 | 60 | 120 | 638.4 | 375.9 | 13.2 | 7.8 |
| Monitoring frequency (obs/day) | 4.5 | 2.0 | 8.0 | 745.3 | 278.7 | 15.4 | 5.8 |
| Ward occupancy | 0.90 | 0.75 | 0.95 | 696.1 | 512.7 | 12.0 | 11.2 |
| Device cost per bed (¥) | 665,000 | 400,000 | 1,000,000 | 371.1 | 778.1 | 7.7 | 16.1 |
| Device useful life (yr) | 7 | 5 | 10 | 666.6 | 464.1 | 13.8 | 9.6 |
| Maintenance rate (%) | 8 | 5 | 12 | 490.1 | 631.8 | 10.1 | 13.1 |
| Device-related staff time (min/pd) | 3 | 1 | 8 | 434.2 | 842.5 | 9.0 | 17.4 |
| Adverse event cost (¥) | 476,420 | 300,000 | 2,000,000 | 550.9 | 550.9 | 18.1 | 2.7 |

*Base case incremental cost ¥550.9/pd, base case break-even 11.4 events/year (0.83 per 1,000 patient-days). **Note on reconciliation with main-text Table 3:** the sensitivity scenario uses a representative EarlySense-type device (¥665,000/bed) with explicit annual sensor-replacement cost (~¥90,250/year, derived from £475/year × ¥190/£); this raises the base incremental cost to ¥550.9/pd compared with ¥388.9/pd shown in the main-text Table 3, where annual sensor replacement is included implicitly within the maintenance term. Both treatments are valid; the sensitivity scenario isolates sensor-replacement as a separately varying cost component for transparency. Sensitivity range corresponds to the "Range" column in main-text Table 1. The most influential parameters (largest break-even spread) are adverse event cost, device cost per bed, and monitoring frequency.*

---

### Supplementary Table S4. Multi-Way Scenario Analysis

Break-even thresholds under simultaneous variation of all assumption parameters. Best case = all parameters set to values favoring device adoption (high nurse cost, long manual counting time, high observation frequency, low device cost, long useful life, low maintenance, minimal device staff time, high adverse event cost); worst case = all values reversed. Full machine-readable data: `tables/table6_scenario_analysis.csv`.

| Scenario | Incremental cost (¥/pd) | Adverse event cost (¥/event) | Break-even (events/year) | Per 1,000 patient-days |
|----------|------------------------:|-----------------------------:|-------------------------:|-----------------------:|
| Best case (device favored) | −336.7 | 2,000,000 | −1.8 | −0.17 |
| Base case | 550.9 | 476,420 | 11.4 | 1.16 |
| Worst case (device disfavored) | 1,778.6 | 300,000 | 48.7 | 5.93 |

*Negative break-even in the best case indicates that the device scenario is less expensive than manual counting even without crediting any avoided adverse events; under such conditions, automated monitoring is dominant on cost alone. The worst-case threshold (5.93 events per 1,000 patient-days) remains within the published range of ward deterioration rates (2–10 per 1,000 patient-days [17, 21]).*

---

## S10. CHEERS 2022 Reporting Checklist

Completed checklist per Husereau et al. (BMJ 2022;376:e067975) [11].

| Item No. | CHEERS 2022 Item | Location in Manuscript |
|----------|-----------------|----------------------|
| 1 | Title: identify as economic evaluation | Title: "Economic Evaluation...Cost-Minimization and Break-Even Modeling Study" |
| 2 | Abstract: structured summary | Abstract |
| 3 | Background and objectives | Introduction, paragraphs 1–3 |
| 4 | Health economic analysis plan | Methods: Study Design and Reporting (CHEERS 2022 compliance stated) |
| 5 | Study population | Methods: Eligibility Criteria; Results: Identified Technologies |
| 6 | Setting and location | Methods: Cost-Effectiveness Model (Japan base case; multi-country) |
| 7 | Comparators | Methods: Cost-Effectiveness Model (manual counting vs 5 automated scenarios) |
| 8 | Perspective | Methods: Cost-Effectiveness Model ("Hospital perspective") |
| 9 | Time horizon | Methods: Cost-Effectiveness Model ("1-year time horizon") |
| 10 | Discount rate | Not applicable (1-year time horizon; no discounting required) |
| 11 | Selection of outcomes | Methods: Cost-Effectiveness Model, Outcomes subsection |
| 12 | Measurement of outcomes | Methods: Cost-Effectiveness Model; Table 1; Supplementary S4 |
| 13 | Valuation of outcomes | Methods: Adverse event costs (4 national sources); Supplementary S4 |
| 14 | Measurement and valuation of resources and costs | Methods: Cost-Effectiveness Model; Table 1; data/cost_parameters.csv |
| 15 | Currency, price date, and conversion | Methods: Currency, price year, and conversion (¥ at 2024 mid-year rates; price years 2019–2024; no inflation adjustment with rationale); Table 1 note |
| 16 | Rationale for and description of model | Methods: Cost-Effectiveness Model, Structure subsection; Model Validation (face validity, extreme value, cross-validation) |
| 17 | Analytics and assumptions | Methods: Cost-Effectiveness Model; Table 1 (Published/Assumption classification); Supplementary S2 |
| 18 | Characterizing heterogeneity | Results: Multi-country break-even analysis (Figure 4); Supplementary S3 |
| 19 | Characterizing distributional effects | Not performed (deterministic model); see Limitations paragraph 1 |
| 20 | Characterizing uncertainty | Results: Sensitivity Analysis (Figure 5); Multi-Way Scenario Analysis (Figure 6) |
| 21 | Approach to engagement with patients and others affected | Not applicable (no patient engagement in model construction) |
| 22 | Study parameters | Table 1 (complete parameter set with sources and ranges) |
| 23 | Summary of main results | Results: Break-Even Analysis; Discussion: Principal Findings |
| 24 | Effect of uncertainty | Results: Sensitivity Analysis; Multi-Way Scenario Analysis |
| 25 | Effect of engagement with patients and others affected | Not applicable |
| 26 | Study findings, limitations, generalizability, and current knowledge | Discussion: Limitations (6 paragraphs); Research Priorities |
| 27 | Source of funding | Funding section (after Conclusions) |
| 28 | Conflicts of interest | Conflicts of Interest section (after Conclusions) |
