var clock = false;

function APIRequest(url, callback, callback_data) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.onload = function(e) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        callback(xhr.responseText, callback_data)
      }
    }
  };
  xhr.onerror = function(e) {
    console.error(xhr.statusText);
  };
  xhr.send(null);
}
// Update topbar to debug mode if needed
APIRequest('/topbar', update_topbar)
setInterval(function() {
  APIRequest('/topbar', update_topbar)
  APIRequest('/reload', sinkhole)
}, 20000);

// Callback sinhhole, a function that has no effect
function sinkhole() {}

function update_topbar(data) {
  data = data.split("\n");
  document.getElementById('pageTitle')
    .innerText = data[0];
  clock = (data[1] == 'clock')
  if (!clock) {
    document.getElementById('currentTime')
      .innerText = data[1];
  }
}
