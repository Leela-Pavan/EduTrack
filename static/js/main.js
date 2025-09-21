// Main JavaScript file for School Management System

// Global variables
let currentUser = null;
let attendanceData = [];
let chartInstances = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadUserData();
});

// Initialize application
function initializeApp() {
    // Add loading animation to all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fade-in');
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Real-time clock
    updateClock();
    setInterval(updateClock, 1000);
}

// Load user data
function loadUserData() {
    // This would typically fetch from an API
    const userRole = document.body.getAttribute('data-user-role');
    if (userRole) {
        currentUser = { role: userRole };
        initializeRoleBasedFeatures();
    }
}

// Initialize role-based features
function initializeRoleBasedFeatures() {
    if (!currentUser) return;
    
    switch (currentUser.role) {
        case 'student':
            initializeStudentFeatures();
            break;
        case 'teacher':
            initializeTeacherFeatures();
            break;
        case 'admin':
            initializeAdminFeatures();
            break;
    }
}

// Student-specific features
function initializeStudentFeatures() {
    // Load attendance history
    loadAttendanceHistory();
    
    // Setup QR scanner
    setupQRScanner();
    
    // Initialize task suggestions
    loadTaskSuggestions();
}

// Teacher-specific features
function initializeTeacherFeatures() {
    // Load class data
    loadClassData();
    
    // Setup attendance tracking
    setupAttendanceTracking();
    
    // Initialize charts
    initializeCharts();
}

// Admin-specific features
function initializeAdminFeatures() {
    // Load analytics data
    loadAnalyticsData();
    
    // Setup real-time updates
    setupRealTimeUpdates();
    
    // Initialize all charts
    initializeAllCharts();
}

// QR Code Scanner functionality
function setupQRScanner() {
    const scannerContainer = document.getElementById('scanner-container');
    if (!scannerContainer) return;
    
    // Add click to focus functionality
    scannerContainer.addEventListener('click', function() {
        this.style.borderColor = '#007bff';
        this.style.boxShadow = '0 0 0 0.2rem rgba(0, 123, 255, 0.25)';
    });
}

// Load attendance history
function loadAttendanceHistory() {
    // Simulate API call
    const mockData = [
        {
            date: '2024-01-15',
            class: '10A',
            subject: 'Mathematics',
            status: 'present',
            time: '08:30'
        },
        {
            date: '2024-01-15',
            class: '10A',
            subject: 'Physics',
            status: 'present',
            time: '09:15'
        },
        {
            date: '2024-01-14',
            class: '10A',
            subject: 'English',
            status: 'absent',
            time: null
        }
    ];
    
    displayAttendanceHistory(mockData);
}

// Display attendance history
function displayAttendanceHistory(data) {
    const tbody = document.getElementById('attendance-history');
    if (!tbody) return;
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No attendance records yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(record => `
        <tr>
            <td>${formatDate(record.date)}</td>
            <td>${record.class}</td>
            <td>${record.subject}</td>
            <td><span class="badge bg-${record.status === 'present' ? 'success' : 'danger'}">${record.status}</span></td>
            <td>${record.time || 'Not marked'}</td>
        </tr>
    `).join('');
}

// Load task suggestions
function loadTaskSuggestions() {
    // This would typically fetch from an API
    console.log('Loading task suggestions...');
}

// Load class data for teachers
function loadClassData() {
    // This would typically fetch from an API
    console.log('Loading class data...');
}

// Setup attendance tracking
function setupAttendanceTracking() {
    // This would setup real-time attendance tracking
    console.log('Setting up attendance tracking...');
}

// Initialize charts
function initializeCharts() {
    // Initialize attendance charts
    const attendanceChartCanvas = document.getElementById('attendanceChart');
    if (attendanceChartCanvas) {
        createAttendanceChart(attendanceChartCanvas);
    }
}

