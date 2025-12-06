# 🚀 Quick Start Guide - Flight Delay Prediction System

## Overview
This system uses your trained Decision Tree model (99.47% accuracy) from the Jupyter notebook to predict flight delays through a web interface.

## Architecture
```
Frontend (HTML/CSS/JS) → Flask API → Decision Tree Model → Prediction
```

## Setup Instructions

### Option 1: Automated Setup (Recommended)
Run the PowerShell setup script:
```powershell
.\setup.ps1
```

### Option 2: Manual Setup

#### Step 1: Install Dependencies
```powershell
pip install flask flask-cors pandas numpy scikit-learn
```

#### Step 2: Train and Export Model
```powershell
python train_and_export_model.py
```

This script will:
- Load the Flight_delay.csv dataset (484,551 records)
- Preprocess data (one-hot encoding, MinMax scaling)
- Train Decision Tree model
- Export 4 files:
  - `flight_delay_model.pkl` - Trained model
  - `scaler.pkl` - Feature scaler
  - `feature_columns.pkl` - Column names for alignment
  - `model_info.pkl` - Metadata (airlines, airports)

**Expected output:**
```
Loading dataset...
Preprocessing data...
Found 12 airlines
Found 274 origin airports
Found 274 destination airports
Total features after encoding: 566
Training set: (339185, 566)
Test set: (145366, 566)

Training Decision Tree model...
Model Accuracy: 0.9947 (99.47%)

Saving model and preprocessing objects...
✓ Model saved: flight_delay_model.pkl
✓ Scaler saved: scaler.pkl
✓ Feature columns saved: feature_columns.pkl
✓ Model info saved: model_info.pkl

SUCCESS! All files exported.
```

#### Step 3: Start Flask Server
```powershell
python app.py
```

You should see:
```
Loading model and preprocessing objects...
Model loaded successfully!
Model accuracy: 0.9947
Total features: 566

==================================================
Starting Flask server...
API available at: http://localhost:5000
==================================================
```

#### Step 4: Open Web Interface
Open `index.html` in your web browser.

## Usage

### Making a Prediction

1. Fill in all 8 fields:
   - **Day of Week**: Select Monday-Sunday (1-7)
   - **Month**: Select 1-12
   - **Day**: Enter 1-31
   - **Departure Time**: Enter in HHMM format (e.g., 1430 for 2:30 PM)
   - **Scheduled Arrival**: Enter in HHMM format
   - **Airline**: Select from dropdown
   - **Origin Airport**: Select from top 20 airports
   - **Destination Airport**: Select from top 20 airports

2. Click **"Predict Flight Status"**

3. View results showing:
   - **Delayed** (⏰) or **On Time** (✅)
   - Delay probability percentage
   - Model confidence level

### Example Input
```
Day of Week: Friday (5)
Month: July (7)
Day: 15
Departure Time: 1815 (6:15 PM)
Scheduled Arrival: 2045 (8:45 PM)
Airline: American Eagle Airlines Inc.
Origin: ORD (Chicago O'Hare)
Destination: DFW (Dallas/Fort Worth)
```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Flight Delay Prediction API",
  "accuracy": "99.47%",
  "endpoints": {
    "/predict": "POST - Make a prediction",
    "/info": "GET - Get model information"
  }
}
```

#### 2. Model Information
```http
GET /info
```

**Response:**
```json
{
  "accuracy": 0.9947,
  "airlines": ["Southwest Airlines Co.", ...],
  "origins": ["ORD", "DFW", "ATL", ...],
  "destinations": ["ORD", "DFW", "ATL", ...],
  "total_features": 566
}
```

#### 3. Make Prediction
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "dayOfWeek": 5,
  "month": 7,
  "day": 15,
  "departureTime": "1815",
  "arrivalTime": "2045",
  "airline": "American Eagle Airlines Inc.",
  "originAirport": "ORD",
  "destAirport": "DFW"
}
```

**Response:**
```json
{
  "prediction": "delayed",
  "isDelayed": true,
  "confidence": 95.67,
  "probability_delayed": 95.67,
  "probability_ontime": 4.33
}
```

## Troubleshooting

### Issue: "Connection Error" in UI
**Cause:** Flask server not running

**Solution:**
```powershell
python app.py
```

### Issue: "Model files not found"
**Cause:** Model not trained/exported yet

**Solution:**
```powershell
python train_and_export_model.py
```

### Issue: Import errors
**Cause:** Missing dependencies

**Solution:**
```powershell
pip install -r requirements.txt
```

### Issue: CORS errors
**Cause:** Browser security policy

**Solution:** 
- Make sure flask-cors is installed
- Or use browser extensions to disable CORS temporarily for localhost

## Model Details

### Preprocessing Pipeline
1. **Date Parsing**: Extract month and day from Date column
2. **Target Creation**: Delay = 1 if total delay > 30 minutes
3. **One-Hot Encoding**: Convert categorical features (Airline, Origin, Dest)
4. **Feature Scaling**: MinMax normalization (0-1 range)

### Features
- **Numerical** (5): DayOfWeek, DepTime, ArrTime, CRSArrTime, month, day
- **Categorical** (3): Airline (12 values), Origin (274 values), Dest (274 values)
- **Total after encoding**: 566 features

### Model Configuration
- **Algorithm**: Decision Tree Classifier
- **Max Depth**: 20 (for faster training)
- **Random State**: 1
- **Train/Test Split**: 70/30
- **Accuracy**: 99.47%

## Files Generated

After running `train_and_export_model.py`:

| File | Size | Purpose |
|------|------|---------|
| `flight_delay_model.pkl` | ~50-100 MB | Trained Decision Tree |
| `scaler.pkl` | ~5 KB | MinMax scaler object |
| `feature_columns.pkl` | ~10 KB | Column names list |
| `model_info.pkl` | ~5 KB | Airlines, airports metadata |

## Tips for Best Results

1. **Use realistic combinations**: 
   - Match origin/destination with actual airline routes
   - Use valid date ranges (days 1-31 for the month)

2. **Test edge cases**:
   - Late night flights (after 10 PM)
   - Early morning flights (before 6 AM)
   - Peak travel days (Friday, Sunday, Monday)

3. **Compare predictions**:
   - Try the same route with different airlines
   - Try different times for the same route

## Support

If you encounter issues:
1. Check that all dependencies are installed
2. Verify Python version (3.8+)
3. Ensure dataset file exists: `Flight_delay.csv`
4. Check terminal output for error messages

## Next Steps

- Deploy to cloud (Heroku, AWS, Azure)
- Add more features (weather data, historical patterns)
- Create mobile-responsive design improvements
- Add prediction history/comparison features
