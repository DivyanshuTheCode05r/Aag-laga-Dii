// ========== 1. Missions data (easy -> hard) ==========

function addXP(amount){
  const XP_PER_LEVEL = 1000;
  const KEY_XP = "solo_xp";
  const KEY_LEVEL = "solo_level";

  let xp = parseInt(localStorage.getItem(KEY_XP)) || 0;
  let level = parseInt(localStorage.getItem(KEY_LEVEL)) || 1;
  xp += amount;
  const newLevel = Math.floor(xp / XP_PER_LEVEL) + 1;
  level = newLevel;
  localStorage.setItem(KEY_XP, String(xp));
  localStorage.setItem(KEY_LEVEL, String(level));
}

const dailyMissions = [
  {
    title: "Day 1 missions",
    items: [
      "Workout: 10 min light stretching + 10 squats.",
      "Water: Drink at least 2 liters.",
      "Study (SSC GD): 10 GK questions – India, states, capitals.",
      "Reading: 10 minutes any book / newspaper."
    ]
  },
  {
    title: "Day 2 missions",
    items: [
      "Workout: 20 min walk.",
      "Water: 2.5 liters.",
      "Study (SSC GD): 10 reasoning questions – odd one out, simple series.",
      "Reading: 10–15 min (underline 3 new words)."
    ]
  },
  {
    title: "Day 3 missions",
    items: [
      "Workout: 3 sets – 8 push‑ups (ya wall push‑ups) + 12 squats.",
      "Water: 3 liters.",
      "Study (SSC GD): 15 previous‑year questions (mix GK + reasoning).",
      "Reading: 15 min book/newspaper."
    ]
  },
  {
    title: "Day 4 missions",
    items: [
      "Workout: 25 min brisk walk.",
      "Water: 3 liters.",
      "Study (SSC GD): 15 reasoning questions – direction sense, blood relation.",
      "Reading: 20 min, 5 important points note karo."
    ]
  },
  {
    title: "Day 5 missions",
    items: [
      "Workout: 3 sets – 10 push‑ups + 15 squats + 20 jumping jacks.",
      "Water: 3.5 liters.",
      "Study (SSC GD): 15 GK questions – history basics.",
      "Reading: 20 min; 5 new words likho + meaning dekho."
    ]
  },
  {
    title: "Day 6 missions",
    items: [
      "Workout: 30 min mix walk + thoda slow run.",
      "Water: 4 liters.",
      "Study (SSC GD): 1 small mock – 20 questions timer ke sath (20–25 min).",
      "Reading: 25 min book/newspaper bina phone disturb ke."
    ]
  },
  {
    title: "Day 7 missions",
    items: [
      "Workout: 4 sets – 10 push‑ups, 15 squats, 20 jumping jacks.",
      "Water: 4 liters.",
      "Study (SSC GD): Revision – iss week ke sare notes + weak topics.",
      "Reading: 30 min; pure week ka reflection likho."
    ]
  }
];

// ========== 2. Helpers: start day + daily reset ==========

function getDayFromStart() {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let startStr = localStorage.getItem("missionStartDate");
  if (!startStr) {
    localStorage.setItem("missionStartDate", today.toISOString());
    return 1;
  }

  const startDate = new Date(startStr);
  startDate.setHours(0, 0, 0, 0);

  const diffMs = today - startDate;
  const oneDay = 1000 * 60 * 60 * 24;
  return Math.floor(diffMs / oneDay) + 1;
}

function resetIfNewDay() {
  const todayStr = new Date().toDateString();
  const lastDay = localStorage.getItem("missionsLastOpenDay");
  if (lastDay !== todayStr) {
    localStorage.setItem("missionsLastOpenDay", todayStr);
    // New day, clear previous completion state
    localStorage.removeItem("missionsCompletedToday");
  }
}

// ========== 3. UI build: missions list with checkboxes ==========

function buildMissionList(mission) {
  const listEl = document.getElementById("mission-list");
  listEl.innerHTML = "";

  mission.items.forEach((text, idx) => {
    const li = document.createElement("li");

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.id = "m" + idx;
    cb.className = "mission-checkbox";

    const label = document.createElement("label");
    label.htmlFor = cb.id;
    label.innerText = text;

    li.appendChild(cb);
    li.appendChild(document.createTextNode(" "));
    li.appendChild(label);
    listEl.appendChild(li);
  });
}

// ========== 4. Completion check + back button block ==========

function allMissionsCompleted() {
  const boxes = document.querySelectorAll("#mission-list .mission-checkbox");
  if (boxes.length === 0) return false;
  return Array.from(boxes).every(cb => cb.checked);
}

function setupBackButton() {
  const backBtn = document.getElementById("backBtn");
  const errorEl = document.getElementById("error-msg");

  backBtn.addEventListener("click", function () {
    if (!allMissionsCompleted()) {
      errorEl.innerText = "There is no going back before completing the mission.";
      return;
    }
    // Completed -> flag save + navigate
    localStorage.setItem("missionsCompletedToday", "yes");
    window.location.href = "profile.html";
  });
}

// Remove error message on checkbox change
function setupCheckboxClearError() {
  const errorEl = document.getElementById("error-msg");
  document.addEventListener("change", function (e) {
    if (e.target.classList.contains("mission-checkbox")) {
      errorEl.innerText = "";
    }
  });
}

// ========== 5. Checkbox logic to handle completion and XP addition ==========

function setupCheckboxLogic() {
  const checkboxes = document.querySelectorAll(".mission-checkbox");

  checkboxes.forEach(cb => {
    cb.addEventListener("change", function () {
      if (this.checked) {
        this.classList.add("completed");
        this.disabled = true;
        checkAllMissionsDone();
      }
    });
  });
}

function checkAllMissionsDone() {
  const checkboxes = document.querySelectorAll(".mission-checkbox");
  if (checkboxes.length === 0) return;
  const allDone = Array.from(checkboxes).every(cb => cb.checked || cb.disabled);
  if (!allDone) return;

  if (localStorage.getItem("missionsCompletedToday") === "yes") return;

  localStorage.setItem("missionsCompletedToday", "yes");
  alert("Mission Completed! Here is your reward: 300 XP");
  addXP(300);
  window.location.href = 'profile.html';
}

// ========== 6. Main loader ==========

function loadDailyMissions() {
  resetIfNewDay();

  const dayFromStart = getDayFromStart(); // 1,2,3...
  const index = (dayFromStart - 1) % dailyMissions.length; // 0..6 cycle
  const mission = dailyMissions[index];

  const titleEl = document.getElementById("challenge-title");
  titleEl.innerText = `Welcome to Day ${dayFromStart} missions`;

  buildMissionList(mission);
  setupBackButton();
  setupCheckboxClearError();
  setupCheckboxLogic();
}

document.addEventListener("DOMContentLoaded", loadDailyMissions);
