// --- Initialization Functions ---
function initDOMElements() {
    domElements = {
        pageForm: document.getElementById(ELEMENT_IDS.PAGE_FORM),
        editSlug: document.getElementById(ELEMENT_IDS.EDIT_SLUG),
        title: document.getElementById(ELEMENT_IDS.TITLE),
        slug: document.getElementById(ELEMENT_IDS.SLUG),
        tags: document.getElementById(ELEMENT_IDS.TAGS),
        markdown: document.getElementById(ELEMENT_IDS.MARKDOWN),
        content: document.getElementById(ELEMENT_IDS.CONTENT),
        html: document.getElementById(ELEMENT_IDS.HTML),
        saveButton: document.getElementById(ELEMENT_IDS.SAVE_BUTTON),
        clearButton: document.getElementById(ELEMENT_IDS.CLEAR_BUTTON),
        siteBuilderLink: document.getElementById(ELEMENT_IDS.SITE_BUILDER_LINK),
        pagesTableBody: document.querySelector(ELEMENT_IDS.PAGES_TABLE_BODY),
        searchBox: document.getElementById(ELEMENT_IDS.SEARCH_BOX),
        statusMessage: document.getElementById(ELEMENT_IDS.STATUS_MESSAGE),
        editFormTitle: document.getElementById(ELEMENT_IDS.EDIT_FORM_TITLE),
        noPagesMessage: document.getElementById(ELEMENT_IDS.NO_PAGES_MESSAGE),
        newPageButton: document.getElementById(ELEMENT_IDS.NEW_PAGE_BUTTON)
    };
}

function initEventListeners() {
    domElements.pageForm.addEventListener('submit', savePage);
    domElements.clearButton.addEventListener('click', clearForm);
    domElements.newPageButton.addEventListener('click', prepareNewPage);
    domElements.searchBox.addEventListener('input', filterTable);
    domElements.title.addEventListener('input', updateSiteBuilderLink);
    domElements.slug.addEventListener('input', updateSiteBuilderLink);
    
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            switchTab(button.dataset.tab);
        });
    });
}

function initApp() {
    initDOMElements();
    initEventListeners();
    fetchPages();
    updateSiteBuilderLink();
    switchTab('manage-tab');
}