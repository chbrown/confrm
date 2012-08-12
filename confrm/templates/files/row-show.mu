<td>
  <a href="#" class="state" data-state="normal">{{filename}}</a>
  {{#contents}}
    <div style="margin: 10px 0; white-space: pre; background-color: white" class="well">{{contents}}</div>
  {{/contents}}
  {{#img}}
    <img src="{{img}}" />
  {{/img}}
  {{^img}}
    <a href="{{url}}">Download {{filename}}<a/>
  {{/img}}
</td>
<td class="controls">
  <a href="#" class="state" data-state="normal"><i class="icon-list-alt"></i> Back (discard unsaved changes)</a>
</td>