<%inherit file='/master.mako' />

<h3>All Users</h3>
<table class="table table-bordered table-striped table-condensed tablesorter">
  <tr>
    <th>Email</th>
    <th>First name</th>
    <th>Middle name</th>
    <th>Last name</th>
    <th>Other Emails</th>
    <th>Tags</th>
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
    <td>${user.middle_name or ''}</td>
    <td>${user.last_name}</td>
    <td>${user.other_emails or ''}</td>
    <td>${user.tags or ''}</td>
    <td>${user.role.name}</td>
    <td>${user.classification or ''}</td>
    <td>${user.institution or ''}</td>
    <td>${user.department or ''}</td>
    <td>${user.international or ''}</td>
    <td>${user.notes or ''}</td>
    <td class="nowrap">${user.created.strftime('%Y-%m-%d')}</td>
    <td class="nowrap">
      % if user.archived:
        ${user.archived.strftime('%Y-%m-%d')}
      % else:
        <a href="/users/archive/${user.id}" class="btn btn-info btn-mini"><i class="icon-lock"></i> archive</a>
      % endif
      ${user.deleted or ''}
    </td>
    <td class="nowrap">
      % if user.deleted:
        ${user.deleted.strftime('%Y-%m-%d')}
      % else:
        <a href="/users/delete/${user.id}" class="btn btn-danger btn-mini"><i class="icon-trash"></i> delete</a>
      % endif
    </td>
  </tr>
% endfor
</table>