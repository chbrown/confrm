<%inherit file='/master.mako' />

<h3>Groups</h3>
<table class="table table-bordered table-striped table-condensed tablesorter">
  <thead>
    <tr>
      <th>Name</th>
      <th>Created</th>
      <th>Archived</th>
      <th>Deleted</th>
    </tr>
  </thead>
  <tbody>
  % for group in groups:
    <tr>
      <td><a href="/groups/edit/${group.id}">${group.name}</a></td>
      <td>${group.created.strftime('%Y-%m-%d')}</td>
      <td>
        % if group.archived:
          ${group.archived.strftime('%Y-%m-%d')}
        % else:
          <a href="/groups/archive/${group.id}" class="btn btn-info btn-mini"><i class="icon-lock"></i> Archive</a>
        % endif
      </td>
      <td>
        % if group.deleted:
          ${group.deleted.strftime('%Y-%m-%d')}
        % else:
          <a href="/groups/delete/${group.id}" class="btn btn-danger btn-mini" data-method="DELETE"><i class="icon-trash"></i> Delete</a>
        % endif
      </td>
    </tr>
  % endfor
  </tbody>
</table>

<a href="/groups/new" class="btn">Add Group</a>
