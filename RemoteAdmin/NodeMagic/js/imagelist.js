var RELOADER_ID = 0;
var html_template = `<div class="image-node-container hidden-flex">
<div class="flex-fill"></div>
  <div style="position:relative;">
    <img class='image-node max100' src="[server]:[port]/uploads/[filename]" alt="">
    <h1 class="absolute filename">[filename]</h1>
  </div>
  <div class="flex-fill"></div>
  <button type="button" name="button" class="image-delete" onclick="deleteImage('[filename]')">Delete file</button>
</div>`

var upload_image = `<div class="hidden-flex" style="color:#fff">
    <iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
    <form id="uploadbanner" enctype="multipart/form-data" method="post"
          action="http://localhost:1337/http_upload" target="dummyframe">
        <input id="fileupload" name="myfile" type="file"/>
        <input type="hidden" name='password' id="form-password" value=""/>
        <input type="submit" value="submit" id="submit"/>
    </form>
</div>`

function openImageList(){
  clearInterval(RELOADER_ID);
  RELOADER_ID = setInterval(function () {
    _openImageList()
  }, 500);
  _openImageList();
}

function _openImageList() {
  document.getElementById('image-list-main')
    .classList.remove('hidden');

    document.getElementById('image-list-main')
        .classList.remove('hidden');
  APIRequest('/list_files',{},makeFileList);
}

function closeImageList() {
    clearInterval(RELOADER_ID);
    document.getElementById('image-list-main')
        .classList.add('hidden');
}

function makeFileList(files) {
  out = "";
  files = JSON.parse(files);
  for (var i = 0; i < files.length; i++) {
    out += (html_template.split('[filename]').join(files[i])).replace('[server]',SERVER).replace('[port]',PORT);
  }
  document.getElementById('image-list-content').innerHTML = out;
}


function deleteImage(filename){
  APIRequest('/delete_file',{'filename':filename},function(){
    setTimeout(function () {
      openImageList();
    }, 150);
  });
}
