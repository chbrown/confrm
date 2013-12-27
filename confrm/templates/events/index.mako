<%inherit file='/master.mako' />

<h3>All Events</h3>
<table class="table table-bordered table-striped">
  <tr>
    <th>Name</th>
    <th>Tags</th>
    <th>Details</th>
    <th>Created</th>
    <th>Archived</th>
    <th>Deleted</th>
  </tr>
% for event in events:
  <tr>
    <td>${event.name}</td>
    <td>${event.tags}</td>
    <td>${event.json}</td>
    <td>${event.created}</td>
    <td>${event.archived}</td>
    <td>${event.deleted}</td>
  </tr>
% endfor
</table>
