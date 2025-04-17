/**
 * Set up deployment functionality
 * @param {HTMLTextAreaElement} htmlCode - The HTML editor element
 */
function setupDeployment(htmlCode) {
    // Get the deploy button element
    const deployBtn = document.getElementById('deploy-btn');
    // Get the site title input element
    const siteTitleInput = document.getElementById('site-title');

    // Handle deployment when the deploy button is clicked
    deployBtn.addEventListener('click', async () => {
        const title = siteTitleInput.value;
        const content = htmlCode.value;

        if (!title) {
            alert('Please enter a site title!');
            return;
        }

        try {
            const response = await fetch('/save-html', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: content,
                    title: title
                })
            });

            const result = await response.json();

            if (response.ok) {
                showNotification(`Site deployed successfully! 🎉 Access it at <a href="/${result.path}" target="_blank">${result.path}</a>`, 'success');
            } else {
                showNotification(`Deployment failed: ${result.detail}`, 'error');
            }
        } catch (error) {
            console.error('Deployment error:', error);
            showNotification('Yabai! Deployment failed (╥﹏╥)', 'error');
        }
    });
}