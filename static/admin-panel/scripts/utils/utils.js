// --- Utility Functions ---
function formatTagsForApi(tagsString) {
    return tagsString.split(',')
                    .map(tag => tag.trim().toLowerCase())
                    .filter(tag => tag.length > 0);
}

function parseTagsForDisplay(tagsData) {
    if (!tagsData) return '';
    try {
        const tagsArray = (typeof tagsData === 'string') ? JSON.parse(tagsData) : tagsData;
        return Array.isArray(tagsArray) ? tagsArray.join(', ') : String(tagsData);
    } catch (e) {
        return String(tagsData);
    }
}

function showStatus(message, isError = false) {
    const statusMessageDiv = domElements.statusMessage;
    statusMessageDiv.innerHTML = `<i class="fas ${isError ? 'fa-exclamation-circle' : 'fa-check-circle'}"></i> ${message}`;
    statusMessageDiv.className = `status ${isError ? 'error' : 'success'}`;
    statusMessageDiv.style.display = 'flex';
    
    window.scrollTo({ top: 0, behavior: 'smooth' });

    setTimeout(() => {
        statusMessageDiv.textContent = '';
        statusMessageDiv.className = 'status';
        statusMessageDiv.style.display = 'none';
    }, 5000);
}