"""
COVID Data Cleaning Script
Cleans COVID_DATA.xlsx for binary classification: predict Result (positive/negative).

Run from anywhere:
  python src/clean_covid_data.py
(from project root)
"""
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
XLSX_PATH = DATA_DIR / "COVID_DATA.xlsx"
OUT_PATH = DATA_DIR / "COVID_DATA_cleaned.csv"

# Load data (first sheet)
print(f"Loading {XLSX_PATH}...")
df = pd.read_excel(XLSX_PATH, sheet_name=0)
print(f"Original shape: {df.shape}")

# 1. Drop rows with missing Age_60_And_Above or Sex
df_clean = df.dropna(subset=["Age_60_And_Above", "Sex"]).copy()
dropped = len(df) - len(df_clean)
print(f"Dropped {dropped} rows with missing Age_60_And_Above or Sex. Shape: {df_clean.shape}")

# 2. Encode categorical columns for modeling
# Age_60_And_Above: Yes -> 1, No -> 0
df_clean["Age_60_And_Above"] = (df_clean["Age_60_And_Above"].str.strip().str.lower() == "yes").astype(int)

# Sex: female -> 0, male -> 1 (arbitrary; can flip)
df_clean["Sex"] = (df_clean["Sex"].str.strip().str.lower() == "male").astype(int)

# Result (target): positive -> 1, negative -> 0
df_clean["Result"] = (df_clean["Result"].str.strip().str.lower() == "positive").astype(int)

# 3. Ensure symptom/contact columns are int (they already are 0/1)
for col in ["Cough", "Fever", "Sore_Throat", "Shortness_Of_Breath", "Headache", "Contact"]:
    df_clean[col] = df_clean[col].astype(int)

print("\nCleaned data sample:")
print(df_clean.head())
print("\nResult distribution (cleaned):")
print(df_clean["Result"].value_counts())
print("\nDtypes:")
print(df_clean.dtypes)
print("\nNull counts (should be 0):")
print(df_clean.isnull().sum())

# Save cleaned data for modeling
df_clean.to_csv(OUT_PATH, index=False)
print(f"\nCleaned data saved to {OUT_PATH}")

# Optional: stratified train/test split
from sklearn.model_selection import train_test_split

X = df_clean.drop(columns=["Result"])
y = df_clean["Result"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")
print("Train Result % positive:", y_train.mean() * 100)
print("Test Result % positive:", y_test.mean() * 100)
