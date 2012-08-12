<%inherit file='/master.mako' />
<%! from confrm.lib import jsonize %>

<div id="uploader" style="float: right"></div>

<h3>User files</h3>
<table id="files" class="table table-bordered table-striped tablesorter"></table>

<script>
var files = ${jsonize(files) | n};
head.js('/js/lib/jquery.js', '/js/lib/underback.js', '/js/lib/jquery-ui.js', '/js/lib/jquery.iframe-transport.js', '/js/lib/jquery.fileupload.js', '/js/lib/jquery.fileupload-ui.js', '/js/fileupload.js', '/js/lib/jquery.mustache.js', '/js/local.js', '/js/grid.js', function() {
  var $table = $('table.table'), uploader = new FileUploader({title: 'Add', el: $('#uploader')});
  files.forEach(function(file) {
    FileRow.addToTable(file, $table);
  });
  uploader.on('done', function(result) {
    var file_row_view = FileRow.addToTable(result.file, $table);
    setTimeout(function() { // wait for it to be added. xxx: don't race-hack
      file_row_view.$('a:first').prepend('<i class="icon-certificate"></i> ');
    }, 250);
  });
});
</script>
