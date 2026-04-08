// DOM Elements
const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('message');
const resultContainer = document.getElementById('resultContainer');
const resultContent = document.getElementById('resultContent');

const gmailLoginForm = document.getElementById('gmailLoginForm');
const gmailLoginCard = document.getElementById('gmailLoginCard');
const gmailDashboard = document.getElementById('gmailDashboard');
const scanBtn = document.getElementById('scanBtn');
const deleteBtn = document.getElementById('deleteBtn');
const disconnectBtn = document.getElementById('disconnectBtn');

const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressPercent = document.getElementById('progressPercent');
const messagesList = document.getElementById('messagesList');

const statTotal = document.getElementById('stat-total');
const statFake = document.getElementById('stat-fake');
const statReal = document.getElementById('stat-real');

// State
let gmailAuthenticated = false;
let selectedFakeMessages = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateNavigation();
});

function setupEventListeners() {
    messageForm.addEventListener('submit', handleMessageSubmit);
    gmailLoginForm.addEventListener('submit', handleGmailLogin);
    scanBtn.addEventListener('click', handleScanGmail);
    deleteBtn.addEventListener('click', handleDeleteFakeMessages);
    disconnectBtn.addEventListener('click', handleDisconnect);
    
    // Smooth scroll for nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

// ==================== Message Analysis ====================

async function handleMessageSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    
    if (!message) {
        showError('Please enter a message');
        return;
    }

    const submitBtn = messageForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<svg class="btn-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1" fill="currentColor"><animate attributeName="r" from="1" to="8" dur="1.5s" repeatCount="indefinite" /></circle></svg>Analyzing...';

    try {
        const formData = new FormData();
        formData.append('message', message);

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        displayResult(data);
    } catch (error) {
        showError(error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}

function displayResult(data) {
    const isFake = data.is_fake;
    const result = data.result;
    const confidence = data.confidence;

    const html = `
        <div class="result-content ${isFake ? 'fake' : 'real'}">
            <div class="result-title">
                ${isFake ? '⚠️ Fake Message Detected' : '✓ Legitimate Message'}
            </div>
            <div class="result-confidence">
                <strong>Result:</strong> ${result}
            </div>
            <div class="result-confidence">
                <strong>Confidence:</strong> ${confidence}
            </div>
            ${isFake ? `
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); color: var(--text-secondary); font-size: 0.9rem;">
                    <strong>⚠️ Warning:</strong> This message appears to be spam, phishing, or fraudulent. Do not click any links or provide personal information.
                </div>
            ` : `
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); color: var(--text-secondary); font-size: 0.9rem;">
                    <strong>✓ Safe:</strong> This message appears to be legitimate. However, always exercise caution with sensitive information.
                </div>
            `}
        </div>
    `;

    resultContent.innerHTML = html;
    resultContainer.classList.remove('hidden');
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

// ==================== Gmail Integration ====================

async function handleGmailLogin(e) {
    e.preventDefault();

    const email = document.getElementById('gmailEmail').value.trim();
    const password = document.getElementById('gmailPassword').value;

    if (!email || !password) {
        showError('Please enter both email and password');
        return;
    }

    const submitBtn = gmailLoginForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<svg class="btn-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1" fill="currentColor"><animate attributeName="r" from="1" to="8" dur="1.5s" repeatCount="indefinite" /></circle></svg>Connecting...';

    try {
        const response = await fetch('/gmail-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }

        gmailAuthenticated = true;
        gmailLoginCard.style.display = 'none';
        gmailDashboard.classList.remove('hidden');
        showSuccess('Gmail connected successfully!');

    } catch (error) {
        showError(error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}

async function handleScanGmail() {
    if (!gmailAuthenticated) {
        showError('Please connect Gmail first');
        return;
    }

    scanBtn.disabled = true;
    deleteBtn.disabled = true;
    selectedFakeMessages = [];
    messagesList.innerHTML = '';

    try {
        // Start scanning
        const response = await fetch('/check-gmail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Scan failed');
        }

        // Show progress bar
        progressContainer.classList.remove('hidden');
        
        // Poll for stats
        const pollInterval = setInterval(async () => {
            const statsResponse = await fetch('/gmail-stats');
            const stats = await statsResponse.json();

            // Update progress
            progressFill.style.width = stats.progress + '%';
            progressPercent.textContent = stats.progress + '%';

            // Update main stats
            statTotal.textContent = stats.total_messages;
            statFake.textContent = stats.fake_messages;
            statReal.textContent = stats.real_messages;

            // Update messages list
            displayMessagesList(stats.messages_data);

            if (!stats.processing) {
                clearInterval(pollInterval);
                progressContainer.classList.add('hidden');
                
                if (stats.fake_messages > 0) {
                    deleteBtn.disabled = false;
                    showSuccess(`Scan complete! Found ${stats.fake_messages} fake message(s)`);
                } else {
                    showSuccess('Scan complete! No fake messages found');
                }
            }
        }, 500);

    } catch (error) {
        showError(error.message);
        scanBtn.disabled = false;
    }
}

function displayMessagesList(messages) {
    messagesList.innerHTML = '';

    if (messages.length === 0) {
        messagesList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No messages scanned yet</p>';
        return;
    }

    messages.forEach(msg => {
        const div = document.createElement('div');
        div.className = `message-item ${msg.is_fake ? 'fake' : 'real'}`;
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.style.width = '20px';
        checkbox.style.height = '20px';
        checkbox.style.cursor = 'pointer';
        checkbox.disabled = !msg.is_fake;
        
        if (msg.is_fake) {
            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    selectedFakeMessages.push(msg.id);
                } else {
                    selectedFakeMessages = selectedFakeMessages.filter(id => id !== msg.id);
                }
            });
        }

        const infoDiv = document.createElement('div');
        infoDiv.className = 'message-info';
        infoDiv.innerHTML = `
            <div class="message-subject">${escapeHtml(msg.subject || 'No Subject')}</div>
            <div class="message-from">${escapeHtml(msg.from || 'Unknown')}</div>
        `;

        const badgeDiv = document.createElement('div');
        badgeDiv.className = `message-badge ${msg.is_fake ? 'fake' : 'real'}`;
        badgeDiv.textContent = msg.is_fake ? `🚨 Fake (${msg.confidence})` : `✓ Real`;

        const wrapper = document.createElement('div');
        wrapper.style.display = 'flex';
        wrapper.style.alignItems = 'center';
        wrapper.style.gap = '1rem';

        if (msg.is_fake) {
            wrapper.appendChild(checkbox);
        }
        wrapper.appendChild(infoDiv);
        wrapper.appendChild(badgeDiv);

        div.appendChild(wrapper);
        messagesList.appendChild(div);
    });
}

