// returns subnodes in order visible,invisible
function getSortedSubnodes(node) {
  let subs = node.children;
  if (subs[0].classList.contains('hidden')) {
    return [subs[1], subs[0]];
  }
  return [subs[0], subs[1]];
}

// Abstraction for getting a list of all user-nodes from the DOM
function getNodes() {
  return document.getElementById('user-nodes')
    .children;
}

// Main function called every second, updates everything
function updateNodes(newContentAvailable) {
  newContentAvailable = JSON.parse(newContentAvailable); // the request retrurns stringified json
  let nodes = getNodes(); // get all existing nodes
  for (let nodeId = 0; nodeId < nodes.length; nodeId++) { // Loop over all nodes
    if (newContentAvailable[nodeId]) { // If nothing new is available, no need do change anything
      APIRequest('/node_html?node_id=' + nodeId, updateNode, nodes[nodeId]) // Trigger a node update
    }
  }
}

function updateNode(html, node) {
  console.log('' + html);
  let subnodes = getSortedSubnodes(node);
  subnodes[1].innerHTML = html
  crossfade(subnodes[0], subnodes[1])
}

// relaods base grid and empty nodes [wrapper for API request to /grid_settings]
function init() {
  APIRequest('/grid_settings', updateGrid);
}

// Acc
function updateGrid(settings) {
  // Parse and seperate returned data
  settings = JSON.parse(settings);
  let rows = settings[0];
  let columns = settings[1];
  let nodeAmount = settings[2];
  let nodeTemplate = settings[3];
  if (nodeAmount != getNodes()
    .length || document.documentElement.style.getPropertyValue('--grid-columns') != columns ||
    document.documentElement.style.getPropertyValue('--grid-rows') != rows) {
    // Change grid settings CSS variables
    document.documentElement.style
      .setProperty('--grid-columns', '' + columns);
    document.documentElement.style
      .setProperty('--grid-rows', '' + rows);
    // Reset grid nodes
    document.getElementById('user-nodes')
      .innerHTML = nodeTemplate.repeat(nodeAmount);
    APIRequest('/force_update', sinkhole);
  }
}

// Registers a callback every second to update nodes and base grid
init();
setInterval(function() {
  APIRequest('/newContentAvailable', updateNodes);
  init(); // reload grid if node amount changes
}, 1000);
