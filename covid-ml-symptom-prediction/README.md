# COVID Symptom & Demographics — ML Prediction

**By [@matthewkennedy22](https://github.com/matthewkennedy22)**

End-to-end machine learning project on **binary COVID test prediction** (positive vs negative) using symptoms, known contact, age 60+, and sex. The pipeline covers data cleaning for **~1M rows**, severe **class imbalance** (~10% positive), and **ensemble models** with threshold tuning for sensitivity vs precision tradeoffs.

---

## What’s in this repo

| Path | Contents |
|------|----------|
| `data/` | `COVID_DATA.xlsx` (raw), `COVID_DATA_cleaned.csv` (cleaned for modeling), and `data/README.md`. |
| `notebooks/` | Random Forest, Histogram Gradient Boosting, XGBoost, agglomerative clustering, and a variant RF notebook without age/sex. |
| `src/` | `clean_covid_data.py` — loads Excel, drops incomplete rows, encodes categoricals, writes cleaned CSV. |
| `docs/` | Data cleaning guide, ensemble-learning findings (Markdown + HTML), report PDF (`COVID_Data_Mining_Project_Report.pdf`). |

---

## Quick start

From the **project root** (`covid-ml-symptom-prediction/`):

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Regenerate cleaned data (requires `data/COVID_DATA.xlsx`):

```bash
python src/clean_covid_data.py
```

Open notebooks (paths assume you run Jupyter with working directory = `notebooks/` or open cells as-is — data is loaded via `../data/...`):

```bash
cd notebooks && jupyter notebook
```

---

## Methods (summary)

- **Cleaning:** Drop rows with missing `Age_60_And_Above` or `Sex`; encode Yes/No and male/female and positive/negative to numeric; keep duplicate rows to preserve prevalence (see `docs/COVID_Data_Cleaning_Guide.md`).
- **Models:** Randomized hyperparameter search on stratified samples; refit on full training set; evaluation with **AUC**, **F1** / **Fβ**, sensitivity, specificity, and threshold sweeps.
- **Clustering:** Exploratory agglomerative clustering on the cleaned feature space (`notebooks/COVID_Agglomerative_Clustering.ipynb`).

Detailed metrics and interpretation: **`docs/Ensemble_Learning_Findings.md`**.

---

## Tech stack

Python, pandas, scikit-learn, XGBoost, Jupyter, openpyxl

---

## GitHub

Push this folder as its own repository (suggested name: `covid-ml-symptom-prediction`) so it matches your other portfolio repos.

**Note:** `data/` contains large files (~50MB combined). GitHub allows files under 100MB; if you prefer a smaller clone, consider [Git LFS](https://git-lfs.github.com/) or hosting the Excel/CSV elsewhere and documenting the download in `data/README.md`.
