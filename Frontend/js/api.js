// This function performes an HTTP request to the given URL and calls a given
// callback function with the request data and user supplied static data.
function APIRequest(url, callback, callback_data) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url + '?auth=' + AUTH_KEY, true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(xhr.responseText, callback_data)
            }
        }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
    };
    xhr.send(null);
}
