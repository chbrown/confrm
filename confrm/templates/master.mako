<%! from confrm.lib import jsonize %>
<!DOCTYPE html>
<meta charset="utf-8">
<link rel="stylesheet/less" href="/static/css/master.less">
<script src="/js/lib/less.js"></script>
<link rel="Shortcut Icon" href="/static/img/favicon.ico">
<link rel="icon" href="/static/img/favicon.ico" type="image/x-icon">
<title>ConfRM</title>
<script src="/js/lib/head.js"></script>
<div id="navbar">
  <h2>ConfRM</h2>
  % if organization:
    <h3>${organization.name}</h3>
    /{organization.slug}
  % endif
  <a href="/users" class="btn"><i class="icon-user"></i> Users</a>
  <a href="/files" class="btn"><i class="icon-file"></i> Files</a>
  <a href="/groups" class="btn"><i class="icon-calendar"></i> Groups</a>
  <span class="center"></span>
  <span class="right">
    % if user:
      <a href="/users/${user.id}">${user.full_name or user.email}</a>
    % endif
  </span>
</div>
<div>
  ${next.body()}
</div>
<script>
var debug = ${jsonize(debug) | n};
var flash = window.location.search.match(/[?&]flash=([^?&]+)/);
// '/js/lib/jquery.tablesorter.js', // $('.tablesorter').tablesorter();
head.js('/js/lib/jquery.js', '/js/lib/jquery.flags.js', function() {
  if (flash) $('#navbar h2').flag({text: flash[1].replace(/\+/g, ' '), anchor: 'r'});
});
head.js('/js/lib/underscore.js').js('/js/lib/date.js').js('/js/local.js').js('/js/lib/jquery.cookie.js');
</script>