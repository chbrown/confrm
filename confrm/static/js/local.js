// requires: jquery, jquery.mustache
var DATE_FORMAT = 'MMMM d, yyyy, h:mm tt';
function refresh() { window.location = window.location; }
function auto(string) {
  return string.replace(/_/g, ' ').split(/\s+/).map(function(part) {
    return part[0].toUpperCase() + part.slice(1);
  }).join(' ');
}

function ajax(url, data, callback) {
  if (callback === undefined) {
    callback = data;
    data = undefined;
  }
  $.ajax(url, {type: 'POST', data: data, contentType: 'application/json', dataType: 'json'})
    .done(function(data, textStatus, jqXHR) {
      callback(response);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      var response;
      try {
        response = JSON.parse(jqXHR.responseText);
        response.success = false;
      }
      catch (exc) {
        response = {success: false, message: 'Request failed: ' + jqXHR.statusText + ' (' + jqXHR.status + ')'};
      }
      callback(response);
    });
}

function getTemplate(template_name, callback) {
  // callback signature (template_str)
  // not necessarily async (by design)
  var cache_key = 'templates:' + template_name;
  if (localStorage[cache_key])
    return callback(localStorage[cache_key]);
  $.get('/templates/' + template_name + '.mu', function(template) {
    localStorage[cache_key] = template;
    callback(template);
  });
}
function interpolate(template_name, context, callback) {
  // callback signature (html_str)
  return getTemplate(template_name, function(template_string) {
    return callback($.mustache(template_string, context));
  });
}

// function Uploader(callback) {
//   // callback signature: function(file_id)
//   this.callback = callback;
// }
