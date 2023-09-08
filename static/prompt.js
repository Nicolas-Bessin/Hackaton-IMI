const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const mainContainer = document.getElementById("main-container");
const prompt = document.getElementById("prompt");
const choisirButton = document.getElementById("uplaod-button")
const resetButton = document.getElementById("reset-button")
const indicateurfichierButton = document.getElementById("file-indicator")

const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};

const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};

const handlePrompt = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }

  appendHumanMessage(data.get("prompt"));
  submitButton.disabled = true
  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    submitButton.disabled = false
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";
    return question;
  });
};

questionButton.addEventListener("click", handleQuestionClick);

export { appendAIMessage };

// Récupérer le bouton "Dark mode" et les éléments que vous voulez mettre en mode sombre
const darkModeToggle = document.getElementById("darkModeToggle");
const body = document.body; // Le corps du document
const elementsToToggle = document.querySelectorAll('.dark-mode-toggle'); // Ajoutez la classe "dark-mode-toggle" aux éléments que vous voulez mettre en mode sombre

// Écouter l'événement de clic sur le bouton "Dark mode"
darkModeToggle.addEventListener("click", () => {
    // Ajouter ou supprimer la classe "dark-mode" au corps du document
    body.classList.toggle("dark-mode");
    messagesContainer.classList.toggle("dark-mode");
    promptForm.classList.toggle("dark-mode");
    submitButton.classList.toggle("dark-mode");
    questionButton.classList.toggle("dark-mode");
    mainContainer.classList.toggle("dark-mode");
    prompt.classList.toggle("dark-mode");
    choisirButton.classList.toggle("dark-mode");
    resetButton.classList.toggle("dark-mode");
    indicateurfichierButton.classList.toggle("dark-mode");
    
    // Parcourir les éléments à basculer et ajouter ou supprimer la classe "dark-mode"
    elementsToToggle.forEach(element => {
        element.classList.toggle("dark-mode");
    });
});

