<%inherit file='/master.mako' />

<div style="margin: 50px auto; width: 268px;">
  <h3>Please login first:</h3>
  <div class="well form-vertical">
    <div class="control-group">
      <label for="email">Email</label>
      <input type="text" id="email" />
    </div>
    <div class="control-group">
      <label for="password">Password</label>
      <input type="password" id="password" />
    </div>
    <div class="control-group">
      <button type="submit" class="btn">Sign in</button>
    </div>
  </div>
</div>

<script>
$('button[type=submit]').click(function() {
  $.ajax('/user_sessions/create', {
    type: 'POST',
    data: {email: $('#email').val(), password: $('#password').val()},
    dataType: 'json',
    success: function(data, textStatus, jqXHR) {
      $('button[type=submit]').flag({text: data.message});
    }
  });
});
</script>
