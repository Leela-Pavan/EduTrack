/**
 * Timetable Dashboard JavaScript
 * Handles interactive timetable display with drag-and-drop functionality
 */

// Global variables
let currentView = 'group';
let currentEntityId = null;
let timetableData = [];
let conflictsData = [];
let draggedElement = null;

// Time slots configuration
const TIME_SLOTS = [
    { id: 1, start: '09:00', end: '10:00', display: '9:00-10:00 AM' },
    { id: 2, start: '10:00', end: '11:00', display: '10:00-11:00 AM' },
    { id: 3, start: '11:15', end: '12:15', display: '11:15-12:15 PM' },
    { id: 4, start: '12:15', end: '13:15', display: '12:15-1:15 PM' },
    { id: 5, start: '14:00', end: '15:00', display: '2:00-3:00 PM' },
    { id: 6, start: '15:00', end: '16:00', display: '3:00-4:00 PM' },
    { id: 7, start: '16:00', end: '17:00', display: '4:00-5:00 PM' }
];

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

// Initialize dashboard
function initializeDashboard() {
    setupEventListeners();
    generateTimetableGrid();
}

function setupEventListeners() {
    // View toggle buttons
    document.getElementById('btnGroupView').addEventListener('click', () => setView('group'));
    document.getElementById('btnTeacherView').addEventListener('click', () => setView('teacher'));
    document.getElementById('btnRoomView').addEventListener('click', () => setView('room'));
    
    // Filter changes
    document.getElementById('academicYearFilter').addEventListener('change', loadTimetableData);
    document.getElementById('semesterFilter').addEventListener('change', loadTimetableData);
    document.getElementById('entityFilter').addEventListener('change', filterTimetable);
}

// Generate the basic timetable grid structure
function generateTimetableGrid() {
    const tbody = document.getElementById('timetableBody');
    tbody.innerHTML = '';
    
    TIME_SLOTS.forEach(slot => {
        const row = document.createElement('tr');
        
        // Time column
        const timeCell = document.createElement('td');
        timeCell.className = 'time-header';
        timeCell.style.position = 'sticky';
        timeCell.style.left = '0';
        timeCell.style.zIndex = '9';
        timeCell.innerHTML = `<strong>${slot.display}</strong>`;
        row.appendChild(timeCell);
        
        // Day columns
        DAYS.forEach(day => {
            const dayCell = document.createElement('td');
            dayCell.className = 'time-slot';
            dayCell.dataset.day = day;
            dayCell.dataset.timeSlot = slot.id;
            dayCell.dataset.start = slot.start;
            dayCell.dataset.end = slot.end;
            
            // Add drag and drop event listeners
            setupDragAndDrop(dayCell);
            
            row.appendChild(dayCell);
        });
        
        tbody.appendChild(row);
    });
}

// Set up drag and drop functionality for time slots
function setupDragAndDrop(cell) {
    // Drop zone events
    cell.addEventListener('dragover', handleDragOver);
    cell.addEventListener('drop', handleDrop);
    cell.addEventListener('dragleave', handleDragLeave);
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.currentTarget.classList.remove('drag-over');
}

async function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    
    if (!draggedElement) return;
    
    const sourceCell = draggedElement.parentElement;
    const targetCell = e.currentTarget;
    
    // Get entry data
    const entryId = draggedElement.dataset.entryId;
    const newTimeSlotId = getTimeSlotIdFromCell(targetCell);
    const newDay = targetCell.dataset.day;
    
    // Validate the move
    const isValid = await validateMove(entryId, newTimeSlotId, targetCell);
    
    if (isValid) {
        // Move the element
        targetCell.appendChild(draggedElement);
        
        // Update database
        await updateClassSchedule(entryId, newTimeSlotId);
        
        showAlert('Class rescheduled successfully!', 'success');
    } else {
        showAlert('Cannot reschedule: Conflict detected!', 'danger');
    }
    
    draggedElement.classList.remove('dragging');
    draggedElement = null;
}

