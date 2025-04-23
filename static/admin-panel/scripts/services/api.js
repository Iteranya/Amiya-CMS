// --- API Service Functions ---
async function fetchPages() {
    try {
        const response = await fetch(`${API_BASE_URL}/list`);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error fetching pages' }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        allPagesData = await response.json();
        renderTable(allPagesData);
    } catch (error) {
        console.error('Error fetching pages:', error);
        showStatus(`Error fetching pages: ${error.message}`, true);
        allPagesData = [];
        renderTable([]);
    }
}

async function deletePage(slug) {
    if (!confirm(`Are you sure you want to delete the page "${slug}"? This action cannot be undone.`)) {
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/delete/${slug}`, {
            method: 'DELETE',
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.detail || `HTTP error! status: ${response.status}`);
        }
        showStatus(result.message || `Page '${slug}' deleted successfully.`);
        fetchPages();
        if (domElements.editSlug.value === slug) {
            clearForm();
        }
    } catch (error) {
        console.error('Error deleting page:', error);
        showStatus(`Error deleting page: ${error.message}`, true);
    }
}

async function savePage(event) {
    event.preventDefault();
    const currentEditSlug = domElements.editSlug.value;
    const isUpdating = !!currentEditSlug;
    
    const slugValue = domElements.slug.value.trim();
    const titleValue = domElements.title.value.trim();
    const tagsValue = formatTagsForApi(domElements.tags.value.trim() || "");
    const markdownValue = domElements.markdown.value.trim() || "";
    const contentValue = domElements.content.value.trim() || "";
    const htmlValue = domElements.html.value.trim() || "";

    if (!titleValue || !slugValue) {
        showStatus("Title and Slug are required.", true);
        return null;
    }
    if (!/^[a-z0-9\-]+$/.test(slugValue)) {
        showStatus("Slug can only contain lowercase letters, numbers, and hyphens.", true);
        return null;
    }
    
    let requestUrl;
    let requestMethod;
    let headers = { 'Content-Type': 'application/json' };

    const payload = {
        title: titleValue,
        slug: slugValue,
        tags: tagsValue,
        markdown: markdownValue,
        content: contentValue,
        html: htmlValue
    };

    if (isUpdating) {
        requestUrl = `${API_BASE_URL}/update/${currentEditSlug}`;
        requestMethod = 'PUT';
    } else {
        requestUrl = `${API_BASE_URL}/add`;
        requestMethod = 'POST';
    }

    domElements.saveButton.disabled = true;
    domElements.saveButton.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${isUpdating ? 'Saving...' : 'Adding...'}`;

    try {
        const response = await fetch(requestUrl, {
            method: requestMethod,
            headers: headers,
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            let errorMsg = result.detail;

            if (Array.isArray(errorMsg) && errorMsg.length > 0) {
                // Pydantic-style validation error
                errorMsg = errorMsg.map(err => `${err.loc?.[err.loc.length - 1] || 'field'}: ${err.msg}`).join('; ');
            } else if (typeof errorMsg === 'string') {
                // Use the plain error message
                // (like from slug validation or duplicates)
                // Keep as-is
            } else {
                // Fallback
                errorMsg = `Unexpected error. Status: ${response.status}`;
            }
            
            // Show the error message to the user
            showStatus(errorMsg, true);
            
            // Reset button state
            domElements.saveButton.innerHTML = isUpdating ? 'Save Changes' : 'Add Page';
            return null;
        }

        // Success case
        showStatus(result.message || `Page ${isUpdating ? 'updated' : 'added'} successfully.`);
        fetchPages();
        
        if (isUpdating) {
            prepareEditUI(slugValue);
        } else {
            clearForm();
        }
        
        return slugValue;
    } catch (error) {
        console.error(`Error ${isUpdating ? 'updating' : 'adding'} page:`, error);
        showStatus(`Error: ${error.message}`, true);
        return null;
    } finally {
        domElements.saveButton.disabled = false;
        domElements.saveButton.innerHTML = isUpdating ? 'Save Changes' : 'Add Page';
    }
}