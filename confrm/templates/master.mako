<!DOCTYPE html>
<meta charset="utf-8">
<link rel="stylesheet/less" href="/static/css/master.less">
<script src="/static/js/less.js"></script>
<link rel="Shortcut Icon" href="http://henrian.com/favicon.ico">
<link rel="icon" href="http://henrian.com/favicon.ico" type="image/x-icon">
<title>ConfRM</title>
<script src="/static/js/underscore.js"></script>
<script src="/static/js/jquery.js"></script>
<script src="/static/js/date.js"></script>
<div id="container">
  <div id="navbar">
    <h1>ConfRM</h1>
    <h2>${site.name}</h2>
    <a href="/users/index" class="btn">Users</a>
    <a href="/events/index" class="btn">Events</a>
    <a href="/uploads/index" class="btn">Uploads</a>
  </div>
  <div id="content">
    ${next.body()}
  </div>
</div>
