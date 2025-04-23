document.addEventListener('DOMContentLoaded', function() {
    // Initialize the HTML editor and preview
    const htmlCode = document.getElementById('html-code');
    const preview = document.getElementById('preview');
    
    // Initialize welcome message
    const editingHTML = ""
    const welcomeHTML = "<!DOCTYPE html>\n<html>\n<head>\n    <title>Welcome to Aina\'s Playground!</title>\n    <style>\n        body {\n            font-family: \'Comic Sans MS\', cursive, sans-serif;\n            background: linear-gradient(135deg, #f5f9fa 0%, #e0f7fa 100%);\n            display: flex;\n            justify-content: center;\n            align-items: center;\n            height: 100vh;\n            margin: 0;\n            text-align: center;\n        }\n        .welcome-box {\n            background: white;\n            padding: 30px;\n            border-radius: 15px;\n            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);\n            max-width: 500px;\n        }\n        h1 {\n            color: #4CAF50;\n            margin-bottom: 20px;\n        }\n        p {\n            color: #666;\n            line-height: 1.6;\n        }\n        .kawaii {\n            font-size: 2rem;\n            margin: 20px 0;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"welcome-box\">\n        <h1>Konnichiwa! (◕‿◕✿)</h1>\n        <div class=\"kawaii\">(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧</div>\n        <p>Start coding in the editor and see your creation come to life here!</p>\n        <p>Or describe your dream website below and let me generate it for you~</p>\n    </div>\n</body>\n</html>";
    if(editingHTML == ""){
        htmlCode.value = welcomeHTML;
    }else{
        htmlCode.value = editingHTML;
    }
    
    
    // Initialize all modules
    initPreview(htmlCode, preview);
    initAiGeneration(htmlCode, updatePreview);
    setupFileHandlers(htmlCode, updatePreview);
    setupDeployment(htmlCode);
    initSettingsManager();
    setupEffects();
    
    // FAB event listener
    document.getElementById("fab").addEventListener("click", function() {
        var panel = document.getElementById("settings-panel");
        panel.style.display = panel.style.display === "none" || panel.style.display === "" ? "block" : "none";
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('deploy-modal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});