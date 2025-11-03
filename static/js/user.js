// User Dashboard JavaScript

let currentSession = null;

// Load available plans
function loadPlans() {
    showLoading('plansList');
    
    // Simulate API call - replace with actual AJAX call
    setTimeout(() => {
        const plansHtml = `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Basic Plan</h5>
                        <p class="card-text">1GB data with 24 hours validity</p>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-database text-primary me-2"></i>1.00 GB</li>
                            <li><i class="fas fa-clock text-success me-2"></i>24h 0m</li>
                            <li><i class="fas fa-money-bill text-warning me-2"></i>₹50.00</li>
                        </ul>
                        <button class="btn btn-primary" onclick="selectPlan(1, 'Basic Plan', 50.00, '1.00 GB', '24h 0m')">
                            Select Plan
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Standard Plan</h5>
                        <p class="card-text">5GB data with 7 days validity</p>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-database text-primary me-2"></i>5.00 GB</li>
                            <li><i class="fas fa-clock text-success me-2"></i>7d 0h</li>
                            <li><i class="fas fa-money-bill text-warning me-2"></i>₹200.00</li>
                        </ul>
                        <button class="btn btn-primary" onclick="selectPlan(2, 'Standard Plan', 200.00, '5.00 GB', '7d 0h')">
                            Select Plan
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Premium Plan</h5>
                        <p class="card-text">10GB data with 30 days validity</p>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-database text-primary me-2"></i>10.00 GB</li>
                            <li><i class="fas fa-clock text-success me-2"></i>30d 0h</li>
                            <li><i class="fas fa-money-bill text-warning me-2"></i>₹500.00</li>
                        </ul>
                        <button class="btn btn-primary" onclick="selectPlan(3, 'Premium Plan', 500.00, '10.00 GB', '30d 0h')">
                            Select Plan
                        </button>
                    </div>
                </div>
            </div>
        `;
        hideLoading('plansList', plansHtml);
    }, 1000);
}

// Select plan for recharge
function selectPlan(planId, planName, price, dataLimit, timeLimit) {
    document.getElementById('selectedPlanId').value = planId;
    
    const planDetails = `
        <div class="alert alert-info">
            <h5>${planName}</h5>
            <p><strong>Data:</strong> ${dataLimit}</p>
            <p><strong>Time:</strong> ${timeLimit}</p>
            <p><strong>Price:</strong> ₹${price}</p>
        </div>
    `;
    
    document.getElementById('planDetails').innerHTML = planDetails;
    
    const modal = new bootstrap.Modal(document.getElementById('rechargeModal'));
    modal.show();
}

// Start internet session
function startSession() {
    const startBtn = document.getElementById('startSessionBtn');
    const stopBtn = document.getElementById('stopSessionBtn');
    const statusDiv = document.getElementById('sessionStatus');
    
    startBtn.disabled = true;
    startBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Starting...';
    
    // Simulate session start
    setTimeout(() => {
        currentSession = {
            id: Date.now(),
            startTime: new Date(),
            dataUsed: 0,
            timeUsed: 0
        };
        
        startBtn.style.display = 'none';
        stopBtn.style.display = 'block';
        
        statusDiv.className = 'alert alert-success session-active';
        statusDiv.innerHTML = '<i class="fas fa-wifi me-2"></i>Session Active - Connected to Wi-Fi';
        
        // Start session timer
        startSessionTimer();
        
        showAlert('Internet session started successfully!', 'success');
    }, 2000);
}

// Stop internet session
function stopSession() {
    const startBtn = document.getElementById('startSessionBtn');
    const stopBtn = document.getElementById('stopSessionBtn');
    const statusDiv = document.getElementById('sessionStatus');
    
    stopBtn.disabled = true;
    stopBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Stopping...';
    
    setTimeout(() => {
        currentSession = null;
        
        startBtn.style.display = 'block';
        startBtn.disabled = false;
        startBtn.innerHTML = '<i class="fas fa-play me-1"></i>Start Session';
        
        stopBtn.style.display = 'none';
        stopBtn.disabled = false;
        stopBtn.innerHTML = '<i class="fas fa-stop me-1"></i>Stop Session';
        
        statusDiv.className = 'alert alert-info';
        statusDiv.innerHTML = '<i class="fas fa-info-circle me-2"></i>No active session';
        
        showAlert('Internet session stopped.', 'info');
        
        // Update balance display
        updateBalanceDisplay();
    }, 1000);
}

// Session timer
let sessionTimer;
function startSessionTimer() {
    sessionTimer = setInterval(() => {
        if (currentSession) {
            currentSession.timeUsed++;
            currentSession.dataUsed += Math.random() * 0.1; // Simulate data usage
            
            // Update session info (if you want to display it)
            console.log(`Session time: ${currentSession.timeUsed} minutes, Data used: ${currentSession.dataUsed.toFixed(2)} MB`);
        } else {
            clearInterval(sessionTimer);
        }
    }, 60000); // Update every minute
}

// Update balance display
function updateBalanceDisplay() {
    fetch('/user/check_balance')
        .then(response => response.json())
        .then(data => {
            document.getElementById('dataBalance').textContent = data.data_balance_formatted;
            document.getElementById('timeBalance').textContent = data.time_balance_formatted;
        })
        .catch(error => {
            console.error('Error updating balance:', error);
        });
}

// Auto-refresh balance every 30 seconds
setInterval(updateBalanceDisplay, 30000);