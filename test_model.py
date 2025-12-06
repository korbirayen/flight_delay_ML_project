import pickle
import pandas as pd
import numpy as np

# Load model
with open('flight_delay_model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    scaler = model_data['scaler']
    feature_columns = model_data['feature_columns']

# Test case: High-risk delayed flight
test_data = {
    'DayOfWeek': [5],  # Friday
    'DepTime': [1830],  # 6:30 PM
    'ArrTime': [2100],  # 9:00 PM
    'CRSArrTime': [2100],
    'Airline': ['American Eagle Airlines Inc.'],
    'Origin': ['ORD'],
    'Dest': ['EWR'],
    'month': [12],
    'day': [15]
}

df_input = pd.DataFrame(test_data)
print("Input data:")
print(df_input)

# One-hot encode
df_encoded = pd.get_dummies(df_input, dtype=int)

# Align with training features
missing_cols = set(feature_columns) - set(df_encoded.columns)
if missing_cols:
    missing_df = pd.DataFrame(0, index=df_encoded.index, columns=list(missing_cols))
    df_encoded = pd.concat([df_encoded, missing_df], axis=1)

df_encoded = df_encoded[feature_columns]

print(f"\nEncoded features shape: {df_encoded.shape}")
print(f"Expected features: {len(feature_columns)}")

# Scale
df_scaled = scaler.transform(df_encoded)

# Predict
prediction = model.predict(df_scaled)[0]
prediction_proba = model.predict_proba(df_scaled)[0]

print("\n" + "="*50)
print("PREDICTION RESULTS")
print("="*50)
print(f"Raw prediction: {prediction}")
print(f"Probability on-time (0): {prediction_proba[0]:.4f}")
print(f"Probability delayed (1): {prediction_proba[1]:.4f}")
print(f"Final: {'DELAYED' if prediction == 1 else 'ON-TIME'}")
print("="*50)

# Test a second case: Should be on-time
test_data2 = {
    'DayOfWeek': [2],  # Tuesday
    'DepTime': [1000],  # 10:00 AM
    'ArrTime': [1200],  # 12:00 PM
    'CRSArrTime': [1200],
    'Airline': ['Southwest Airlines Co.'],
    'Origin': ['LAX'],
    'Dest': ['SFO'],
    'month': [3],
    'day': [10]
}

df_input2 = pd.DataFrame(test_data2)
df_encoded2 = pd.get_dummies(df_input2, dtype=int)
missing_cols2 = set(feature_columns) - set(df_encoded2.columns)
if missing_cols2:
    missing_df2 = pd.DataFrame(0, index=df_encoded2.index, columns=list(missing_cols2))
    df_encoded2 = pd.concat([df_encoded2, missing_df2], axis=1)
df_encoded2 = df_encoded2[feature_columns]
df_scaled2 = scaler.transform(df_encoded2)

prediction2 = model.predict(df_scaled2)[0]
prediction_proba2 = model.predict_proba(df_scaled2)[0]

print("\nTest Case 2 (Should be ON-TIME):")
print(f"Prediction: {prediction2}")
print(f"Probability on-time: {prediction_proba2[0]:.4f}")
print(f"Probability delayed: {prediction_proba2[1]:.4f}")
print(f"Final: {'DELAYED' if prediction2 == 1 else 'ON-TIME'}")
