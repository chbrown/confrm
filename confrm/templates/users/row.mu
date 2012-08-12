<td><a href="/users/edit/{{id}}">{{email}}</a></td>
<td>{{first_name}}</td>
<td>{{middle_name}}</td>
<td>{{last_name}}</td>
<td>{{all_emails}}</td>
<td>{{tags}}</td>
<td>{{classification}}</td>
<td>{{institution}}</td>
<td>{{department}}</td>
<td>{{international}}</td>
<td>{{notes}}</td>
<td>{{root}}</td>
<td class="nowrap">{{created}}</td>
<td class="nowrap">
  {{#archived}}
    {{archived}}
  {{/archived}}
  {{^archived}}
    <a href="/users/archive/{{id}}" class="btn btn-info btn-mini"><i class="icon-lock"></i> archive</a>
  {{/archived}}
</td>
<td class="nowrap">
  {{#deleted}}
    {{deleted}}
  {{/deleted}}
  {{^deleted}}
    <a href="/users/delete/{{id}}" class="btn btn-danger btn-mini"><i class="icon-trash"></i> delete</a>
  {{/deleted}}
</td>