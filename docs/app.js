const API_URL =
  "https://student-performance-prediction-system-y5pm.onrender.com/predict";

const form = document.getElementById("predictForm");
const btnReset = document.getElementById("btnReset");

const stateEmpty = document.getElementById("stateEmpty");
const stateLoading = document.getElementById("stateLoading");
const stateResult = document.getElementById("stateResult");

const badge = document.getElementById("badge");
const confidenceText = document.getElementById("confidenceText");
const confidenceBar = document.getElementById("confidenceBar");

const sAttendance = document.getElementById("sAttendance");
const sAssignment = document.getElementById("sAssignment");
const sQuiz = document.getElementById("sQuiz");
const sExam = document.getElementById("sExam");

function showState(which) {
  stateEmpty.classList.add("hidden");
  stateLoading.classList.add("hidden");
  stateResult.classList.add("hidden");
  which.classList.remove("hidden");
}

function setBadge(outcome) {
  badge.classList.remove("pass", "fail");
  if (outcome === "PASS") {
    badge.textContent = "PASS";
    badge.classList.add("pass");
  } else {
    badge.textContent = "FAIL";
    badge.classList.add("fail");
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const attendance = Number(document.getElementById("attendance").value);
  const assignment = Number(document.getElementById("assignment").value);
  const quiz = Number(document.getElementById("quiz").value);
  const exam = Number(document.getElementById("exam").value);

  // show loading
  showState(stateLoading);

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ attendance, assignment, quiz, exam }),
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();

    // update UI
    setBadge(data.outcome);
    confidenceText.textContent = `${data.confidence}%`;
    confidenceBar.style.width = `${data.confidence}%`;

    sAttendance.textContent = attendance;
    sAssignment.textContent = assignment;
    sQuiz.textContent = quiz;
    sExam.textContent = exam;

    // show result
    showState(stateResult);
  } catch (err) {
    console.error(err);
    alert(`Prediction failed: ${err?.message || err}`);
    showState(stateEmpty);
  }
});

btnReset.addEventListener("click", () => {
  form.reset();
  confidenceBar.style.width = "0%";
  confidenceText.textContent = "0%";
  showState(stateEmpty);
});
