<a href="#" class="state" data-state="normal">{{filename}}</a>
<a href="#" class="save btn btn-success"><i class="icon-white icon-check"></i> Save</a>
<a href="#" class="state" data-state="normal"><i class="icon-list-alt"></i> Back (discard unsaved changes)</a>
<div>
  {{#contents}}
    <textarea style="margin: 10px 0; background-color: white; width: 95%; height: 400px;">{{contents}}</textarea>
  {{/contents}}
  {{^contents}}
    <p>Can only edit text files.</p>
  {{/contents}}
</div>
