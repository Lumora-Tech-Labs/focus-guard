import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

def main(day_number):
    file_path = f"./data/processed/cleaned_day{day_number + 1}.csv"
    try:
        # 1. Load data
        df = pd.read_csv(file_path)

        # 2. Define Features (X) and Target (y)
        X = df.drop('label', axis=1)
        y = df['label']

        # 3. Split into Training and Testing sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Initialize and train
        model = LogisticRegression(class_weight="balanced")
        model.fit(X_train_scaled, y_train)

        # Make predictions
        y_pred = model.predict(X_test_scaled)

        # See how we did
        print("--- Confusion Matrix ---")
        print(confusion_matrix(y_test, y_pred))
        print("\n--- Classification Report ---")
        print(classification_report(y_test, y_pred))
        
        # Match coefficients to feature names
        importance = pd.DataFrame({'Feature': X.columns, 'Weight': model.coef_[0]})
        print(importance.sort_values(by='Weight', ascending=False))
            
    except FileNotFoundError:
        print("File not found.")
        
        
if __name__ == "__main__":
    main(day_number=0)