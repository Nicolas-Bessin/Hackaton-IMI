import { masquerElements } from "./reset.js";
import { appendAIMessage } from "./prompt.js";

const indicator = document.getElementById("file-indicator");
const file_input = document.getElementById("file-input");
const uploadForm = document.getElementById('upload-form');
const uploadButton = document.getElementById('upload-button');

function handleUpload() {
    document.getElementById("file-input").click();
};

// uploadForm.onchange = function () {
//     uploadForm.submit();
//     masquerElements();
//     indicator.innerHTML = "Fichier : " + document.getElementById("file-input").files[0].name;
// };

const upload = async (event) => {
    event.preventDefault();

    masquerElements();
    indicator.innerHTML = "Fichier : " + document.getElementById("file-input").files[0].name;

    const data = new FormData();
    data.append("file", file_input.files[0]);

    let url = "/upload";
    // const xhr = new XMLHttpRequest();
    // xhr.onload = () => {
    //     console.log(xhr.responseText);
    // };
    // xhr.open("POST", url);
    // xhr.send(data);
    await appendAIMessage(async () => {
        const response = await fetch(url, {
            method: "POST",
            body: data,
        });
        const result = await response.json();
        return result.answer;
    });
};


uploadButton.addEventListener("click", handleUpload);
uploadForm.onchange = upload;

