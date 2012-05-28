function auto(string) {
  return string.replace(/_/g, ' ').split(/\s+/).map(function(part) {
    return part[0].toUpperCase() + part.slice(1);
  }).join(' ');
}

function Form($form, fields, values) {
  this.widgets = fields.map(function(field) {
    var value = values[field.key];
    var $controls = bootstrapWrapper($form, field);
    var widget = new Widgets[field.type]();
    widget.field = field;
    widget.init($controls, field, value);
    return widget;
  });
}
Form.prototype.get = function() {
  var values = {};
  this.widgets.forEach(function(widget) {
    values[widget.field.key] = widget.get();
  });
  return values;
};

function bootstrapWrapper($container, field) {
  var $group = $('<div class="control-group"></div>').appendTo($container);
  $group.append('<label class="control-label" for="' + field.key + '">' + auto(field.key) + '</label>');
  return $('<div class="controls"></div>').appendTo($group);
  // if (field.help) {
    // $controls.append('<p class="help-block">What tags should be applied to each user below?</p>');
  // }
}


var Widgets = {};
Widgets.text = function() {};
Widgets.text.prototype.init = function($container, field, value) {
  this.$input = $('<input type="text" id="' + field.key + '" value="' + (value || '') + '">').appendTo($container);
};
Widgets.text.prototype.get = function() {
  return this.$input.val();
};

Widgets.bool = function() {};
Widgets.bool.prototype.init = function($container, field, value) {
  this.$input = $('<input type="checkbox" id="' + field.key + '" ' + (value ? 'checked="checked"' : '') + '>');
  $('<label class="checkbox">' + (field.label || '') + '</label>').append(this.$input).appendTo($container);
};
Widgets.bool.prototype.get = function() {
  return this.$input.prop('checked');
};

Widgets.csv = function() {};
Widgets.csv.prototype.init = function($container, field, value) {
  this.$input = $('<input type="text" id="' + field.key + '" value="' + (value || '') + '">').appendTo($container);
};
Widgets.csv.prototype.get = function() {
  return this.$input.val();
};
