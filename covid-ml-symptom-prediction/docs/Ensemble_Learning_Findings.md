# COVID Ensemble Learning Models: Findings Summary

This document summarizes the setup, results, and conclusions from three ensemble-learning notebooks for binary COVID prediction (Result: positive vs negative) using symptoms and demographics on the cleaned COVID dataset.

---

## 1. Shared Context

- **Data:** `data/COVID_DATA_cleaned.csv` — symptoms (Cough, Fever, Sore_Throat, Shortness_Of_Breath, Headache), demographics (Age_60_And_Above, Sex, Contact), and target **Result**.
- **Split:** 60% train / 40% test, stratified, `random_state=321`.  
  - Train: **587,095** rows | Test: **391,398** rows.
- **Class imbalance:** ~90% negative, ~10% positive. Accuracy alone is misleading; tuning and evaluation use F1/Fβ, sensitivity, specificity, and AUC.
- **Tuning strategy:** All models tune on a **60k stratified sample** for speed, then the best estimator is **refit on the full training set** and evaluated on the held-out test set.

---

## 2. Model Setup and Tuning

| Aspect | Random Forest | HistGradientBoosting | XGBoost |
|--------|----------------|----------------------|---------|
| **Tuning search** | RandomizedSearchCV | RandomizedSearchCV | RandomizedSearchCV |
| **Candidates** | 30 | 30 | 30 |
| **CV** | 5-fold | 3-fold | 3-fold |
| **Scoring** | F1 | Fβ (β=2) | Fβ (β=2) |
| **Imbalance** | `class_weight='balanced'` | — | `scale_pos_weight` from data |

- **F1** (Random Forest): balances precision and recall equally.  
- **Fβ with β=2** (HistGB, XGBoost): favors **recall** over precision, suitable for “catch more cases” with some control on false positives.

---

## 3. Random Forest

- **Best F1 params (from run):**  
  `n_estimators=200`, `min_samples_split=50`, `min_samples_leaf=5`, `max_features='sqrt'`, `max_depth=8`.

### Threshold sweep (test set)

Lower thresholds increase recall and false positives; higher thresholds increase precision and false negatives.

| Threshold | Recall | Precision | FP     | FN     |
|-----------|--------|-----------|--------|--------|
| 0.300     | 0.794  | 0.156     | 176,591| 8,492  |
| 0.350     | 0.794  | 0.156     | 176,591| 8,492  |
| 0.355     | 0.576  | 0.393     | 36,742 | 17,472 |
| 0.360     | 0.576  | 0.393     | 36,742 | 17,472 |
| 0.365     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.370     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.375     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.380     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.400     | 0.542  | 0.599     | 14,917 | 18,888 |

### Evaluation at chosen threshold (e.g. t = 0.355)

| Metric | Value |
|--------|--------|
| Accuracy | 0.8615 |
| Sensitivity (recall positive) | 0.576 |
| Specificity (recall negative) | 0.895 |
| **AUC** | **0.7695** |

### Feature importance (Gini)

1. **Contact** (~0.51)  
2. Fever (~0.16)  
3. Headache (~0.15)  
4. Cough (~0.10)  
5. Sore_Throat (~0.05)  
6. Shortness_Of_Breath (~0.01)  
7. Sex (~0.01)  
8. Age_60_And_Above (~0.001)  

**Contact** is by far the strongest predictor; symptoms and demographics add smaller contributions.

---

## 4. Histogram Gradient Boosting

- Tuned for **Fβ (β=2)**; early stopping and validation fraction used in training.

### Threshold sweep (test set)

| Threshold | Recall | Precision | FP    | FN     |
|-----------|--------|-----------|-------|--------|
| 0.300     | 0.526  | 0.629     | 12,791| 19,536 |
| 0.350     | 0.526  | 0.629     | 12,791| 19,536 |
| 0.355     | 0.526  | 0.629     | 12,791| 19,536 |
| 0.360     | 0.526  | 0.629     | 12,791| 19,536 |
| 0.365     | 0.516  | 0.637     | 12,142| 19,936 |
| 0.370     | 0.511  | 0.641     | 11,766| 20,159 |
| 0.375     | 0.511  | 0.641     | 11,766| 20,159 |
| 0.380     | 0.509  | 0.643     | 11,638| 20,248 |
| 0.400     | 0.509  | 0.643     | 11,638| 20,248 |
| 0.450     | 0.509  | 0.643     | 11,638| 20,248 |
| 0.500     | 0.407  | 0.697     | 7,283 | 24,440 |

HistGB tends to give more conservative probability estimates (less extreme recall at low thresholds) and higher precision at similar recall.

### Evaluation at chosen threshold (e.g. THRESHOLD = 0.36)

| Metric | Value |
|--------|--------|
| Accuracy | 0.9185 |
| Sensitivity (recall positive) | 0.509 |
| Specificity (recall negative) | 0.967 |
| **AUC** | **0.7695** |

### Feature importance (permutation, 30k test sample)

1. **Contact** (~0.032)  
2. Headache (~0.021)  
3. Sore_Throat (~0.009)  
4. Fever (~0.005)  
5. Shortness_Of_Breath (~0.002)  
6. Age_60_And_Above (~0.001)  
7. Cough (~0.001)  
8. Sex (slightly negative)  

