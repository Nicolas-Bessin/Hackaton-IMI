const uploadForm = document.getElementById('upload-form');
const uploadButton = document.getElementById('upload-button');

function handleUpload() {
    document.getElementById("file-input").click();
};

uploadForm.onchange = function() {
    uploadForm.submit();
};


uploadButton.addEventListener("click", handleUpload);

