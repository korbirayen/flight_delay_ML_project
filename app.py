"""
Flask API for Flight Delay Prediction
Serves predictions from the trained Decision Tree model
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import numpy as np
import warnings

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Suppress performance warnings
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)

# Load the trained model and preprocessing objects
print("Loading model and preprocessing objects...")

with open('flight_delay_model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    scaler = model_data['scaler']
    feature_columns = model_data['feature_columns']
    model_info = model_data['model_info']

print(f"Model loaded successfully!")
print(f"Model accuracy: {model_info['accuracy']:.4f}")
print(f"Total features: {len(feature_columns)}")

@app.route('/')
def home():
    return jsonify({
        'message': 'Flight Delay Prediction API',
        'accuracy': f"{model_info['accuracy']*100:.2f}%",
        'endpoints': {
            '/predict': 'POST - Make a prediction',
            '/info': 'GET - Get model information'
        }
    })

@app.route('/info')
def info():
    return jsonify({
        'accuracy': model_info['accuracy'],
        'airlines': model_info['airlines'],
        'origins': model_info['origins'],
        'destinations': model_info['destinations'],
        'total_features': len(feature_columns)
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['dayOfWeek', 'month', 'day', 'departureTime', 
                          'arrivalTime', 'airline', 'originAirport', 'destAirport']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Validate date is in 2019 (training data year)
        month = int(data['month'])
        day = int(data['day'])
        if month < 1 or month > 12:
            return jsonify({'error': 'Month must be between 1-12'}), 400
        if day < 1 or day > 31:
            return jsonify({'error': 'Day must be between 1-31'}), 400
        
        # Create input dataframe with the same structure as training data
        input_data = {
            'DayOfWeek': [int(data['dayOfWeek'])],
            'DepTime': [int(data['departureTime'])],
            'ArrTime': [int(data['arrivalTime'])],
            'CRSArrTime': [int(data['arrivalTime'])],  # Using same as ArrTime
            'Airline': [data['airline']],
            'Origin': [data['originAirport']],
            'Dest': [data['destAirport']],
            'month': [int(data['month'])],
            'day': [int(data['day'])]
        }
        
        df_input = pd.DataFrame(input_data)
        
        # One-hot encode categorical features (same as training)
        df_encoded = pd.get_dummies(df_input, dtype=int)
        
        # Align with training features efficiently
        missing_cols = set(feature_columns) - set(df_encoded.columns)
        if missing_cols:
            # Add all missing columns at once
            missing_df = pd.DataFrame(0, index=df_encoded.index, columns=list(missing_cols))
            df_encoded = pd.concat([df_encoded, missing_df], axis=1)
        
        # Ensure column order matches training
        df_encoded = df_encoded[feature_columns]
        
        # NO SCALING - Decision Trees don't need it and it was breaking predictions
        # Make prediction directly on encoded features
        prediction = model.predict(df_encoded)[0]
        prediction_proba = model.predict_proba(df_encoded)[0]
        
        # Debug logging
        print(f"\n=== PREDICTION DEBUG ===")
        print(f"Input: {data['airline']} from {data['originAirport']} to {data['destAirport']}")
        print(f"Time: {data['departureTime']} -> {data['arrivalTime']}")
        print(f"Raw prediction: {prediction}")
        print(f"Probabilities: On-time={prediction_proba[0]:.4f}, Delayed={prediction_proba[1]:.4f}")
        print(f"========================\n")
        
        # Get confidence
        confidence = float(max(prediction_proba) * 100)
        
        result = {
            'prediction': 'delayed' if prediction == 1 else 'on-time',
            'isDelayed': bool(prediction == 1),
            'confidence': round(confidence, 2),
            'probability_delayed': round(float(prediction_proba[1] * 100), 2),
            'probability_ontime': round(float(prediction_proba[0] * 100), 2)
        }
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR: {error_trace}")
        return jsonify({'error': str(e), 'trace': error_trace}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Starting Flask server...")
    print("API available at: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
