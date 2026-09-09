/* Main JavaScript Application Logic */

const API_BASE = '/api';
const TOKEN_KEY = 'auth_token';

// Get JWT token from localStorage
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

// Set JWT token
function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

// Remove JWT token
function removeToken() {
    localStorage.removeItem(TOKEN_KEY);
}

// API Request with Authorization
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            removeToken();
            window.location.href = '/login';
            return null;
        }

        const data = await response.json();
        return { status: response.status, data };
    } catch (error) {
        console.error('API Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
        return null;
    }
}

// Show Alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.insertBefore(alertDiv, document.body.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format Date Time
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Load Notifications
function loadNotifications() {
    // Fetch and display notifications
    apiRequest('/patient/notifications').then(response => {
        if (response && response.data.notifications) {
            const count = response.data.notifications.length;
            const badge = document.getElementById('notification-count');
            if (badge) {
                badge.textContent = count;
            }
        }
    });
}

// Logout
function logout() {
    removeToken();
    window.location.href = '/login';
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    if (getToken()) {
        loadNotifications();
        // Refresh notifications every 30 seconds
        setInterval(loadNotifications, 30000);
    }
});
