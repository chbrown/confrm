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
  <a href="/users/index" class="btn"><i class="icon-user"></i> Users</a>
  <a href="/files/index" class="btn"><i class="icon-file"></i> Files</a>
  <a href="/groups/index" class="btn"><i class="icon-calendar"></i> Groups</a>
  <span></span>
</div>
<div>
  ${next.body()}
</div>
<script>
var flash = window.location.search.match(/[?&]flash=([^?&]+)/);
head.js('/js/lib/jquery.js', '/js/lib/jquery.flags.js', '/js/lib/jquery.tablesorter.js', '/js/lib/jquery.cookie.js', function() {
  $('.tablesorter').tablesorter();
  if (flash) {
    console.log('flash', flash);
    $('#navbar h2').flag({text: flash[1].replace(/\+/g, ' '), anchor: 'r'});
  }
  $(document).on('click', 'a[data-method=DELETE]', function(ev) {
    ev.preventDefault();
    var $a = $(this);
    post($a.attr('href'), function(data) {
      console.log(data);
      $a.flag({text: data.message});
    });
  });
});
head.js('/js/lib/underscore.js').js('/js/lib/date.js').js('/js/local.js');
</script>