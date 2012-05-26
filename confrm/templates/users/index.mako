<%inherit file='/master.mako' />

<h3>All Users</h3>
<table class="table table-bordered table-striped">
  <tr>
    <th>Email</th>
    <th>First name</th>
    <th>Middle name</th>
    <th>Last name</th>
    <th>Other Emails</th>
    <th>Role</th>
    <th>Classification</th>
    <th>Institution</th>
    <th>Department</th>
    <th>International</th>
    <th>Notes</th>
    <th>Created</th>
    <th>Archived</th>
    <th>Deleted</th>
  </tr>
% for user in users:
  <tr>
    <td>${user.email}</td>
    <td>${user.first_name}</td>
    <td>${user.middle_name}</td>
    <td>${user.last_name}</td>
    <td>${user.other_emails}</td>
    <td>${user.role}</td>
    <td>${user.classification}</td>
    <td>${user.institution}</td>
    <td>${user.department}</td>
    <td>${user.international}</td>
    <td>${user.notes}</td>
    <td>${user.created}</td>
    <td>${user.archived}</td>
    <td>${user.deleted}</td>
  </tr>
% endfor
</table>