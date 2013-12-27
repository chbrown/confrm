<link href="/static/css/jquery.fileupload-ui.css" rel="stylesheet" />
<form action="/files/upload" method="POST" enctype="multipart/form-data" class="fileupload">
  <h3>{{title}}</h3>
  <span class="btn btn-primary fileinput-button">
    <i class="icon-upload icon-white"></i> Select files...
    <input type="file" name="files[]" multiple>
  </span>
  <div class="dropzone progress fade input-medium">
    <h4 class="underlay">Drag files here</h4>
    <div class="bar"></div>
  </div>
  <input type="text" class="pastezone input-medium" placeholder="Paste csv here" />
</form>
