<%inherit file='/master.mako' />
<%! from confrm.lib import jsonize %>

<div id="uploader" style="float: right"></div>

<h3>All Users</h3>
<table class="table table-bordered table-striped table-condensed tablesorter">
  <tr>
    <th>Email</th>
    <th>First name</th>
    <th>Middle name</th>
    <th>Last name</th>
    <th>All Emails</th>
    <th>Tags</th>
    <th>Classification</th>
    <th>Institution</th>
    <th>Department</th>
    <th>International</th>
    <th>Notes</th>
    <th>Root</th>
    <th>Created</th>
    <th>Archived</th>
    <th>Deleted</th>
  </tr>
</table>

<script>
var users = ${jsonize(users) | n};
// accept files directly on this page. When a file is dragged over, instantly allow uploading it, perhaps 
// to-do: support non-dragging?
head.js('/js/lib/jquery.js', '/js/lib/underback.js', '/js/lib/jquery.mustache.js', '/js/local.js', '/js/grid.js', function() {
  var $table = $('table.table');
  users.forEach(function(user) {
    var row = new UserRow({model: user});
    $table.append(row.$el)
  });
  // Uploader() constructor takes a function that will translate an uploaded file_id
  // to the url: where do we go after loading?
  // var uploader = new Uploader('Upload from file', function(file_id) {
  //   window.location = '/users/new_from_file/' + file_id;
  // });
});

head.js('/js/lib/jquery.js', '/js/lib/jquery-ui.js', '/js/lib/jquery.iframe-transport.js', '/js/lib/jquery.fileupload.js', '/js/lib/jquery.fileupload-ui.js', '/js/fileupload.js', function() {
  var uploader = new FileUploader({title: 'Add from file', el: $('#uploader')});
  // $('body').append(uploader.$el);
});

</script>