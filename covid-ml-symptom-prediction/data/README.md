# Data

| File | Description |
|------|-------------|
| `COVID_DATA.xlsx` | Original spreadsheet (~1M+ rows, symptoms + demographics + test result). |
| `COVID_DATA_cleaned.csv` | Cleaned, encoded dataset after running `src/clean_covid_data.py` (missing Age/Sex dropped; labels binarized). |

Notebooks under `notebooks/` load these files via `../data/...`.

If you clone without the raw Excel file, regenerate the CSV from your own copy of `COVID_DATA.xlsx` and place it in this folder.
