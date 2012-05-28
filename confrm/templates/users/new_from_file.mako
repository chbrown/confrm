<%inherit file='/master.mako' />

<div class="form-horizontal">
  <fieldset><legend>Import options</legend></fieldset>
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Add users</button>
  </div>
</div>

<h3>Preview users:</h3>
<table class="table table-bordered table-striped tablesorter">
  <thead>
    <tr>
      <th></th>
      % for header in headers:
        <th>${header}</th>
      % endfor
    </tr>
  </thead>
  <tbody>
    % for i, row in enumerate(data):
    <tr>
      <td>${i}</td>
      % for cell in row:
        <td>${cell}</td>
      % endfor
    </tr>
    % endfor
  </tbody>
</table>

<div class="form-horizontal">
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Add users</button>
  </div>
</div>

<script>
function User() { }
User.prototype.add = function(key, value) {
  if (key === 'full_name') {
    var name_parts = value.split(/\s+/);
    this.first_name = name_parts[0];
    if (name_parts.length > 2) {
      this.middle_name = name_parts.slice(1, name_parts.length - 1).join(' ');
    }
    this.last_name = name_parts[name_parts.length - 1];
  }
  else if (key) {
    this[key] = value;
  }
};

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
var form = new Form($('.form-horizontal fieldset'), fields, {});

function getUsers() {
  var headers = $('table thead th').map(function(i, th) {
    return $(th).text();
  }).toArray();
  return $('table tbody tr').map(function(i, tr) {
    // zip headers+data
    var user = new User();
    $(tr).children('td').each(function(i, td) {
      user.add(headers[i], $(td).text());
    })
    return user;
  }).toArray();
}
function submit() {
  var data = form.get();
  data.users = getUsers();
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
$('button[type=submit]').click(submit);
</script>
