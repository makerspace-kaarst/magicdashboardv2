function loadGridSize() {
  rawAPIRequestGET(SERVER+':'+PORT+'/grid_settings',{'auth':PASSWORD},_loadGridSize);
}

function _loadGridSize(data) {
  data = JSON.parse(data);
  let rows = data[0];
  let columns = data[1];
  document.getElementById('grid-size-rows').value = rows;
  document.getElementById('grid-size-columns').value = columns;
}

function updateGridSize(){
  let rows = document.getElementById('grid-size-rows').value;
  let columns = document.getElementById('grid-size-columns').value;
  APIRequest('/update_grid',{'rows':rows,'columns':columns},sinkhole);
}
