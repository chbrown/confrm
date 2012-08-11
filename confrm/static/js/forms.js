// requires: jquery, underback, local
var Widgets = {}, Form = Backbone.View.extend({
  initialize: function(options) {
    this.fields = options.fields;
    this.values = options.values;
    this.widgets = [];
    this.render();
  },
  render: function() {
    var self = this;
    (function next() {
      var field = self.fields.shift();
      if (field) {
        field.value = self.values[field.key];
        interpolate('forms/group', field, function(html) {
          var $control_group = $(html).appendTo(self.$el);
          var widget = new Widgets[field.type]({el: $control_group.children('.controls'), field: field});
          self.widgets.push(widget);
          next();
        });
      }
    })();
    return this;
  },
  get: function() {
    var values = {};
    this.widgets.forEach(function(widget) {
      values[widget.field.key] = widget.get();
    });
    return values;
  }
});

Widgets.base = Backbone.View.extend({
  initialize: function(options) {
    this.field = options.field;
  },
  render: function() {
    interpolate('forms/' + this.type, this.field, function(template) {
      this.$el.html(this.field);
    });
    return this;
  }
});

Widgets.text = Widgets.base.extend({
  val: function() {
    return this.$('input').val();
  }
});

Widgets.multiline = Widgets.base.extend({
  val: function() {
    return this.$('textarea').val();
  }
});

Widgets.bool = Widgets.base.extend({
  val: function() {
    return this.$input.prop('checked');
  }
});

Widgets.csv = Widgets.base.extend({
  events: {
    'change input': 'inputChange'
  },
  inputChange: function() {
    var parts = [], $input = this.$('input');
    $input.val().replace(/[- _]+/g, '-').split(',').forEach(function(part) {
      part = part.replace(/^-|-$/g, '');
      if (part)
        parts.push(part);
    });
    $input.val(parts.join(', '));
  },
  val: function() {
    return this.$('input').val().split(/\s*,\s*/);
  }
});

Widgets.radiolist = Widgets.base.extend({
  render: function() {
    this.field.children.forEach(function(child) {
      child.option_auto = auto(option);
    });
    if (field['default'])
      this.$('input[value="' + field['default'] + '"]').prop('checked', true);
    return this;
  },
  val: function() {
    return this.$('input:checked').val();
  }
});

// Widgets.list = Widgets.base.extend({
//   render: function($container, field, value) {
//   },
//   val: function() {
//   }
// });

Widgets.object = Widgets.base.extend({
  render: function() {
    var $select = $('<select><option value="">-- not set --</option></select>').appendTo(this.$el);
    ajax(this.field.url, function(result) {
      var values = [];
      for (var key in data) {
        if ($.isArray(data[key]))
          values = data[key];
      }
      values.map(function(value) {
        $select.append('<option value="' + value.id + '">' + value.name + '</option>');
      });
    });
    return this;
  },
  val: function() {
    return this.$('option:selected').val();
  }
});

for (var type in Widgets) Widgets[type].type = type;
