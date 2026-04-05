let allSymptoms = [];
let selectedSymptomIds = new Set();
let allDiseases = [];
let lastResults = [];
let isOnline = false;

const symptomIcons = [
    'fa-thermometer-half', 'fa-head-side-virus', 'fa-lungs', 'fa-stomach',
    'fa-bone', 'fa-eye', 'fa-hand-sparkles', 'fa-brain',
    'fa-heartbeat', 'fa-allergies', 'fa-tint', 'fa-weight',
    'fa-running', 'fa-bed', 'fa-baby', 'fa-dizzy',
    'fa-skull-crossbones', 'fa-hand-holding-medical', 'fa-virus', 'fa-shield-virus'
];

document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    checkConnectivity();
    loadSymptoms();
    loadDiseases();
    checkAIAvailability();
    setInterval(checkConnectivity, 30000);
    loadHistory();
    registerSW();
});

function registerSW() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(() => {});
    }
}

async function checkConnectivity() {
    try {
        const response = await fetch('/api/health', { method: 'GET', cache: 'no-store' });
        if (response.ok) {
            isOnline = true;
            document.getElementById('modeIndicator').innerHTML = '<span class="mode-dot online"></span><span class="mode-text">Online</span>';
        }
    } catch {
        isOnline = false;
        document.getElementById('modeIndicator').innerHTML = '<span class="mode-dot offline"></span><span class="mode-text">Offline</span>';
    }
}

function navigateTo(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    const target = document.getElementById(`page-${page}`);
    if (target) target.classList.add('active');

    const navLink = document.querySelector(`.nav-link[data-page="${page}"]`);
    if (navLink) navLink.classList.add('active');

    if (page === 'results' && lastResults.length > 0) {
        renderResults(lastResults);
    }

    closeMobileMenu();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleMobileMenu() {
    document.getElementById('mainNav').classList.toggle('open');
}

function closeMobileMenu() {
    document.getElementById('mainNav').classList.remove('open');
}

function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);

    const icon = document.querySelector('#themeToggle i');
    icon.className = next === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
}

function loadTheme() {
    const saved = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    const icon = document.querySelector('#themeToggle i');
    icon.className = saved === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
}

async function loadSymptoms() {
    try {
        const response = await fetch('/api/symptoms');
        const data = await response.json();
        allSymptoms = data.symptoms;
        renderSymptoms(allSymptoms);
    } catch (error) {
        document.getElementById('symptomsGrid').innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><h3>Failed to load symptoms</h3><p>Please refresh the page.</p></div>';
    }
}

function renderSymptoms(symptoms) {
    const grid = document.getElementById('symptomsGrid');
    if (symptoms.length === 0) {
        grid.innerHTML = '<div class="empty-state"><i class="fas fa-search"></i><h3>No symptoms found</h3><p>Try a different search term.</p></div>';
        return;
    }

    grid.innerHTML = symptoms.map((symptom, index) => {
        const icon = symptomIcons[index % symptomIcons.length];
        const isSelected = selectedSymptomIds.has(symptom.id);
        return `
            <div class="symptom-card ${isSelected ? 'selected' : ''}" onclick="toggleSymptom(${symptom.id}, '${symptom.name.replace(/'/g, "\\'")}')" data-id="${symptom.id}">
                <div class="symptom-icon"><i class="fas ${icon}"></i></div>
                <span class="symptom-name">${symptom.name}</span>
            </div>
        `;
    }).join('');
}

function filterSymptoms(query) {
    const filtered = allSymptoms.filter(s =>
        s.name.toLowerCase().includes(query.toLowerCase())
    );
    renderSymptoms(filtered);
}

function toggleSymptom(id, name) {
    if (selectedSymptomIds.has(id)) {
        selectedSymptomIds.delete(id);
    } else {
        selectedSymptomIds.add(id);
    }
    renderSymptoms(allSymptoms);
    updateSelectedDisplay();
}

function updateSelectedDisplay() {
    const tagsContainer = document.getElementById('selectedTags');
    const countEl = document.getElementById('symptomCount');
    const analyzeBtn = document.getElementById('analyzeBtn');

    countEl.textContent = selectedSymptomIds.size;
    analyzeBtn.disabled = selectedSymptomIds.size === 0;

    const selected = allSymptoms.filter(s => selectedSymptomIds.has(s.id));
    tagsContainer.innerHTML = selected.map(s => `
        <span class="selected-tag">
            ${s.name}
            <i class="fas fa-times remove-tag" onclick="toggleSymptom(${s.id}, '${s.name.replace(/'/g, "\\'")}')"></i>
        </span>
    `).join('');
}

