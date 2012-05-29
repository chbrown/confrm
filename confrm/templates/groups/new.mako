<%inherit file='/master.mako' />

<div class="form-horizontal">
  <fieldset><legend>New Group</legend></fieldset>
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Create Group</button>
  </div>
</div>

<script>
var fields = [
  {key: 'name', type: 'text'},
];

var form = new Form($('.form-horizontal fieldset'), fields, {});
function submit() {
  $.ajax('/groups/create', {
    type: 'POST',
    data: form.get(),
    dataType: 'json',
    success: function(data, textStatus, jqXHR) {
      $('button[type=submit]').flag({text: data.message});
    },
    error: function(jqXHR, textStatus, errorThrown) {
      $('button[type=submit]').flag({text: 'Connection failed: ' + textStatus});
    }
  });
}
$('button[type=submit]').click(submit);
</script>
