let currentCard = null;
let currentSpeed = 1.0;
let recognition = null;
let isListening = false;
let availableVoices = [];

document.addEventListener("DOMContentLoaded", () => {
  setupSpeechVoices();
  setupSpeechRecognition();
  setupCardClickToFlip();
  loadNextCard();

  // Desbloqueia a síntese de voz no primeiro toque/clique na página
  document.body.addEventListener("pointerdown", () => {
    if (window.speechSynthesis && window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
    }
  }, { once: true });
});

function setupSpeechVoices() {
  function populateVoices() {
    availableVoices = window.speechSynthesis.getVoices();
  }
  populateVoices();
  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = populateVoices;
  }
}

function setupCardClickToFlip() {
  const flashcard = document.getElementById("flashcard");
  flashcard.addEventListener("click", (e) => {
    if (e.target.closest(".no-flip")) {
      return;
    }
    flashcard.classList.toggle("is-flipped");
  });
}

async function loadNextCard() {
  resetCardState();
  try {
    const response = await fetch("/api/cards/next");
    if (!response.ok) {
      document.getElementById("frontPhrase").innerText = "Nenhum cartão disponível.";
      return;
    }

    currentCard = await response.json();
    renderCardData(currentCard);

    // Entrada automática da voz masculina
    setTimeout(() => {
      speakCurrentPhrase();
    }, 450);

  } catch (error) {
    console.error("Erro ao carregar card:", error);
    document.getElementById("frontPhrase").innerText = "Erro ao carregar cartão.";
  }
}

function renderCardData(card) {
  document.getElementById("frontPhrase").innerText = `"${card.english_phrase}"`;
  document.getElementById("frontIpa").innerText = card.phonetic_ipa;

  const cadenceContainer = document.getElementById("cadenceWords");
  cadenceContainer.innerHTML = "";

  if (Array.isArray(card.cadence_data)) {
    card.cadence_data.forEach(item => {
      const tokenDiv = document.createElement("div");
      tokenDiv.className = "cadence-token";

      const bubble = document.createElement("span");
      bubble.className = `token-bubble ${item.emphasis}`;
      bubble.innerText = item.word;

      const mark = document.createElement("span");
      mark.className = `token-mark ${item.emphasis}`;

      tokenDiv.appendChild(bubble);
      tokenDiv.appendChild(mark);
      cadenceContainer.appendChild(tokenDiv);
    });
  }

  document.getElementById("backTranslation").innerText = `"${card.portuguese_translation}"`;
  document.getElementById("backOriginal").innerText = `"${card.english_phrase}"`;
  document.getElementById("backContext").innerText = card.context_note || "Frase de uso comum no dia a dia.";
}

function togglePlaybackSpeed() {
  if (currentSpeed === 1.0) currentSpeed = 0.75;
  else if (currentSpeed === 0.75) currentSpeed = 1.25;
  else currentSpeed = 1.0;

  const buttons = document.querySelectorAll(".btn-audio-speed");
  buttons.forEach(btn => {
    if (btn.id === "btnSpeed") btn.innerText = `${currentSpeed}x`;
  });
}

// Reproduz estritamente com Voz Masculina
function speakCurrentPhrase() {
  if (!currentCard || !currentCard.english_phrase) return;

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(currentCard.english_phrase);
  utterance.lang = "en-US";
  utterance.rate = currentSpeed;
  utterance.pitch = 0.9; // Tom masculino e firme

  if (availableVoices.length === 0) {
    availableVoices = window.speechSynthesis.getVoices();
  }

  const enVoices = availableVoices.filter(v => v.lang.startsWith("en"));
  if (enVoices.length > 0) {
    // Busca vozes masculinas do Windows (David, Mark, Guy) ou Google US English Male
    const maleVoice = enVoices.find(v => /david|male|guy|mark|george|alex/i.test(v.name)) || 
                      (enVoices.length > 1 ? enVoices[1] : enVoices[0]);
    if (maleVoice) {
      utterance.voice = maleVoice;
    }
  }

  window.speechSynthesis.speak(utterance);
}

function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) return;

  recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    isListening = true;
    document.getElementById("btnMic").classList.add("listening");
    document.getElementById("recognizedInput").placeholder = "Ouvindo... fale agora com clareza...";
  };

  recognition.onend = () => {
    isListening = false;
    document.getElementById("btnMic").classList.remove("listening");
  };

  recognition.onerror = () => {
    isListening = false;
    document.getElementById("btnMic").classList.remove("listening");
  };

  recognition.onresult = (event) => {
    const spokenText = event.results[0][0].transcript;
    document.getElementById("recognizedInput").value = spokenText;
    verifyPronunciation(spokenText);
  };
}

function toggleMicrophone() {
  if (!recognition) {
    alert("Reconhecimento de voz requer o Google Chrome ou Microsoft Edge.");
    return;
  }
  if (isListening) {
    recognition.stop();
  } else {
    document.getElementById("recognizedInput").value = "";
    hideFeedback();
    recognition.start();
  }
}

async function verifyPronunciation(spokenText) {
  if (!currentCard) return;

  try {
    const response = await fetch(`/api/cards/${currentCard.id}/check-pronunciation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ spoken_text: spokenText })
    });

    const result = await response.json();
    const scoreBadge = document.getElementById("scoreBadge");
    scoreBadge.style.display = "block";
    scoreBadge.innerText = `${result.score}% de acerto`;

    if (result.approved) {
      scoreBadge.style.background = "#ecfdf5";
      scoreBadge.style.color = "#059669";
      document.getElementById("feedbackSuccess").style.display = "block";
      document.getElementById("feedbackFail").style.display = "none";
      document.getElementById("feedbackScoreText").innerText = 
        `Excelente! Pontuação: ${result.score}%. Pronúncia precisa e aprovada.`;
    } else {
      scoreBadge.style.background = "#fef2f2";
      scoreBadge.style.color = "#dc2626";
      document.getElementById("feedbackFail").style.display = "block";
      document.getElementById("feedbackSuccess").style.display = "none";
      document.getElementById("feedbackFailText").innerText = 
        `Pontuação: ${result.score}%. Foi detetado: "${result.recognized_text}". Fale a frase completa com nitidez.`;
    }
  } catch (err) {
    console.error("Erro na verificação de pronúncia:", err);
  }
}

async function submitReview(difficulty) {
  if (!currentCard) return;

  try {
    await fetch(`/api/cards/${currentCard.id}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ difficulty: difficulty })
    });

    const flashcard = document.getElementById("flashcard");
    flashcard.classList.remove("is-flipped");
    setTimeout(() => {
      loadNextCard();
    }, 350);
  } catch (err) {
    console.error("Erro ao registrar revisão:", err);
  }
}

function resetCardState() {
  document.getElementById("recognizedInput").value = "";
  document.getElementById("scoreBadge").style.display = "none";
  hideFeedback();
}

function hideFeedback() {
  document.getElementById("feedbackSuccess").style.display = "none";
  document.getElementById("feedbackFail").style.display = "none";
}