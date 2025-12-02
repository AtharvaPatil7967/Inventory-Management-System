// Main JavaScript for Inventory Management System

// Show loading spinner
function showLoading(buttonElement) {
    if (buttonElement) {
        buttonElement.disabled = true;
        const originalText = buttonElement.innerHTML;
        buttonElement.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        return originalText;
    }
}

// Hide loading spinner
function hideLoading(buttonElement, originalText) {
    if (buttonElement && originalText) {
        buttonElement.disabled = false;
        buttonElement.innerHTML = originalText;
    }
}

// Show success toast
function showSuccess(message) {
    // Simple alert for now - can be replaced with toast library
    alert('✓ ' + message);
}

// Show error toast
function showError(message) {
    alert('✗ Error: ' + message);
}

// Format currency
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Validate form inputs
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }
    return true;
}

// Confirm action
function confirmAction(message) {
    return confirm(message);
}

// Get today's date in YYYY-MM-DD format
function getTodayDate() {
    return new Date().toISOString().split('T')[0];
}

// Debounce function for search
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

// Initialize tooltips (Bootstrap)
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips if any
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (typeof bootstrap !== 'undefined') {
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Handle API errors
function handleApiError(error, customMessage = 'An error occurred') {
    console.error('API Error:', error);
    showError(customMessage);
}

// Export data to CSV
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Convert JSON to CSV
function convertToCSV(objArray) {
    const array = typeof objArray !== 'object' ? JSON.parse(objArray) : objArray;
    let str = '';
    
    // Header
    const headers = Object.keys(array[0]);
    str += headers.join(',') + '\r\n';
    
    // Rows
    for (let i = 0; i < array.length; i++) {
        let line = '';
        for (let index in array[i]) {
            if (line !== '') line += ',';
            line += array[i][index];
        }
        str += line + '\r\n';
    }
    
    return str;
}

// Print current page
function printPage() {
    window.print();
}

// Filter table rows
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {
        const td = tr[i].getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                const txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        tr[i].style.display = found ? '' : 'none';
    }
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
});

// Check if user is online
window.addEventListener('online', function() {
    console.log('Connection restored');
});

window.addEventListener('offline', function() {
    alert('⚠️ No internet connection. Some features may not work.');
});

console.log('Inventory Management System loaded successfully!');
