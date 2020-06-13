function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function updateClock() {
  let date = new Date();
  let curr = pad(date.getHours(),2) + ":"  + pad(date.getMinutes(),2);
  document.getElementById("currentTime").innerText = curr;
}

updateClock();
setInterval(function(){updateClock() }, 2000);
