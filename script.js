// DOM Elements
const form = document.getElementById('predictionForm');
const resetBtn = document.getElementById('resetBtn');
const resultCard = document.getElementById('resultCard');
const resultContent = document.getElementById('resultContent');

// Form submission handler
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Get form values
    const formData = {
        dayOfWeek: parseInt(document.getElementById('dayOfWeek').value),
        month: parseInt(document.getElementById('month').value),
        day: parseInt(document.getElementById('day').value),
        departureTime: document.getElementById('departureTime').value,
        arrivalTime: document.getElementById('arrivalTime').value,
        airline: document.getElementById('airline').value,
        originAirport: document.getElementById('originAirport').value,
        destAirport: document.getElementById('destAirport').value
    };
    
    // Make prediction using the ML model via Flask API
    predictDelay(formData);
});

// Reset button handler
resetBtn.addEventListener('click', function() {
    form.reset();
    resultCard.classList.add('hidden');
});

// Form validation
function validateForm() {
    const departureTime = document.getElementById('departureTime').value;
    const arrivalTime = document.getElementById('arrivalTime').value;
    
    // Validate time format (HHMM)
    const timePattern = /^([0-1][0-9]|2[0-3])[0-5][0-9]$/;
    
    if (!timePattern.test(departureTime)) {
        alert('Invalid departure time format. Please use HHMM format (e.g., 1430)');
        return false;
    }
    
    if (!timePattern.test(arrivalTime)) {
        alert('Invalid arrival time format. Please use HHMM format (e.g., 1725)');
        return false;
    }
    
    return true;
}

// Prediction using trained ML model via Flask API
async function predictDelay(data) {
    const submitBtn = form.querySelector('button[type="submit"]');
    
    try {
        // Disable button and show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Analyzing...';
        
        // Call Flask API
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        
        const prediction = await response.json();
        
        // Display result
        displayResult(prediction);
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        // Show error message to user
        resultCard.classList.remove('hidden');
        resultContent.innerHTML = `
            <div style="color: #e53e3e;">
                <span style="font-size: 2rem;">⚠️</span>
                <div style="margin-top: 15px; font-size: 1.5rem;">Connection Error</div>
                <div style="font-size: 1rem; font-weight: normal; color: #718096; margin-top: 10px;">
                    Make sure the Flask server is running on port 5000
                </div>
                <div style="font-size: 0.9rem; color: #a0aec0; margin-top: 10px;">
                    Run: python app.py
                </div>
            </div>
        `;
        
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Predict Flight Status';
    }
}

// Display result from ML model
function displayResult(prediction) {
    resultCard.classList.remove('hidden');
    
    if (prediction.isDelayed) {
        resultContent.innerHTML = `
            <div class="result-delayed">
                <span style="font-size: 3rem;">⏰</span>
                <div style="margin-top: 15px;">Flight Likely Delayed</div>
                <div style="font-size: 1rem; font-weight: normal; color: #718096; margin-top: 10px;">
                    Delay Probability: ${prediction.probability_delayed}%
                </div>
                <div style="font-size: 0.9rem; color: #a0aec0; margin-top: 5px;">
                    Model Confidence: ${prediction.confidence}%
                </div>
            </div>
        `;
    } else {
        resultContent.innerHTML = `
            <div class="result-ontime">
                <span style="font-size: 3rem;">✅</span>
                <div style="margin-top: 15px;">Flight On Time</div>
                <div style="font-size: 1rem; font-weight: normal; color: #718096; margin-top: 10px;">
                    On-Time Probability: ${prediction.probability_ontime}%
                </div>
                <div style="font-size: 0.9rem; color: #a0aec0; margin-top: 5px;">
                    Model Confidence: ${prediction.confidence}%
                </div>
            </div>
        `;
    }
    
    // Smooth scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Add input formatting for time fields
document.getElementById('departureTime').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '').slice(0, 4);
});

document.getElementById('arrivalTime').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '').slice(0, 4);
});
