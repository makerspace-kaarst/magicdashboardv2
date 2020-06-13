function updateNode(html_string, node_id) {
  if (html_string == "") {

  } else if (html_string == "reset") {
    document.getElementById('node' + node_id)
      .innerHTML = ""
  } else {
    document.getElementById('node' + node_id)
      .innerHTML = html_string;
  }
}

function updateAllNodes() {
  for (let node_id = 0; node_id < 6; node_id++) {
    APIRequest("nodes/" + node_id, updateNode, node_id);
  }
}

setInterval(function() {
  updateAllNodes()
}, 10000);
updateAllNodes()
