function updateClock() {
  let date = new Date();
  let curr = date.getHours() + ":"  + date.getMinutes();
  document.getElementById("currentTime").innerText = curr;
}


setInterval(function(){updateClock() }, 2000);
