// EduTrack JavaScript Functions

// Toggle floating contact box
function toggleContact() {
    const contactContent = document.getElementById('contactContent');
    contactContent.classList.toggle('active');
}

// Close contact box when clicking outside
document.addEventListener('click', function(event) {
    const floatingContact = document.querySelector('.floating-contact');
    const contactContent = document.getElementById('contactContent');
    
    if (!floatingContact.contains(event.target)) {
        contactContent.classList.remove('active');
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Dashboard sidebar toggle for mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.dashboard-sidebar');
    sidebar.classList.toggle('active');
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// File upload preview
function previewFile(input, previewId) {
    const file = input.files[0];
    const preview = document.getElementById(previewId);
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            if (file.type.startsWith('image/')) {
                preview.innerHTML = `<img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px;">`;
            } else {
                preview.innerHTML = `<i class="fas fa-file"></i> ${file.name}`;
            }
        };
        reader.readAsDataURL(file);
    }
}

// Verification code functions
function generateVerificationCodes() {
    const codes = [];
    for (let i = 0; i < 3; i++) {
        codes.push(Math.floor(100000 + Math.random() * 900000));
    }
    return codes;
}

function displayVerificationCodes(correctCode) {
    const codes = generateVerificationCodes();
    const correctIndex = Math.floor(Math.random() * 3);
    codes[correctIndex] = correctCode;
    
    const codeContainer = document.getElementById('verificationCodes');
    codeContainer.innerHTML = '';
    
    codes.forEach((code, index) => {
        const codeElement = document.createElement('div');
        codeElement.className = 'verification-code-option';
        codeElement.innerHTML = `
            <input type="radio" name="verification_code" value="${code}" id="code_${index}" ${index === correctIndex ? 'data-correct="true"' : ''}>
            <label for="code_${index}" class="btn btn-outline-primary">${code}</label>
        `;
        codeContainer.appendChild(codeElement);
    });
}

// Real-time attendance scanner simulation
function startAttendanceScanner() {
    const scannerStatus = document.getElementById('scannerStatus');
    const lastUpdate = document.getElementById('lastUpdate');
    
    setInterval(() => {
        if (scannerStatus && lastUpdate) {
            const now = new Date();
            lastUpdate.textContent = now.toLocaleTimeString();
            
            // Simulate scanner activity
            scannerStatus.classList.add('scanning');
            setTimeout(() => {
                scannerStatus.classList.remove('scanning');
            }, 1000);
        }
    }, 30000); // Update every 30 seconds
}

// Dashboard stats animation
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            stat.textContent = Math.floor(current);
            
            if (current >= target) {
                stat.textContent = target;
                clearInterval(timer);
            }
        }, 20);
    });
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    return isValid;
}

// Email validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Mobile validation
function validateMobile(mobile) {
    const mobileRegex = /^[6-9]\d{9}$/;
    return mobileRegex.test(mobile);
}

// Show loading spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div>Loading...';
    element.disabled = true;
}

// Hide loading spinner
function hideLoading(elementId, originalText) {
    const element = document.getElementById(elementId);
    element.innerHTML = originalText;
    element.disabled = false;
}

// Success message
function showSuccess(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.main-content') || document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Error message
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.main-content') || document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Initialize page-specific functions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize based on page type
    const page = document.body.getAttribute('data-page');
    
    switch(page) {
        case 'dashboard':
            animateStats();
            startAttendanceScanner();
            break;
        case 'verification':
            // Initialize verification codes if needed
            break;
        default:
            // General initialization
            break;
    }
});

// Project submission with file validation
function validateProjectSubmission() {
    const title = document.getElementById('projectTitle').value;
    const description = document.getElementById('projectDescription').value;
    const file = document.getElementById('projectFile').files[0];
    
    if (!title.trim()) {
        showError('Project title is required');
        return false;
    }
    
    if (!description.trim()) {
        showError('Project description is required');
        return false;
    }
    
    if (!file) {
        showError('Please select a file to upload');
        return false;
    }
    
    // Check file size (max 16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size must be less than 16MB');
        return false;
    }
    
    return true;
}

// Assignment submission
function submitAssignment(assignmentId) {
    const formData = new FormData();
    const file = document.getElementById(`assignment_file_${assignmentId}`).files[0];
    const text = document.getElementById(`assignment_text_${assignmentId}`).value;
    
    if (!file && !text.trim()) {
        showError('Please provide either a file or text submission');
        return false;
    }
    
    formData.append('assignment_id', assignmentId);
    if (file) formData.append('file', file);
    if (text) formData.append('text', text);
    
    // Submit via AJAX
    fetch('/submit_assignment', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Assignment submitted successfully');
            // Update UI to show submitted status
            updateAssignmentStatus(assignmentId, 'submitted');
        } else {
            showError(data.message || 'Submission failed');
        }
    })
    .catch(error => {
        showError('Network error occurred');
    });
    
    return false;
}

// Update assignment status in UI
function updateAssignmentStatus(assignmentId, status) {
    const statusElement = document.getElementById(`status_${assignmentId}`);
    const submitButton = document.getElementById(`submit_${assignmentId}`);
    
    if (statusElement) {
        statusElement.className = status === 'submitted' ? 'badge bg-success' : 'badge bg-danger';
        statusElement.textContent = status === 'submitted' ? 'Submitted' : 'Not Submitted';
    }
    
    if (submitButton && status === 'submitted') {
        submitButton.disabled = true;
        submitButton.textContent = 'Submitted';
    }
}

// Search functionality
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');
    
    input.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        
        for (let i = 1; i < rows.length; i++) { // Skip header row
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length; j++) {
                if (cells[j].textContent.toLowerCase().includes(searchTerm)) {
                    found = true;
                    break;
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    });
}