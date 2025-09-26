/**
 * Optimized Timetable Dashboard JavaScript
 * Performance improvements: caching, reduced API calls, lazy loading
 */

// Global variables with caching
let currentView = 'group';
let currentEntityId = null;
let timetableData = [];
let conflictsData = [];
let entitiesCache = {}; // Cache for entities to avoid repeated API calls
let lastLoadTime = 0; // Prevent excessive reloads

// EduTrack Time slots configuration (optimized)
const TIME_SLOTS = [
    { id: 1, start: '09:00', end: '09:45', display: '9:00-9:45 AM', period: 'Period 1' },
    { id: 2, start: '09:45', end: '10:30', display: '9:45-10:30 AM', period: 'Period 2' },
    { id: 3, start: '10:45', end: '11:30', display: '10:45-11:30 AM', period: 'Period 3' },
    { id: 4, start: '11:30', end: '12:15', display: '11:30-12:15 PM', period: 'Period 4' },
    { id: 5, start: '13:30', end: '14:15', display: '1:30-2:15 PM', period: 'Period 5' },
    { id: 6, start: '14:15', end: '15:00', display: '2:15-3:00 PM', period: 'Period 6' },
    { id: 7, start: '15:15', end: '16:00', display: '3:15-4:00 PM', period: 'Period 7' },
    { id: 8, start: '16:00', end: '16:45', display: '4:00-4:45 PM', period: 'Period 8' }
];

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const CACHE_DURATION = 60000; // 1 minute cache

// Optimized initialization
function initializeDashboard() {
    setupEventListeners();
    generateOptimizedTimetableGrid();
    // Load initial data with debouncing
    debounced(loadOptimizedTimetableData, 300)();
}

