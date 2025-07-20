let roundStart    = Date.now();
let questionStart = Date.now();
let totalTimer    = 300; // 5 minutes in seconds
let intervalID;
let roundScore    = 0;

function startTimers() {
  intervalID = setInterval(() => {
    const elapsed = Math.floor((Date.now() - roundStart)/1000);
    const left    = totalTimer - elapsed;
    if (left <= 0) {
      clearInterval(intervalID);
      endRound();
    } else {
      document.getElementById("timeLeft").innerText = left;
    }
  }, 500);
}

function endRound() {
  fetch("/end_round", {method:"POST"})
    .then(resp => resp.json())
    .then(data => {
      alert("Time’s up! Your round score: " + roundScore +
            "\nYour TOP score: " + data.new_top);
      window.location = "/";
    });
}

function submitGuess() {
  const guessText = document.getElementById("guess").value;
  const elapsedSec = (Date.now() - questionStart)/1000;

  fetch("/submit_guess", {
    method:"POST",
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ guess: guessText, elapsed: elapsedSec })
  })
  .then(resp => resp.json())
  .then(data => {
    if (data.correct) {
      document.getElementById("feedback").innerText = 
        `Correct! +${data.points} pts`;
    } else {
      document.getElementById("feedback").innerText = 
        `Wrong! The answer was: ${CORRECT_TITLE}`;
    }
    roundScore = data.round_score;
    document.getElementById("score").innerText = roundScore;
    // move on
    setTimeout(() => {
      window.location.reload();
    }, 1500);
  });
}

// wire up
document.getElementById("submitBtn").addEventListener("click", submitGuess);
startTimers();
questionStart = Date.now();
