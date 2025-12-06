# Flight Delay Prediction System - Quick Start

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Flight Delay Prediction System - Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found! Please install Python first." -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
Write-Host ""
Write-Host "[2/4] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "  Installing: flask, flask-cors, pandas, numpy, scikit-learn" -ForegroundColor Gray
pip install -q flask flask-cors pandas numpy scikit-learn 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
}

# Step 3: Train model
Write-Host ""
Write-Host "[3/4] Training Decision Tree model..." -ForegroundColor Yellow
Write-Host "  This may take 30-60 seconds with 484K records..." -ForegroundColor Gray
python train_and_export_model.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Model trained and exported" -ForegroundColor Green
} else {
    Write-Host "  ✗ Model training failed" -ForegroundColor Red
    Write-Host "  Try running manually: python train_and_export_model.py" -ForegroundColor Yellow
}

# Step 4: Instructions
Write-Host ""
Write-Host "[4/4] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the Flask API server:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Open index.html in your browser" -ForegroundColor White
Write-Host ""
Write-Host "3. Make predictions!" -ForegroundColor White
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
