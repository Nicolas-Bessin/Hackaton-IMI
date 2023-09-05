uploadButton = document.getElementById('upload-button');

function handleUpload() {
    document.getElementById("file").click();
}

uploadButton.addEventListener("click", handleUpload);