// Create attendance chart
function createAttendanceChart(canvas) {
    const ctx = canvas.getContext('2d');
    
    chartInstances.attendance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Present', 'Absent', 'Late'],
            datasets: [{
                data: [75, 20, 5],
                backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Load analytics data for admin
function loadAnalyticsData() {
    // This would fetch comprehensive analytics
    console.log('Loading analytics data...');
}

// Setup real-time updates
function setupRealTimeUpdates() {
    // This would setup WebSocket or polling for real-time updates
    console.log('Setting up real-time updates...');
}

// Initialize all charts for admin
function initializeAllCharts() {
    // Initialize all admin charts
    console.log('Initializing all charts...');
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatTime(timeString) {
    if (!timeString) return 'Not marked';
    const time = new Date(`2000-01-01T${timeString}`);
    return time.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function updateClock() {
    const clockElements = document.querySelectorAll('.clock');
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    clockElements.forEach(element => {
        element.textContent = timeString;
    });
}

// Notification system
function showNotification(message, type = 'info', duration = 3000) {
    const alertContainer = document.querySelector('.container-fluid');
    if (!alertContainer) return;
    
    const alertId = 'alert-' + Date.now();
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-remove after duration
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            const bsAlert = new bootstrap.Alert(alertElement);
            bsAlert.close();
        }
    }, duration);
}

// API helper functions
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(endpoint, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'API call failed');
        }
        
        return data;
    } catch (error) {
        console.error('API call failed:', error);
        showNotification('Error: ' + error.message, 'danger');
        throw error;
    }
}

// Attendance marking
async function markAttendance(qrData) {
    try {
        const result = await apiCall('/attendance/mark', {
            method: 'POST',
            body: JSON.stringify({ qr_data: qrData })
        });
        
        if (result.success) {
            showNotification('Attendance marked successfully!', 'success');
            loadAttendanceHistory();
        } else {
            showNotification(result.message, 'warning');
        }
        
        return result;
    } catch (error) {
        showNotification('Failed to mark attendance', 'danger');
        throw error;
    }
}

// Generate QR code
async function generateQRCode(class_name, section, subject, period) {
    try {
        const result = await apiCall(`/generate_qr/${class_name}/${section}/${subject}/${period}`);
        return result;
    } catch (error) {
        showNotification('Failed to generate QR code', 'danger');
        throw error;
    }
}

// Load attendance statistics
async function loadAttendanceStats() {
    try {
        const result = await apiCall('/api/attendance_stats');
        return result;
    } catch (error) {
        console.error('Failed to load attendance stats:', error);
        return null;
    }
}

// Export functions for global access
window.SchoolSystem = {
    showNotification,
    markAttendance,
    generateQRCode,
    loadAttendanceStats,
    apiCall
};

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K for quick actions
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        showQuickActions();
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
    }
});

// Quick actions menu
function showQuickActions() {
    const actions = [
        { label: 'Mark Attendance', action: () => window.location.href = '/attendance/qr' },
        { label: 'View Dashboard', action: () => window.location.href = '/dashboard' },
        { label: 'Generate Report', action: () => generateReport() },
        { label: 'Settings', action: () => showSettings() }
    ];
    
    // Create quick actions modal
    const modalHtml = `
        <div class="modal fade" id="quickActionsModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Quick Actions</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="list-group">
                            ${actions.map(action => `
                                <button class="list-group-item list-group-item-action" onclick="${action.action.name}()">
                                    ${action.label}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('quickActionsModal');
    if (existingModal) existingModal.remove();
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('quickActionsModal'));
    modal.show();
}

// Placeholder functions
function generateReport() {
    showNotification('Report generation feature coming soon!', 'info');
}

function showSettings() {
    showNotification('Settings panel coming soon!', 'info');
}

// Service Worker registration for offline support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Performance monitoring
function measurePerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }, 0);
        });
    }
}

// Initialize performance monitoring
measurePerformance();



