// requires jquery, underback, jquery.mustache, and local

var UserModel = Backbone.Model.extend({});
var FileModel = Backbone.Model.extend({});
var FileCollection = Backbone.Collection.extend({
  model: FileModel,
  url: '/files'
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


var TemplateView = Backbone.View.extend({
  templateName: function() {
    return this.path + '/row-' + this.state;
  },
  render: function() {
    var self = this;
    interpolate(this.templateName(), this.model.toJSON(), function(html) {
      self.$el.html(html);
    });
    return this;
  }
});

var RowView = TemplateView.extend({
  // path: '/object',
  initialize: function() {
    this.mode = 'normal';
    return this.render();
  },
  templateName: function() {
    return this.path + '/row-' + this.mode;
  },
  events: {
    'click a.state': 'setMode',
    'click a[data-method=DELETE]': 'delete',
    'click .save': 'save'
  },
  setMode: function(ev) {
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
  delete: function(ev) {
    ev.preventDefault();
    this.model.destroy({
      success: function(model, response) {
        // console.log('success:data', response);
        $(ev.target).flag({text: response.message, fade: 2000});
      }
    });
    // ajax($(ev.target).attr('href'), function(data) {
    //   console.log(data);
    //   $(ev.target).flag({text: data.message, fade: 2000});
    // });
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

// var UserRow = StatefulRowView.extend({
//   path: 'users'
// });

// var FileView = StatefulRowView.extend({
//   path: 'files',
//   events: _.extend({
//     'change textarea': 'changed'
//   }, StatefulRowView.prototype.events),
//   changed: function(ev) {
//     this.model.set('contents', ev.target.value);
//   }
// });

var ListView = Backbone.View.extend({
  item: StatefulRowView,
  initialize: function() {
    return this.render();
  },
  render: function() {
    var self = this;
    this.collection.forEach(function(model) {
      var subview = new self.item(model);
      self.$el.append(subview.$el);
    });
  }
});

var FileCollectionView = ListView.extend({item: FileView});

// FileRow.addToTable = function(raw_file, $table) {
//   var file_model = new FileModel(raw_file),
//     row = new FileRow({model: file_model});
//   $table.append(row.$el);
//   return row;
// };
