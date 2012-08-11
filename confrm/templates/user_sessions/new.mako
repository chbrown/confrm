<%inherit file='/master.mako' />

<div style="margin: 50px auto; width: 268px;">
  <h3>Please login:</h3>
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
head(function() {
  function submit() {
    ajax('/user_sessions/create', {email: $('#email').val(), password: $('#password').val()}, function(data) {
      $('button[type=submit]').flag({text: data.message});
      if (data.success) {
        $.cookie('ticket', data.ticket, {expires: 31, path: '/'});
        var return_url = window.location.search.match(/[?&]url=([^?&]+)/);
        // window.location = return_url ? decodeURIComponent(return_url[1]) : '/users/index';
      }
    });
  }
  $('button[type=submit]').click(submit);
  $('.form-vertical').on('keypress', function(ev) {
    if (ev.keyCode === 13 && ev.target.type !== "textarea") {
      ev.preventDefault();
      submit();
    }
  });
});
</script>
