
/*
 * Replace this URL with your deployed Render backend URL.
 * Example: https://your-dictionary-api.onrender.com
 */
const API_URL = "https://YOUR-RENDER-SERVICE.onrender.com";

const form = document.getElementById("searchForm");
const input = document.getElementById("wordInput");
const searchButton = document.getElementById("searchButton");

const lowValue = document.getElementById("lowValue");
const middleValue = document.getElementById("middleValue");
const highValue = document.getElementById("highValue");

const wordArray = document.getElementById("wordArray");
const message = document.getElementById("message");
const stepBadge = document.getElementById("stepBadge");
const stepExplanation = document.getElementById("stepExplanation");

const previousButton = document.getElementById("previousButton");
const playButton = document.getElementById("playButton");
const nextButton = document.getElementById("nextButton");
const resetButton = document.getElementById("resetButton");

const resultWord = document.getElementById("resultWord");
const definition = document.getElementById("definition");
const comparisonCount = document.getElementById("comparisonCount");
const resultStatus = document.getElementById("resultStatus");

let searchData = null;
let currentStep = -1;
let playTimer = null;

function stopPlayback() {
  if (playTimer !== null) {
    clearInterval(playTimer);
    playTimer = null;
  }
  playButton.textContent = "▶ Play";
}

function setMessage(text, isError = false) {
  message.textContent = text;
  message.style.color = isError ? "#ff8e9e" : "#b8c8e8";
}

function clearVisualization() {
  stopPlayback();
  searchData = null;
  currentStep = -1;

  lowValue.textContent = "—";
  middleValue.textContent = "—";
  highValue.textContent = "—";

  wordArray.replaceChildren();

  const empty = document.createElement("p");
  empty.className = "empty-state";
  empty.textContent = "Search for a word to visualize the algorithm.";
  wordArray.appendChild(empty);

  stepBadge.textContent = "Ready";
  stepExplanation.textContent =
    "The algorithm compares the target word with the middle word.";

  resultWord.textContent = "Waiting for a search...";
  definition.textContent = "The word meaning will appear here.";
  comparisonCount.textContent = "Comparisons: 0";
  resultStatus.textContent = "Status: Ready";

  updateControls();
}

function updateControls() {
  const steps = searchData?.steps || [];
  const hasSteps = steps.length > 0;

  previousButton.disabled = !hasSteps || currentStep <= 0;
  nextButton.disabled = !hasSteps || currentStep >= steps.length - 1;
  playButton.disabled = !hasSteps || currentStep >= steps.length - 1;
  resetButton.disabled = !hasSteps;
}

function renderStep() {
  if (!searchData || currentStep < 0) return;

  const steps = searchData.steps;
  const step = steps[currentStep];

  lowValue.textContent = step.low;
  middleValue.textContent = step.mid;
  highValue.textContent = step.high;

  stepBadge.textContent = `Step ${currentStep + 1} / ${steps.length}`;

  stepExplanation.textContent = step.explanation;

  wordArray.replaceChildren();

  searchData.words.forEach((word, index) => {
    const cell = document.createElement("div");
    cell.className = "word-cell";

    const wordLabel = document.createElement("span");
    wordLabel.textContent = word;

    const indexLabel = document.createElement("span");
    indexLabel.className = "index";
    indexLabel.textContent = `Index ${index}`;

    cell.append(wordLabel, indexLabel);

    // Show the active search range.
    if (index < step.low || index > step.high) {
      cell.classList.add("discarded");
    }

    if (index === step.low) cell.classList.add("low");
    if (index === step.high) cell.classList.add("high");
    if (index === step.mid) cell.classList.add("middle");

    if (
      searchData.found &&
      currentStep === steps.length - 1 &&
      index === searchData.index
    ) {
      cell.classList.add("found");
    }

    wordArray.appendChild(cell);
  });

  comparisonCount.textContent =
    `Comparisons: ${step.comparison_number}`;

  if (currentStep === steps.length - 1) {
    if (searchData.found) {
      resultWord.textContent = searchData.word;
      definition.textContent = searchData.meaning;
      resultStatus.textContent = `Status: Found at index ${searchData.index}`;
      setMessage(`Found "${searchData.word}" successfully.`);
    } else {
      resultWord.textContent = `"${searchData.word}" not found`;
      definition.textContent =
        "Try another word from the dictionary.";
      resultStatus.textContent = "Status: Not found";
      setMessage(`"${searchData.word}" is not in the dictionary.`);
    }
  } else {
    resultWord.textContent = "Searching...";
    definition.textContent =
      "Follow the highlighted middle word to see how the search range changes.";
    resultStatus.textContent = "Status: Searching";
    setMessage(`Comparing step ${currentStep + 1} of ${steps.length}.`);
  }

  updateControls();
}

async function performSearch(event) {
  if (event) event.preventDefault();

  const word = input.value.trim();

  if (!word) {
    setMessage("Please enter a word to search.", true);
    input.focus();
    return;
  }

  stopPlayback();
  searchButton.disabled = true;
  searchButton.textContent = "Searching...";
  clearVisualization();
  setMessage("Connecting to the Python backend...");

  try {
    const response = await fetch(`${API_URL}/api/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ word })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "The search request failed.");
    }

    if (!Array.isArray(data.words) || !Array.isArray(data.steps)) {
      throw new Error("The backend returned an invalid search response.");
    }

    searchData = data;

    if (searchData.steps.length === 0) {
      // The dictionary is empty: no comparisons can be performed.
      wordArray.replaceChildren();
      resultWord.textContent = `"${data.word}" not found`;
      definition.textContent = "No dictionary words are available.";
      resultStatus.textContent = "Status: Not found";
      comparisonCount.textContent = "Comparisons: 0";
      stepBadge.textContent = "No steps";
      stepExplanation.textContent = "The dictionary is empty.";
      setMessage("The backend dictionary is empty.", true);
      updateControls();
      return;
    }

    currentStep = 0;
    renderStep();
  } catch (error) {
    console.error("Dictionary search error:", error);
    clearVisualization();
    setMessage(
      "Unable to connect to the backend. Check API_URL and the Render service.",
      true
    );
    resultStatus.textContent = "Status: Connection error";
  } finally {
    searchButton.disabled = false;
    searchButton.textContent = "Search";
  }
}

previousButton.addEventListener("click", () => {
  stopPlayback();
  if (currentStep > 0) {
    currentStep--;
    renderStep();
  }
});

nextButton.addEventListener("click", () => {
  stopPlayback();
  if (searchData && currentStep < searchData.steps.length - 1) {
    currentStep++;
    renderStep();
  }
});

playButton.addEventListener("click", () => {
  if (!searchData) return;

  if (playTimer !== null) {
    stopPlayback();
    return;
  }

  if (currentStep >= searchData.steps.length - 1) {
    currentStep = 0;
    renderStep();
  }

  playButton.textContent = "Ⅱ Pause";

  playTimer = setInterval(() => {
    if (currentStep >= searchData.steps.length - 1) {
      stopPlayback();
      updateControls();
      return;
    }

    currentStep++;
    renderStep();

    if (currentStep >= searchData.steps.length - 1) {
      stopPlayback();
    }
  }, 1200);
});

resetButton.addEventListener("click", () => {
  stopPlayback();
  if (searchData?.steps?.length) {
    currentStep = 0;
    renderStep();
  }
});

form.addEventListener("submit", performSearch);

input.addEventListener("keydown", event => {
  if (event.key === "Escape") {
    input.value = "";
    input.focus();
  }
});
