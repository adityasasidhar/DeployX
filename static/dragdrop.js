document.addEventListener('DOMContentLoaded', function () {
    const dropzone = document.getElementById('dropzone');
    const preview = document.getElementById('preview-panel');

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.style.background = "#eef";
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.style.background = "";
    });

    dropzone.addEventListener('drop', async (e) => {
        e.preventDefault();
        dropzone.style.background = "";

        let files = [...e.dataTransfer.files];
        let formData = new FormData();

        let folderName = prompt("Enter a name for this project preview:");
        formData.append('folder_name', folderName);

        files.forEach(file => formData.append('files[]', file));

        let response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        let result = await response.json();
        if (result.status === 'success') {
            preview.src = result.url;
        } else {
            alert("Error: " + result.message);
        }
    });
});
