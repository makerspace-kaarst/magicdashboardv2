// Pads a string with leading 0 to a given length
// Example: 1 padded to len 3 is 001
function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1)
    .join(z) + n;
}

// Updates the innerText of the DOM node with the tag 'currentTime' using the current time,
// padded to 2 places
function updateClock() {
  let date = new Date();
  let curr = pad(date.getHours(), 2) + ":" + pad(date.getMinutes(), 2);
  document.getElementById("currentTime")
    .innerText = curr;
}

// Registers a callback every 2 seconds to update the clock
updateClock();
setInterval(function() {
  updateClock();
  APIRequest('/windowtitle', function(title) {
    document.getElementById('pageTitle')
      .innerText = title;
  })
}, 2000);
