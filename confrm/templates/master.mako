<%! from confrm.lib import jsonize %>
<!DOCTYPE html>
<meta charset="utf-8">
<link rel="stylesheet/less" href="/static/css/master.less">
<script src="/js/lib/less.js"></script>
<link rel="Shortcut Icon" href="/static/img/favicon.ico">
<link rel="icon" href="/static/img/favicon.ico" type="image/x-icon">
<title>ConfRM</title>
<script src="/js/lib/head.js"></script>
<script>
head.ls = function(scripts, callback) {
  if (callback) scripts.push(callback);
  head.js.apply(head, scripts);
})
var debug = ${jsonize(debug) | n},
  script = {
    jquery: '/js/lib/jquery.js',
    underback: '/js/lib/underback.js',
    jqueryui: '/js/lib/jquery-ui.js',
    jqueryfileupload: '/js/lib/jquery.fileupload.js',
    jqueryfileuploadui: '/js/lib/jquery.fileupload-ui.js',
    jquerycookie: '/js/lib/jquery.cookie.js',
    date: '/js/lib/date.js',
    mu: '/js/lib/jquery.mustache.js',

    forms: '/js/forms.js',
    local: '/js/local.js',
    models: '/js/models.js'
  },
  scripts = {
    uploader: [script.jquery, script.underback, script.jqueryui, script.jqueryfileupload,
      script.jqueryfileuploadui, script.fileupload, script.mu, script.local, script.models],
    flags: [script.jquery, script.flags],
    basic: [script.jquery, script.underback, script.local, script.models],
    // script.date, script.jquerycookie,
  };
</script>

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
flash = window.location.search.match(/[?&]flash=([^?&]+)/),
head.js(scripts.flags, function() {
  if (flash) {
    var $focal_point = $('.focal-point');
    if (!$focal_point.length) $focal_point = $('#navbar h2');
    $focal_point.flag({
      text: flash[1].replace(/\+/g, ' '),
      anchor: 'l'
    });
  }
}).js(script.basic);
</script>
