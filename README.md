# SFCR Table Extraction - Italian Life Insurance Market

## Overview
This project extracts and structures Solvency and Financial Condition Report (SFCR) data from PDFs using Mistral OCR and Pydantic schemas.

Current table categories processed by `main.py`:
- `S_02_01_02 – Balance sheet`
- `S_23_01_01 – Own funds`
- `S_25_01_21 – Solvency Capital Requirement – for undertakings on Standard Formula`

The original implementation was developed in Jupyter Notebook and is being incrementally refactored into a modular Python codebase. Core Python source files are organized under `Code/`.

## Pipeline

| Phase | What happens | Folder / script |
|-------|----------------|-----------------|
| 1. Catalog | Map companies, PDFs, and page numbers | `master_list_partial.csv`, `Input/` |
| 2. Extract | Isolate table pages and run Mistral OCR | `Code/main.py` → `Output/`, `Single_pdf/` |
| 3. Manual review | Spot-check OCR output against source PDFs | `Output/` → `Output_final/` |
| 4. Cross-validate | Run internal consistency checks on corrected tables | `Code/run_cross_checks.py` → `Validation/` |
| 5. Measure accuracy | Compare raw OCR output with corrected finals | `Code/compare_output_tables.py` |

`Final_output/` is a legacy duplicate of `Output_final/` and is kept for backward compatibility.

## Quick start

### 1) Create and activate a virtual environment
Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Set API key
`main.py` expects the Mistral key in an environment variable:
```powershell
$env:MISTRAL_API_KEY="your_api_key_here"
```

### 4) Prepare inputs
- Put source PDFs in `Input/`
- Ensure `master_list_partial.csv` exists in the project root

### 5) Run extraction
```powershell
python Code/main.py
```

Raw aggregated tables are written to `Output/`.

### 6) Run cross-validation (after manual corrections in `Output_final/`)
Run all table checks in one pass:
```powershell
python Code/run_cross_checks.py
```

Or run a single table:
```powershell
python Code/cross_check_S020102.py
python Code/cross_check_S230101.py
python Code/cross_check_S250121.py
```

Validation summaries are written to `Validation/validation_summary_*.csv`. Failed checks also produce per-company diagnostic CSVs in `Validation/`.

### 7) Compare raw OCR output with corrected tables
```powershell
python Code/compare_output_tables.py
```

Use `--atol 1.5` to count near-matches as equal. Default is exact numeric match after parsing.

## Validation results

Cross-validation was run against the corrected tables in `Output_final/` (May 2026). All internal consistency checks passed for every company:

| Table | Cross-check result |
|-------|-------------------|
| S.02.01.02 balance sheet | PASS (17 tests) |
| S.23.01.01 own funds | PASS (4 tests) |
| S.25.01.21 SCR standard formula | PASS (1 test) |

OCR accuracy was measured by comparing `Output/` (raw extraction) with `Output_final/` (manually corrected values):

| Table | Compared cells | Equal cells | Match rate |
|-------|----------------|-------------|------------|
| S.02.01.02 | 1,162 | 999 | 85.97% |
| S.23.01.01 | 448 | 351 | 78.35% |
| S.25.01.21 | 96 | 81 | 84.38% |
| **Overall** | **1,706** | **1,431** | **83.88%** |

These figures reflect exact numeric equality after parsing. Manual corrections in `Output_final/` fix OCR errors and formatting differences before the cross-validation step.

## Companies in Scope

 - [Credemvita S.p.A.]
 - [AXA MPS Assicurazioni Vita]
 - [CRÈDIT AGRICOLE VITA]
 - [Società Reale Mutua di Assicurazioni]
 - [Cardif Vita S.p.A.]
 - [MEDIOLANUM VITA S.p.A.]
 - [Generali Italia S.p.A.]
 - [Banco BPM Vita S.p.A.]
 - [HDI ASSICURAZIONI S.p.A.]
 - [Gruppo Assicurativo Poste Vita]
 - [FIDEURAM VITA S.P.A.]
 - [CNP Vita Assicura S.p.A.]
 - [ITAS VITA]
 - [Helvetia Vita S.p.A.]
 - [Vittoria Assicurazioni S.p.A.]
 - [GROUPAMA ASSICURAZIONI S.P.A.]
 - [UniCredit Allianz Vita S.p.A.]
 - [Zurich Investments Life S.p.A.]
 - [UniCredit Life Insurance S.p.A.]
 - [Athora Italia S.p.A.]
 - [Nobis Vita S.p.A.]

## Contact
A version of this process is used by us to extract data for our actuarial models. One of the benefits of releasing our code is the feedback and improvement ideas. If you have any, you can contact us at gregor@osmodelling.com.

## License
MIT license

[Credemvita S.p.A.]:https://www.credemvita.it/content/credemvita/it/home/investor-relations.html
[AXA MPS Assicurazioni Vita]:https://corporate.axa.it/
[CRÈDIT AGRICOLE VITA]:https://www.ca-vita.it/bilanci-e-sfcr
[Società Reale Mutua di Assicurazioni]:https://www.realegroup.eu/IT/corporate/relazioni-e-bilanci
[Cardif Vita S.p.A.]:https://bnpparibascardif.it/notizie-e-comunicati/
[MEDIOLANUM VITA S.p.A.]:https://www.mediolanumassicurazioni.it/relazione-solvibilita-condizione-finanziaria
[Generali Italia S.p.A.]:https://www.generali.it/note-legali
[Banco BPM Vita S.p.A.]:https://www.bancobpmvita.it/chi-siamo/dati-societari/
[HDI ASSICURAZIONI S.p.A.]:https://www.hdiassicurazioni.it/it/comunicazioni-e-avvisi/assicurazioni-hdi-informativa-mercato
[Gruppo Assicurativo Poste Vita]:https://postevita.poste.it/dati-di-bilancio-di-poste-vita/
[FIDEURAM VITA S.P.A.]:https://www.fideuramvita.it/solvency-2
[CNP Vita Assicura S.p.A.]:https://www.gruppocnp.it/chi-siamo/societ%C3%A0
[ITAS VITA]:https://www.gruppoitas.it/it/dati-societari/sfcr-unico-di-gruppo
[Helvetia Vita S.p.A.]:https://www.helvetia.com/it/web/it/chi-siamo/helvetia/helvetia-in-italia/solvencyII.html
[Vittoria Assicurazioni S.p.A.]:https://www.vittoriaassicurazioni.com/investor-relations-eng/sfcr-solvency-and-financial-condition-of-group/
[GROUPAMA ASSICURAZIONI S.P.A.]:https://www.groupama.com/en/analysts/financial-publications/solvency-and-financial-condition-reports-sfcr/
[UniCredit Allianz Vita S.p.A.]:https://www.unicreditallianzvita.it/chi-siamo/governance/solvency-ii---sfcr.html
[Zurich Investments Life S.p.A.]:https://www.zurich.it/zurich-per-te/avvisi/sfcr-report
[UniCredit Life Insurance S.p.A.]:https://www.unicreditlife.it/chisiamo/solvency
[Athora Italia S.p.A.]:https://www.athora.it/chi-siamo/documenti-societari/
[Nobis Vita S.p.A.]:https://corporate.axa.it/
