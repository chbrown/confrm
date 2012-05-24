<%inherit file="/master.mako" />
<link href="/static/css/jquery.fileupload-ui.css" rel="stylesheet" />
<script src="/static/js/jquery-ui.js"></script>
<script src="/static/js/jquery.iframe-transport.js"></script>
<script src="/static/js/jquery.fileupload.js"></script>
<script src="/static/js/jquery.fileupload-ui.js"></script>
<script>
  $('#fileupload').fileupload({
      acceptFileTypes: /(\.|\/)(csv|tsv|xls|xlsx|txt)$/i,
      maxFileSize: 20000000,
      sequentialUploads: true
  });

  // // Load existing files
  // $.getJSON($('#fileupload form').prop('action'), function (files) {
  //     var fu = $('#fileupload').data('fileupload');
  //     fu._adjustMaxNumberOfFiles(-files.length);
  //     fu._renderDownload(files)
  //     .appendTo($('#fileupload .files'))
  // });

  // Open download dialogs via iframes,
  // to prevent aborting current uploads
  // $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
  //     e.preventDefault();
  //     $('<iframe style="display:none;"></iframe>')
  //     .prop('src', this.href)
  //     .appendTo('body');
  // });
</script>

<div id="fileupload">
  <form action="/uploads/create" method="POST" enctype="multipart/form-data">
    <div class="fileupload-buttonbar">
      <span class="btn btn-success fileinput-button">
        <i class="icon-plus icon-white"></i> Add files...
        <input type="file" name="files[]" multiple>
      </span>
      <!-- <button type="submit btn-primary start" class="start">
        <i class="icon-upload icon-white"></i>Start upload
      </button> -->
      <button type="reset" class="btn btn-warning cancel">
        <i class="icon-ban-circle icon-white"></i> Cancel upload
      </button>
      <button type="button" class="btn btn-danger delete">
        <i class="icon-trash icon-white"></i> Delete
      </button>
    </div>
  </form>
  <div class="fileupload-content">
    <table class="files"></table>
    <div class="fileupload-progressbar"></div>
  </div>
</div>

<script id="template-upload" type="text/x-jquery-tmpl">
    <tr class="template-upload{{if error}} ui-state-error{{/if}}">
        <td class="preview"></td>
        <td class="name"><%text>${name}</%text></td>
        <td class="size"><%text>${sizef}</%text></td>
        {{if error}}
        <td class="error" colspan="2">'Error:'
            {{if error === 'maxFileSize'}}'File is too big'
            {{else error === 'minFileSize'}}'File is too small'
            {{else error === 'acceptFileTypes'}}'Filetype not allowed'
            {{else error === 'maxNumberOfFiles'}}'Max number of files exceeded'
            {{else}}<%text>${error}</%text>
            {{/if}}
        </td>
        {{else}}
        <td class="progress">
            <div></div>
        </td>
        <td class="start">
            <button>'Start'</button>
        </td>
        {{/if}}
        <td class="cancel">
            <button>'Cancel'</button>
        </td>
    </tr>
</script>
<script id="template-download" type="text/x-jquery-tmpl">
    <tr class="template-download{{if error}} ui-state-error{{/if}}">
        {{if error}}
        <td class="preview">
            {{if url}}<a href="<%text>${url}</%text>" target="_blank">
            {{if thumbnail_url}}<img src="<%text>${thumbnail_url}</%text>" style="max-height: 80px; max-width: 80px;">
            {{else}}Show image{{/if}}
            </a>{{/if}}
        </td>
        <td class="name"><%text>${name}</%text></td>
        <td class="size"><%text>${sizef}</%text></td>
        <td class="error" colspan="2">Error:
            {{if error === 1}}File exceeds upload_max_filesize (php.ini directive)
            {{else error === 2}}File exceeds MAX_FILE_SIZE (HTML form directive)
            {{else error === 3}}File was only partially uploaded
            {{else error === 4}}No File was uploaded
            {{else error === 5}}Missing a temporary folder
            {{else error === 6}}Failed to write file to disk
            {{else error === 7}}File upload stopped by extension
            {{else error === 'maxFileSize'}}File is too big
            {{else error === 'minFileSize'}}File is too small
            {{else error === 'acceptFileTypes'}}Filetype not allowed
            {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
            {{else error === 'uploadedBytes'}}Uploaded bytes exceed file size
            {{else error === 'emptyResult'}}Empty file upload result
            {{else}}<%text>${error}</%text>
            {{/if}}
        </td>
        {{else}}
        <td class="preview">
            {{if thumbnail_url}}
            <a href="<%text>${url}</%text>" target="_blank"><img src="<%text>${thumbnail_url}</%text>" style="max-height: 80px; max-width: 80px;"></a>
            {{/if}}
        </td>
        <td class="name">
            <a href="<%text>${url}</%text>" {{if thumbnail_url}}
               target="_blank"{{/if}}><%text>${name}</%text></a>
        </td>
        <td class="size"><%text>${sizef}</%text></td>
        <td colspan="2"></td>
        {{/if}}
        <td class="delete">
            <button data-type="<%text>${delete_type}</%text>" data-url="<%text>${delete_url}</%text>">'Delete'</button>
        </td>
    </tr>
</script>
