<!DOCTYPE html>
<meta charset="utf-8">
<link rel="stylesheet/less" href="/static/css/master.less">
<script src="/static/js/less.js"></script>
<link rel="Shortcut Icon" href="/static/img/favicon.ico">
<link rel="icon" href="/static/img/favicon.ico" type="image/x-icon">
<title>ConfRM</title>
<script src="/static/js/underscore.js"></script>
<script src="/static/js/jquery.js"></script>
<script src="/static/js/jquery.flags.js"></script>
<script src="/static/js/jquery.tablesorter.js"></script>
<script src="/static/js/date.js"></script>
<script src="/static/js/jquery.cookie.js"></script>
<script src="/static/js/confrm.js"></script>
<div id="navbar">
  <h2>ConfRM</h2>
  % if organization:
    <h3>${organization.name}</h3>
  % endif
  <!-- <i class="icon-home"></i> -->
  <a href="/users/index" class="btn"><i class="icon-user"></i> Users</a>
  <a href="/files/index" class="btn"><i class="icon-plus"></i> Files</a>
  % if organization:
    <a href="/{organization.slug}/groups/index" class="btn"><i class="icon-calendar"></i> Groups</a>
  % endif
</div>
<div class="container">
  ${next.body()}
</div>
<script>
  $('.tablesorter').tablesorter();
  var flash = window.location.search.match(/[?&]flash=([^?&]+)/);
  if (flash)
    $('#navbar h2').flag({text: flash[1].replace(/\+/g, ' ')});
</script>
