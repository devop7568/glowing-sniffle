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
bindRoutineButtons();
bindCopyPrompt();
