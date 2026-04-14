import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def main():
    try:
        # 1. Load data
        df1 = pd.read_csv(f"./data/processed/cleaned_day1.csv")
        df2 = pd.read_csv(f"./data/processed/cleaned_day2.csv")
        
        df = pd.concat([df1, df2])

        # 2. Define Features (X) and Target (y)
        X = df.drop('label', axis=1)
        y = df['label']

        # 3. Split into Training and Testing sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Initialize and train
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # See how we did
        print("--- Confusion Matrix ---")
        print(confusion_matrix(y_test, y_pred))
        print("\n--- Classification Report ---")
        print(classification_report(y_test, y_pred))
        print("\n--- Accuracy Score ---")
        print(accuracy_score(y_test, y_pred))
        
        # Match coefficients to feature names
        importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
        print("\n--- Feature Importance ---")
        print(importance.sort_values(by='Importance', ascending=False))
        
    except FileNotFoundError:
        print("File not found.")
        
        
if __name__ == "__main__":
    main()