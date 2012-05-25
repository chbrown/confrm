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
<script src="/static/js/date.js"></script>
<div id="container">
  <div id="navbar">
    <h2>ConfRM</h2>
    <h3>${site.name}</h3>
    <!-- <i class="icon-home"></i> -->
    <a href="/users/index" class="btn"><i class="icon-user"></i> Users</a>
    <a href="/events/index" class="btn"><i class="icon-calendar"></i> Events</a>
    <a href="/uploads/index" class="btn"><i class="icon-plus"></i> Uploads</a>
  </div>
  <div id="content">
    ${next.body()}
  </div>
</div>
<script>
</script>
