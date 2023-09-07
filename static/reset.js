import { appendAIMessage } from "./prompt.js";

const resetButton = document.getElementById("reset-button");

function masquerElements() {
    const messages = document.querySelectorAll(".message");
    messages.forEach((message) => {
      message.style.display = "none";
    });
  }
  
  
  
async function reset() {
    masquerElements()
    await appendAIMessage(async () => {
      const response = await fetch('/resetcontext', {
        method: "GET",
      });
      const message = await response.text();
      return message;
    });
  }  

resetButton.addEventListener("click", reset);