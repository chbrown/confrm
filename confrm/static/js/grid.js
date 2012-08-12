// requires jquery, underback, jquery.mustache, and local

var UserModel = Backbone.Model.extend({
});

var FileModel = Backbone.Model.extend({
  url: function() {
    return '/files/show/' + this.get('id');
  }
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

var UserRow = RowView.extend({
  render: function() {
    return this.useTemplate('users/row');
  }
});

var FileRow = RowView.extend({
  events: {
    'click a.state': 'clickState',
    'click a[data-method=DELETE]': 'clickDelete'
  },
  clickState: function(ev) {
    ev.preventDefault();
    var self = this, state = $(ev.target).attr('data-state');
    this.model.fetch({
      success: function() {
        return self.useTemplate('files/row-' + state);
      }
    });
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
    return this.useTemplate('files/row-normal');
  }
});
FileRow.addToTable = function(raw_file, $table) {
  var file_model = new FileModel(raw_file),
    row = new FileRow({model: file_model});
  $table.append(row.$el);
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

