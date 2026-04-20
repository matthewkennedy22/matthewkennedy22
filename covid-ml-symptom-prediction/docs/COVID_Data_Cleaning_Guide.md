# COVID Data Cleaning Guide — Predict Whether a Patient Has COVID

## Data overview

| Item | Value |
|------|--------|
| **Rows** | 1,030,724 |
| **Columns** | 9 |
| **Target** | `Result` (positive / negative) |

### Columns

| Column | Type | Values | Notes |
|--------|------|--------|--------|
| Cough | int | 0, 1 | Binary symptom |
| Fever | int | 0, 1 | Binary symptom |
| Sore_Throat | int | 0, 1 | Binary symptom |
| Shortness_Of_Breath | int | 0, 1 | Binary symptom |
| Headache | int | 0, 1 | Binary symptom |
| Age_60_And_Above | object | "Yes", "No" | **50,988 nulls (~5%)** |
| Sex | object | "male", "female" | **2,601 nulls (~0.25%)** |
| Contact | int | 0, 1 | Binary (contact with case) |
| Result | object | "positive", "negative" | **Target — no nulls** |

---

## Issues and how to clean them

### 1. Missing values

- **Age_60_And_Above:** 50,988 nulls  
- **Sex:** 2,601 nulls  

**Options:**

- **Option A (recommended for large data):** Drop rows with missing values.  
  You still have ~977k rows; loss is small relative to size.
- **Option B:** Impute:
  - **Age_60_And_Above:** Mode ("No") or a separate "Unknown" category.
  - **Sex:** Mode or "Unknown" category.
- **Option C:** Use only complete rows for modeling and document that ~5% of records were excluded.

### 2. Duplicate rows

- **1,030,088** rows are exact duplicates (same values in all 9 columns).
- After `drop_duplicates()` you get **636 unique feature combinations** (with ~368 positive, ~268 negative in that deduped set).

**Options:**

- **Option A (recommended for “real” prevalence):** **Keep duplicates.**  
  Duplicates reflect how often each symptom profile appears; the 90% negative / 10% positive ratio is meaningful. Clean only missing values, then train on the full (or missing-dropped) dataset.
- **Option B (explore patterns):** **Use deduped data** (636 rows) for EDA and maybe for a small model. Be aware: this is a tiny sample and class balance in this subset is not the same as in the full data.

For a class project, **keeping duplicates and dropping rows with missing Age_60_And_Above or Sex** is a good default.

### 3. Categorical encoding for modeling

- **Age_60_And_Above:** "Yes" / "No" → map to **1 / 0** (or use a label encoder).
- **Sex:** "male" / "female" → **0/1** or one-hot (e.g. `Female=0`, `Male=1`).
- **Result (target):** "positive" / "negative" → **1 / 0** (e.g. positive = 1) for binary classification.

### 4. Class imbalance

- **Negative:** 925,290 (~90%)  
- **Positive:** 105,434 (~10%)  

**Options:**

- Use **stratified train/test split** so both sets have similar positive rate.
- In the model: **class_weight='balanced'** (e.g. in scikit-learn) or **scale_pos_weight** in XGBoost.
- Optionally: oversample minority (e.g. SMOTE) or undersample majority — only if you need it after trying balanced weights.

### 5. No issues found

- Symptom and Contact columns are already 0/1.
- Result has no nulls.
- No obvious invalid values (e.g. only 0/1 where expected).

---

## Recommended cleaning steps (summary)

1. **Load data** from `data/COVID_DATA.xlsx` (first sheet).
2. **Drop rows** where `Age_60_And_Above` or `Sex` is null (optional: impute instead; see above).
3. **Encode:**
   - `Age_60_And_Above`: Yes → 1, No → 0  
   - `Sex`: e.g. female → 0, male → 1  
   - `Result`: positive → 1, negative → 0  
4. **Keep duplicate rows** (do not deduplicate) so the model sees the true class distribution.
5. **Split:** stratified by `Result` for train/test (and validation if needed).

After cleaning you’ll have one dataframe ready for feature matrix `X` and target `y` for predicting whether a patient has COVID. The script writes `data/COVID_DATA_cleaned.csv`.
