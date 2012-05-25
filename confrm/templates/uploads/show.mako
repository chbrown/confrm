<%inherit file="/master.mako" />
<table class="table table-bordered table-striped">
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