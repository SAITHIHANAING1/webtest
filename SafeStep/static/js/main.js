// Safe-Step Main JavaScript

// Global Variables
let isMonitoring = false;
let monitoringTimer = null;
let currentSession = null;
let connectionStatus = 'connected';

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    startPeriodicUpdates();
});

// App Initialization
function initializeApp() {
    console.log('Safe-Step application initialized');
    
    // Check connection status
    updateConnectionStatus();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Setup service worker for offline functionality
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    }
}

// Event Listeners Setup
function setupEventListeners() {
    // Navigation active state
    updateActiveNavigation();
    
    // Form submissions
    setupFormHandlers();
    
    // Button click handlers
    setupButtonHandlers();
    
    // Modal event handlers
    setupModalHandlers();
    
    // Real-time updates
    setupWebSocketConnection();
}

// Update active navigation item
function updateActiveNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Form Handlers
function setupFormHandlers() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Registration form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistration);
    }
    
    // Profile update
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileUpdate);
    }
}

// Login Handler
function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password');
    const userType = formData.get('userType');
    
    // Basic validation
    if (!username || !password || !userType) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Signing In...';
    submitBtn.disabled = true;
    
    // Submit the form normally (let Flask handle authentication)
    setTimeout(() => {
        form.submit();
    }, 500);
}

// Registration Handler
function handleRegistration(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const password = formData.get('password');
    const confirmPassword = formData.get('confirmPassword');
    
    // Check password match
    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating Account...';
    submitBtn.disabled = true;
    
    // Submit the form
    form.submit();
}

// Profile Update Handler
function handleProfileUpdate(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const profileData = Object.fromEntries(formData);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Updating...';
    submitBtn.disabled = true;
    
    // In a real app, this would send the data to the server
    console.log('Updating profile:', profileData);
    
    // Simulate API call
    setTimeout(() => {
        showNotification('Profile updated successfully', 'success');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('profileModal'));
        if (modal) {
            modal.hide();
        }
    }, 1000);
}

// Button Handlers
function setupButtonHandlers() {
    // Emergency button
    const emergencyBtn = document.getElementById('emergencyBtn');
    if (emergencyBtn) {
        emergencyBtn.addEventListener('click', handleEmergency);
    }
    
    // Monitoring toggle
    const monitoringToggle = document.getElementById('monitoringToggle');
    if (monitoringToggle) {
        monitoringToggle.addEventListener('click', toggleMonitoring);
    }
}

// Modal Handlers
function setupModalHandlers() {
    // Profile modal
    const profileModal = document.getElementById('profileModal');
    if (profileModal) {
        profileModal.addEventListener('shown.bs.modal', loadProfileData);
    }
    
    // Emergency modal auto-dismiss
    const emergencyModal = document.getElementById('emergencyModal');
    if (emergencyModal) {
        // Auto-dismiss after 30 seconds if no action taken
        let emergencyTimeout = setTimeout(() => {
            const modal = bootstrap.Modal.getInstance(emergencyModal);
            if (modal) {
                modal.hide();
            }
        }, 30000);
        
        emergencyModal.addEventListener('hidden.bs.modal', () => {
            clearTimeout(emergencyTimeout);
        });
    }
}

// WebSocket Connection for Real-time Updates
function setupWebSocketConnection() {
    // Simulated WebSocket connection
    // In a real app, this would connect to a WebSocket server
    console.log('WebSocket connection established (simulated)');
    
    // Simulate periodic updates
    setInterval(() => {
        if (isMonitoring) {
            updateVitals();
        }
    }, 2000);
}

// Monitoring Functions
function toggleMonitoring() {
    if (isMonitoring) {
        stopMonitoring();
    } else {
        startMonitoring();
    }
}

function startMonitoring() {
    isMonitoring = true;
    const startBtn = document.getElementById('startMonitoringBtn');
    const stopBtn = document.getElementById('stopMonitoringBtn');
    
    if (startBtn) startBtn.style.display = 'none';
    if (stopBtn) stopBtn.style.display = 'inline-block';
    
    // Start session timer
    monitoringTimer = setInterval(updateMonitoringTimer, 1000);
    
    // Create new session
    createMonitoringSession();
    
    // Update UI
    updateMonitoringStatus('active');
    
    showNotification('Monitoring started successfully', 'success');
}

