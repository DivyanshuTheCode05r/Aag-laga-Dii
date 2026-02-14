function addXP(amount){
  const XP_PER_LEVEL = 1000;
  const KEY_XP = "solo_xp";
  const KEY_LEVEL = "solo_level";

  let xp    = parseInt(localStorage.getItem(KEY_XP) || "0", 10);
  let level = parseInt(localStorage.getItem(KEY_LEVEL) || "1", 10);

  xp += amount;

  // level up logic: har 1000 xp par +1 level [web:220]
  const newLevel = Math.floor(xp / XP_PER_LEVEL) + 1;
  level = newLevel;

  localStorage.setItem(KEY_XP, String(xp));
  localStorage.setItem(KEY_LEVEL, String(level));
}

document.getElementById('backtoprofile').addEventListener('click',function(event){
  event.preventDefault();
  // Back button handler ke andar (jab allMissionsCompleted() true ho):
  localStorage.setItem("missionsCompletedToday", "yes");
  addXP(300);                      // aaj ke missions -> 300 XP
  window.location.href = "profile.html";
});


