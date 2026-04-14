# 🌳 Training Day 2: Random Forest Model

## Objective
Train a Random Forest model to predict **"Focus" (1)** vs **"Distracted" (0)** using app usage patterns, and evaluate whether a non-linear model improves performance over Logistic Regression.

---

## Dataset
- **Raw Data:** `/data/raw/data_day1.csv`, `/data/raw/data_day2.csv`  
- **Processed Data:** `/data/processed/cleaned_day1.csv`, `/data/processed/cleaned_day2.csv`  
- **Observations:** The dataset is imbalanced, with more distraction sessions than focus sessions, though improved by combining multiple days.

---

## Process
1. **Data Loading:** Combined multiple days using `pandas.concat`.
2. **Feature Selection:**  
   - $X$ → features (app flags, duration, hour)  
   - $y$ → binary label (focus vs distracted)
3. **Data Splitting:** 80% Training / 20% Testing using `stratify=y`.
4. **Feature Scaling:** ❌ Not applied (tree-based model).
5. **Training:** Used `RandomForestClassifier` with 100 trees.
6. **Prediction:** Evaluated on unseen test data.

---

## Feature Importance

| Feature | Importance | Impact |
| :--- | :---: | :--- |
| **duration** | 0.5290 | **Primary Driver:** Session length dominates prediction |
| **is_study** | 0.2224 | Strong indicator of focus |
| **is_social** | 0.0652 | Strong distraction signal |
| **is_ai** | 0.0647 | Positive contribution to focus |
| **is_media** | 0.0438 | Negative indicator |
| **hour** | 0.0376 | Minor influence |
| **is_coding** | 0.0373 | Small positive signal |

---

## Confusion Matrix Results

| | Predicted: Distracted (0) | Predicted: Focused (1) |
| :--- | :---: | :---: |
| **Actual: Distracted (0)** | 142 (TN) | 0 (FP) |
| **Actual: Focused (1)** | 0 (FN) | 21 (TP) |

---

## Classification Report

| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **0 (Distracted)** | 1.00 | 1.00 | 1.00 | 142 |
| **1 (Focused)** | 1.00 | 1.00 | 1.00 | 21 |
| | | | | |
| **Accuracy** | | | **1.00** | 163 |
| **Macro Avg** | 1.00 | 1.00 | 1.00 | 163 |
| **Weighted Avg** | 1.00 | 1.00 | 1.00 | 163 |

---

## 🚨 Critical Observation

The model achieved **100% accuracy**, which is **extremely unusual** for real-world data.

This likely indicates:
- Possible **data leakage** (e.g., a feature directly revealing the label)
- Overfitting due to:
  - small dataset size  
  - highly predictable patterns  
- Duplicate or overly similar data between train and test sets

---

## Conclusion & Insights

- The model perfectly separates "Focus" vs "Distracted" sessions.
- **duration (52.9%)** is by far the most important feature.
- **is_study (22.2%)** strongly reinforces focus prediction.
- Behavioral features (social/media) correctly act as negative signals.

However:

> ⚠️ This performance is likely **too good to be true** and should not be trusted without further validation.

---

## Next Steps

- ✅ Verify no **data leakage**
- 🔁 Test on a completely **unseen day (Day 3)**
- 📉 Use **cross-validation**
- 🎯 Try **Gradient Boosting** for comparison
- 🧠 Improve features:
  - session transitions  
  - time-based patterns  
  - streaks / consistency  

---

## Code for Random Forest Model

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def main():
    try:
        # Load data
        df1 = pd.read_csv(f"./data/processed/cleaned_day1.csv")
        df2 = pd.read_csv(f"./data/processed/cleaned_day2.csv")
        df = pd.concat([df1, df2])

        # Features and target
        X = df.drop('label', axis=1)
        y = df['label']

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        # Train
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Evaluate
        print("--- Confusion Matrix ---")
        print(confusion_matrix(y_test, y_pred))

        print("\n--- Classification Report ---")
        print(classification_report(y_test, y_pred))

        print("\n--- Accuracy Score ---")
        print(accuracy_score(y_test, y_pred))

        # Feature importance
        importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        })

        print("\n--- Feature Importance ---")
        print(importance.sort_values(by='Importance', ascending=False))

    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    main()
```