function stopMonitoring() {
    isMonitoring = false;
    const startBtn = document.getElementById('startMonitoringBtn');
    const stopBtn = document.getElementById('stopMonitoringBtn');
    
    if (startBtn) startBtn.style.display = 'inline-block';
    if (stopBtn) stopBtn.style.display = 'none';
    
    // Stop timer
    if (monitoringTimer) {
        clearInterval(monitoringTimer);
        monitoringTimer = null;
    }
    
    // End session
    if (currentSession) {
        endMonitoringSession();
    }
    
    // Update UI
    updateMonitoringStatus('inactive');
    
    showNotification('Monitoring stopped', 'info');
}

function updateMonitoringTimer() {
    const timerElement = document.getElementById('monitoringDuration');
    if (timerElement && currentSession) {
        const duration = Math.floor((Date.now() - currentSession.startTime) / 1000);
        const hours = Math.floor(duration / 3600);
        const minutes = Math.floor((duration % 3600) / 60);
        const seconds = duration % 60;
        
        timerElement.textContent = 
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
}

function updateMonitoringStatus(status) {
    const statusElement = document.getElementById('statusText');
    const indicatorElement = document.getElementById('statusIndicator');
    const cardElement = document.getElementById('statusCard');
    
    if (statusElement) {
        statusElement.textContent = status === 'active' ? 'Monitoring Active' : 'Monitoring Inactive';
    }
    
    if (indicatorElement) {
        indicatorElement.className = status === 'active' 
            ? 'fas fa-circle text-success me-2'
            : 'fas fa-circle text-secondary me-2';
    }
    
    if (cardElement) {
        cardElement.className = status === 'active'
            ? 'card border-success'
            : 'card border-secondary';
    }
}

// Session Management
function createMonitoringSession() {
    currentSession = {
        id: Date.now(),
        startTime: Date.now(),
        vitals: [],
        events: []
    };
    
    // In a real app, this would make an API call
    fetch('/api/sessions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            severity: 'monitoring',
            location: 'Current Location',
            notes: 'Monitoring session started'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentSession.serverId = data.session_id;
            updateSessionDisplay();
        }
    })
    .catch(error => {
        console.error('Error creating session:', error);
    });
}

function endMonitoringSession() {
    if (currentSession && currentSession.serverId) {
        fetch(`/api/sessions/${currentSession.serverId}/end`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Session ended successfully');
            }
        })
        .catch(error => {
            console.error('Error ending session:', error);
        });
    }
    
    currentSession = null;
    updateSessionDisplay();
}

function updateSessionDisplay() {
    const sessionElement = document.getElementById('sessionId');
    if (sessionElement) {
        sessionElement.textContent = currentSession 
            ? `Session #${currentSession.serverId || currentSession.id}`
            : 'No Active Session';
    }
}

// Vitals Updates
function updateVitals() {
    if (!isMonitoring) return;
    
    // Simulate sensor data
    const vitals = {
        heartRate: 70 + Math.floor(Math.random() * 30),
        movement: Math.floor(Math.random() * 100),
        riskLevel: Math.floor(Math.random() * 100),
        battery: Math.max(20, 100 - Math.floor(Math.random() * 5))
    };
    
    // Update display
    updateVitalDisplay('heartRate', vitals.heartRate + ' BPM');
    updateVitalDisplay('movementLevel', vitals.movement + '%');
    updateVitalDisplay('riskLevel', vitals.riskLevel + '%');
    updateVitalDisplay('batteryLevel', vitals.battery + '%');
    
    // Store in session
    if (currentSession) {
        currentSession.vitals.push({
            timestamp: Date.now(),
            ...vitals
        });
        
        // Limit stored vitals to last 1000 readings
        if (currentSession.vitals.length > 1000) {
            currentSession.vitals = currentSession.vitals.slice(-1000);
        }
    }
    
    // Check for alerts
    checkVitalAlerts(vitals);
}

function updateVitalDisplay(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = value;
    }
}

function checkVitalAlerts(vitals) {
    const alerts = [];
    
    if (vitals.heartRate > 100) {
        alerts.push('High heart rate detected');
    }
    
    if (vitals.movement > 80) {
        alerts.push('High movement activity');
    }
    
    if (vitals.riskLevel > 75) {
        alerts.push('Elevated seizure risk');
    }
    
    if (vitals.battery < 30) {
        alerts.push('Low battery warning');
    }
    
    alerts.forEach(alert => {
        logEvent(alert, 'warning');
    });
}

