var node_update_timer = [0, 0, 0, 0, 0, 0]

function updateNode(html_string, node_id) {
  let split = html_string.split('\n');
  let duration = split[0];
  node_update_timer[node_id] = parseInt(duration, 10);
  split.shift();
  html_string = split.join('\n');
  if (html_string == "") {

  } else if (html_string == "reset") {
    document.getElementById('node' + node_id)
      .innerHTML = "";
  } else {
    document.getElementById('node' + node_id)
      .innerHTML = html_string;
  }
}

function updateAllNodes() {
  for (let node_id = 0; node_id < 6; node_id++) {
    if (node_update_timer[node_id] <= 0) {
      APIRequest("nodes/" + node_id, updateNode, node_id);
    } else {
      node_update_timer[node_id]--;
    }
  }
}

setInterval(function() {
  updateAllNodes()
}, 1000);
updateAllNodes()
