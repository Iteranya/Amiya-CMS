async function post_media(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/media/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        const result = await response.json();
        console.log("Upload success:", result);
        return result;
    } catch (error) {
        console.error("Error uploading file:", error);
        return null;
    }
}


