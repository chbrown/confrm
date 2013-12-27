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
  $.ajax(url, {type: 'POST', data: JSON.stringify(data), contentType: 'application/json', dataType: 'json'})
    .done(function(response, textStatus, jqXHR) {
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
  if (localStorage[cache_key] && !debug)
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

// requires jquery, jquery.fileuploader, local
// function logf(prefix) {
//   return function() {
//     console.log('[' + prefix + ']', arguments);
//   };
// }

var FileUploader = Backbone.View.extend({
  initialize: function(options) {
    if (options) this.title = options.title;
    this.render();
  },
  render: function() {
    var self = this;
    interpolate('files/upload', {title: this.title || 'Add file'}, function(html) {
      self.$el.html(html);
      self.activate();
    });
    return this;
  },
  activate: function() {
    var self = this;
    var upload = this.$('form').fileupload({
      autoUpload: true,
      dropZone: self.$('.dropzone')
    })
    .bind('fileuploaddone', function(ev, response) {
      self.trigger('done', response.result);
    })
    .bind('fileuploadprogressall', function(ev, status) {
      self.$('.bar').width((status.loaded / status.total) * 100 + '%');
    })
    .bind('fileuploaddragover', function(ev) {
      self.$('.bar').width('0');
      var $dropzone = self.$('.dropzone'),
        timeout = window.dropzoneTimeout;
      // console.log('fileuploaddragover', $dropZone, ev);
      if (!timeout) {
        $dropzone.addClass('in');
      } else {
        clearTimeout(timeout);
      }
      $dropzone.toggleClass('hover', ev.target === $dropzone[0]);
      window.dropzoneTimeout = setTimeout(function () {
        window.dropzoneTimeout = null;
        $dropzone.removeClass('in hover');
      }, 100);
    });
    // .bind('fileuploadadd', function(ev, data) { })
    // .bind('fileuploadalways',     logf('fileuploadalways'     ))
    // .bind('fileuploaddone',       logf('fileuploaddone'     ))
    // .bind('fileuploadfail',       logf('fileuploadfail'       ))
    // .bind('fileuploadfailed',     logf('fileuploadfailed'     ))
    // .bind('fileuploaddestroy',    logf('fileuploaddestroy'    ))
    // .bind('fileuploadadded',      logf('fileuploadadded'      ))
    // .bind('fileuploadstarted',    logf('fileuploadstarted'    ))
    // .bind('fileuploadsent',       logf('fileuploadsent'       ))
    // .bind('fileuploadcompleted',  logf('fileuploadcompleted'  ))
    // .bind('fileuploadstopped',    logf('fileuploadstopped'    ))
    // .bind('fileuploaddestroyed',  logf('fileuploaddestroyed'  ))
    // .bind('fileuploadsubmit',     logf('fileuploadsubmit'     ))
    // .bind('fileuploadsend',       logf('fileuploadsend'       ))
    // .bind('fileuploadprogress',   logf('fileuploadprogress'   ))
    // .bind('fileuploadstart',      logf('fileuploadstart'      ))
    // .bind('fileuploadstop',       logf('fileuploadstop'       ))
    // .bind('fileuploadchange',     logf('fileuploadchange'     ))
    // .bind('fileuploadpaste',      logf('fileuploadpaste'      ))
  }
});
