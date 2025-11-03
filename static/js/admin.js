// Admin Dashboard JavaScript

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    // Auto-refresh statistics every 60 seconds
    setInterval(refreshStats, 60000);
    
    // Initialize real-time updates
    if (window.location.pathname.includes('/admin/sessions')) {
        setInterval(refreshSessions, 30000);
    }
}

// Refresh statistics
function refreshStats() {
    // This would typically make an AJAX call to get updated stats
    console.log('Refreshing statistics...');
}

// Refresh active sessions
function refreshSessions() {
    // Auto-refresh sessions page
    if (confirm('Refresh sessions data?')) {
        location.reload();
    }
}

// Generate vouchers in bulk
function generateBulkVouchers() {
    const quantity = prompt('Enter number of vouchers to generate:');
    const planId = document.getElementById('bulkPlanSelect').value;
    
    if (quantity && planId) {
        if (confirm(`Generate ${quantity} vouchers?`)) {
            // Submit form
            document.getElementById('bulkVoucherForm').submit();
        }
    }
}

// Export data with loading
function exportData(type) {
    showAlert('Preparing export... Please wait.</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-wifi me-2"></i>Wi-Fi Hotspot
            </a>
            
            {% if session.user_id %}
            <div class="navbar-nav ms-auto">
                <span class="navbar-text me-3">
                    Welcome, {{ session.username }}!
                </span>
                {% if session.role == 'admin' %}
                <a class="nav-link" href="{{ url_for('admin.dashboard') }}">
                    <i class="fas fa-tachometer-alt me-1"></i>Dashboard
                </a>
                {% else %}
                <a class="nav-link" href="{{ url_for('user.dashboard') }}">
                    <i class="fas fa-user me-1"></i>Dashboard
                </a>
                {% endif %}
                <a class="nav-link" href="{{ url_for('auth.logout') }}">
                    <i class="fas fa-sign-out-alt me-1"></i>Logout
                </a>
            </div>
            {% endif %}
        </div>
    </nav>

    <main class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>