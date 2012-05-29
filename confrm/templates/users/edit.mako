<%inherit file='/master.mako' />

<div class="form-horizontal">
  <fieldset><legend>Edit User</legend></fieldset>
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
var $submit = $('button[type=submit]').click(submit);
function submit() {
  post('/users/update/${user.id}', form.get(), function(data) {
     $submit.flag({text: data.message});
  });
}
</script>
