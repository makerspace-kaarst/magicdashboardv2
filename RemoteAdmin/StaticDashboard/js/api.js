SERVER = 'http://192.168.178.107'
SERVER = 'http://127.0.0.1'
PORT = 1337
PASSWORD = "ChangeMe"
// This function performes an HTTP request to the given URL and calls a given
// callback function with the request data and user supplied static data.
function APIRequest(url, data, callback, callback_data) {
  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      if (request.status === 200) {
        if (callback) {
          callback(request.responseText, callback_data)
        }
      }
    }
  }
  request.open("POST", '' + SERVER + ':' + PORT + url, true);
  request.setRequestHeader("X-API-Auth", PASSWORD);
  request.setRequestHeader("Accept", "text/plain");
  request.send(JSON.stringify(data));
}

function rawAPIRequest(url, data, callback, callback_data) {
  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      if (request.status === 200) {
        if (callback) {
          callback(request.responseText, callback_data)
        }
      }
    }
  }
  request.open("POST", url, true);
  request.setRequestHeader("X-API-Auth", PASSWORD);
  request.setRequestHeader("Accept", "text/plain");
  request.send(JSON.stringify(data));
}

function rawAPIRequestGET(url, data, callback, callback_data) {
  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      if (request.status === 200) {
        if (callback) {
          callback(request.responseText, callback_data)
        }
      }
    }
  }
  request.open("GET", url, true);
  request.setRequestHeader("X-API-Auth", PASSWORD);
  request.setRequestHeader("Accept", "text/plain");
  request.send(JSON.stringify(data));
}

function sinkhole() {

}
