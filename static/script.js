const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileElem');
const fileList = document.getElementById('file-list');
const form = document.getElementById('uploadForm');
const loader = document.getElementById('loader');
const iframeContainer = document.getElementById('iframe-container');
const previewFrame = document.getElementById('preview-frame');

let filesToUpload = [];

function updateFileList() {
  fileList.innerHTML = '';
  filesToUpload.forEach(file => {
    const item = document.createElement('div');
    item.textContent = '📄 ' + file.name;
    fileList.appendChild(item);
  });
}

dropArea.addEventListener('dragover', e => {
  e.preventDefault();
  dropArea.style.borderColor = 'lime';
});

dropArea.addEventListener('dragleave', e => {
  e.preventDefault();
  dropArea.style.borderColor = '#555';
});

dropArea.addEventListener('drop', e => {
  e.preventDefault();
  dropArea.style.borderColor = '#555';
  filesToUpload.push(...e.dataTransfer.files);
  updateFileList();
});

fileInput.addEventListener('change', () => {
  filesToUpload.push(...fileInput.files);
  updateFileList();
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  loader.style.display = 'block';

  const formData = new FormData();
  const folderName = document.getElementById('folderName').value.trim();
  const repoURL = form.querySelector('input[name="repo_url"]').value.trim();

  if (!folderName) {
    alert("Folder name is required.");
    loader.style.display = 'none';
    return;
  }

  formData.append('folder_name', folderName);
  if (repoURL !== "") {
    formData.append('repo_url', repoURL);
  }

  filesToUpload.forEach(file => {
    formData.append('files[]', file);
  });

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    loader.style.display = 'none';

    if (data.status === 'static' || data.status === 'flask') {
      previewFrame.src = data.url;
      form.style.display = 'none';
      iframeContainer.style.display = 'block';
    } else {
      alert('Error: ' + data.message || 'Unknown error.');
    }
  })
  .catch(err => {
    loader.style.display = 'none';
    alert('Upload failed: ' + err.message);
  });
});
