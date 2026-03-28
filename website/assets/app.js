
const skillLibrary = {
  "Ground Control": [
    "First Touch Control", "Catches", "Bounce Dribbles", "Powerslide Cuts", "Ball Carries",
    "Hook Shots", "Front Flick", "45-Degree Flick", "Musty Flick Setup", "Dribble Challenging",
    "Low 50/50s", "Wall to Ground Touch", "Ground Pinch", "Wave Dash Dribble", "Soft Touch to Air Dribble"
  ],
  "Aerial Attack": [
    "Fast Aerial", "Air Roll Shots", "Backboard Double Tap", "Redirect Shots", "Ceiling Shot Setup",
    "Flip Reset Setup", "Single Reset Shot", "Air Dribble Start", "Air Dribble Bump", "Off-Wall Read",
    "Infield Pass Shot", "Backboard Follow", "High Aerial Save to Counter", "Pre-Jump Read", "Delayed Aerial Finish"
  ],
  Defense: [
    "Shadow Defense", "Back Post Rotation", "Near Post Decision", "Backboard Clears", "Low Boost Save",
    "Goal Line Patience", "Fake Challenge", "Challenge Timing", "50/50 Directional Control", "Corner Defense",
    "Save to Safe Corner", "Defensive Recoveries", "Second Man Positioning", "Third Man Discipline", "Clear to Teammate"
  ],
  "Speed & Recoveries": [
    "Half Flip", "Speed Flip", "Chain Wave Dashes", "Landing Recovery", "Boost Pad Routes",
    "Wall Recovery", "Ceiling Recovery", "Quick Turn with Drift", "Powerslide Recovery", "Aerial Recovery",
    "No Boost Movement", "Supersonic Route Planning", "Kickoff Recovery", "Flip Cancel Control", "Wall to Ground Recovery"
  ],
  "Game Sense": [
    "Rotation Timing", "Boost Denial", "Demo Route Awareness", "Pressure vs Possession Choice", "Teammate Spacing",
    "Second Touch Prediction", "Read Opponent First Touch", "Safe Challenge Selection", "Infield Passing Decision", "When to Slow Play",
    "When to Boom Clear", "Counterattack Timing", "Overtime Risk Management", "Clock Awareness", "Shot Selection Quality"
  ],
  "Mental Consistency": [
    "Reset After Mistake", "Composure Under Pressure", "Tilt Prevention", "Focus Cue Breathing", "Positive Communication",
    "Process Over Outcome", "One-Play Mentality", "Confidence Routine", "Short Memory on Whiffs", "Pre-Queue Mindset"
  ]
};

const coachIssueMap = {
  "Inconsistent shooting": ["Powershots", "Front Flick", "Shot Selection Quality", "Hook Shots"],
  "Bad first touch": ["First Touch Control", "Catches", "Soft Touch to Air Dribble", "Ball Carries"],
  "Poor defense": ["Shadow Defense", "Backboard Clears", "Back Post Rotation", "Challenge Timing"],
  "Slow aerials": ["Fast Aerial", "Pre-Jump Read", "Air Roll Shots", "Delayed Aerial Finish"],
  "Bad rotations": ["Rotation Timing", "Second Man Positioning", "Third Man Discipline", "Teammate Spacing"],
  "Low boost management": ["Boost Pad Routes", "No Boost Movement", "Supersonic Route Planning", "Boost Denial"],
  "Weak recoveries": ["Landing Recovery", "Wall Recovery", "Half Flip", "Powerslide Recovery"],
  "Panic in ranked": ["Composure Under Pressure", "Focus Cue Breathing", "One-Play Mentality", "Process Over Outcome"]
};

function randomPick(list, count) {
  const copy = [...list];
  const output = [];
  for (let i = 0; i < count && copy.length; i += 1) {
    const index = Math.floor(Math.random() * copy.length);
    output.push(copy.splice(index, 1)[0]);
  }
  return output;
}

function flattenSkills() {
  return Object.entries(skillLibrary).flatMap(([category, skills]) =>
    skills.map((skill) => ({ category, skill }))
  );
}

function setActiveNav() {
  const page = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("[data-nav]").forEach((link) => {
    if (link.getAttribute("href") === page) link.classList.add("active");
  });
}

function renderSkills() {
  const grid = document.getElementById("skillsGrid");
  const stats = document.getElementById("skillsStats");
  if (!grid) return;

  const allSkills = flattenSkills();
  allSkills.forEach((item, i) => {
    const card = document.createElement("article");
    card.className = "skill-card";
    card.innerHTML = `<h3>${i + 1}. ${item.skill}</h3><p>${item.category}</p>`;
    grid.appendChild(card);
  });

  if (stats) {
    stats.innerHTML = `
      <article><h3>${allSkills.length}</h3><p>Total Skills</p></article>
      <article><h3>${Object.keys(skillLibrary).length}</h3><p>Skill Categories</p></article>
      <article><h3>Pro</h3><p>Progression Structure</p></article>
    `;
  }
}

function buildRoutine(rank, focus, length) {
  const minutes = Number(length);
  const pool = [...skillLibrary[focus], ...skillLibrary["Speed & Recoveries"], ...skillLibrary["Game Sense"]];
  const chosen = randomPick(pool, minutes >= 60 ? 7 : minutes >= 45 ? 6 : 5);

  const block = Math.floor(minutes / chosen.length);
  return chosen.map((skill, i) => `${block}m Block ${i + 1}: ${skill}`);
}

