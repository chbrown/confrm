<%inherit file='/master.mako' />
<%! from confrm.lib import jsonize %>

<div id="uploader" style="float: right"></div>

<h3>All Users</h3>
<table class="table table-bordered table-striped table-condensed tablesorter">
  <thead>
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
  </thead>
  <tbody>
  </tbody>
</table>

<script>
var users = ${jsonize(users) | n};
// accept files directly on this page. When a file is dragged over, instantly allow uploading it, perhaps
// to-do: support non-dragging?
head.js('/js/lib/jquery.js', '/js/lib/underback.js', '/js/lib/jquery.mustache.js', '/js/local.js', '/js/grid.js', function() {
  var $table = $('table.table tbody');
  users.forEach(function(user) {
    var user_model = new UserModel(user),
      row = new UserRow({model: user_model});
    $table.append(row.$el)
  });

  var importFile = function(file_id) {
    ajax('/files/' + file_id + '/as_users', function(data) {
      $table.empty();
      data.users.forEach(function(user) {
        var user_model = new UserModel(user),
          row = new UserRow({model: user_model});
        $table.append(row.$el)
      });
    });
  }

  head.js('/js/lib/jquery-ui.js', '/js/lib/jquery.iframe-transport.js', '/js/lib/jquery.fileupload.js', '/js/lib/jquery.fileupload-ui.js', '/js/fileupload.js', function() {
    var uploader = new FileUploader({title: 'Add from file', el: $('#uploader')});
    uploader.on('done', function(result) {
      importFile(result.file.id);
    });
  });

  var from_file_id = window.location.search.match(/[?&]file=([^?&]+)/);
  if (from_file_id) {
    importFile(parseInt(from_file_id[1], 10));
  }
});


var fields = [
  {
    key: 'tags',
    type: 'csv',
    help: 'What tags should be applied to each user below?<br/>Separate with commas. Spaces and underscores will be merged and converted to hyphens.',
  },
  {
    key: 'add_replace_tags',
    type: 'radiolist',
    children: ['add', 'replace'],
    default: 'add',
    help: 'Add or replace tags, if user already exists?',
  },
  {
    key: 'groups',
    // type: 'list',
    // child: {
      type: 'object',
      object: 'group',
      url: '/groups/index.json',
    // }
  },
  {
    key: 'add_replace_groups',
    type: 'radiolist',
    children: ['add', 'replace'],
    default: 'add',
    help: 'Add or replace groups, if user already exists?',
  },
];
// var form = new Form($('.form-horizontal fieldset'), fields, {});

function submit() {
  var data = form.get();
  // data.users = getUsers();
  var $button = $(this);
  $.ajax('/users/create', {
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
    dataType: 'json',
    success: function(data, textStatus, jqXHR) {
      $button.flag({html: 'Imported users.'});
    }
  });
}
// $('button[type=submit]').click(submit);
</script>
