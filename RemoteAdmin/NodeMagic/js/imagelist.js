var html_template = `<div class="image-node-container hidden-flex">
<div class="flex-fill"></div>
  <div style="position:relative;">
    <img class='image-node max100' src="../../Frontend/uploads/[filename]" alt="">
    <h1 class="absolute filename">[filename]</h1>
  </div>
  <div class="flex-fill"></div>
  <button type="button" name="button" class="image-delete" onclick="deleteImage('[filename]')">Delete file</button>
</div>`

function openImageList() {
  document.getElementById('imagelist-main')
    .classList.remove('hidden');

    APIRequest('/list_files',{},makeFileList);
    document.getElementById('imagelist-main')
        .classList.remove('hidden');
}

function closeImageList() {
    document.getElementById('imagelist-main')
        .classList.add('hidden');
}

function makeFileList(files) {
  out = "";
  files = JSON.parse(files);
  for (var i = 0; i < files.length; i++) {
    out += html_template.split('[filename]').join(files[i])
  }
  document.getElementById('image-list-main').innerHTML = out;
}


function deleteImage(filename){
  alert(filename);
}
