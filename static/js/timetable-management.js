/**
 * Timetable Management JavaScript
 * Handles all frontend interactions for the automated timetable scheduling system
 */

// API Base URL
const API_BASE = '/api/timetable';

// Utility Functions
function showAlert(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Insert at top of page
    const container = document.querySelector('.container-fluid');
    container.insertAdjacentHTML('afterbegin', alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

function showLoading(title, description) {
    document.getElementById('loadingMessage').textContent = title;
    document.getElementById('loadingDescription').textContent = description;
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    loadingModal.show();
    return loadingModal;
}

function hideLoading(modalInstance) {
    if (modalInstance) {
        modalInstance.hide();
    }
}

// Teachers Management
async function loadTeachers() {
    try {
        const response = await fetch(`${API_BASE}/teachers`);
        const teachers = await response.json();
        
        const tbody = document.getElementById('teachersTableBody');
        tbody.innerHTML = '';
        
        teachers.forEach(teacher => {
            const unavailability = JSON.parse(teacher.weekly_unavailability || '{}');
            const unavailableDays = Object.keys(unavailability).join(', ') || 'None';
            
            const row = `
                <tr>
                    <td><strong>${teacher.teacher_code}</strong></td>
                    <td>${teacher.first_name} ${teacher.last_name}</td>
                    <td>
                        <small class="text-muted">
                            ${JSON.parse(teacher.subject_qualifications || '[]').join(', ')}
                        </small>
                    </td>
                    <td>${teacher.max_hours_per_week} hrs</td>
                    <td>
                        <small class="text-warning">
                            ${unavailableDays}
                        </small>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editTeacher(${teacher.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteTeacher(${teacher.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
        
        // Update coordinator dropdown in student group modal
        updateTeacherDropdown(teachers);
        
    } catch (error) {
        console.error('Error loading teachers:', error);
        showAlert('Error loading teachers data', 'danger');
    }
}

async function submitTeacher(event) {
    event.preventDefault();
    const loading = showLoading('Saving Teacher', 'Adding teacher to the system...');
    
    try {
        const formData = new FormData(event.target);
        
        // Collect subject qualifications
        const qualifications = [];
        document.querySelectorAll('#subjectQualifications input:checked').forEach(checkbox => {
            qualifications.push(checkbox.value);
        });
        
        // Collect unavailability data
        const unavailability = {};
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
        days.forEach(day => {
            const checkbox = document.getElementById(day + 'Unavailable');
            const select = document.getElementById(day + 'Slots');
            if (checkbox && checkbox.checked) {
                unavailability[day] = [select.value];
            }
        });
        
        const teacherData = {
            teacher_code: formData.get('teacher_code'),
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            subject_qualifications: JSON.stringify(qualifications),
            weekly_unavailability: JSON.stringify(unavailability),
            max_hours_per_week: parseInt(formData.get('max_hours')) || 40
        };
        
        const response = await fetch(`${API_BASE}/teachers`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(teacherData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Teacher added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addTeacherModal')).hide();
            event.target.reset();
            loadTeachers();
        } else {
            showAlert(result.error || 'Error adding teacher', 'danger');
        }
        
    } catch (error) {
        console.error('Error submitting teacher:', error);
        showAlert('Network error. Please try again.', 'danger');
    } finally {
        hideLoading(loading);
    }
}

// Subjects Management
async function loadSubjects() {
    try {
        const response = await fetch(`${API_BASE}/subjects`);
        const subjects = await response.json();
        
        const tbody = document.getElementById('subjectsTableBody');
        tbody.innerHTML = '';
        
        subjects.forEach(subject => {
            const totalHours = subject.weekly_lecture_hours + subject.weekly_lab_hours + subject.weekly_tutorial_hours;
            const roomReq = subject.requires_special_room || 'Any';
            
            const row = `
                <tr>
                    <td><strong>${subject.subject_code}</strong></td>
                    <td>${subject.subject_name}</td>
                    <td>
                        <span class="badge bg-secondary">${subject.subject_type}</span>
                    </td>
                    <td>
                        <small>
                            L:${subject.weekly_lecture_hours} 
                            Lab:${subject.weekly_lab_hours} 
                            T:${subject.weekly_tutorial_hours}
                            <br><strong>Total: ${totalHours}hrs</strong>
                        </small>
                    </td>
                    <td>
                        <small class="text-info">${roomReq}</small>
                        <br><small class="text-muted">Min: ${subject.min_room_capacity}</small>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-success me-1" onclick="editSubject(${subject.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteSubject(${subject.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
        
        // Update subject checkboxes in teacher modal
        updateSubjectCheckboxes(subjects);
        
    } catch (error) {
        console.error('Error loading subjects:', error);
        showAlert('Error loading subjects data', 'danger');
    }
}

async function submitSubject(event) {
    event.preventDefault();
    const loading = showLoading('Saving Subject', 'Adding subject to the curriculum...');
    
    try {
        const formData = new FormData(event.target);
        
        const subjectData = {
            subject_code: formData.get('subject_code'),
            subject_name: formData.get('subject_name'),
            subject_type: formData.get('subject_type'),
            weekly_lecture_hours: parseInt(formData.get('lecture_hours')) || 0,
            weekly_lab_hours: parseInt(formData.get('lab_hours')) || 0,
            weekly_tutorial_hours: parseInt(formData.get('tutorial_hours')) || 0,
            requires_special_room: formData.get('special_room') || null,
            min_room_capacity: parseInt(formData.get('min_capacity')) || 30,
            description: formData.get('description') || ''
        };
        
        const response = await fetch(`${API_BASE}/subjects`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subjectData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Subject added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addSubjectModal')).hide();
            event.target.reset();
            loadSubjects();
        } else {
            showAlert(result.error || 'Error adding subject', 'danger');
        }
        
    } catch (error) {
        console.error('Error submitting subject:', error);
        showAlert('Network error. Please try again.', 'danger');
    } finally {
        hideLoading(loading);
    }
}

// Classrooms Management
async function loadClassrooms() {
    try {
        const response = await fetch(`${API_BASE}/classrooms`);
        const classrooms = await response.json();
        
        const tbody = document.getElementById('classroomsTableBody');
        tbody.innerHTML = '';
        
        classrooms.forEach(classroom => {
            const facilities = JSON.parse(classroom.facilities || '{}');
            const facilityList = Object.keys(facilities).filter(key => facilities[key]).join(', ') || 'Basic';
            
            const row = `
                <tr>
                    <td><strong>${classroom.room_number}</strong></td>
                    <td>${classroom.room_name}</td>
                    <td>
                        <span class="badge bg-warning text-dark">${classroom.room_type.replace('_', ' ')}</span>
                    </td>
                    <td>
                        <strong>${classroom.seating_capacity}</strong> seats
                        <br><small class="text-muted">Floor ${classroom.floor_number || 'N/A'}</small>
                    </td>
                    <td>
                        <small class="text-info">${facilityList}</small>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-warning me-1" onclick="editClassroom(${classroom.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteClassroom(${classroom.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
        
    } catch (error) {
        console.error('Error loading classrooms:', error);
        showAlert('Error loading classrooms data', 'danger');
    }
}

async function submitClassroom(event) {
    event.preventDefault();
    const loading = showLoading('Saving Classroom', 'Adding classroom to the system...');
    
    try {
        const formData = new FormData(event.target);
        
        // Collect facilities
        const facilities = {};
        document.querySelectorAll('#addClassroomModal input[name="facilities"]:checked').forEach(checkbox => {
            facilities[checkbox.value] = true;
        });
        
        const classroomData = {
            room_number: formData.get('room_number'),
            room_name: formData.get('room_name'),
            room_type: formData.get('room_type'),
            seating_capacity: parseInt(formData.get('seating_capacity')),
            floor_number: parseInt(formData.get('floor_number')) || null,
            building_name: formData.get('building_name') || '',
            facilities: JSON.stringify(facilities)
        };
        
        const response = await fetch(`${API_BASE}/classrooms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(classroomData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Classroom added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addClassroomModal')).hide();
            event.target.reset();
            loadClassrooms();
        } else {
            showAlert(result.error || 'Error adding classroom', 'danger');
        }
        
    } catch (error) {
        console.error('Error submitting classroom:', error);
        showAlert('Network error. Please try again.', 'danger');
    } finally {
        hideLoading(loading);
    }
}

// Student Groups Management
async function loadStudentGroups() {
    try {
        const response = await fetch(`${API_BASE}/student-groups`);
        const groups = await response.json();
        
        const tbody = document.getElementById('groupsTableBody');
        tbody.innerHTML = '';
        
        groups.forEach(group => {
            const coordinator = group.coordinator_name || 'Not assigned';
            
            const row = `
                <tr>
                    <td><strong>${group.group_code}</strong></td>
                    <td>${group.group_name}</td>
                    <td>
                        ${group.academic_year}
                        <br><small class="text-muted">Semester ${group.semester}</small>
                    </td>
                    <td>
                        <strong>${group.student_count}</strong> students
                    </td>
                    <td>
                        <small class="text-success">${coordinator}</small>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-info me-1" onclick="manageGroupSubjects(${group.id})">
                            <i class="fas fa-book"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editGroup(${group.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteGroup(${group.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
        
    } catch (error) {
        console.error('Error loading student groups:', error);
        showAlert('Error loading student groups data', 'danger');
    }
}

async function submitGroup(event) {
    event.preventDefault();
    const loading = showLoading('Saving Student Group', 'Creating student group...');
    
    try {
        const formData = new FormData(event.target);
        
        const groupData = {
            group_code: formData.get('group_code'),
            group_name: formData.get('group_name'),
            academic_year: formData.get('academic_year'),
            semester: parseInt(formData.get('semester')),
            student_count: parseInt(formData.get('student_count')),
            coordinator_teacher_id: parseInt(formData.get('coordinator_teacher')) || null
        };
        
        const response = await fetch(`${API_BASE}/student-groups`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(groupData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Student group added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addGroupModal')).hide();
            event.target.reset();
            loadStudentGroups();
        } else {
            showAlert(result.error || 'Error adding student group', 'danger');
        }
        
    } catch (error) {
        console.error('Error submitting student group:', error);
        showAlert('Network error. Please try again.', 'danger');
    } finally {
        hideLoading(loading);
    }
}

// Helper Functions
function updateSubjectCheckboxes(subjects) {
    const container = document.getElementById('subjectQualifications');
    container.innerHTML = '';
    
    subjects.forEach((subject, index) => {
        const colClass = index % 2 === 0 ? 'col-md-6' : 'col-md-6';
        const checkbox = `
            <div class="${colClass} mb-2">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="subject_${subject.id}" value="${subject.subject_code}">
                    <label class="form-check-label small" for="subject_${subject.id}">
                        ${subject.subject_name}
                    </label>
                </div>
            </div>
        `;
        container.innerHTML += checkbox;
    });
}

function updateTeacherDropdown(teachers) {
    const select = document.getElementById('coordinatorTeacher');
    const currentOptions = select.innerHTML;
    
    // Keep the "Select Coordinator" option
    let options = '<option value="">Select Coordinator (Optional)</option>';
    
    teachers.forEach(teacher => {
        options += `<option value="${teacher.id}">${teacher.first_name} ${teacher.last_name}</option>`;
    });
    
    select.innerHTML = options;
}

// Timetable Generation
async function generateTimetable() {
    const loading = showLoading('Generating Timetable', 'This may take a few minutes. Please do not close this page.');
    
    try {
        const response = await fetch(`${API_BASE}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                academic_year: '2024-25',
                semester: 1,
                method: 'auto'
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert(`Timetable generated successfully! ${result.total_classes} classes scheduled with ${result.success_rate}% success rate.`, 'success');
            
            // Redirect to timetable view after 2 seconds
            setTimeout(() => {
                window.location.href = '/admin/timetable/view';
            }, 2000);
        } else {
            showAlert(result.error || 'Error generating timetable', 'danger');
        }
        
    } catch (error) {
        console.error('Error generating timetable:', error);
        showAlert('Network error. Please try again.', 'danger');
    } finally {
        hideLoading(loading);
    }
}

// Edit/Delete functions (placeholders for now)
function editTeacher(id) {
    // TODO: Implement teacher editing
    showAlert('Edit teacher functionality coming soon!', 'info');
}

function deleteTeacher(id) {
    if (confirm('Are you sure you want to delete this teacher?')) {
        // TODO: Implement teacher deletion
        showAlert('Delete teacher functionality coming soon!', 'info');
    }
}

function editSubject(id) {
    showAlert('Edit subject functionality coming soon!', 'info');
}

function deleteSubject(id) {
    if (confirm('Are you sure you want to delete this subject?')) {
        showAlert('Delete subject functionality coming soon!', 'info');
    }
}

function editClassroom(id) {
    showAlert('Edit classroom functionality coming soon!', 'info');
}

function deleteClassroom(id) {
    if (confirm('Are you sure you want to delete this classroom?')) {
        showAlert('Delete classroom functionality coming soon!', 'info');
    }
}

function editGroup(id) {
    showAlert('Edit group functionality coming soon!', 'info');
}

function deleteGroup(id) {
    if (confirm('Are you sure you want to delete this student group?')) {
        showAlert('Delete group functionality coming soon!', 'info');
    }
}

function manageGroupSubjects(id) {
    showAlert('Manage group subjects functionality coming soon!', 'info');
}