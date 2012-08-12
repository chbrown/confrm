// requires jquery, underback, jquery.mustache, and local

var UserModel = Backbone.Model.extend({
});

var FileModel = Backbone.Model.extend({
  urlRoot: '/files'
});
// FileModel.prototype.beforeGet = function(key) {
//   if (key === 'contents' && this.get(key) === undefined) {
//     this.fetch();
//   }
// };
// FileModel.prototype.get = function(key) {
//   console.log('FileModel.prototype.get', key);
//   this.beforeGet(attrs);
//   FileModel.__super__.get.apply(this, arguments);
// };


var RowView = Backbone.View.extend({
  tagName: 'tr',
  initialize: function() {
    return this.render();
  },
  useTemplate: function(template_name) {
    var self = this;
    interpolate(template_name, this.model.toJSON(), function(html) {
      self.$el.html(html);
    });
    return this;
  }
});

var StatefulRowView = RowView.extend({
  state: 'normal',
  events: {
    'click a.state': 'changeState',
    'click a[data-method=DELETE]': 'clickDelete',
    'click .save': 'save'
  },
  changeState: function(ev) {
    ev.preventDefault();
    this.state = $(ev.target).attr('data-state');
    var self = this;
    if (this.state !== 'normal') {
      this.model.fetch({
        success: function() {
          self.render();
        }
      });
    }
    else {
      this.render();
    }
  },
  clickDelete: function(ev) {
    ev.preventDefault();
    var $a = $(ev.target);
    ajax($a.attr('href'), function(data) {
      console.log(data);
      $a.flag({text: data.message});
    });
  },
  render: function() {
    if (this.state === undefined) this.state = 'normal'; // not sure why this happens
    return this.useTemplate(this.path + '/row-' + this.state);
  },
  save: function(ev) {
    ev.preventDefault();
    console.log('model saving');
    this.model.save({}, {
      success: function(model, response) {
        // console.log('success:data', response);
        $(ev.target).flag({text: response.message, fade: 2000});
      }
    });
  }
});

var UserRow = StatefulRowView.extend({
  path: 'users'
});

var FileRow = StatefulRowView.extend({
  path: 'files',
  events: _.extend({
    'change textarea': 'changed'
  }, StatefulRowView.prototype.events),
  changed: function(ev) {
    // console.log('content changed');
    this.model.set('contents', ev.target.value);
  }
});
FileRow.addToTable = function(raw_file, $table) {
  var file_model = new FileModel(raw_file),
    row = new FileRow({model: file_model});
  $table.append(row.$el);
  return row;
};

  // (function($) {
  //   $.fn.datagrid = function(render) {
  //     return this.each(function() {
  //       var $this = $(this),
  //           $tbody = $this.children('tbody'),
  //           url = $this.attr('data-url');

  //       // cache the render function, or pull it from cache if needed
  //       // (need failover if it's not in the cache, either)
  //       if (render === undefined)
  //         render = $this.data('render');
  //       else
  //         $this.data('render', render);

  //       // make sure there is a tbody (which will be cleared)
  //       if (!$tbody.length)
  //         $tbody = $('<tbody></tbody>').appendTo($this);

  //       $.ajax(url, {
  //         dataType: 'json',
  //         success: function(response, textStatus, jqXHR) {
  //           $tbody.empty();
  //           response.data.forEach(function(item) {
  //             var tr = render(item);
  //             $this.append(tr);
  //           });
  //         }
  //       });
  //     });
  //   };
  // })(jQuery);
// });

