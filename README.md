# Apple Music Genre Prediction (Metadata-Only)

Predicting a track’s **primary genre** using **metadata only** (no audio features). This project demonstrates a clean analytics-to-ML workflow suitable for junior data analyst roles: data preparation, exploratory analysis, feature engineering, model benchmarking, and clear reporting with reproducible steps.

## Project Overview

Music platforms need reliable genre tags for search, recommendations, and catalog hygiene. Audio features can be expensive to compute at scale. This project evaluates how far genre prediction can go using readily available **metadata** such as duration, release year, explicitness, and price.

- Problem type: Multi-class classification  
- Target: `primaryGenreName`  
- Scope: Metadata-only features; no raw audio or embeddings

---

## Dataset Card

- **Source:** Apple Music Dataset — 10,000 Tracks Uncovered  
  https://www.kaggle.com/datasets/kanchana1990/apple-music-dataset-10000-tracks-uncovered
- **Records:** ~10,000 tracks
- **Target column:** `primaryGenreName`
- **Representative features used:**
  - Prices: `trackPrice`, `collectionPrice`
  - Time: `trackTimeMillis` → engineered `trackDurationMinutes`
  - Date: `releaseDate` → engineered `releaseYear`
  - Flags: `trackExplicitness` (one-hot), `isStreamable` (boolean)
- **Data access:** Raw dataset is **not** stored in this repo (licensing/size). Place your CSV under `data/raw/` locally.

---

## Data Preparation & Cleaning

The following steps are applied in the notebook before modeling:

1. **Invalid/missing values**
   - `collectionPrice == -1` → `NaN` then imputed (median)
   - `trackPrice_missing` indicator; median imputation for `trackPrice`
2. **Type normalization**
   - `isStreamable`: map `"true"/"false"` → boolean → integer
3. **Feature engineering**
   - `trackDurationMinutes = trackTimeMillis / 60000`
   - `releaseYear = year(releaseDate)` (robust datetime parsing)
   - One-hot encode `trackExplicitness`
4. **Feature reduction**
   - Drop high-cardinality text/ID columns (names, URLs, IDs)
5. **Scaling**
   - Standardize numeric features (after split if using pipelines)
6. **Target refinement**
   - Keep only genres with ≥ 15 training samples (to stabilize metrics)
7. **Split**
   - Stratified train/test (80/20), fixed random seed

**Notebook-reported shapes (after preprocessing):**
- `X_train`: **(6983, 11)**
- Retained classes: **20**
- Training samples after filtering: **6849**

---

## Exploratory Data Analysis (Selected)

- **Distributions**: Track prices cluster around common retail points (≈ $0.99–$1.29); track duration centers at ≈ 3–4 minutes with a long tail.
- **Class balance**: A small number of genres dominate the catalog; minority classes have far fewer samples.
- **Correlations**: Price- and time-related features show mild correlation patterns and skew; explicitness and streamability behave as useful categorical flags.

Figures extracted from the notebook (representative set):

- `images/histogram_01.png`, `images/histogram_02.png`, `images/histogram_04.png`  
- `images/heatmap_07.png`, `images/heatmap_17.png`  
- `images/barplot_03.png`, `images/barplot_09.png`, `images/barplot_14.png`

---

## Modeling & Evaluation

Three supervised models were trained on the processed data with a stratified 80/20 split:

- Random Forest Classifier  
- Extra Trees Classifier  
- XGBoost Classifier

**Test-set results (from the notebook):**

| Model                    | Accuracy | Macro F1 | Weighted F1 | Macro ROC AUC |
|--------------------------|:--------:|:--------:|:-----------:|:-------------:|
| Random Forest            | 0.8112   | 0.79     | 0.81        | —             |
| Extra Trees              | 0.8036   | 0.81     | 0.80        | —             |
| **XGBoost**              | **0.8263** | **0.83** | **0.83**   | **≈ 0.98**    |

Additional details observed in the notebook:
- XGBoost: Precision ≈ 0.88, Recall ≈ 0.80  
- Extra Trees: Macro Precision ≈ 0.84, Macro Recall ≈ 0.81

Visual evaluations (exported from the notebook):
- Confusion matrices: `images/confusion_matrix_11.png`, `images/confusion_matrix_12.png`, `images/confusion_matrix_13.png`
- Macro ROC curves: `images/roc_15.png`, `images/roc_16.png`

**Interpretation:**  
XGBoost delivered the best overall balance of accuracy and macro-averaged F1, and the strongest ranking power (macro ROC AUC). Random Forest and Extra Trees provided consistent baselines.

---

## Key Insights & Learnings

- Metadata is surprisingly effective: Without audio features, the model attains ~0.83 accuracy and high macro AUC, showing practical utility for cold-start or low-compute scenarios.
- Class imbalance matters: Minority genres lag in per-class metrics; consider resampling (SMOTE), class-weighting, or threshold tuning for better macro performance.
- Feature quality & business context: Duration and year contribute signal, but can reflect catalog/market effects. Incorporating richer features (e.g., audio embeddings) would likely boost minority-genre performance.

---

## Future Work

- Hyperparameter search for XGBoost (e.g., `max_depth`, `n_estimators`, `subsample`)
- Class-balancing strategies (SMOTE, class weights), calibration, and threshold tuning
- Packaging the pipeline into reusable scripts/CLI and adding basic unit tests

---

## Technical Stack

- Python, Jupyter Notebook  
- Pandas, NumPy, SciPy  
- Matplotlib, Seaborn (visualization)  
- scikit-learn (preprocessing, models, metrics)  
- XGBoost (gradient boosting classifier)  
- GitHub (version control and publishing)

---

## Repository Structure

```
.
├── data/                     # (empty; raw data not tracked; keep CSV under data/raw/)
│   └── .gitkeep
├── images/                   # exported figures from the notebook (histograms, heatmaps, ROC, confusion matrices)
├── notebooks/
│   └── AppleMusicGenrePrediction.ipynb
├── scripts/
│   └── preprocess.py         # optional helper for reproducible cleaning outside the notebook
├── .gitignore
├── LICENSE                   # MIT
├── README.md
└── requirements.txt
```

---

## How to Reproduce

1) Create and activate a virtual environment  
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
```

2) Install dependencies  
```bash
pip install -r requirements.txt
```

3) Download the dataset from Kaggle and place it locally (not in git), for example:  
`data/raw/apple_music_dataset.csv`

4) Open and run the notebook  
```bash
jupyter notebook notebooks/AppleMusicGenrePrediction.ipynb
```

Update the path to your CSV at the top of the notebook if needed.

---

## Author

**Kajal Singh** — Post-Degree Diploma in Data Analytics, Douglas College  
This project was completed as part of the Post-Degree Diploma in Data Analytics program at Douglas College.  
License: MIT (see `LICENSE`)
