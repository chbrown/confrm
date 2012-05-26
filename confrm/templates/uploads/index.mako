<%inherit file='/master.mako' />
<link href="/static/css/jquery.fileupload-ui.css" rel="stylesheet" />
<script src="/static/js/jquery-ui.js"></script>
<script src="/static/js/jquery.iframe-transport.js"></script>
<script src="/static/js/jquery.fileupload.js"></script>
<script src="/static/js/jquery.fileupload-ui.js"></script>

<h3>Upload new file</h3>
<div id="fileupload">
  <form action="/uploads/create" method="POST" enctype="multipart/form-data">
    <span class="btn btn-primary fileinput-button">
      <i class="icon-plus icon-white"></i> Add files...
      <input type="file" name="files[]" multiple>
    </span>
    <h4 id="dropzone" class="well fade">Drag here</h4>
    <button type="reset" class="btn btn-warning cancel">
      <i class="icon-ban-circle icon-white"></i> Cancel upload
    </button>
    <button type="button" class="btn btn-danger delete">
      <i class="icon-trash icon-white"></i> Delete
    </button>
    <div class="progress" style="width: 486px; opacity: 0.01;">
      <div class="bar" style="width: 0%"></div>
    </div>
  </form>
</div>
<h3>Pending files</h3>
<table id="uploads" class="table table-bordered table-striped">
  % for upload in uploads:
    <tr>
      <td><a href="/uploads/show/${upload}">${upload}</a></td>
      <td>
        <a href="/uploads/delete/${upload}" class="btn btn-danger btn-mini"><i class="icon-trash"></i> delete</a>
      </td>
    </tr>
  % endfor
</table>

<script>
  function logf(prefix) {
    return function() {
      console.log('[' + prefix + ']', arguments);
    }
  }
  $('#fileupload form').fileupload({
    // acceptFileTypes: /(\.|\/)(csv|tsv|xls|xlsx|txt)$/i,
    maxFileSize: 20000000,
    autoUpload: true,
    dropZone: $('#dropzone')
  }).bind('fileuploaddestroy',    logf('fileuploaddestroy'    ))
    // .bind('fileuploadadded',      logf('fileuploadadded'      ))
    // .bind('fileuploadstarted',    logf('fileuploadstarted'    ))
    .bind('fileuploadsent',       logf('fileuploadsent'       ))
    .bind('fileuploadcompleted',  logf('fileuploadcompleted'  ))
    .bind('fileuploadfailed',     logf('fileuploadfailed'     ))
    // .bind('fileuploadstopped',    logf('fileuploadstopped'    ))
    .bind('fileuploaddestroyed',  logf('fileuploaddestroyed'  ))
    .bind('fileuploadadd', function(ev, status) {
      $('.progress').fadeTo('fast', 1);
    })
    // .bind('fileuploadsubmit',     logf('fileuploadsubmit'     ))
    .bind('fileuploadsend',       logf('fileuploadsend'       ))
    .bind('fileuploaddone', function(ev, status) {
      status.result.forEach(function(upload_result) {
        var $tr = $('<tr><td><a href="' + upload_result.url + '">' + upload_result.name + '</a>').appendTo('#uploads');
        $tr.append('<td><a href="' + upload_result.delete_url + '" class="btn btn-danger btn-mini"><i class="icon-trash"></i> delete</a>');
      });
      setTimeout(function() {
        $('.progress .bar').width((status.loaded / status.total) * 100 + '%');
        $('.progress').fadeTo('slow', 0.01);
        setTimeout(function() {
          $('.progress .bar').width('0%');
        }, 1000);
      }, 2000);
    })
    .bind('fileuploadfail',       logf('fileuploadfail'       ))
    // .bind('fileuploadalways',     logf('fileuploadalways'     ))
    .bind('fileuploadprogress',   logf('fileuploadprogress'   ))
    .bind('fileuploadprogressall', function(ev, status) {
      $('.progress .bar').width((status.loaded / status.total) * 100 + '%');
    })
    // .bind('fileuploadstart',      logf('fileuploadstart'      ))
    // .bind('fileuploadstop',       logf('fileuploadstop'       ))
    // .bind('fileuploadchange',     logf('fileuploadchange'     ))
    .bind('fileuploadpaste',      logf('fileuploadpaste'      ))
    .bind('fileuploaddrop', function(ev, status) {
      console.log('fileuploaddrop', ev, status);
      // $('#dropzone').removeClass('btn btn-success');
    })
    .bind('fileuploaddragover', function(ev) {
      var $dropZone = $('#dropzone'),
        timeout = window.dropZoneTimeout;
      console.log('fileuploaddragover', $dropZone, ev);
      if (!timeout) {
        $dropZone.addClass('in');
      } else {
        clearTimeout(timeout);
      }
      if (ev.target === $dropZone[0]) {
        $dropZone.addClass('hover');
      } else {
        $dropZone.removeClass('hover');
      }
      window.dropZoneTimeout = setTimeout(function () {
        window.dropZoneTimeout = null;
        $dropZone.removeClass('in hover');
      }, 100);
    });
</script>