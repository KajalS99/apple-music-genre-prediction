# Apple Music Genre Prediction — Metadata-Only Case Study

This repository packages the exact notebook you worked on with a clean, industry-style structure. Figures below are exported directly from the notebook (no placeholders).

## Dataset and Goal
- ~10,000 Apple Music tracks, target: `primaryGenreName`
- Predict genre using metadata only (duration, year, price, explicitness, isStreamable)

## Data Prep & Feature Engineering
- `releaseYear` from `releaseDate`
- `trackDurationMinutes` from `trackTimeMillis`
- Median imputation for prices (and `trackPrice_missing` indicator)
- Map `isStreamable` to boolean/int
- One-hot encode `trackExplicitness`
- Drop high-cardinality text/IDs, filter rare classes (≥ 15 in train)
- Stratified split with fixed seed

**Notebook-reported shapes:**
- X_train: (6983, 11)
- Retained classes: 20
- Train samples after filtering: 6849

## Models and Results (test set)
| Model         | Accuracy | F1 (Macro) | ROC AUC (Macro) |
|---------------|:--------:|:----------:|:---------------:|
| Random Forest | 0.811 | 0.82 | — |
| Extra Trees   | 0.8036 | 0.82 | — |
| **XGBoost**   | **0.83** | **0.83** | **0.98** |

Additional details:
- XGBoost Precision ≈ 0.88, Recall ≈ 0.80
- Extra Trees Macro Precision ≈ 0.84, Macro Recall ≈ 0.81

## Figures (exported from notebook)
![Histogram](images/histogram_01.png)
![Histogram](images/histogram_02.png)
![Bar Plot](images/barplot_03.png)
![Histogram](images/histogram_04.png)
![Figure](images/figure_05.png)
![Figure](images/figure_06.png)
![Heatmap](images/heatmap_07.png)
![Figure](images/figure_08.png)
![Bar Plot](images/barplot_09.png)
![Figure](images/figure_10.png)
![Confusion Matrix](images/confusion_matrix_11.png)
![Confusion Matrix](images/confusion_matrix_12.png)
![Confusion Matrix](images/confusion_matrix_13.png)
![Bar Plot](images/barplot_14.png)
![ROC Curve](images/roc_15.png)
![ROC Curve](images/roc_16.png)
![Heatmap](images/heatmap_17.png)

## How to Run
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/AppleMusicGenrePrediction.ipynb
```

## Structure
```
.
├── data/
├── images/
├── notebooks/
│   └── AppleMusicGenrePrediction.ipynb
├── scripts/
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Author
Kajal Singh — Post-Degree Diploma in Data Analytics, Douglas College
License: MIT