**Contact** again leads; order and magnitudes differ from RF (permutation importance is on a different scale and sample).

---

## 5. XGBoost

- Tuned for **Fβ (β=2)**; `scale_pos_weight` set from training class ratio for imbalance.

### Threshold sweep (test set)

| Threshold | Recall | Precision | FP     | FN     |
|-----------|--------|-----------|--------|--------|
| 0.300     | 0.794  | 0.156     | 176,591| 8,492  |
| 0.350     | 0.794  | 0.156     | 176,591| 8,492  |
| 0.355     | 0.576  | 0.393     | 36,742 | 17,472 |
| 0.360     | 0.576  | 0.393     | 36,742 | 17,472 |
| 0.365     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.370     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.375     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.380     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.400     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.450     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.500     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.550     | 0.542  | 0.599     | 14,917 | 18,888 |
| 0.600     | 0.542  | 0.599     | 14,917 | 18,888 |

XGBoost can reach high recall at low thresholds but at the cost of many false positives. At **t = 0.37** recall and precision are balanced (0.54 / 0.60).

### Evaluation at chosen threshold (THRESHOLD = 0.37)

| Metric | Value |
|--------|--------|
| Accuracy | 0.9135 |
| Sensitivity (recall positive) | 0.542 |
| Specificity (recall negative) | 0.957 |
| **AUC** | **0.7695** |

At **threshold 0.37** XGBoost is run in a more balanced regime: sensitivity 0.54, specificity 0.96, and accuracy 0.91, with fewer false positives than at very low thresholds.

### Feature importance (gain-style)

1. **Contact** (~0.55)  
2. Headache (~0.17)  
3. Fever (~0.15)  
4. Cough (~0.06)  
5. Sore_Throat (~0.04)  
6. Shortness_Of_Breath (~0.02)  
7. Sex (~0.01)  
8. Age_60_And_Above (~0.003)  

Again **Contact** dominates; ordering is similar to Random Forest.

---

## 6. Cross-Model Comparison

| Model | AUC | Accuracy (at chosen t) | Sensitivity | Specificity | Operating point |
|-------|-----|------------------------|-------------|-------------|------------------|
| Random Forest | 0.7695 | 0.86 | 0.58 | 0.90 | t ≈ 0.355, balanced |
| HistGradientBoosting | 0.7695 | 0.92 | 0.51 | 0.97 | t = 0.36, precision-oriented |
| XGBoost | 0.7695 | 0.91 | 0.54 | 0.96 | t = 0.37, balanced |

- **AUC is the same (0.7695)** across all three models — discrimination ability is comparable; differences are in **where** each model is run (threshold choice) and how probability distributions behave.
- **Random Forest** at t≈0.355 gives a middle ground: moderate sensitivity, good specificity, high accuracy.
- **HistGradientBoosting** at t=0.36 is the most precision- and specificity-heavy: fewer false positives, fewer positives predicted overall.
- **XGBoost** at t=0.37 gives a balanced operating point: sensitivity 0.54, specificity 0.96, accuracy 0.91 (see threshold sweep table for other options, e.g. lower t for higher recall).

For a **hospital with limited space**, the threshold sweep in each notebook allows choosing a point that balances “catching cases” (recall) vs “not over-admitting” (precision/specificity). No single threshold fits all; the same model can be used at different thresholds for different policies.

---

## 7. Feature Importance: Consistency Across Models

- **Contact** is the dominant predictor in all three models (RF, HistGB permutation, XGBoost).  
- **Fever, Headache, Cough** are next most important in RF and XGBoost; HistGB’s permutation order differs but still highlights Contact and Headache.  
- **Shortness_Of_Breath, Sex, Age_60_And_Above** have smaller (or minimal) importance in these runs.

This supports that **known contact** is the strongest single feature in this dataset for predicting positive COVID result, with symptoms and demographics adding secondary signal.

---

## 8. Conclusions and Next Steps

1. **Discrimination (AUC)** is equivalent across the three ensembles (~0.77); choice among them can be driven by interpretability, speed, or desired probability/calibration behavior rather than AUC.
2. **Threshold choice** is critical: the same model can be run at a higher threshold (fewer admissions, higher precision) or lower threshold (more cases caught, lower precision). The notebooks’ threshold sweeps support this decision.
3. **Contact** is the most important predictor; collection and quality of contact history should be prioritized. Symptoms and demographics still add value for prediction and interpretation.
4. **Next steps to consider:**  
   - Try other operating points (e.g. fix a target recall and choose threshold to meet it).  
   - Compare calibration (reliability diagrams) across the three models.  
   - If needed, explore resampling (e.g. SMOTE) or class weights further to improve recall without excessive false positives.  
   - Validate on a separate time period or geography if available.  
   - Consider logistic regression or simpler models for interpretability and comparison.

---

*Summary derived from: `notebooks/COVID_Random_Forest_Analysis.ipynb`, `notebooks/COVID_HistGradientBoosting_Analysis.ipynb`, and `notebooks/COVID_XGBoost_Analysis.ipynb`.*
