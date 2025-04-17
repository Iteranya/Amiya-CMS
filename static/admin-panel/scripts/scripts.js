document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = '/admin'; // Your FastAPI prefix
    const pageForm = document.getElementById('page-form');
    const editSlugField = document.getElementById('edit-slug');
    const titleField = document.getElementById('title');
    const slugField = document.getElementById('slug');
    const tagsField = document.getElementById('tags');
    const markdownField = document.getElementById('markdown');
    const contentField = document.getElementById('content');
    const htmlField = document.getElementById('html'); // Added this field
    const saveButton = document.getElementById('save-button');
    const clearButton = document.getElementById('clear-button');
    const siteBuilderButton = document.getElementById('site-builder-button');
    const pagesTableBody = document.querySelector('#pages-table tbody');
    const searchBox = document.getElementById('search-box');
    const statusMessageDiv = document.getElementById('status-message');

    let allPagesData = []; // Cache fetched pages for filtering and editing

    // --- Utility Functions ---

    function showStatus(message, isError = false) {
        statusMessageDiv.textContent = message;
        statusMessageDiv.className = `status ${isError ? 'error' : 'success'}`;
        // Auto-hide after 5 seconds
        setTimeout(() => {
            statusMessageDiv.textContent = '';
            statusMessageDiv.className = 'status';
        }, 5000);
    }

    function clearForm() {
        pageForm.reset();
        editSlugField.value = '';
        saveButton.textContent = 'Add Page';
        siteBuilderButton.disabled = true; // Disable site builder when form is cleared
        slugField.readOnly = false; // Make slug editable for new pages
        // Optionally scroll to top or form
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Function to format tags string into a JSON string list if needed
    // Based on your backend `tags: str = Form("[]")`, it might expect a string
    // that looks like a JSON list. If it just expects a plain string, remove JSON.stringify.
    // Let's assume it expects a simple comma-separated string for now based on the usage.
    // If the backend expects a JSON string like '["tag1", "tag2"]':
    /*
    function formatTagsForApi(tagsString) {
        if (!tagsString || tagsString.trim() === '') {
            return '[]';
        }
        const tagsArray = tagsString.split(',').map(tag => tag.trim()).filter(tag => tag !== '');
        return JSON.stringify(tagsArray);
    }
    */
   // Let's keep it simple and send the raw string for now, assuming backend handles it.
    function formatTagsForApi(tagsString) {
        return tagsString; // Send raw string
    }
    // If backend returns a JSON string for tags, parse it for display
    function parseTagsForDisplay(tagsData) {
        if (!tagsData) return '';
        // Check if it looks like a JSON array string '["a","b"]'
        if (typeof tagsData === 'string' && tagsData.startsWith('[') && tagsData.endsWith(']')) {
            try {
                const tagsArray = JSON.parse(tagsData);
                return Array.isArray(tagsArray) ? tagsArray.join(', ') : tagsData; // Join back for display
            } catch (e) {
                return tagsData; // Return original string if parsing fails
            }
        }
        // If it's already an array (less likely from Form(...)) or just a string
        return Array.isArray(tagsData) ? tagsData.join(', ') : String(tagsData);
    }


    // --- API Interaction ---

    async function fetchPages() {
        try {
            const response = await fetch(`${API_BASE_URL}/list`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            allPagesData = await response.json();
            renderTable(allPagesData);
        } catch (error) {
            console.error('Error fetching pages:', error);
            showStatus(`Error fetching pages: ${error.message}`, true);
            allPagesData = []; // Clear cache on error
            renderTable([]); // Clear table
        }
    }

    async function deletePage(slug) {
        if (!confirm(`Are you sure you want to delete the page with slug: ${slug}?`)) {
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
            fetchPages(); // Refresh the list
            if (editSlugField.value === slug) { // If the deleted page was being edited
                clearForm();
            }
        } catch (error) {
            console.error('Error deleting page:', error);
            showStatus(`Error deleting page: ${error.message}`, true);
        }
    }

    async function savePage(event) {
        event.preventDefault(); // Prevent default HTML form submission
        const currentEditSlug = editSlugField.value;
        const isUpdating = !!currentEditSlug;

        // --- Prepare Data ---
        // Use FormData for POST as the backend expects Form(...)
        // Use JSON for PUT as the backend example expects a dict (though it could also use Form)
        let requestBody;
        let requestUrl;
        let requestMethod;
        let headers = {};

        const slugValue = slugField.value.trim();
        const titleValue = titleField.value.trim();
        const tagsValue = formatTagsForApi(tagsField.value.trim()); // Format tags
        const markdownValue = markdownField.value;
        const contentValue = contentField.value;
        const htmlValue = htmlField.value; // Get HTML value

        if (isUpdating) {
            // --- UPDATE (PUT) ---
            requestUrl = `${API_BASE_URL}/update/${currentEditSlug}`;
            requestMethod = 'PUT';
            headers['Content-Type'] = 'application/json';
            // The PUT endpoint expects a dictionary of fields to update.
            // Send all fields from the form. The backend should handle this.
            requestBody = JSON.stringify({
                title: titleValue,
                slug: slugValue, // Send the potentially updated slug
                tags: tagsValue,
                markdown: markdownValue,
                content: contentValue,
                html: htmlValue // Include html field
            });
        } else {
            // --- ADD (POST) ---
            requestUrl = `${API_BASE_URL}/add`;
            requestMethod = 'POST';
            // FastAPI's Form(...) expects 'multipart/form-data' or 'application/x-www-form-urlencoded'
            // FormData handles this automatically.
            const formData = new FormData();
            formData.append('title', titleValue);
            formData.append('slug', slugValue);
            formData.append('tags', tagsValue);
            formData.append('markdown', markdownValue);
            formData.append('content', contentValue);
            formData.append('html', htmlValue); // Include html field
            requestBody = formData;
            // No 'Content-Type' header needed; fetch sets it for FormData
        }

        // --- Send Request ---
        try {
            const response = await fetch(requestUrl, {
                method: requestMethod,
                headers: headers, // Empty for POST with FormData
                body: requestBody
            });

            const result = await response.json(); // Try parsing JSON regardless of status for error details

            if (!response.ok) {
                // FastAPI often returns errors in 'detail' field
                throw new Error(result.detail || `HTTP error! status: ${response.status}`);
            }

            showStatus(result.message || `Page ${isUpdating ? 'updated' : 'created'} successfully.`);
            clearForm(); // Clear form on success
            fetchPages(); // Refresh list

            // Special handling after save if Site Builder was intended next
            if (window.pendingSiteBuilderNav) {
                 // Use the slug from the form *after* potential update/add
                const finalSlug = slugField.value.trim();
                navigateToSiteBuilder(finalSlug);
                window.pendingSiteBuilderNav = false; // Reset flag
            }

        } catch (error) {
            console.error(`Error ${isUpdating ? 'updating' : 'adding'} page:`, error);
            showStatus(`Error: ${error.message}`, true);
            window.pendingSiteBuilderNav = false; // Reset flag on error
        }
    }

    // --- UI Rendering and Event Handlers ---

    function renderTable(pages) {
        pagesTableBody.innerHTML = ''; // Clear existing rows
        if (!pages || pages.length === 0) {
            pagesTableBody.innerHTML = '<tr><td colspan="4">No pages found.</td></tr>';
            return;
        }

        pages.forEach(page => {
            const row = pagesTableBody.insertRow();
            row.setAttribute('data-slug', page.slug); // Store slug for easy access

            row.insertCell().textContent = page.title;
            row.insertCell().textContent = page.slug;
            row.insertCell().textContent = parseTagsForDisplay(page.tags); // Display parsed tags

            // Actions cell
            const actionsCell = row.insertCell();
            const editButton = document.createElement('button');
            editButton.textContent = 'Edit';
            editButton.classList.add('action-button', 'edit-button');
            editButton.onclick = () => prepareEdit(page.slug);
            actionsCell.appendChild(editButton);

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.classList.add('action-button', 'delete-button');
            deleteButton.onclick = () => deletePage(page.slug);
            actionsCell.appendChild(deleteButton);
        });
    }

    function prepareEdit(slug) {
        const pageData = allPagesData.find(p => p.slug === slug);
        if (!pageData) {
            showStatus(`Could not find page data for slug: ${slug}`, true);
            return;
        }

        editSlugField.value = pageData.slug;
        titleField.value = pageData.title;
        slugField.value = pageData.slug;
        tagsField.value = parseTagsForDisplay(pageData.tags); // Use parsed tags for editing
        markdownField.value = pageData.markdown || '';
        contentField.value = pageData.content || '';
        htmlField.value = pageData.html || ''; // Populate html field

        saveButton.textContent = 'Save Changes';
        siteBuilderButton.disabled = false; // Enable site builder button when editing
        slugField.readOnly = false; // Allow slug editing (backend needs to handle lookup by old slug)

        // Scroll to the form for better UX
        const editArea = document.getElementById('edit-area');
         if (editArea) {
             editArea.scrollIntoView({ behavior: 'smooth' });
         }
    }

    function filterTable() {
        const searchTerm = searchBox.value.toLowerCase();
        const filteredPages = allPagesData.filter(page =>
            page.title.toLowerCase().includes(searchTerm) ||
            page.slug.toLowerCase().includes(searchTerm)
        );
        renderTable(filteredPages);
    }

    function navigateToSiteBuilder(slug) {
        if (!slug) {
            showStatus("Cannot navigate to Site Builder without a valid slug.", true);
            return;
        }
        console.log(`Navigating to site builder for slug: ${slug}`);
        window.location.href = `/site-builder?slug=${encodeURIComponent(slug)}`;
    }

    function handleSiteBuilderClick() {
        // Set a flag indicating the user wants to navigate after saving
        window.pendingSiteBuilderNav = true;
        // Trigger the save process
        savePage(new Event('submit', { cancelable: true })); // Simulate form submission
        // The actual navigation will happen inside savePage's success handler
    }


    // --- Initial Setup ---
    pageForm.addEventListener('submit', savePage);
    clearButton.addEventListener('click', clearForm);
    searchBox.addEventListener('input', filterTable);
    siteBuilderButton.addEventListener('click', handleSiteBuilderClick);

    fetchPages(); // Load initial data
});