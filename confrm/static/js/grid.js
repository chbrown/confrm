// requires jquery, underback, jquery.mustache, and local
var RowView = Backbone.View.extend({
  tagName: 'tr',
  initialize: function() {
    return this.render();
  }
});

var UserRow = RowView.extend({
  render: function() {
    var self = this;
    interpolate('users/single', this.model, function(html) {
      self.$el.html(html);
    });
    return this;
  }
});

var FileRow = RowView.extend({
  render: function() {
    var self = this;
    interpolate('files/single', this.model, function(html) {
      self.$el.html(html);
    });
    return this;
  }
});

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

