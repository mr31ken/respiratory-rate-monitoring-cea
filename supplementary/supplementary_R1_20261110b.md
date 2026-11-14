# Supplementary Materials

## Automated Respiratory Rate Monitoring in General Hospital Wards: A Deterministic Break-Even Threshold Analysis

**Target Journal:** Journal of Clinical Monitoring and Computing (Springer)

**Authors:** Kenichi Saito¹,²; Kazumasa Kishimoto³,⁴,⁵; Naoki Ishizuka¹; Kaori Kusuda¹,³; Tomohiro Kuroda¹,³,⁴,⁵

¹ Center for Digital Transformation of Healthcare, Kyoto University Graduate School of Medicine, Kyoto, Japan
² Graduate School of Medicine, Osaka Metropolitan University, Osaka, Japan
³ Division of Medical Information Technology and Administration Planning, Kyoto University Hospital, Kyoto, Japan
⁴ Graduate School of Medicine, Kyoto University, Kyoto, Japan
⁵ Graduate School of Informatics, Kyoto University, Kyoto, Japan

**Corresponding author:** Kenichi Saito, Center for Digital Transformation of Healthcare, Kyoto University Graduate School of Medicine, 53 Kawahara-cho, Shogoin, Sakyo-ku, Kyoto 606-8507, Japan. Tel: +81-75-751-4836. E-mail: mr31ken@kuhp.kyoto-u.ac.jp. ORCID: [0000-0003-2301-706X](https://orcid.org/0000-0003-2301-706X).

---

## S1. Model Assumptions and Parameter Sources

Model parameters are documented in `data/cost_parameters.csv` with source attribution, and device-specific costs are defined in `analysis/model_core.py`. Parameters are classified as:
- **Published**: Value derived directly from a cited source (peer-reviewed, government, or regulatory)
- **Assumption**: Author-determined value requiring sensitivity testing

All results are calculated with a single cost function (`analysis/model_core.py`), so the main analysis, the sensitivity analyses, and the scenario analyses use the same inputs.

### Explicitly Assumed Parameters (flagged for sensitivity analysis)

1. **Nurse time released per observation (20 seconds)**: The nurse time released when RR no longer has to be counted and documented manually. Because RR is usually measured during a bedside visit that continues for other vital signs, the full counting time (80 seconds: 60-second count + 20-second documentation) is treated as an upper bound. The base-case value of 20 seconds, corresponding to the documentation component, is a model assumption, not a measured reduction. Range: 0–80 seconds; the 0-second and 80-second scenarios are reported for all devices (Supplementary Table S5).

2. **Nurse hourly cost (¥3,500 Japan)**: Approximated from average nursing salary with overhead. Japanese nursing salary data from MHLW suggest base hourly rates of ¥2,500–3,000; the ¥3,500 figure includes estimated social insurance and indirect costs. Sensitivity range: ¥2,800–4,200.

3. **Device-related staff time (2–5 min/patient-day, by device)**: Time for device application, checking, troubleshooting, and alarm handling; alarm handling is included within this total rather than added to it. Values: radar sensor 2, under-mattress sensor 3, bedside monitor 4 (including electrode change), wearable patch 5 (application and checking), capnography 5 (including sampling-line change) min/patient-day. Highly variable in practice and dependent on alarm algorithm tuning. Range for the representative under-mattress scenario: 1–8 min/patient-day; an additional 5 min/patient-day of alarm handling is examined for all devices (Supplementary Table S5).

4. **Radar sensor price (¥500,000/bed)**: The Vitalthings Guardian M10 price is not publicly disclosed; ¥500,000 is a model assumption.

5. **Consumables**: wearable patch £35 per patch, assumed to last about 7 days (£5/patient-day); bedside monitor ECG electrodes ~¥200/patient-day; capnography sampling line (FilterLine) ~$10/patient-day. Capnography device price: $4,500 (midpoint of the $3,000–6,000 retail range). For the wearable patch, the kit (£5,000 per kit, including six reusable sensor lobes, a charging station and an iPad) and the installation and network costs (£12,000 per hospital) reported in NICE MIB299 [10] were not included. The company states that one kit is needed per ward, but each patient wears one lobe, whereas the model assumes that all patients are monitored. If the hospital-level costs are allocated to a single 30-bed ward and all costs are amortized over 5 years (the minimum lobe lifespan stated by the company), without maintenance, these costs would add about ¥66 per patient-day with one kit and about ¥143 with five kits (30 lobes, one per bed). The incremental cost of this scenario would then be ¥1,219.7–1,296.8 per patient-day instead of ¥1,154.2, and the Japanese threshold 2.53–2.69 instead of 2.39 averted transfers per 1,000 patient-days (q_required at the illustrative rate, 50.6–53.8% instead of 47.9%). With five kits, the incremental cost would exceed that of the bedside monitor scenario (¥1,261.7). Actual configurations and contract prices were not available, so these figures are illustrative.

6. **General maintenance (8% of purchase price per year)**: Applied to scenarios with capital equipment (radar sensor, under-mattress sensor, bedside monitor, capnography). This assumption does not include the under-mattress sensor replacement (£475 per bed per year [9]), which is costed separately. Range: 5–12%.

7. **Device useful life (7 years)**: Range: 5–10 years.

8. **Days averted per unplanned ICU transfer (3 ICU days and 5 ward days)**: Used to construct the Japanese and UK event values (S3). These days are assumed to be added to the stay by the transfer; no data source was identified. If some of them replace, rather than add to, ward days, the event value would be smaller.

9. **Baseline unplanned ICU transfer rate (illustrative 5 per 1,000 patient-days)**: A rounded value close to two single-centre estimates with the same denominator: 5.6 per 1,000 patient-days on one orthopedic unit before a monitoring intervention (Taenzer et al. [6]) and 5.4 per 1,000 patient-days in a 200-bed Norwegian hospital, including transfers to level 2 ICUs (Torvik et al. [26]). Used only as an illustrative reading point, not as a representative value; results are presented across 1–12 per 1,000 patient-days (main text Fig. 6).

10. **Exchange rates**: USD/JPY 150, GBP/JPY 190, AUD/JPY 100, EUR/JPY 160 (approximate 2024 mid-year values). The GBP/JPY rate, which determines the under-mattress device and sensor costs, was varied by ±15% in the one-way sensitivity analysis.

### Device Prices: Source Classification

| Device | Price | Value used in model | Source | Classification |
|--------|-------|---------------------|--------|---------------|
| Masimo Rad-G | €795 | Not modeled | DocCheckShop.eu retail | Published (retail) |
| EarlySense (10-bed) | £35,000; sensor replacement £475/bed/year | £3,500/bed; £475/bed/year | NICE MIB49 [9] | Published (HTA) |
| RespiraSense (per patch) | £35 | £5/patient-day (7-day patch life assumed) | NICE MIB299 [10] | Published (HTA); patch life assumed |
| Nihon Kohden PVM-4000 | ¥1,350,000 | ¥1,350,000/bed | Press release | Published (manufacturer) |
| Capnostream 35 | $3,000–6,000 | $4,500/bed | Third-party retailers | Published (range); midpoint used |
| Neteera 130H/131H | Not disclosed | Not modeled | — | **Assumption** |
| Guardian M10 | Not disclosed | ¥500,000/bed | — | **Assumption** |
| Equivital eq02+ | €1,944 | Not modeled | Mindtecstore retail | Published (retail) |

---

## S2. Detailed Break-Even Calculations

The model is defined by the following formulas (main text Equations 1–5):

- Value of released nurse time (¥/pd) = released seconds per observation / 3,600 × nurse hourly cost × observations per patient-day
- Gross device cost (¥/pd) = capital + general maintenance + sensor replacement + consumables + device-related staff time
- Incremental cost ΔC (¥/pd) = gross device cost − value of released nurse time
- Break-even BE (per 1,000 patient-days) = ΔC / V × 1,000
- Break-even (events/year) = BE × patient-days per year / 1,000
- Required avoidable fraction q_required = BE / I

Where V is the event value (the incremental cost assumed to be averted per averted unplanned ICU transfer; S3), patient-days per year = beds × occupancy × 365, and I is the baseline unplanned ICU transfer rate per 1,000 patient-days. When ΔC ≤ 0, no transfers need to be averted and no threshold is defined.

### Worked example (under-mattress sensor, Japan, fee-schedule event value)

- Capital: £3,500 × ¥190 / 7 years / (0.90 × 365) = ¥289.2/patient-day
- General maintenance: £3,500 × ¥190 × 8% / (0.90 × 365) = ¥161.9/patient-day
- Sensor replacement: £475 × ¥190 / (0.90 × 365) = ¥274.7/patient-day
- Device-related staff time: 3 min × ¥3,500/60 = ¥175.0/patient-day
- Gross device cost: ¥900.9/patient-day
- Value of released nurse time: 20 s / 3600 × ¥3,500 × 4.5 = ¥87.5/patient-day
- Incremental cost: 900.9 − 87.5 = **¥813.4/patient-day**
- Event value (Japan, fee schedule): 3 × ¥98,900 + 5 × ¥37,102 = ¥482,210
- Break-even: 813.4 / 482,210 × 1,000 = **1.69 per 1,000 patient-days** (16.6 averted transfers/year on a 30-bed ward with 9,855 patient-days/year)
- Required avoidable fraction at I = 5 per 1,000 patient-days: 1.687 / 5 = **33.7%** (threshold before rounding)

### Event-value scenarios (under-mattress sensor)

| Event-value scenario | Role | Endpoint | Event value (local) | In JPY | Break-even (events/year) | Per 1,000 pt-days | q_required at I = 5 (%) |
|---------------------|------|----------|--------------------:|-------:|-------------------------:|------------------:|--------------------------:|
| Japan, fee schedule | primary | Unplanned ICU transfer | ¥482,210 | ¥482,210 | 16.6 | 1.69 | 33.7 |
| UK, NHS cost collection | primary | Unplanned ICU transfer | £7,368 | ¥1,399,920 | 5.7 | 0.58 | 11.6 |
| Japan, claims-based ICU charges | variant | Unplanned ICU transfer | ¥777,341 | ¥777,341 | 10.3 | 1.05 | 20.9 |
| Australia, deterioration episode | separate | MET call, cardiac arrest or unplanned ICU admission within 72 h of admission | A$14,134 | ¥1,413,400 | 5.7 | 0.58 | — |
| USA, operating margin | separate | Transfer to a higher level of care (intermediate or critical care) | $10,700 | ¥1,605,000 | 5.0 | 0.51 | — |

*q_required is not calculated for the Australian value (composite endpoint broader than unplanned ICU transfer) or the US value (transfer to a higher level of care; operating-margin effect, not a cost).*

### Stress test (all one-way inputs at their extremes simultaneously)

For transparency only, all inputs varied in the one-way sensitivity analysis (Supplementary Table S3) were set simultaneously to their most favorable or least favorable values for the under-mattress scenario. This joint state is not plausible and is not used as evidence of robustness.

| Stress test | Incremental cost (¥/pd) | Event value (¥/event) | Break-even (per 1,000 pt-days) | q_required at I = 5 (%) | Note |
|-------------|------------------------:|----------------------:|-------------------------------:|--------------------------:|------|
| All inputs at most favorable values | −308.4 | 777,341 | — | — | Incremental cost ≤ 0; no threshold |
| All inputs at least favorable values | 2,283.4 | 482,210 | 4.74 | 94.7 | — |

*Most favorable: nurse cost ¥4,200/hour, 80 s released per observation, 8 observations/patient-day, occupancy 95%, device price ¥400,000/bed, useful life 10 years, maintenance 5%, staff time 1 min/patient-day, GBP/JPY −15%, claims-based event value. Least favorable: nurse cost ¥4,200/hour, 0 s released, 2 observations/patient-day, occupancy 75%, device price ¥1,000,000/bed, useful life 5 years, maintenance 12%, staff time 8 min/patient-day, GBP/JPY +15%, fee-schedule event value. The nurse cost of ¥4,200/hour is the extreme value in both directions: with 80 s released and 1 min of device-related staff time a higher nurse cost favors the device, whereas with 0 s released and 8 min it disfavors it. Device prices are expressed at the base exchange rate, and the ±15% exchange-rate extreme is applied on top of them (effective ¥340,000 and ¥1,150,000 per bed). Full machine-readable data: `tables/table8_stress_test.csv`.*

---

## S3. Event-Value Derivation

The endpoint of the model is an unplanned transfer from the general ward to an ICU. The event value V is the incremental cost assumed to be averted when one such transfer is averted; it is not the total cost of the admission in which the transfer occurs. Values are grouped by endpoint and cost construct. Only scenarios that relate to an unplanned ICU transfer are used to calculate the required avoidable fraction.

### Japan, fee schedule (primary)
- ICU day: ¥98,900 (Specified ICU Management Fee 3 or 4, first 7 days: 9,890 points × ¥10; FY2024 medical fee schedule [24])
- Inpatient day: ¥37,102 (mean claims per inpatient day across all inpatient care, 3,710.2 points × ¥10; MHLW 2021 [14]); used as a proxy for a post-ICU ward day
- Event value: 3 × ¥98,900 + 5 × ¥37,102 = **¥482,210**
- Construct: payments under the national fee schedule, used as proxies for the resources released. The ICU fee covers the daily management fee only; separately billed procedures, drugs, imaging, and laboratory tests are not included.

### Japan, claims-based ICU charges (variant)
- ICU day: ¥197,277, the mean charge per ICU patient-day in fiscal years 2018–2022 (1,453,929 ICU patients) reported by Ohbe et al. [15]. Ohbe et al. took the payer perspective and used charges at national fee-schedule reference prices derived from administrative claims data, excluding surgery and cardiac catheterization.
- Event value: 3 × ¥197,277 + 5 × ¥37,102 = **¥777,341**
- Construct: payments (claims-based charges), including separately billed items on ICU days. This variant lowers the Japanese thresholds by 38%.

### United Kingdom (primary)
- Critical care bed-day: £1,881 (2020/21 cost collection data, via Parliament Written Question 165361 [16]); an average across adult, paediatric, and neonatal critical care
- General and acute bed-day: £345 (2020/21 [16]); average cost of a bed-day excluding treatment costs
- Event value: 3 × £1,881 + 5 × £345 = **£7,368** (¥1,399,920)
- Construct: provider cost. The most granular data (HRG-level critical care costs, 2023/24 National Cost Collection) are published as interactive dashboards and were not available as citable tabulated per-day values.
- In this scenario, only the event value is British; device and staff costs are the Japanese base case.

### Australia (reported separately)
- Incremental cost per episode of clinical deterioration: A$14,134 (Curtis et al. 2021 [17]), after controlling for length of stay and Australian Refined Diagnosis Related Group
- Endpoint: clinical deterioration within 72 h of admission via the emergency department, defined as a medical emergency team call, cardiac arrest, or unplanned ICU admission (two regional hospitals in New South Wales, March 2018 to February 2019; 1,600 patients deteriorated, of whom 929 had linked cost data)
- Because this composite endpoint is broader than an unplanned ICU transfer, the threshold is reported separately and is not converted to a required avoidable fraction.

### USA (reported separately)
- Operating-margin difference per patient: $10,700 (Blike et al. 2025 [8]), the difference in median operating margin between general-care patients transferred to a higher level of care (intermediate or critical care) and patients with an uncomplicated stay ($10,762, rounded to $10,700 by the authors); per rescue event avoided: $5,500 ($5,532) [8]
- Endpoint: transfer to a higher level of care (intermediate or critical care), which is broader than an unplanned ICU transfer
- These are effects on hospital operating margin (revenue minus cost), not costs, in US dollars of 2016–2019
- Derived from 31,993 adult general-care admissions over 3.5 years (July 2016 to December 2019) at Dartmouth-Hitchcock Medical Center. The authors projected that a 10% reduction in such transfers across 196–201 monitored beds would improve operating margin by approximately $409,000 per year, and cautioned that the per-patient value should not be assumed to apply at every hospital
- Reported separately; the required avoidable fraction is not calculated.

---

## S4. Accuracy Data Quality Notes

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
- Neteera [23] reports percentage within 10% or 2 bpm

These reporting differences preclude a formal meta-analysis and require caution in cross-device comparisons. The accuracy data are not inputs to the economic model.

---

## S5. Reproducibility Statement

All analyses in this paper are fully reproducible. The analysis environment used is **Python 3.9** (tested with 3.9.6) with pandas 2.3.3, numpy 2.0.2, matplotlib 3.9.4, and scipy 1.13.1; minimum-version constraints (`pandas≥2.0`, `numpy≥1.24`, `matplotlib≥3.7`, `scipy≥1.10`) are encoded in `requirements.txt`. The complete repository includes:
- `data/`: All input data with documented sources (CSV format with source attribution)
- `data/DATA_DICTIONARY.md`: Complete variable definitions for all data files
- `analysis/model_core.py`: the single cost and break-even function used by all analyses
- `analysis/`: Python scripts that generate all figures and tables
- `requirements.txt`: minimum-version requirements
- `supplementary/`: This document

To reproduce:
```bash
pip install -r requirements.txt
cd analysis/
python3 05_generate_all.py
```

All intermediate outputs are regenerated from source data. No manual data manipulation is performed outside the documented scripts. Parameters classified as "Assumption" in `data/cost_parameters.csv` are explicitly flagged and tested in sensitivity analysis.

---

## S6. Device-by-Device Accuracy Data (Detail)

This section provides detailed accuracy findings for each device category, supplementing the summary in the main text (Results: Technology Landscape).

### Radar-based non-contact sensors
The Vitalthings Guardian M10 was validated against respiratory inductance plethysmography (Nox T3s) in 32 emergency ward patients (1,112 paired measurements). Bland-Altman analysis showed bias of 0.1 breaths/min (stationary) and 0.0 breaths/min (mobile), with 95% LoA of −1.09 to +1.19 and −1.07 to +1.07 breaths/min, respectively [18]. This represents the narrowest LoA among devices evaluated in a hospital setting.

### Pulse-oximetry-derived RR
The Medtronic Nellcor Continuous RR (CNRRS) was validated against clinician-overscored capnography in a multicenter study of 79 subjects (23,243 paired observations). Overall bias was 0.18 breaths/min with 95% LoA of −3.06 to +3.42 (RMSD 1.35 breaths/min). Among 53 hospitalized patients, bias was 0.07 breaths/min with wider LoA of −3.84 to +3.97 [20]. For the Masimo Rad-G (pulse-oximetry plethysmographic RR), peer-reviewed adult-ward accuracy data (Bland-Altman bias, limits of agreement, or sensitivity/specificity) were not identified within the scope of our literature search.

### Thoracic impedance
Transthoracic impedance (TTI) showed the poorest agreement across multiple studies. Van Loon et al. reported thoracic impedance pneumography (IPG) bias of −1.9 breaths/min with 98.9% LoA of −13.1 to +9.2 in 20 PACU patients [12]; notably, these are 98.9% LoA (using ±2.63×SD with repeated-measures correction), and 95% LoA would be somewhat narrower. In a recent ED study, telemetry-based impedance showed bias of 0.2 breaths/min but LoA of −6.2 to +6.6 against capnography [13]. In the same study, manual nurse-documented RR showed bias of −0.6 with LoA of −13.5 to +12.3 against capnography, illustrating the magnitude of manual measurement error [13].

### Wearable patches
For RespiraSense, NICE MIB299 reported mean bias of −0.41 breaths/min versus ECG-derived RR with 95% LoA of −3.9 to +3.1 [10]. Against nurse manual counting, the agreement was wider (mean bias −0.58, LoA −5.5 to +4.3), with 20% of intervals showing differences exceeding 3 breaths/min [10]. The Equivital chest belt has primarily been validated in non-clinical exercise and occupational settings rather than in adult hospital wards; peer-reviewed ward-based accuracy data within the scope of this review were not identified.

### Under-mattress sensors
For EarlySense, NICE MIB49 summarized accuracy rates from manufacturer-submitted studies rather than Bland-Altman metrics: adult sleep lab accuracy 93.1%, ICU accuracy 82% versus end-tidal CO₂, and 75% versus manual counting [9]. The varying definitions of "accuracy" across these source studies preclude direct comparison with Bland-Altman data from other devices.

### Non-contact radar (Neteera)
The Neteera 130H/131H received FDA 510(k) clearance with reported accuracy of approximately 93% (within 10% or 2 breaths/min of reference) based on clinical validation in ~170 subjects [23]. The manufacturer's website claims 95% accuracy; the basis for this discrepancy is unclear.

---

## S7. Supplementary Tables

### Supplementary Table S1. Device Characteristics

Characteristics of commercially available automated respiratory rate monitoring devices identified through literature search (PubMed, NICE Evidence, FDA 510(k), PMDA, manufacturer documentation). Full machine-readable data: `tables/table1_device_comparison.csv`.

| Device | Manufacturer | Measurement principle | Category | Contact type | FDA cleared | CE marked | EMR integration | Abnormal pattern detection | Price (local) | Status |
|--------|--------------|----------------------|----------|--------------|-------------|-----------|-----------------|---------------------------|---------------|--------|
| Rad-G (RRp) | Masimo | PPG-derived RR (plethysmography) | Pulse-ox derived | Finger clip | Yes | Yes | Limited | No (rate only) | €795 | Active |
| Patient SafetyNet + Rad-97 | Masimo | PPG-derived RR + SpO₂ + alarm notification | Pulse-ox derived + notification | Finger clip | Yes | Yes | Yes (HL7/ADT) | Limited (rate trend + threshold) | NR (USD) | Active |
| PVM-4000 series | Nihon Kohden | Thoracic impedance via ECG | Bedside monitor (impedance) | ECG electrodes | Not identified | Yes | Yes (HL7 Gateway) | Limited (rate alarm) | ¥1,350,000 | Active |
| Capnostream 35 | Medtronic | Sidestream capnography (EtCO₂) + SpO₂ | Capnography | Nasal cannula/mask | Yes | Yes | Yes (Vital Sync) | Yes (apnea; EtCO₂ waveform) | $3,000–6,000 | Active |
| EarlySense System 2.0 | Baxter/Hillrom | Piezoelectric under-mattress (ballistocardiography) | Non-contact (under-mattress) | Non-contact | Yes | Yes | Partial | Yes (apnea; bed-exit) | £35,000/10 beds | Discontinued (acquired Feb 2021) |
| Neteera 130H/131H | Neteera | Sub-THz micro-radar (122–123 GHz) | Non-contact (radar) | Non-contact | Yes (K212143, 2022) | Yes (CE MDR) | Partial | Limited | NR | Active |
| Guardian M10 | Vitalthings | Ultra-wideband radar (7.29 GHz) | Non-contact (radar) | Non-contact | Not identified | Yes (CE MDR Class IIb) | Yes | Yes (waveform; continuous trend) | NR | Active (early commercialization) |
| RespiraSense | PMD Solutions | Piezoelectric chest/abdomen patch | Wearable patch | Adhesive patch | Yes (K220111, 2022) | Yes | Yes (Bluetooth) | Yes (waveform; motion-tolerant) | £35/patch | Active |
| eq02+ LifeMonitor | Equivital (Hidalgo) | Respiratory inductive plethysmography + ECG | Wearable chest belt | Chest belt | Yes | Yes | Limited | Limited | €1,944 | Active |

*NR = not publicly reported. PPG = photoplethysmography. EtCO₂ = end-tidal CO₂. Status reflects market availability as of March 2025; “Not identified” means that no clearance was identified in our search.*

---

### Supplementary Table S2. Per-Patient-Day Cost Components (Japan Base Case)

Per-patient-day cost components of the five automated monitoring scenarios relative to manual respiratory rate counting. Japan base case: 30-bed ward, 90% occupancy, nurse hourly cost ¥3,500, 4.5 observations/patient-day, 20 s of nurse time released per observation. The wearable patch scenario excludes the kit and installation costs (see S1, Consumables). Full machine-readable data: `tables/table3_cost_per_patient_day.csv`.

| Scenario | Capital (¥/pd) | General maintenance (¥/pd) | Sensor replacement (¥/pd) | Consumables (¥/pd) | Device-related staff time (¥/pd) | Gross device cost (¥/pd) | Released nurse time (¥/pd) | Incremental cost (¥/pd) | Annual incremental (¥) | Staff time (min/pd) |
|----------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Radar sensor (Guardian M10-type) | 217.4 | 121.8 | 0.0 | 0.0 | 116.7 | 455.9 | −87.5 | 368.4 | 3,630,295 | 2 |
| Under-mattress sensor (EarlySense-type) | 289.2 | 161.9 | 274.7 | 0.0 | 175.0 | 900.9 | −87.5 | 813.4 | 8,015,812 | 3 |
| Wearable patch (RespiraSense-type) | 0.0 | 0.0 | 0.0 | 950.0 | 291.7 | 1,241.7 | −87.5 | 1,154.2 | 11,374,312 | 5 |
| Bedside monitor (impedance RR) | 587.1 | 328.8 | 0.0 | 200.0 | 233.3 | 1,349.2 | −87.5 | 1,261.7 | 12,433,902 | 4 |
| Capnography (Capnostream-type) | 293.5 | 164.4 | 0.0 | 1,500.0 | 291.7 | 2,249.6 | −87.5 | 2,162.1 | 21,307,420 | 5 |

*Capital = purchase price per bed / (useful life × occupancy × 365). General maintenance = 8% of purchase price per year / (occupancy × 365); it does not include sensor replacement. Released nurse time = 4.5 observations × 20 s × ¥3,500/hour. Incremental cost = gross device cost − released nurse time. Annual incremental = incremental cost × 9,855 patient-days/year. Each cost component appears once; the incremental cost of the under-mattress scenario (¥813.4) is the single base-case value used in all analyses.*

---

### Supplementary Table S3. One-Way Sensitivity Analysis (Under-Mattress Sensor, Japan)

Effect of varying each input (one at a time) across its range on the incremental cost, the break-even threshold (unplanned ICU transfers averted per 1,000 patient-days), and the required avoidable fraction at the illustrative rate of 5 per 1,000 patient-days. Event value: Japan, fee schedule (¥482,210), except for the event-value row. Full machine-readable data: `tables/table5_sensitivity.csv`.

| Input | Base | Low | High | Incremental at low (¥/pd) | Incremental at high (¥/pd) | Break-even at low (per 1,000 pd) | Break-even at high (per 1,000 pd) | q_required at low (%) | q_required at high (%) |
|-------|-----:|----:|-----:|---:|---:|---:|---:|---:|---:|
| Nurse hourly cost (JPY) | 3,500 | 2,800 | 4,200 | 795.9 | 830.9 | 1.65 | 1.72 | 33.0 | 34.5 |
| Nurse time released per observation (s) | 20 | 0 | 80 | 900.9 | 550.9 | 1.87 | 1.14 | 37.4 | 22.8 |
| Monitoring frequency (obs/day) | 4.5 | 2 | 8 | 862.0 | 745.3 | 1.79 | 1.55 | 35.8 | 30.9 |
| Ward occupancy | 90% | 75% | 95% | 958.6 | 775.2 | 1.99 | 1.61 | 39.8 | 32.2 |
| Device price per bed (JPY) | 665,000 | 400,000 | 1,000,000 | 633.6 | 1,040.6 | 1.31 | 2.16 | 26.3 | 43.2 |
| Device useful life (yr) | 7 | 5 | 10 | 929.1 | 726.6 | 1.93 | 1.51 | 38.5 | 30.1 |
| General maintenance rate | 8% | 5% | 12% | 752.6 | 894.3 | 1.56 | 1.85 | 31.2 | 37.1 |
| Device-related staff time incl. alarms (min/pd) | 3 | 1 | 8 | 696.7 | 1,105.0 | 1.44 | 2.29 | 28.9 | 45.8 |
| GBP/JPY exchange rate (±15%) | 190 | 161.5 | 218.5 | 704.5 | 922.3 | 1.46 | 1.91 | 29.2 | 38.3 |
| Event value, Japan (fee schedule → claims-based ICU charges) | 482,210 | 482,210 | 777,341 | 813.4 | 813.4 | 1.69 | 1.05 | 33.7 | 20.9 |

*Base case: incremental cost ¥813.4/patient-day; break-even 1.69 per 1,000 patient-days (16.6 averted transfers/year); q_required 33.7% at 5 per 1,000 patient-days. Ranges correspond to the "Range" column in main-text Table 1. The device-price range is applied to the purchase price per bed (base ¥665,000); the GBP/JPY range applies to the device and sensor costs.*

---

### Supplementary Table S4. Two-Way Sensitivity Analysis: Released Nurse Time and Device-Related Staff Time (Under-Mattress Sensor)

Break-even thresholds (unplanned ICU transfers averted per 1,000 patient-days) and required avoidable fractions at the illustrative rate of 5 per 1,000 patient-days, varying released nurse time per observation and device-related staff time (including alarm handling) jointly; all other inputs at base-case values. Full machine-readable data: `tables/table7_two_way.csv`.

| Released time (s/obs) | Staff time (min/pd) | Incremental cost (¥/pd) | Break-even, Japan (per 1,000 pd) | q_required, Japan (%) | Break-even, UK (per 1,000 pd) | q_required, UK (%) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 784.2 | 1.63 | 32.5 | 0.56 | 11.2 |
| 0 | 3 | 900.9 | 1.87 | 37.4 | 0.64 | 12.9 |
| 0 | 5 | 1,017.5 | 2.11 | 42.2 | 0.73 | 14.5 |
| 0 | 8 | 1,192.5 | 2.47 | 49.5 | 0.85 | 17.0 |
| 20 | 1 | 696.7 | 1.44 | 28.9 | 0.50 | 10.0 |
| 20 | 3 | 813.4 | 1.69 | 33.7 | 0.58 | 11.6 |
| 20 | 5 | 930.0 | 1.93 | 38.6 | 0.66 | 13.3 |
| 20 | 8 | 1,105.0 | 2.29 | 45.8 | 0.79 | 15.8 |
| 40 | 1 | 609.2 | 1.26 | 25.3 | 0.44 | 8.7 |
| 40 | 3 | 725.9 | 1.51 | 30.1 | 0.52 | 10.4 |
| 40 | 5 | 842.5 | 1.75 | 34.9 | 0.60 | 12.0 |
| 40 | 8 | 1,017.5 | 2.11 | 42.2 | 0.73 | 14.5 |
| 60 | 1 | 521.7 | 1.08 | 21.6 | 0.37 | 7.5 |
| 60 | 3 | 638.4 | 1.32 | 26.5 | 0.46 | 9.1 |
| 60 | 5 | 755.0 | 1.57 | 31.3 | 0.54 | 10.8 |
| 60 | 8 | 930.0 | 1.93 | 38.6 | 0.66 | 13.3 |
| 80 | 1 | 434.2 | 0.90 | 18.0 | 0.31 | 6.2 |
| 80 | 3 | 550.9 | 1.14 | 22.8 | 0.39 | 7.9 |
| 80 | 5 | 667.5 | 1.38 | 27.7 | 0.48 | 9.5 |
| 80 | 8 | 842.5 | 1.75 | 34.9 | 0.60 | 12.0 |

---

### Supplementary Table S5. Scenario Analyses: Released Nurse Time and Alarm Handling (All Device Scenarios)

Break-even thresholds and required avoidable fractions for all five device scenarios under alternative released-time and alarm-handling assumptions, with the Japanese fee-schedule and UK event values. The final row for each device gives the additional alarm-handling time (min/patient-day, added to the base-case device-related staff time) at which q_required would reach 100% at the illustrative rate of 5 per 1,000 patient-days. Full machine-readable data: `tables/table6_scenario_analysis.csv`.

| Device scenario | Scenario | Incremental cost (¥/pd) | Break-even, Japan (per 1,000 pd) | q_required, Japan (%) | Break-even, UK (per 1,000 pd) | q_required, UK (%) |
|-----------------|----------|---:|---:|---:|---:|---:|
| Radar sensor (Guardian M10-type) | Base case (20 s released) | 368.4 | 0.76 | 15.3 | 0.26 | 5.3 |
| Radar sensor (Guardian M10-type) | No nurse time released (0 s) | 455.9 | 0.95 | 18.9 | 0.33 | 6.5 |
| Radar sensor (Guardian M10-type) | Full counting time released (80 s) | 105.9 | 0.22 | 4.4 | 0.08 | 1.5 |
| Radar sensor (Guardian M10-type) | Alarm handling +5 min/patient-day | 660.0 | 1.37 | 27.4 | 0.47 | 9.4 |
| Radar sensor (Guardian M10-type) | Additional alarm handling (min/pd) at which q_required = 100% at I = 5 | — | Japan: 35.0 min | — | UK: 113.7 min | — |
| Under-mattress sensor (EarlySense-type) | Base case (20 s released) | 813.4 | 1.69 | 33.7 | 0.58 | 11.6 |
| Under-mattress sensor (EarlySense-type) | No nurse time released (0 s) | 900.9 | 1.87 | 37.4 | 0.64 | 12.9 |
| Under-mattress sensor (EarlySense-type) | Full counting time released (80 s) | 550.9 | 1.14 | 22.8 | 0.39 | 7.9 |
| Under-mattress sensor (EarlySense-type) | Alarm handling +5 min/patient-day | 1,105.0 | 2.29 | 45.8 | 0.79 | 15.8 |
| Under-mattress sensor (EarlySense-type) | Additional alarm handling (min/pd) at which q_required = 100% at I = 5 | — | Japan: 27.4 min | — | UK: 106.0 min | — |
| Wearable patch (RespiraSense-type) | Base case (20 s released) | 1,154.2 | 2.39 | 47.9 | 0.82 | 16.5 |
| Wearable patch (RespiraSense-type) | No nurse time released (0 s) | 1,241.7 | 2.57 | 51.5 | 0.89 | 17.7 |
| Wearable patch (RespiraSense-type) | Full counting time released (80 s) | 891.7 | 1.85 | 37.0 | 0.64 | 12.7 |
| Wearable patch (RespiraSense-type) | Alarm handling +5 min/patient-day | 1,445.8 | 3.00 | 60.0 | 1.03 | 20.7 |
| Wearable patch (RespiraSense-type) | Additional alarm handling (min/pd) at which q_required = 100% at I = 5 | — | Japan: 21.5 min | — | UK: 100.2 min | — |
| Bedside monitor (impedance RR) | Base case (20 s released) | 1,261.7 | 2.62 | 52.3 | 0.90 | 18.0 |
| Bedside monitor (impedance RR) | No nurse time released (0 s) | 1,349.2 | 2.80 | 56.0 | 0.96 | 19.3 |
| Bedside monitor (impedance RR) | Full counting time released (80 s) | 999.2 | 2.07 | 41.4 | 0.71 | 14.3 |
| Bedside monitor (impedance RR) | Alarm handling +5 min/patient-day | 1,553.4 | 3.22 | 64.4 | 1.11 | 22.2 |
| Bedside monitor (impedance RR) | Additional alarm handling (min/pd) at which q_required = 100% at I = 5 | — | Japan: 19.7 min | — | UK: 98.4 min | — |
| Capnography (Capnostream-type) | Base case (20 s released) | 2,162.1 | 4.48 | 89.7 | 1.54 | 30.9 |
| Capnography (Capnostream-type) | No nurse time released (0 s) | 2,249.6 | 4.67 | 93.3 | 1.61 | 32.1 |
| Capnography (Capnostream-type) | Full counting time released (80 s) | 1,899.6 | 3.94 | 78.8 | 1.36 | 27.1 |
| Capnography (Capnostream-type) | Alarm handling +5 min/patient-day | 2,453.8 | 5.09 | 101.8 | 1.75 | 35.1 |
| Capnography (Capnostream-type) | Additional alarm handling (min/pd) at which q_required = 100% at I = 5 | — | Japan: 4.3 min | — | UK: 82.9 min | — |

*Alarm handling is varied as total handling time; device-specific alarm counts were not derived from accuracy data.*

---

## S8. CHEERS 2022 Reporting Checklist

Completed checklist per Husereau et al. (BMJ 2022;376:e067975) [11].

| Item No. | CHEERS 2022 Item | Location in Manuscript |
|----------|-----------------|----------------------|
| 1 | Title: identify as economic evaluation | Title: "...A Deterministic Break-Even Threshold Analysis" |
| 2 | Abstract: structured summary | Abstract |
| 3 | Background and objectives | Introduction |
| 4 | Health economic analysis plan | No health economic analysis plan was registered or published. An internal, unpublished study outline described the model structure, perspective, time horizon, and planned one-way sensitivity analysis; analyses added during revision (released-time, alarm-handling, two-way, and event-value variant analyses) were not pre-specified (Methods: Sensitivity and scenario analyses) |
| 5 | Study population | Methods: Break-Even Threshold Model (adult general ward; base-case parameters) |
| 6 | Setting and location | Methods: Break-Even Threshold Model (30-bed ward, Japan base case; Japanese and UK event values, with Australian and US values reported separately) |
| 7 | Comparators | Methods: Break-Even Threshold Model, Structure (manual counting vs 5 automated scenarios) |
| 8 | Perspective | Methods: Break-Even Threshold Model, Perspective and time horizon; Endpoint and event value |
| 9 | Time horizon | Methods: Break-Even Threshold Model ("1-year time horizon") |
| 10 | Discount rate | Not applicable (1-year time horizon; no discounting required) |
| 11 | Selection of outcomes | Methods: Endpoint and event value (averted unplanned ICU transfer); Required avoidable fraction |
| 12 | Measurement of outcomes | Not measured: the model calculates the number of transfers that must be averted (Equations 4 and 5) rather than estimating the number averted |
| 13 | Valuation of outcomes | Methods: Endpoint and event value; Table 1; Supplementary S3 |
| 14 | Measurement and valuation of resources and costs | Methods: Break-Even Threshold Model; Table 1; Supplementary S1; data/cost_parameters.csv |
| 15 | Currency, price date, and conversion | Methods: Currency, price year, and conversion (¥ at approximate 2024 mid-year rates; price years 2016–2024; no inflation adjustment); Limitations |
| 16 | Rationale for and description of model | Methods: Study Design and Reporting; Break-Even Threshold Model (Equations 1–5); Model Validation (face validity, extreme value testing, internal consistency) |
| 17 | Analytics and assumptions | Methods: Break-Even Threshold Model; Table 1 (published/assumption classification); Supplementary S1 |
| 18 | Characterizing heterogeneity | Results: event-value scenarios (Table 3; Fig. 4) and dependence on the baseline transfer rate (Fig. 6) |
| 19 | Characterizing distributional effects | Not assessed (distributional effects on population subgroups were outside the scope of this hospital-level threshold analysis) |
| 20 | Characterizing uncertainty | Methods: Sensitivity and scenario analyses (one-way, two-way, scenario; PSA not performed, with rationale) |
| 21 | Approach to engagement with patients and others affected | Not applicable (no patient engagement in model construction) |
| 22 | Study parameters | Table 1 (parameter set with sources and ranges); Supplementary S1 |
| 23 | Summary of main results | Results: Break-Even Thresholds and Required Avoidable Fraction (Table 3); Discussion: Principal Findings |
| 24 | Effect of uncertainty | Results: Sensitivity and Scenario Analyses (Fig. 5; Supplementary Tables S3–S5; stress test in Supplementary S2) |
| 25 | Effect of engagement with patients and others affected | Not applicable |
| 26 | Study findings, limitations, generalizability, and current knowledge | Discussion (including Limitations and Research Priorities) |
| 27 | Source of funding | Statements and Declarations: Funding |
| 28 | Conflicts of interest | Statements and Declarations: Conflicts of interest |
