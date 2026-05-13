# SFCR Table Extraction - Italian Life Insurance Market

## Overview
This project extracts and structures Solvency and Financial Condition Report (SFCR) data from PDFs using Mistral OCR and Pydantic schemas.

Current table categories processed by `main.py`:
- `S_02_01_02 – Balance sheet`
- `S_23_01_01 – Own funds`
- `S_25_01_21 – Solvency Capital Requirement – for undertakings on Standard Formula`

The original implementation was developed in Jupyter Notebook and is being incrementally refactored into a modular Python codebase.
Core Python source files are organized under `Code/`.

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

### 5) Run the pipeline
```powershell
python Code/main.py
```

Final aggregated tables are written to `Output/`. 

Produced tables are then manually checked against the pdf-s and saved into `output_final`.

Note that previously the final folder was `Final_output`. Therefore for legacy reasons it is kept as a duplicate copy of `Output_final`.

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
[Società Reale Mutua di Assicurazioni]:https://www.realegroup.eu/EN/corporate/reports-and-financial-statements
[Cardif Vita S.p.A.]:https://bnpparibascardif.it/notizie-e-comunicati/
[MEDIOLANUM VITA S.p.A.]:https://www.mediolanumassicurazioni.it/relazione-solvibilita-condizione-finanziaria
[Generali Italia S.p.A.]:https://www.generali.it/note-legali
[Banco BPM Vita S.p.A.]:https://www.bancobpmvita.it/dati-societari/
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
