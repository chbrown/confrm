<%inherit file='/master.mako' />

<div class="form-horizontal">
  <fieldset>
    <legend>Import options</legend>
    <div class="control-group">
      <label class="control-label" for="tags">Tags</label>
      <div class="controls">
        <input type="text" class="input-xlarge" id="tags">
        <p class="help-block">What tags should be applied to each user below?</p>
        <p class="help-block">Separate with commas. Spaces and underscores will be merged and converted to hyphens.</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="role">Role</label>
      <div class="controls">
        <select id="role">
          <option value="">Not Set</option>
          <option value="admin">Admin</option>
          <option value="teacher">Teacher</option>
          <option value="assistant">Assistant</option>
          <option value="student">Student</option>
        </select>
        <p class="help-block">What role should be applied to each user below?</p>
      </div>
    </div>
  </fieldset>
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
  }
  $('.tablesorter').tablesorter();
  $('button[type=submit]').click(function() {
    var headers = $('table thead th').map(function(i, th) {
      return $(th).text();
    }).toArray();
    var users = $('table tbody tr').map(function(i, tr) {
      // zip headers+data
      var user = new User();
      $(tr).children('td').each(function(i, td) {
        user.add(headers[i], $(td).text());
      })
      return user;
    }).toArray();
    var tags = $('#tags').val().replace(/[ _]+/g, '-').split(',');
    var role = $('#role option:selected').val();
    $.ajax('/uploads/update/${filename}', {
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({tags: tags, role: role, users: users}),
      dataType: 'json',
      success: function(data, textStatus, jqXHR) {
        console.log(data, textStatus, jqXHR);
      }
    });
  });
</script>

<div class="form-horizontal">
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Add users</button>
  </div>
</div>
