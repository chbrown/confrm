<%inherit file='/master.mako' />
<%! from confrm.lib import jsonize %>

<div id="uploader" style="float: right"></div>

<h3>User files</h3>
<div id="files"></div>

<script>
head.ls(scripts.basic, function() {
  var file_collection = new FileCollection(${jsonize(files) | n});
  var file_collection_view = new FileCollectionView({
    el: $('#files'),
    collection: file_collection
  });
}).ls(scripts.uploader, function() {
  // var uploader = new FileUploader({title: 'Add', el: $('#uploader')});
  uploader.on('done', function(result) {
    var file_row_view = FileRow.addToTable(result.file, $table);
    setTimeout(function() { // wait for it to be added. xxx: don't race-hack
      file_row_view.$('a:first').prepend('<i class="icon-certificate"></i> ');
    }, 250);
  });
});
</script>