// Event Logging
function logEvent(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const eventLog = document.getElementById('eventLog');
    
    if (eventLog) {
        const colorClass = {
            'info': 'text-info',
            'success': 'text-success',
            'warning': 'text-warning',
            'danger': 'text-danger'
        }[type] || 'text-light';
        
        const entry = document.createElement('div');
        entry.className = colorClass;
        entry.innerHTML = `[${timestamp}] ${message}`;
        
        eventLog.appendChild(entry);
        eventLog.scrollTop = eventLog.scrollHeight;
        
        // Limit log entries
        const entries = eventLog.children;
        if (entries.length > 100) {
            eventLog.removeChild(entries[0]);
        }
    }
    
    // Store in session
    if (currentSession) {
        currentSession.events.push({
            timestamp: Date.now(),
            message,
            type
        });
    }
}

// Emergency Functions
function handleEmergency() {
    const emergencyModal = new bootstrap.Modal(document.getElementById('emergencyModal'));
    emergencyModal.show();
    
    logEvent('EMERGENCY ALERT TRIGGERED', 'danger');
    
    // In a real app, this would send notifications to emergency contacts
    sendEmergencyNotifications();
}

function sendEmergencyNotifications() {
    // Simulate sending notifications
    console.log('Sending emergency notifications...');
    
    // In a real app, this would:
    // 1. Send SMS/calls to emergency contacts
    // 2. Alert medical professionals
    // 3. Contact emergency services if configured
    // 4. Send push notifications to family members
}

function callEmergency() {
    if (confirm('This will call emergency services (911). Continue?')) {
        // In a real app, this would initiate the call
        window.location.href = 'tel:911';
        logEvent('Emergency services contacted', 'danger');
    }
}

function acknowledgeAlert() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('emergencyModal'));
    if (modal) {
        modal.hide();
    }
    logEvent('Emergency alert acknowledged by user', 'info');
}

// Profile Management
function loadProfileData() {
    // Load current user data into the profile form
    const form = document.getElementById('profileForm');
    if (form) {
        // In a real app, this would fetch user data from the server
        console.log('Loading profile data...');
    }
}

function updateProfile() {
    const form = document.getElementById('profileForm');
    if (!form) return;
    
    const formData = new FormData(form);
    const profileData = Object.fromEntries(formData);
    
    // In a real app, this would send the data to the server
    console.log('Updating profile:', profileData);
    
    showNotification('Profile updated successfully', 'success');
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('profileModal'));
    if (modal) {
        modal.hide();
    }
}

// Connection Status
function updateConnectionStatus() {
    const statusElement = document.getElementById('connectionStatus');
    const syncElement = document.getElementById('syncTime');
    
    if (statusElement) {
        if (navigator.onLine) {
            statusElement.innerHTML = '<i class="fas fa-wifi me-1"></i>Connected';
            statusElement.className = 'badge bg-success me-2';
            connectionStatus = 'connected';
        } else {
            statusElement.innerHTML = '<i class="fas fa-wifi-slash me-1"></i>Offline';
            statusElement.className = 'badge bg-danger me-2';
            connectionStatus = 'offline';
        }
    }
    
    if (syncElement) {
        syncElement.textContent = new Date().toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Periodic Updates
function startPeriodicUpdates() {
    // Update connection status every 30 seconds
    setInterval(updateConnectionStatus, 30000);
    
    // Update sync time every minute
    setInterval(() => {
        const syncElement = document.getElementById('syncTime');
        if (syncElement) {
            syncElement.textContent = new Date().toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    }, 60000);
}

// Notifications
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Utility Functions
function formatDate(date) {
    return new Date(date).toLocaleDateString();
}

function formatTime(date) {
    return new Date(date).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDuration(milliseconds) {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) {
        return `${hours}h ${minutes % 60}m`;
    } else if (minutes > 0) {
        return `${minutes}m ${seconds % 60}s`;
    } else {
        return `${seconds}s`;
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global access
window.SafeStep = {
    toggleMonitoring,
    handleEmergency,
    updateProfile,
    showNotification,
    logEvent,
    callEmergency,
    acknowledgeAlert
};

// Handle online/offline events
window.addEventListener('online', () => {
    updateConnectionStatus();
    showNotification('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    updateConnectionStatus();
    showNotification('Connection lost - working offline', 'warning');
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden
        console.log('Page hidden');
    } else {
        // Page is visible
        console.log('Page visible');
        updateConnectionStatus();
    }
});

// Error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    showNotification('An error occurred. Please refresh the page.', 'danger');
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('A network error occurred. Please check your connection.', 'warning');
});

console.log('Safe-Step JavaScript loaded successfully');