async function analyzeSymptoms() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<div class="spinner" style="width:20px;height:20px;border-width:2px;margin:0"></div> Analyzing...';

    try {
        const response = await fetch('/api/match', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symptom_ids: Array.from(selectedSymptomIds),
                top_n: 5
            })
        });
        const data = await response.json();
        lastResults = data.results;
        saveToHistory(selectedSymptomIds, data.results);
        navigateTo('results');
        renderResults(data.results);
    } catch (error) {
        document.getElementById('resultsContent').innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><h3>Analysis failed</h3><p>Please try again.</p></div>';
        navigateTo('results');
    }

    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-microscope"></i> Analyze Symptoms';
}

function renderResults(results) {
    const container = document.getElementById('resultsContent');

    if (!results || results.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search-minus"></i>
                <h3>No Matching Conditions Found</h3>
                <p>Try selecting different or additional symptoms for better results.</p>
                <button class="btn btn-primary" onclick="navigateTo('home')">
                    <i class="fas fa-redo"></i> Try Again
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = results.map((result, index) => {
        const riskLevel = result.match_percentage >= 60 ? 'high' : result.match_percentage >= 30 ? 'medium' : 'low';
        const delay = index * 0.1;

        return `
            <div class="result-card ${riskLevel}" style="animation-delay: ${delay}s">
                <div class="result-header">
                    <div>
                        <span class="result-name">${result.name}</span>
                        <p style="color:var(--text-muted);font-size:0.85rem;margin-top:0.25rem">Possible Conditions</p>
                    </div>
                    <span class="match-badge ${riskLevel}">
                        Estimated Match: ${result.match_percentage}%
                    </span>
                </div>

                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${result.match_percentage}%"></div>
                </div>

                <div class="result-section">
                    <h4><i class="fas fa-info-circle"></i> Description</h4>
                    <p>${result.description || 'No description available.'}</p>
                </div>

                <div class="result-section">
                    <h4><i class="fas fa-link"></i> Causes</h4>
                    <p>${result.causes || 'Not specified.'}</p>
                </div>

                <div class="result-section">
                    <h4><i class="fas fa-check-double"></i> Matched Symptoms (${result.matched_count}/${result.total_symptoms})</h4>
                    <div class="matched-symptoms-list">
                        ${result.matched_symptoms.map(s => `<span class="matched-symptom-tag">${s}</span>`).join('')}
                        ${result.all_symptoms.filter(s => !result.matched_symptoms.includes(s)).map(s => `<span class="unmatched-symptom-tag">${s}</span>`).join('')}
                    </div>
                </div>

                ${result.immediate_action ? `
                <div class="result-section">
                    <h4><i class="fas fa-first-aid"></i> Immediate Actions</h4>
                    <p>${result.immediate_action}</p>
                </div>
                ` : ''}

                ${result.medications ? `
                <div class="result-section">
                    <h4><i class="fas fa-pills"></i> Suggested Medications</h4>
                    <p>${result.medications}</p>
                </div>
                ` : ''}

                ${result.prevention ? `
                <div class="result-section">
                    <h4><i class="fas fa-shield-alt"></i> Prevention Tips</h4>
                    <p>${result.prevention}</p>
                </div>
                ` : ''}

                <button class="btn btn-secondary" onclick="openDiseaseModal(${result.id})" style="margin-top:0.5rem">
                    <i class="fas fa-expand"></i> View Full Details
                </button>
            </div>
        `;
    }).join('');
}

async function loadDiseases() {
    try {
        const response = await fetch('/api/diseases');
        const data = await response.json();
        allDiseases = data.diseases;
        renderDiseases(allDiseases);
    } catch (error) {
        document.getElementById('diseasesList').innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><h3>Failed to load diseases</h3></div>';
    }
}

function renderDiseases(diseases) {
    const container = document.getElementById('diseasesList');
    if (diseases.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-search"></i><h3>No diseases found</h3></div>';
        return;
    }

    container.innerHTML = diseases.map(d => `
        <div class="disease-card" onclick="openDiseaseModal(${d.id})">
            <h3><i class="fas fa-disease" style="color:var(--primary)"></i> ${d.name}</h3>
            <p>${d.description || 'No description available.'}</p>
            <span class="symptom-count"><i class="fas fa-notes-medical"></i> ${d.symptoms ? d.symptoms.length : 0} symptoms</span>
        </div>
    `).join('');
}

function searchDiseases(query) {
    if (!query || query.length < 2) {
        renderDiseases(allDiseases);
        return;
    }

    const filtered = allDiseases.filter(d =>
        d.name.toLowerCase().includes(query.toLowerCase()) ||
        (d.description && d.description.toLowerCase().includes(query.toLowerCase()))
    );
    renderDiseases(filtered);
}

async function openDiseaseModal(diseaseId) {
    try {
        const response = await fetch(`/api/disease/${diseaseId}`);
        const data = await response.json();
        const d = data.disease;

        document.getElementById('modalTitle').textContent = d.name;
        document.getElementById('modalBody').innerHTML = `
            <div class="detail-section">
                <h4><i class="fas fa-info-circle"></i> Description</h4>
                <p>${d.description || 'Not available.'}</p>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-link"></i> Causes</h4>
                <p>${d.causes || 'Not specified.'}</p>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-stethoscope"></i> Symptoms</h4>
                <div class="symptom-tags">
                    ${(d.symptoms || []).map(s => `<span class="symptom-tag">${s}</span>`).join('')}
                </div>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-first-aid"></i> Immediate Actions</h4>
                <p>${d.treatment?.immediate_action || 'Not specified.'}</p>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-pills"></i> Suggested Medications</h4>
                <p>${d.treatment?.medications || 'Not specified.'}</p>
            </div>
            <div class="detail-section">
                <h4><i class="fas fa-shield-alt"></i> Prevention</h4>
                <p>${d.prevention || 'Not specified.'}</p>
            </div>
        `;

        document.getElementById('diseaseModal').classList.add('active');
    } catch (error) {
        console.error('Failed to load disease details:', error);
    }
}

function closeModal() {
    document.getElementById('diseaseModal').classList.remove('active');
}

document.getElementById('diseaseModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('diseaseModal')) {
        closeModal();
    }
});

