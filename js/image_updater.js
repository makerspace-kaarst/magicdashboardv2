var dynamic_nodes = []
var dynamic_data = [[], [], [], [], [], []]
var dynamic_indexes = [0, 0, 0, 0, 0, 0]

function register_node(nodeid,data) {
  if(!dynamic_nodes.includes(nodeid)) {
    dynamic_nodes.push(nodeid);
  }
  dynamic_data[nodeid] = data;
  dynamic_indexes[nodeid] = 0;
}

function unregister_node(nodeid) {
  let index = dynamic_nodes.indexOf(nodeid);
  if (index > -1) {
    dynamic_nodes.splice(index, 1);
  }
  dynamic_data[nodeid] = [];
  dynamic_indexes[nodeid] = 0;
}

function image_updater() {
  for(let nodeid = 0; nodeid < dynamic_nodes.length; nodeid++){
    let index = dynamic_nodes[nodeid];

    let data = dynamic_data[index];
    let img_index = dynamic_indexes[index];
    img_index ++;
    img_index %= data.length;
    dynamic_indexes[index] = img_index;
    document.getElementById('node'+index).children[0].children[1].src = 'img/'+data[img_index];
  }
}

setInterval(function(){image_updater() }, 10000);