async function handleDeleteFakeMessages() {
    if (selectedFakeMessages.length === 0) {
        showError('Please select fake messages to delete');
        return;
    }

    const confirmed = confirm(`Delete ${selectedFakeMessages.length} fake message(s)? This action cannot be undone.`);
    
    if (!confirmed) return;

    deleteBtn.disabled = true;
    deleteBtn.innerHTML = '<svg class="btn-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1" fill="currentColor"><animate attributeName="r" from="1" to="8" dur="1.5s" repeatCount="indefinite" /></circle></svg>Deleting...';

    try {
        const response = await fetch('/delete-fake-messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message_ids: selectedFakeMessages
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Delete failed');
        }

        showSuccess(`${data.deleted_count} message(s) deleted successfully!`);
        selectedFakeMessages = [];
        
        // Refresh scan
        await handleScanGmail();

    } catch (error) {
        showError(error.message);
    } finally {
        deleteBtn.disabled = true;
        deleteBtn.innerHTML = '<svg class="btn-icon" viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>Delete Fake Messages';
    }
}

function handleDisconnect() {
    gmailAuthenticated = false;
    gmailLoginCard.style.display = 'block';
    gmailDashboard.classList.add('hidden');
    gmailLoginForm.reset();
    messagesList.innerHTML = '';
    selectedFakeMessages = [];
    showSuccess('Disconnected from Gmail');
}

// ==================== Utility Functions ====================

function showError(message) {
    showNotification(message, 'error');
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        background: ${type === 'error' ? 'rgba(239, 68, 68, 0.9)' : 'rgba(16, 185, 129, 0.9)'};
        color: white;
        font-weight: 600;
        z-index: 1000;
        animation: slideUp 0.3s ease-out;
        max-width: 400px;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function updateNavigation() {
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}
