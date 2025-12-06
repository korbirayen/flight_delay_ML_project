"""
Train the Decision Tree model and export all necessary files for the Flask API
Run this script first before starting the Flask server
"""

import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

print("Loading dataset...")
df = pd.read_csv('Flight_delay.csv')

print("Preprocessing data...")
# Select relevant columns
df = df[['DayOfWeek','Date','DepTime','ArrTime','CRSArrTime','Airline','Origin','Dest',
         'CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']]

# Create delay target variable (delay > 30 minutes)
delay_cols = ["CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"]
df["Delay"] = (df[delay_cols].sum(axis=1) > 30).astype(int)
df = df.drop(columns=delay_cols)

# Parse date
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df['month'] = df['Date'].dt.month
df['day'] = df['Date'].dt.day
df = df.drop(columns=['Date'])

# Save the original categorical values before encoding
airlines_list = sorted(df['Airline'].unique().tolist())
origins_list = sorted(df['Origin'].unique().tolist())
dests_list = sorted(df['Dest'].unique().tolist())

print(f"Found {len(airlines_list)} airlines")
print(f"Found {len(origins_list)} origin airports")
print(f"Found {len(dests_list)} destination airports")

# One-hot encode categorical features
df_encoded = pd.get_dummies(df, dtype=int)

# Split features and target BEFORE scaling
X = df_encoded.drop(columns=['Delay'])
y = df_encoded['Delay']

# Scale numerical features (only on X, not the target)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

print(f"Total features after encoding: {len(X.columns)}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train Decision Tree model (with max_depth to speed up training)
print("\nTraining Decision Tree model...")
clf = DecisionTreeClassifier(random_state=1, max_depth=20)
clf.fit(X_train, y_train)

# Evaluate model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)')

# Save all necessary data in ONE pickle file
print("\nSaving model and preprocessing objects...")

model_data = {
    'model': clf,
    'scaler': scaler,
    'feature_columns': X.columns.tolist(),
    'model_info': {
        'airlines': airlines_list,
        'origins': origins_list,
        'destinations': dests_list,
        'accuracy': accuracy,
        'year': 2019  # Dataset year
    }
}

with open('flight_delay_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("[OK] All data saved in: flight_delay_model.pkl")

print("\n" + "="*50)
print("SUCCESS! Model exported.")
print("="*50)
print("\nYou can now run: python app.py")
