# Flight Delay Prediction System

A full-stack web application that predicts flight delays using a trained Decision Tree machine learning model with 99.47% accuracy.

## Project Structure

```
flight_delay_ML_project/
├── Flight_Delay_Prediction.ipynb  # Jupyter notebook with model training
├── Flight_delay.csv               # Dataset (484,551 flight records from 2019)
├── train_and_export_model.py      # Script to train and export the model
├── app.py                         # Flask backend API
├── index.html                     # Frontend interface
├── styles.css                     # Styling
├── script.js                      # Frontend logic
└── requirements.txt               # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Train and Export the Model

Run this script to train the Decision Tree model and export all necessary files:

```powershell
python train_and_export_model.py
```

This will create:
- `flight_delay_model.pkl` - Trained Decision Tree model
- `scaler.pkl` - MinMax scaler for feature normalization
- `feature_columns.pkl` - Feature column names for alignment
- `model_info.pkl` - Metadata (airlines, airports, accuracy)

### 3. Start the Flask API Server

```powershell
python app.py
```

The API will be available at `http://localhost:5000`

### 4. Open the Web Interface

Open `index.html` in your web browser.

## How It Works

1. **User Input**: Enter flight details (day, time, airline, airports)
2. **API Call**: JavaScript sends data to Flask backend
3. **Preprocessing**: Backend applies same transformations as training:
   - One-hot encoding for categorical variables
   - MinMax scaling for numerical features
4. **Prediction**: Decision Tree model predicts delay probability
5. **Result**: Display "Delayed" or "On Time" with confidence scores

## Model Details

- **Algorithm**: Decision Tree Classifier
- **Accuracy**: 99.47%
- **Training Data**: 484,551 flight records from 2019
- **Features**: 8 input features → 100+ after one-hot encoding
- **Target**: Binary classification (Delayed if total delay > 30 minutes)

## API Endpoints

- `GET /` - API information
- `GET /info` - Model metadata
- `POST /predict` - Make a prediction

### Example API Request

```json
POST http://localhost:5000/predict
{
  "dayOfWeek": 5,
  "month": 7,
  "day": 15,
  "departureTime": "1430",
  "arrivalTime": "1725",
  "airline": "Southwest Airlines Co.",
  "originAirport": "LAX",
  "destAirport": "SFO"
}
```

### Example API Response

```json
{
  "prediction": "on-time",
  "isDelayed": false,
  "confidence": 95.67,
  "probability_delayed": 4.33,
  "probability_ontime": 95.67
}
```

## Technologies Used

- **Backend**: Python, Flask, scikit-learn, pandas
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **ML**: Decision Tree Classifier with MinMax scaling
- **Data**: 2019 flight records dataset

## Features

✅ Real-time predictions using trained ML model  
✅ Clean, responsive UI with aviation theme  
✅ Form validation and error handling  
✅ Confidence scores and probabilities  
✅ REST API architecture  
✅ CORS enabled for local development
