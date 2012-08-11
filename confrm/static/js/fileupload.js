// requires jquery, jquery.fileuploader, local
function logf(prefix) {
  return function() {
    console.log('[' + prefix + ']', arguments);
  };
}

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
  done: function(result) {
    console.log('Done event result', result);
  },
  activate: function() {
    var self = this;
    var upload = this.$('form').fileupload({
      autoUpload: true,
      dropZone: self.$('.dropzone')
    })
    .bind('fileuploadadd', function(ev, data) {
      self.$('.bar').width('0');
    })
    .bind('fileuploaddone', function(ev, response) {
      self.done(response.result);
    })
    .bind('fileuploadprogressall', function(ev, status) {
      self.$('.bar').width((status.loaded / status.total) * 100 + '%');
    })
    .bind('fileuploaddragover', function(ev) {
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
    // .bind('fileuploadalways',     logf('fileuploadalways'     ))
    // .bind('fileuploaddone',     logf('fileuploaddone'     ))
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


