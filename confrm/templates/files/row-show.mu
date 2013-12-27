<a href="#" class="state" data-state="normal">{{filename}}</a>
<a href="#" class="state btn btn-warning" data-state="edit"><i class="icon-white icon-edit"></i> Edit</a>
<a href="#" class="state" data-state="normal"><i class="icon-list-alt"></i> Back (discard unsaved changes)</a>
<div style="margin-top: 10px">
{{#contents}}
  <div style="white-space: pre; background-color: white; margin-bottom: 0;" class="well">{{contents}}</div>
{{/contents}}
{{#img}}
  <img src="{{img}}" />
{{/img}}
</div>
<div style="margin-top: 10px">
  <a href="{{download}}"><i class="icon-download-alt"></i> Download {{filename}}</a>
</div>