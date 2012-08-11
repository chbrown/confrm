// requires jquery, jquery.fileuploader, local
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
    this.$('form').fileupload({
      // acceptFileTypes: /(\.|\/)(csv|tsv|xls|xlsx|txt)$/i,
      // maxFileSize: 20000000,
      autoUpload: true,
      dropZone: $('#dropzone')
    })
    .bind('fileuploadadd', function(ev, status) {
      $('.progress').fadeTo('fast', 1);
    })
    .bind('fileuploaddone', function(ev, status) {
      $('#files').datagrid();
      setTimeout(function() {
        $('.progress .bar').width((status.loaded / status.total) * 100 + '%');
        $('.progress').fadeTo('slow', 0.01);
        setTimeout(function() {
          $('.progress .bar').width('0%');
        }, 1000);
      }, 2000);
    })
    .bind('fileuploadprogressall', function(ev, status) {
      $('.progress .bar').width((status.loaded / status.total) * 100 + '%');
    })
    .bind('fileuploaddrop', function(ev, status) {
      console.log('fileuploaddrop', ev, status);
      // $('#dropzone').removeClass('btn btn-success');
    })
    .bind('fileuploaddragover', function(ev) {
      var $dropZone = $('#dropzone'),
        timeout = window.dropZoneTimeout;
      // console.log('fileuploaddragover', $dropZone, ev);
      if (!timeout) {
        $dropZone.addClass('in');
      } else {
        clearTimeout(timeout);
      }
      if (ev.target === $dropZone[0]) {
        $dropZone.addClass('hover');
      } else {
        $dropZone.removeClass('hover');
      }
      window.dropZoneTimeout = setTimeout(function () {
        window.dropZoneTimeout = null;
        $dropZone.removeClass('in hover');
      }, 100);
    });
  }
});



// function logf(prefix) {
//   return function() {
//     console.log('[' + prefix + ']', arguments);
//   }
// }
// .bind('fileuploaddestroy',    logf('fileuploaddestroy'    ))
// .bind('fileuploadadded',      logf('fileuploadadded'      ))
// .bind('fileuploadstarted',    logf('fileuploadstarted'    ))
// .bind('fileuploadsent',       logf('fileuploadsent'       ))
// .bind('fileuploadcompleted',  logf('fileuploadcompleted'  ))
// .bind('fileuploadfailed',     logf('fileuploadfailed'     ))
// .bind('fileuploadstopped',    logf('fileuploadstopped'    ))
// .bind('fileuploaddestroyed',  logf('fileuploaddestroyed'  ))
// .bind('fileuploadsubmit',     logf('fileuploadsubmit'     ))
// .bind('fileuploadsend',       logf('fileuploadsend'       ))
// .bind('fileuploadfail',       logf('fileuploadfail'       ))
// .bind('fileuploadalways',     logf('fileuploadalways'     ))
// .bind('fileuploadprogress',   logf('fileuploadprogress'   ))
// .bind('fileuploadstart',      logf('fileuploadstart'      ))
// .bind('fileuploadstop',       logf('fileuploadstop'       ))
// .bind('fileuploadchange',     logf('fileuploadchange'     ))
// .bind('fileuploadpaste',      logf('fileuploadpaste'      ))
