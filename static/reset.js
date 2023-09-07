import { appendAIMessage } from "./prompt.js";

const resetButton = document.getElementById("reset-button");
const indicator = document.getElementById("file-indicator");

function masquerElements() {
    const messages = document.querySelectorAll(".message");
    messages.forEach((message) => {
        message.style.display = "none";
    });
}

async function reset() {
    masquerElements();
    indicator.innerHTML = "Fichier : Aucun fichier mis en ligne";
    await appendAIMessage(async () => {
        const response = await fetch('/resetcontext', {
            method: "GET",
        });
        const message = await response.text();
        return message;
    });
}

resetButton.addEventListener("click", reset);

export { masquerElements };