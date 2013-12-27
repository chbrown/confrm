<%inherit file='/master.mako' />

<div class="form-horizontal">
  <fieldset>
    <div class="control-group">
      <label class="control-label" for="from_user">From</label>
      <div class="controls">
        <select id="from_users">
          % for from_user in from_users:
            <option value="${from_user.id}">${from_user.full_email}</option>
          % endfor
        </select>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="to">To</label>
      <div class="controls">
        % for event_user in event_users:
        <label class="checkbox">
          <input type="checkbox" name="to" value="${user.id}"> ${event_user.user.full_email}
        </label>
        % endfor
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="subject">Subject</label>
      <div class="controls">
        <input type="text" id="subject">
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="body">Body</label>
      <div class="controls">
        <textarea id="body"></textarea>
      </div>
    </div>
  </fieldset>
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Add users</button>
  </div>
</div>
