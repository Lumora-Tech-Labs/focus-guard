# Training Day 1: Logistic Regression Baseline

## Objective
Train a Logistic Regression model to predict "Focus" (1) vs "Distracted" (0) based on app usage patterns.

## Dataset
- **Raw Data:** [raw data](/data/raw/data_day1.csv)
- **Processed Data:** [processed data](/data/processed/data_day1.csv)
- **Observations:** The dataset contains a high number of distractions (67) relative to focus sessions (7), indicating a significant class imbalance.

## Process
1. **Data Loading:** Read from CSV using `pandas.read_csv`.
2. **Feature Selection:** $X$ holds features (app flags, duration, hour), and $y$ holds the binary label.
3. **Data Splitting:** 80% Training / 20% Testing split.
4. **Feature Scaling:** Applied `StandardScaler` to normalize the data. This is crucial because `duration` (0-2000+) and `is_study` (0-1) exist on completely different scales.
5. **Handling Imbalance:** Initialized `LogisticRegression(class_weight="balanced")`. This forces the model to treat the rare "Focus" sessions with higher priority.
6. **Training:** Fit the model to the scaled training data.
7. **Prediction:** Evaluated performance on the unseen test set.

## Feature Importance (Weights)
These weights represent the "logic" the model learned. Positive values increase the probability of a "Focus" label.

| Feature | Weight | Impact |
| :--- | :---: | :--- |
| **duration** | 2.9252 | **Primary Driver:** The longer the session, the higher the focus probability. |
| **is_study** | 2.0263 | **Secondary Driver:** Strong correlation with productivity. |
| **is_ai** | 0.9359 | Positive impact on focus. |
| **is_coding** | 0.6229 | Moderate positive impact. |
| **hour** | 0.0666 | Negligible impact for this dataset. |
| **is_media** | -0.3954 | Negative driver (Predicts distraction). |
| **is_social** | -0.6647 | Strongest negative driver. |

## Confusion Matrix Results
| | Predicted: Distracted (0) | Predicted: Focused (1) |
| :--- | :---: | :---: |
| **Actual: Distracted (0)** | 60 (TN) | 7 (FP) |
| **Actual: Focused (1)** | 0 (FN) | 7 (TP) |

**Analysis:** The model is currently biased towards "Focused." It has zero False Negatives (perfect recall), but it struggles with False Positives (7 false alarms).

## Classification Report
| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **0 (Distracted)** | 1.00 | 0.90 | 0.94 | 67 |
| **1 (Focused)** | 0.50 | 1.00 | 0.67 | 7 |
| | | | | |
| **Accuracy** | | | **0.91** | 74 |
| **Macro Avg** | 0.75 | 0.95 | 0.81 | 74 |
| **Weighted Avg** | 0.95 | 0.91 | 0.92 | 74 |

## Conclusion & Insights
The model is able to catch **all** focused sessions (**100% Recall**). However, it wrongly flags a session as focused approximately 50% of the time (**0.50 Precision**). 

**Next Steps:** - The current linear model struggles to distinguish between "Short Study" (Distraction) and "Long Study" (Focus). 
- I will explore **Random Forest** in Day 2 to see if non-linear decision trees can reduce the False Positive rate.