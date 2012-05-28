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
    widget.help = field.help || '';
    widget.field = field;
    widget.init($controls, field, value);
    if (widget.help)
      $controls.append('<p class="help-block">' + field.help + '</p>');
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
  this.help += '<br/>Separate with commas. Spaces and underscores will be merged and converted to hyphens.';
  var input_html = '<input type="text" class="input-xlarge" id="' + field.key + '" value="' + (value || '') + '">';
  this.$input = $(input_html).appendTo($container);
  this.$input.on('change', function() {
    var raw = $(this).val();
    var parts = raw.replace(/[ _]+/g, '-').split(',');
    $(this).val(parts.join(', '));
  });
};
Widgets.csv.prototype.get = function() {
  return this.$input.val().split(',');
};

Widgets.radiolist = function() {};
Widgets.radiolist.prototype.init = function($container, field, value) {
  this.$container = $container;
  field.children.map(function(option, i) {
    $container.append('<label class="checkbox"><input type="radio" value="' + option + '"> ' + option + '</label> ');
  });
};
Widgets.radiolist.prototype.get = function() {
  return this.$container.find('input:checked').val();
};

Widgets.list = function() {};
Widgets.list.prototype.init = function($container, field, value) {
};
Widgets.list.prototype.get = function() {
};


Widgets.object = function() {};
Widgets.object.prototype.init = function($container, field, value) {
  var $select = $('<select></select>').appendTo($container);
  $.ajax(field.url, {
    success: function(data, textStatus, jqXHR) {
      console.log($select);
      // data
    }
  });
  this.$select = $select;
};
Widgets.object.prototype.get = function() {
  return this.$select.find('option:selected').val();
};
