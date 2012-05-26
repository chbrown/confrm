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
      <td></td>
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
  $('.tablesorter').tablesorter();
</script>

<div class="form-horizontal">
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Add users</button>
  </div>
</div>