function renderRoutine() {
  const output = document.getElementById("routineOutput");
  const rankInput = document.getElementById("planRank");
  const focusInput = document.getElementById("planFocus");
  const lengthInput = document.getElementById("planLength");
  if (!output || !rankInput || !focusInput || !lengthInput) return;

  const rank = rankInput.value;
  const focus = focusInput.value;
  const length = lengthInput.value;
  const steps = buildRoutine(rank, focus, length);

  output.innerHTML = "";

  const intro = document.createElement("article");
  intro.className = "routine-block";
  intro.innerHTML = `<strong>${rank}</strong> | <strong>${focus}</strong> | <strong>${length}m</strong><br/>Match Goal: ${randomPick(skillLibrary["Game Sense"], 1)[0]}`;
  output.appendChild(intro);

  steps.forEach((line) => {
    const block = document.createElement("article");
    block.className = "routine-block";
    block.textContent = line;
    output.appendChild(block);
  });
}

function bindTrainingGenerator() {
  const btn = document.getElementById("generatePlan");
  if (!btn) return;
  btn.addEventListener("click", renderRoutine);
  renderRoutine();
}

function coachReply(rank, issue, customText) {
  const targetedSkills = coachIssueMap[issue] || randomPick(flattenSkills().map((x) => x.skill), 4);
  const keyDrills = randomPick(targetedSkills, 3);
  const matchGoal = randomPick(skillLibrary["Game Sense"], 1)[0];
  const mindCue = randomPick(skillLibrary["Mental Consistency"], 1)[0];

  return `Coach for ${rank}: You said "${customText || issue}".\n` +
    `Drills: 1) ${keyDrills[0]}  2) ${keyDrills[1]}  3) ${keyDrills[2]}.\n` +
    `In-match goal: ${matchGoal}.\n` +
    `Mental cue: ${mindCue}.\n` +
    `Focus on clean reps first, then raise speed.`;
}

function bindCoachConsole() {
  const sendBtn = document.getElementById("coachSend");
  const input = document.getElementById("coachInput");
  const rank = document.getElementById("coachRank");
  const issue = document.getElementById("coachIssue");
  const log = document.getElementById("coachLog");
  if (!sendBtn || !input || !rank || !issue || !log) return;

  const bootMessage = document.createElement("div");
  bootMessage.className = "coach-msg bot";
  bootMessage.textContent = "Coach online. Tell me your weak point and I will build a focused improvement response.";
  log.appendChild(bootMessage);

  sendBtn.addEventListener("click", () => {
    const playerText = input.value.trim() || issue.value;

    const user = document.createElement("div");
    user.className = "coach-msg user";
    user.textContent = `Player: ${playerText}`;

    const bot = document.createElement("div");
    bot.className = "coach-msg bot";
    bot.textContent = coachReply(rank.value, issue.value, playerText);

    log.append(user, bot);
    input.value = "";
    log.scrollTop = log.scrollHeight;
=======
const skillSet = [
  "Ball Control", "Dribbling", "Bounce Dribbles", "Ground Flicks", "Air Dribbles",
  "Fast Aerials", "Double Taps", "Ceiling Shots", "Flip Resets", "Shadow Defense",
  "Backboard Reads", "50/50 Control", "Powershots", "Recoveries", "Boost Management",
  "Rotations", "Passing Plays", "Demo Awareness", "Kickoff Variations", "Mental Reset"
];

const routines = {
  "30": [
    "5m - Free play warm-up (speed flips + recoveries)",
    "10m - First touch + powershot consistency",
    "10m - Fast aerials and backboard clears",
    "5m - 1v1 focus game with no panic challenges"
  ],
  "60": [
    "10m - Warm-up mechanics and recoveries",
    "15m - Dribbles + flick angles",
    "15m - Air dribble or wall read reps",
    "10m - Defensive shadow and saves",
    "10m - Ranked with 2 clear focus objectives"
  ],
  ranked: [
    "3m - Quick warm-up touches",
    "3m - Kickoff and first challenge focus",
    "Queue set: play 3 games max then replay review",
    "Write 3 mistakes and one correction before next set"
  ]
};

function setActiveNav() {
  const page = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("[data-nav]").forEach((link) => {
    if (link.getAttribute("href") === page) {
      link.classList.add("active");
    }
  });
}

function renderSkills() {
  const grid = document.getElementById("skillsGrid");
  if (!grid) return;

  skillSet.forEach((skill, i) => {
    const card = document.createElement("article");
    card.className = "skill-card";
    card.innerHTML = `<h3>${i + 1}. ${skill}</h3><p>Train this with 20-40 focused reps daily.</p>`;
    grid.appendChild(card);
  });
}

function renderRoutine(type = "30") {
  const output = document.getElementById("routineOutput");
  if (!output) return;

  output.innerHTML = "";
  routines[type].forEach((line) => {
    const block = document.createElement("article");
    block.className = "routine-block";
    block.textContent = line;
    output.appendChild(block);
  });
}

function bindRoutineButtons() {
  const buttons = document.querySelectorAll(".routine-btn");
  if (!buttons.length) return;

  renderRoutine("30");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      renderRoutine(btn.dataset.routine);
    });
  });
}

function bindCopyPrompt() {
  const copyBtn = document.getElementById("copyPrompt");
  const promptBox = document.getElementById("promptBox");
  if (!copyBtn || !promptBox) return;

  copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(promptBox.textContent.trim());
      copyBtn.textContent = "Copied";
      setTimeout(() => {
        copyBtn.textContent = "Copy Prompt";
      }, 1200);
    } catch {
      copyBtn.textContent = "Copy failed";
    }

  });
}

setActiveNav();
renderSkills();

bindTrainingGenerator();
bindCoachConsole();

bindRoutineButtons();
bindCopyPrompt();