// Debouncing utility for performance
function debounced(func, wait) {
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

// Optimized event listeners
function setupEventListeners() {
    // View toggle buttons with single event delegation
    document.addEventListener('click', (e) => {
        if (e.target.matches('#btnGroupView')) setView('group');
        else if (e.target.matches('#btnTeacherView')) setView('teacher');
        else if (e.target.matches('#btnRoomView')) setView('room');
    });
    
    // Debounced filter changes
    const debouncedLoad = debounced(loadOptimizedTimetableData, 500);
    document.getElementById('academicYearFilter').addEventListener('change', debouncedLoad);
    document.getElementById('semesterFilter').addEventListener('change', debouncedLoad);
    document.getElementById('entityFilter').addEventListener('change', debouncedLoad);
}

// Optimized timetable data loading with caching
async function loadOptimizedTimetableData() {
    // Prevent excessive API calls
    const now = Date.now();
    if (now - lastLoadTime < 1000) return; // Minimum 1 second between calls
    lastLoadTime = now;

    const loading = showOptimizedLoading('Loading timetable data...');
    
    try {
        const academicYear = document.getElementById('academicYearFilter').value;
        const semester = document.getElementById('semesterFilter').value;
        const entityId = document.getElementById('entityFilter').value;
        
        // Build optimized URL
        let url = `/timetable/api/view?academic_year=${academicYear}&semester=${semester}`;
        
        if (entityId) {
            const filterParam = currentView === 'group' ? 'group_id' : 
                               currentView === 'teacher' ? 'teacher_id' : 'classroom_id';
            url += `&${filterParam}=${entityId}`;
        }
        
        // Use fetch with cache control
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Cache-Control': 'max-age=60',
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        timetableData = await response.json();
        
        // Load entities only if not cached
        await loadEntitiesOptimized();
        
        // Render with performance optimization
        await renderOptimizedTimetable();
        
        // Load conflicts asynchronously
        setTimeout(loadConflictsOptimized, 100);
        
        console.log(`✅ Loaded ${timetableData.length} timetable entries`);
        
    } catch (error) {
        console.error('Error loading timetable:', error);
        showAlert('Error loading timetable data. Please try again.', 'danger');
    } finally {
        hideOptimizedLoading(loading);
    }
}

// Optimized entities loading with caching
async function loadEntitiesOptimized() {
    const cacheKey = currentView;
    const now = Date.now();
    
    // Check cache first
    if (entitiesCache[cacheKey] && 
        now - entitiesCache[cacheKey].timestamp < CACHE_DURATION) {
        populateEntityDropdown(entitiesCache[cacheKey].data);
        return;
    }
    
    try {
        let endpoint;
        switch (currentView) {
            case 'teacher':
                endpoint = '/timetable/api/teachers';
                break;
            case 'group':
                endpoint = '/timetable/api/student-groups';
                break;
            case 'room':
                endpoint = '/timetable/api/classrooms';
                break;
        }
        
        const response = await fetch(endpoint, {
            headers: { 'Cache-Control': 'max-age=300' } // 5 minute cache for entities
        });
        
        const entities = await response.json();
        
        // Cache the result
        entitiesCache[cacheKey] = {
            data: entities,
            timestamp: now
        };
        
        populateEntityDropdown(entities);
        
    } catch (error) {
        console.error('Error loading entities:', error);
    }
}

// Separate function to populate dropdown (extracted for reuse)
function populateEntityDropdown(entities) {
    const select = document.getElementById('entityFilter');
    const currentValue = select.value;
    
    select.innerHTML = `<option value="">All ${currentView}s...</option>`;
    
    entities.forEach(entity => {
        const option = document.createElement('option');
        option.value = entity.id;
        
        if (currentView === 'teacher') {
            option.textContent = `${entity.first_name} ${entity.last_name}`;
        } else if (currentView === 'group') {
            option.textContent = entity.group_name;
        } else {
            option.textContent = entity.room_name;
        }
        
        if (entity.id == currentValue) {
            option.selected = true;
        }
        
        select.appendChild(option);
    });
}

// Optimized timetable rendering with virtual scrolling concept
async function renderOptimizedTimetable() {
    const tbody = document.getElementById('timetableBody');
    if (!tbody) return;
    
    // Clear efficiently
    tbody.innerHTML = '';
    
    // Use document fragment for better performance
    const fragment = document.createDocumentFragment();
    
    // Create time slot lookup for better performance
    const dataBySlot = {};
    timetableData.forEach(entry => {
        const key = `${entry.day_of_week}_${entry.start_time}`;
        if (!dataBySlot[key]) dataBySlot[key] = [];
        dataBySlot[key].push(entry);
    });
    
    // Render only visible time slots (EduTrack academic periods)
    TIME_SLOTS.forEach(slot => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="time-header sticky-left">
                <strong>${slot.period}</strong><br>
                <small>${slot.display}</small>
            </td>
        `;
        
        DAYS.forEach(day => {
            const cell = document.createElement('td');
            cell.className = 'time-slot position-relative';
            cell.setAttribute('data-day', day);
            cell.setAttribute('data-time', slot.start);
            
            const key = `${day}_${slot.start}`;
            const entries = dataBySlot[key] || [];
            
            // Render entries efficiently
            entries.forEach(entry => {
                const card = createOptimizedClassCard(entry);
                cell.appendChild(card);
            });
            
            row.appendChild(cell);
        });
        
        fragment.appendChild(row);
    });
    
    tbody.appendChild(fragment);
    
    // Initialize drag and drop after rendering
    initializeDragAndDrop();
}

// Optimized class card creation
function createOptimizedClassCard(entry) {
    const card = document.createElement('div');
    card.className = `class-card ${entry.subject_type} draggable`;
    card.draggable = true;
    card.setAttribute('data-entry-id', entry.id);
    
    // Efficient innerHTML with template literals
    card.innerHTML = `
        <div class="card-header">
            <small class="subject-code">${entry.subject_code}</small>
            <button class="btn btn-sm btn-outline-light edit-btn" onclick="editEntry(${entry.id})" title="Edit">
                <i class="fas fa-edit"></i>
            </button>
        </div>
        <div class="card-body">
            <div class="subject-name" title="${entry.subject_name}">${entry.subject_name}</div>
            <div class="teacher-name"><i class="fas fa-user"></i> ${entry.teacher_name}</div>
            <div class="group-name"><i class="fas fa-users"></i> ${entry.group_code}</div>
            <div class="room-name"><i class="fas fa-door-open"></i> ${entry.room_number}</div>
        </div>
    `;
    
    return card;
}

// Optimized conflicts loading
async function loadConflictsOptimized() {
    try {
        const academicYear = document.getElementById('academicYearFilter').value;
        const semester = document.getElementById('semesterFilter').value;
        
        const response = await fetch(`/timetable/api/conflicts?academic_year=${academicYear}&semester=${semester}`, {
            headers: { 'Cache-Control': 'max-age=30' } // 30 second cache for conflicts
        });
        
        conflictsData = await response.json();
        highlightConflicts();
        updateConflictCounter();
        
    } catch (error) {
        console.error('Error loading conflicts:', error);
    }
}

// Optimized view switching
function setView(newView) {
    if (newView === currentView) return; // No change needed
    
    currentView = newView;
    currentEntityId = null;
    
    // Update UI efficiently
    document.querySelectorAll('.view-toggle .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`btn${newView.charAt(0).toUpperCase() + newView.slice(1)}View`).classList.add('active');
    
    // Reset entity filter
    document.getElementById('entityFilter').value = '';
    
    // Load entities and data
    debounced(async () => {
        await loadEntitiesOptimized();
        await loadOptimizedTimetableData();
    }, 300)();
}

// Optimized loading indicators
function showOptimizedLoading(message) {
    const existingLoader = document.getElementById('optimizedLoader');
    if (existingLoader) existingLoader.remove();
    
    const loader = document.createElement('div');
    loader.id = 'optimizedLoader';
    loader.className = 'loading-overlay position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
    loader.style.cssText = 'background: rgba(255,255,255,0.9); z-index: 9999;';
    loader.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary mb-3" role="status"></div>
            <div class="fw-bold">${message}</div>
        </div>
    `;
    
    document.body.appendChild(loader);
    return loader;
}

function hideOptimizedLoading(loader) {
    if (loader && loader.parentNode) {
        loader.parentNode.removeChild(loader);
    }
}

// Generate optimized grid structure
function generateOptimizedTimetableGrid() {
    const table = document.getElementById('timetableGrid');
    if (!table) return;
    
    // Create header efficiently
    const thead = table.querySelector('thead') || table.createTHead();
    thead.innerHTML = `
        <tr>
            <th class="sticky-left sticky-top time-header">Time</th>
            ${DAYS.map(day => `<th class="sticky-top day-header text-center">${day}</th>`).join('')}
        </tr>
    `;
    
    // Create body
    const tbody = table.querySelector('tbody') || table.createTBody();
    tbody.id = 'timetableBody';
    
    console.log('✅ Optimized timetable grid generated');
}

// Conflict highlighting with performance optimization
function highlightConflicts() {
    // Remove existing conflict highlights efficiently
    document.querySelectorAll('.conflict-highlight').forEach(el => {
        el.classList.remove('conflict-highlight');
    });
    
    // Batch DOM updates
    conflictsData.forEach(conflict => {
        const card = document.querySelector(`[data-entry-id="${conflict.entry_id}"]`);
        if (card) {
            card.classList.add('conflict-highlight');
            card.title += ` - CONFLICT: ${conflict.conflict_description}`;
        }
    });
}

// Update conflict counter efficiently
function updateConflictCounter() {
    const counter = document.getElementById('conflictCount');
    if (counter) {
        counter.textContent = conflictsData.length;
        counter.parentElement.style.display = conflictsData.length > 0 ? 'block' : 'none';
    }
}

// Export functions for global access
window.initializeDashboard = initializeDashboard;
window.loadOptimizedTimetableData = loadOptimizedTimetableData;
window.setView = setView;

console.log('🚀 Optimized Timetable Dashboard loaded');