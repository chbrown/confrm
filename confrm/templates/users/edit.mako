<%inherit file='/master.mako' />

<h3>New User</h3>
<div class="form-horizontal">
  <fieldset></fieldset>
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Update user</button>
  </div>
</div>

<script>
var fields = [
  {key: 'email', type: 'text'},
  {key: 'first_name', type: 'text'},
  {key: 'middle_name', type: 'text'},
  {key: 'last_name', type: 'text'},
  {key: 'all_emails', type: 'csv'},
  {key: 'tags', type: 'csv'},

  {key: 'classification', type: 'text'},
  {key: 'institution', type: 'text'},
  {key: 'department', type: 'text'},
  {key: 'international', type: 'bool'},

  {key: 'notes', type: 'text'}
];
<%! from confrm.lib import jsonize %>
var values = ${jsonize(user) | n};

var form = new Form($('.form-horizontal fieldset'), fields, values);
function submit() {
  $.ajax('/users/update/${user.id}', {
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