// Validate if a move is allowed (check constraints)
async function validateMove(entryId, newTimeSlotId, targetCell) {
    try {
        const response = await fetch('/api/timetable/validate-move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                entry_id: entryId,
                new_time_slot_id: newTimeSlotId
            })
        });
        
        const result = await response.json();
        
        if (result.conflicts && result.conflicts.length > 0) {
            // Show conflicts in the cell
            targetCell.classList.add('conflict-warning');
            setTimeout(() => targetCell.classList.remove('conflict-warning'), 3000);
            return false;
        }
        
        return true;
    } catch (error) {
        console.error('Validation error:', error);
        return false;
    }
}

// Update class schedule in database
async function updateClassSchedule(entryId, newTimeSlotId) {
    try {
        const response = await fetch(`/api/timetable/entries/${entryId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                time_slot_id: newTimeSlotId
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to update schedule');
        }
        
        // Reload timetable data to reflect changes
        await loadTimetableData();
        
    } catch (error) {
        console.error('Update error:', error);
        showAlert('Failed to update schedule', 'danger');
    }
}

// Get time slot ID from cell data
function getTimeSlotIdFromCell(cell) {
    return parseInt(cell.dataset.timeSlot);
}

// Load timetable data from API
async function loadTimetableData() {
    const loading = showLoading('Loading timetable data...');
    
    try {
        const academicYear = document.getElementById('academicYearFilter').value;
        const semester = document.getElementById('semesterFilter').value;
        
        let url = `/api/timetable/view?academic_year=${academicYear}&semester=${semester}`;
        
        if (currentEntityId) {
            const filterParam = currentView === 'group' ? 'group_id' : 
                               currentView === 'teacher' ? 'teacher_id' : 'classroom_id';
            url += `&${filterParam}=${currentEntityId}`;
        }
        
        const response = await fetch(url);
        timetableData = await response.json();
        
        // Also load entities for the filter dropdown
        await loadEntities();
        
        // Render the timetable
        renderTimetable();
        
        // Load conflicts
        await loadConflicts();
        
    } catch (error) {
        console.error('Error loading timetable:', error);
        showAlert('Error loading timetable data', 'danger');
    } finally {
        hideLoading(loading);
    }
}

// Load entities for filter dropdown
async function loadEntities() {
    try {
        let endpoint = '';
        let labelField = '';
        
        switch (currentView) {
            case 'group':
                endpoint = '/api/timetable/student-groups';
                labelField = 'group_name';
                break;
            case 'teacher':
                endpoint = '/api/timetable/teachers';
                labelField = 'first_name';
                break;
            case 'room':
                endpoint = '/api/timetable/classrooms';
                labelField = 'room_name';
                break;
        }
        
        const response = await fetch(endpoint);
        const entities = await response.json();
        
        const select = document.getElementById('entityFilter');
        select.innerHTML = `<option value="">All ${currentView}s...</option>`;
        
        entities.forEach(entity => {
            const option = document.createElement('option');
            option.value = entity.id;
            
            if (currentView === 'teacher') {
                option.textContent = `${entity.first_name} ${entity.last_name}`;
            } else {
                option.textContent = entity[labelField];
            }
            
            select.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading entities:', error);
    }
}

// Render timetable data in the grid
function renderTimetable() {
    // Clear existing class cards
    document.querySelectorAll('.class-card').forEach(card => card.remove());
    
    // Group data by time slot and day
    const groupedData = groupTimetableData(timetableData);
    
    // Render each class
    Object.entries(groupedData).forEach(([key, classes]) => {
        const [day, timeSlotId] = key.split('_');
        const cell = document.querySelector(`[data-day="${day}"][data-time-slot="${timeSlotId}"]`);
        
        if (cell) {
            classes.forEach((classData, index) => {
                const classCard = createClassCard(classData, index);
                cell.appendChild(classCard);
            });
        }
    });
    
    updateTimetableTitle();
}

// Group timetable data by day and time slot
function groupTimetableData(data) {
    const grouped = {};
    
    data.forEach(entry => {
        const key = `${entry.day_of_week}_${entry.time_slot_id}`;
        if (!grouped[key]) {
            grouped[key] = [];
        }
        grouped[key].push(entry);
    });
    
    return grouped;
}

// Create a class card element
function createClassCard(classData, index = 0) {
    const card = document.createElement('div');
    card.className = `class-card ${classData.session_type.toLowerCase()}`;
    card.dataset.entryId = classData.id;
    card.draggable = true;
    
    // Offset multiple classes in the same slot
    if (index > 0) {
        card.style.top = `${2 + (index * 25)}px`;
        card.style.height = `calc(100% - ${2 + (index * 25)}px)`;
    }
    
    // Add drag event listeners
    card.addEventListener('dragstart', handleDragStart);
    card.addEventListener('dragend', handleDragEnd);
    card.addEventListener('click', () => showClassDetails(classData));
    
    // Card content
    card.innerHTML = `
        <div class="fw-bold">${classData.subject_code}</div>
        <div class="small">${classData.group_code}</div>
        <div class="small">${classData.teacher_name}</div>
        <div class="small">${classData.room_number}</div>
    `;
    
    return card;
}

function handleDragStart(e) {
    draggedElement = e.target;
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
    if (draggedElement === e.target) {
        draggedElement = null;
    }
}

// Show class details modal
function showClassDetails(classData) {
    const modalBody = document.getElementById('classDetailsBody');
    
    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6><i class="fas fa-book me-2"></i>Subject</h6>
                <p>${classData.subject_name} (${classData.subject_code})</p>
                
                <h6><i class="fas fa-users me-2"></i>Student Group</h6>
                <p>${classData.group_name} (${classData.group_code})</p>
                
                <h6><i class="fas fa-chalkboard-teacher me-2"></i>Teacher</h6>
                <p>${classData.teacher_name}</p>
            </div>
            <div class="col-md-6">
                <h6><i class="fas fa-clock me-2"></i>Schedule</h6>
                <p>${classData.day_of_week}, ${classData.start_time} - ${classData.end_time}</p>
                
                <h6><i class="fas fa-door-open me-2"></i>Classroom</h6>
                <p>${classData.room_name} (${classData.room_number})</p>
                
                <h6><i class="fas fa-tag me-2"></i>Session Type</h6>
                <p class="text-capitalize">${classData.session_type}</p>
            </div>
        </div>
    `;
    
    // Store current class data for actions
    document.getElementById('classDetailsModal').dataset.classId = classData.id;
    
    const modal = new bootstrap.Modal(document.getElementById('classDetailsModal'));
    modal.show();
}

// View switching
function setView(view) {
    currentView = view;
    currentEntityId = null;
    
    // Update button states
    document.querySelectorAll('.view-toggle .btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn${view.charAt(0).toUpperCase() + view.slice(1)}View`).classList.add('active');
    
    // Update filter label
    const filterSelect = document.getElementById('entityFilter');
    const labels = { group: 'Group', teacher: 'Teacher', room: 'Room' };
    filterSelect.innerHTML = `<option value="">All ${labels[view]}s...</option>`;
    
    // Reload data
    loadTimetableData();
}

// Filter timetable by entity
function filterTimetable() {
    currentEntityId = document.getElementById('entityFilter').value || null;
    loadTimetableData();
}

// Update timetable title
function updateTimetableTitle() {
    const title = document.getElementById('timetableTitle');
    const academicYear = document.getElementById('academicYearFilter').value;
    const semester = document.getElementById('semesterFilter').value;
    
    let viewLabel = '';
    const entitySelect = document.getElementById('entityFilter');
    
    if (currentEntityId && entitySelect.selectedIndex > 0) {
        viewLabel = ` - ${entitySelect.options[entitySelect.selectedIndex].text}`;
    } else {
        const labels = { group: 'All Groups', teacher: 'All Teachers', room: 'All Rooms' };
        viewLabel = ` - ${labels[currentView]}`;
    }
    
    title.innerHTML = `
        <i class="fas fa-calendar-week me-2"></i>
        Timetable (${academicYear}, Semester ${semester})${viewLabel}
    `;
}

// Load conflicts data
async function loadConflicts() {
    try {
        const academicYear = document.getElementById('academicYearFilter').value;
        const semester = document.getElementById('semesterFilter').value;
        
        const response = await fetch(`/api/timetable/conflicts?academic_year=${academicYear}&semester=${semester}`);
        conflictsData = await response.json();
        
        // Update conflicts count in button
        const conflictsBtn = document.querySelector('[onclick="showConflicts()"]');
        if (conflictsData.length > 0) {
            conflictsBtn.innerHTML = `
                <i class="fas fa-exclamation-triangle me-1"></i>
                Conflicts (${conflictsData.length})
            `;
            conflictsBtn.classList.add('btn-danger');
            conflictsBtn.classList.remove('btn-warning');
        } else {
            conflictsBtn.innerHTML = '<i class="fas fa-check-circle me-1"></i>No Conflicts';
            conflictsBtn.classList.add('btn-success');
            conflictsBtn.classList.remove('btn-warning', 'btn-danger');
        }
        
    } catch (error) {
        console.error('Error loading conflicts:', error);
    }
}

// Show conflicts modal
function showConflicts() {
    const tbody = document.getElementById('conflictsTableBody');
    tbody.innerHTML = '';
    
    if (conflictsData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No conflicts detected</td></tr>';
    } else {
        conflictsData.forEach(conflict => {
            const severityBadge = getSeverityBadge(conflict.severity);
            const row = `
                <tr>
                    <td>${severityBadge}</td>
                    <td>${conflict.conflict_type.replace('_', ' ')}</td>
                    <td>${conflict.conflict_description}</td>
                    <td>${new Date(conflict.detected_at).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="resolveConflict(${conflict.id})">
                            Resolve
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    }
    
    const modal = new bootstrap.Modal(document.getElementById('conflictsModal'));
    modal.show();
}

function getSeverityBadge(severity) {
    const badges = {
        'critical': '<span class="badge bg-danger">Critical</span>',
        'major': '<span class="badge bg-warning">Major</span>',
        'minor': '<span class="badge bg-info">Minor</span>',
        'warning': '<span class="badge bg-secondary">Warning</span>'
    };
    return badges[severity] || badges['warning'];
}

// Export timetable
async function exportTimetable() {
    try {
        const academicYear = document.getElementById('academicYearFilter').value;
        const semester = document.getElementById('semesterFilter').value;
        
        let url = `/api/timetable/export?academic_year=${academicYear}&semester=${semester}&format=pdf`;
        
        if (currentEntityId) {
            const filterParam = currentView === 'group' ? 'group_id' : 
                               currentView === 'teacher' ? 'teacher_id' : 'classroom_id';
            url += `&${filterParam}=${currentEntityId}`;
        }
        
        window.open(url, '_blank');
        
    } catch (error) {
        console.error('Export error:', error);
        showAlert('Error exporting timetable', 'danger');
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container-fluid');
    container.insertAdjacentHTML('afterbegin', alertHtml);
    
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

function showLoading(message) {
    document.getElementById('loadingMessage').textContent = message;
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
    return modal;
}

function hideLoading(modalInstance) {
    if (modalInstance) {
        modalInstance.hide();
    }
}

// Placeholder functions for future implementation
function rescheduleClass() {
    showAlert('Reschedule functionality coming soon!', 'info');
}

function cancelClass() {
    if (confirm('Are you sure you want to cancel this class?')) {
        showAlert('Cancel class functionality coming soon!', 'info');
    }
}

function resolveConflict(conflictId) {
    showAlert('Conflict resolution functionality coming soon!', 'info');
}

function autoResolveConflicts() {
    showAlert('Auto-resolve functionality coming soon!', 'info');
}