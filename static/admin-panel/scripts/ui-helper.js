// --- UI Helper Functions ---
function switchTab(targetTabId) {
    document.querySelectorAll('.tab-button, .tab-content').forEach(el => {
        el.classList.remove('active');
    });

    const targetTabButton = document.querySelector(`.tab-button[data-tab="${targetTabId}"]`);
    const targetTabContent = document.getElementById(targetTabId);

    if (targetTabButton && targetTabContent) {
        targetTabButton.classList.add('active');
        targetTabContent.classList.add('active');
    }
    
    if (targetTabId === 'manage-tab') {
        fetchPages(); 
    }
}

function clearForm() {
    domElements.pageForm.reset();
    domElements.editSlug.value = '';
    domElements.saveButton.innerHTML = '<i class="fas fa-plus"></i> Add Page';
    domElements.saveButton.classList.remove('button-primary');
    domElements.saveButton.classList.add('button-success');
    domElements.slug.readOnly = false;
    domElements.slug.style.backgroundColor = '';
    domElements.slug.style.cursor = '';
    domElements.editFormTitle.innerHTML = '<i class="fas fa-file-alt"></i> Add New Page';
    updateSiteBuilderLink();
    domElements.title.focus();
}

function prepareNewPage() {
    clearForm();
    switchTab('edit-tab');
    domElements.title.focus();
}

function renderTable(pages) {
    domElements.pagesTableBody.innerHTML = '';
    if (!pages || pages.length === 0) {
        domElements.noPagesMessage.style.display = 'block';
        domElements.pagesTableBody.style.display = 'none';
        return;
    }
    
    domElements.noPagesMessage.style.display = 'none';
    domElements.pagesTableBody.style.display = '';

    pages.sort((a, b) => a.title.localeCompare(b.title));

    pages.forEach(page => {
        const row = domElements.pagesTableBody.insertRow();
        row.setAttribute('data-slug', page.slug);

        row.insertCell().textContent = page.title;
        row.insertCell().textContent = page.slug;
        row.insertCell().textContent = parseTagsForDisplay(page.tags);

        const actionsCell = row.insertCell();
        actionsCell.classList.add('action-buttons-cell');

        const editButton = document.createElement('button');
        editButton.innerHTML = '<i class="fas fa-pencil-alt"></i> Edit';
        editButton.classList.add('button', 'button-info', 'action-button');
        editButton.onclick = (e) => {
            e.stopPropagation();
            prepareEdit(page.slug);
        };
        actionsCell.appendChild(editButton);

        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i> Delete';
        deleteButton.classList.add('button', 'button-danger', 'action-button');
        deleteButton.onclick = (e) => {
            e.stopPropagation();
            deletePage(page.slug);
        };
        actionsCell.appendChild(deleteButton);
        
        row.onclick = () => prepareEdit(page.slug);
        row.style.cursor = 'pointer';
    });
}

function prepareEditUI(slug) {
    domElements.editFormTitle.innerHTML = `<i class="fas fa-edit"></i> Edit Page: ${slug}`;
    domElements.saveButton.innerHTML = '<i class="fas fa-save"></i> Save Changes';
    domElements.saveButton.classList.remove('button-success');
    domElements.saveButton.classList.add('button-primary');
    domElements.slug.readOnly = true;
    domElements.slug.style.backgroundColor = '';
    domElements.slug.style.cursor = '';
    updateSiteBuilderLink();
}

function prepareEdit(slug) {
    const pageData = allPagesData.find(p => p.slug === slug);
    if (!pageData) {
        showStatus(`Could not find page data for slug: ${slug}`, true);
        return;
    }

    domElements.editSlug.value = pageData.slug;
    domElements.title.value = pageData.title;
    domElements.slug.value = pageData.slug;
    domElements.tags.value = parseTagsForDisplay(pageData.tags);
    domElements.markdown.value = pageData.markdown || '';
    domElements.content.value = pageData.content || '';
    domElements.html.value = pageData.html || '';

    prepareEditUI(pageData.slug);
    switchTab('edit-tab');
    domElements.pageForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function filterTable() {
    const searchTerm = domElements.searchBox.value.toLowerCase().trim();
    const filteredPages = allPagesData.filter(page =>
        page.title.toLowerCase().includes(searchTerm) ||
        page.slug.toLowerCase().includes(searchTerm) ||
        parseTagsForDisplay(page.tags).toLowerCase().includes(searchTerm)
    );
    renderTable(filteredPages);
}

function updateSiteBuilderLink() {
    const title = domElements.title.value.trim();
    const slug = domElements.slug.value.trim();

    if (title && slug) {
        domElements.siteBuilderLink.removeAttribute('disabled');
        domElements.siteBuilderLink.classList.remove('button-disabled');
        domElements.siteBuilderLink.href = `/site-builder?slug=${encodeURIComponent(slug)}`;
        domElements.siteBuilderLink.style.pointerEvents = '';
        domElements.siteBuilderLink.style.opacity = '1';
    } else {
        domElements.siteBuilderLink.setAttribute('disabled', true);
        domElements.siteBuilderLink.classList.add('button-disabled');
        domElements.siteBuilderLink.removeAttribute('href');
        domElements.siteBuilderLink.style.pointerEvents = 'none';
        domElements.siteBuilderLink.style.opacity = '0.7';
    }
}