async function checkAIAvailability() {
    const statusEl = document.getElementById('aiStatus');
    try {
        const response = await fetch('/api/online/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: 'test', context: '' })
        });
        const data = await response.json();
        if (data.available && !data.error) {
            statusEl.textContent = 'AI Available';
            statusEl.className = 'status-badge available';
        } else {
            statusEl.textContent = 'AI Unavailable (Offline Mode)';
            statusEl.className = 'status-badge unavailable';
        }
    } catch {
        statusEl.textContent = 'AI Unavailable (Offline Mode)';
        statusEl.className = 'status-badge unavailable';
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;

    const messagesContainer = document.getElementById('chatMessages');

    messagesContainer.innerHTML += `
        <div class="message user-message">
            <div class="message-avatar"><i class="fas fa-user"></i></div>
            <div class="message-content"><p>${escapeHtml(message)}</p></div>
        </div>
    `;

    input.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    messagesContainer.innerHTML += `
        <div class="message bot-message" id="typingIndicator">
            <div class="message-avatar"><i class="fas fa-robot"></i></div>
            <div class="message-content"><p><em>Thinking...</em></p></div>
        </div>
    `;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
        const response = await fetch('/api/online/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message, context: '' })
        });
        const data = await response.json();

        const typingEl = document.getElementById('typingIndicator');
        if (typingEl) typingEl.remove();

        if (data.answer) {
            messagesContainer.innerHTML += `
                <div class="message bot-message">
                    <div class="message-avatar"><i class="fas fa-robot"></i></div>
                    <div class="message-content"><p>${formatAnswer(data.answer)}</p></div>
                </div>
            `;
        } else if (data.error) {
            messagesContainer.innerHTML += `
                <div class="message bot-message">
                    <div class="message-avatar"><i class="fas fa-robot"></i></div>
                    <div class="message-content">
                        <p>Sorry, I couldn't process your request. ${data.error}</p>
                        <p class="disclaimer-note"><i class="fas fa-info-circle"></i> This feature requires internet and a valid API key.</p>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        const typingEl = document.getElementById('typingIndicator');
        if (typingEl) typingEl.remove();

        messagesContainer.innerHTML += `
            <div class="message bot-message">
                <div class="message-avatar"><i class="fas fa-robot"></i></div>
                <div class="message-content">
                    <p>Unable to connect to AI service. Please check your internet connection.</p>
                    <p class="disclaimer-note"><i class="fas fa-info-circle"></i> This feature requires internet access.</p>
                </div>
            </div>
        `;
    }

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function handleChatKeypress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function formatAnswer(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getLocationAndAssess() {
    if (!navigator.geolocation) {
        document.getElementById('dashboardContent').innerHTML = '<div class="empty-state"><i class="fas fa-map-marker-alt"></i><h3>Geolocation Not Supported</h3><p>Your browser does not support geolocation. Please enter coordinates manually.</p></div>';
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (position) => {
            assessRisk(position.coords.latitude, position.coords.longitude);
        },
        (error) => {
            document.getElementById('dashboardContent').innerHTML = `<div class="empty-state"><i class="fas fa-map-marker-alt"></i><h3>Location Access Denied</h3><p>${error.message}. Please enter coordinates manually below.</p></div>`;
        }
    );
}

function manualLocationAssess() {
    const lat = parseFloat(document.getElementById('manualLat').value);
    const lon = parseFloat(document.getElementById('manualLon').value);

    if (isNaN(lat) || isNaN(lon)) {
        alert('Please enter valid coordinates.');
        return;
    }

    assessRisk(lat, lon);
}

async function assessRisk(lat, lon) {
    const container = document.getElementById('dashboardContent');
    container.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><p>Assessing risk for your location...</p></div>';

    try {
        const response = await fetch('/api/online/risk-assessment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lon })
        });
        const data = await response.json();
        renderDashboard(data);
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><h3>Failed to assess risk</h3><p>Please check your connection and try again.</p></div>';
    }
}

function renderDashboard(data) {
    const container = document.getElementById('dashboardContent');

    let html = '';

    if (data.location && data.location.data) {
        const loc = data.location.data;
        const city = loc.features?.[0]?.properties?.city || 'Unknown';
        const country = loc.features?.[0]?.properties?.country || 'Unknown';
        html += `<div class="risk-card" style="margin-bottom:1.5rem"><h3><i class="fas fa-map-marker-alt" style="color:var(--primary)"></i> ${city}, ${country}</h3></div>`;
    }

    if (data.weather) {
        const current = data.weather.current || {};
        html += `
            <div class="risk-card" style="margin-bottom:1.5rem">
                <h3><i class="fas fa-cloud-sun" style="color:var(--info)"></i> Current Weather</h3>
                <p>Temperature: ${current.temperature_2m || 'N/A'}°C</p>
                <p>Humidity: ${current.relative_humidity_2m || 'N/A'}%</p>
                <p>Precipitation: ${current.precipitation || 'N/A'} mm</p>
            </div>
        `;
    }

    if (data.risks && data.risks.length > 0) {
        html += '<h3 style="margin-bottom:1rem"><i class="fas fa-exclamation-triangle" style="color:var(--warning)"></i> High Risk Diseases in Your Area</h3>';
        html += '<div class="risk-grid">';
        html += data.risks.map(risk => `
            <div class="risk-card">
                <span class="risk-level ${risk.risk_level?.toLowerCase() || 'medium'}">${risk.risk_level || 'Unknown'} Risk</span>
                <h3>${risk.disease}</h3>
                <p>${risk.reason || risk.message || ''}</p>
                <p style="font-size:0.8rem;color:var(--text-muted);margin-top:0.5rem">Source: ${risk.source || 'N/A'}</p>
            </div>
        `).join('');
        html += '</div>';
    } else {
        html += '<div class="risk-card" style="margin-bottom:1.5rem"><h3><i class="fas fa-check-circle" style="color:var(--success)"></i> No Elevated Risks Detected</h3><p style="color:var(--text-secondary)">Current conditions do not indicate elevated disease risk for your area.</p></div>';
    }

    if (data.smart_alerts && data.smart_alerts.length > 0) {
        html += '<div class="alerts-container">';
        html += '<h3><i class="fas fa-bell" style="color:var(--warning)"></i> Smart Alerts</h3>';
        html += data.smart_alerts.map(alert => `
            <div class="alert-item ${alert.severity}">
                <i class="fas ${alert.severity === 'critical' ? 'fa-radiation' : alert.severity === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle'}"></i>
                <p>${alert.message}</p>
            </div>
        `).join('');
        html += '</div>';
    }

    container.innerHTML = html;
}

function saveToHistory(symptomIds, results) {
    try {
        const history = JSON.parse(localStorage.getItem('mediscan_history') || '[]');
        const entry = {
            date: new Date().toISOString(),
            symptoms: Array.from(symptomIds).map(id => {
                const s = allSymptoms.find(s => s.id === id);
                return s ? s.name : 'Unknown';
            }),
            top_result: results[0]?.name || null,
            match_percentage: results[0]?.match_percentage || 0
        };
        history.unshift(entry);
        if (history.length > 50) history.pop();
        localStorage.setItem('mediscan_history', JSON.stringify(history));
    } catch (e) {
        console.error('Failed to save history:', e);
    }
}

function loadHistory() {
    // History is used for internal tracking; can be extended for a history page
}
