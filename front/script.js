const backendURL = "http://127.0.0.1:8000"; // Change when deployed

async function checkIn() {
  const username = document.getElementById("username").value.trim();
  const errorEl = document.getElementById("error");
  const streakEl = document.getElementById("streak");

  if (!username) {
    errorEl.textContent = "Please enter a username.";
    errorEl.classList.remove("hidden");
    streakEl.classList.add("hidden");
    return;
  }

  try {
    // Step 1: POST check-in
    await fetch(`${backendURL}/checkin?username=${username}`, {
      method: "POST",
    });

    // Step 2: GET streak data
    const res = await fetch(`${backendURL}/streak/${username}`);
    const data = await res.json();

    document.getElementById("currentStreak").textContent = data.current_streak;
    document.getElementById("longestStreak").textContent = data.longest_streak;

    errorEl.classList.add("hidden");
    streakEl.classList.remove("hidden");
  } catch (err) {
    errorEl.textContent = "Something went wrong. Try again.";
    errorEl.classList.remove("hidden");
    streakEl.classList.add("hidden");
  }
}
