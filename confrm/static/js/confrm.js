function post(url, data, callback) {
  if (callback === undefined && typeof data === 'function') {
    callback = data;
    data = undefined;
  }
  $.ajax(url, {
    type: 'POST',
    data: data,
    dataType: 'json',
    success: function(response, textStatus, jqXHR) {
      callback(response);
    },
    error: function(jqXHR, textStatus, errorThrown) {
      var response;
      // console.log(jqXHR.status);
      // jqXHR.status, jqXHR.statusText, jqXHR.responseText
      try {
        response = JSON.parse(jqXHR.responseText);
      }
      catch (exc) {
        response = {success: false, message: 'Request failed: ' + jqXHR.statusText + ' (' + jqXHR.status + ')'};
      }
      callback(response);
    }
  });
}

function auto(string) {
  return string.replace(/_/g, ' ').split(/\s+/).map(function(part) {
    return part[0].toUpperCase() + part.slice(1);
  }).join(' ');
}

(function($) {
  $.fn.datagrid = function(render) {
    return this.each(function() {
      var $this = $(this),
          $tbody = $this.children('tbody'),
          url = $this.attr('data-url');

      // cache the render function, or pull it from cache if needed
      // (need failover if it's not in the cache, either)
      if (render === undefined)
        render = $this.data('render');
      else
        $this.data('render', render);

      // make sure there is a tbody (which will be cleared)
      if (!$tbody.length)
        $tbody = $('<tbody></tbody>').appendTo($this);

      $.ajax(url, {
        dataType: 'json',
        success: function(response, textStatus, jqXHR) {
          $tbody.empty();
          response.data.forEach(function(item) {
            var tr = render(item);
            $this.append(tr);
          });
        }
      });
    });
  };
})(jQuery);

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

Widgets.multiline = function() {};
$.extend(Widgets.multiline.prototype, Widgets.text.prototype);
Widgets.multiline.prototype.init = function($container, field, value) {
  this.$input = $('<textarea id="' + field.key + '">' + (value || '') + '</textarea>').appendTo($container);
  this.$input.css({width: '90%', height: '300px'});
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
  var input_html = '<input type="text" class="input-xlarge" id="' + field.key + '" value="' + (value || '') + '">';
  this.$input = $(input_html).appendTo($container);
  this.$input.on('change', function() {
    var parts = [];
    $(this).val().replace(/[- _]+/g, '-').split(',').forEach(function(part) {
      part = part.replace(/^-|-$/g, '');
      if (part)
        parts.push(part);
    });
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
    $container.append('<label class="radio"><input type="radio" name="' + field.key + '" value="' + option + '"> ' + auto(option) + '</label> ');
  });
  if (field['default'])
    $container.find('input[value="' + field['default'] + '"]').prop('checked', true);
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
  var $select = $('<select><option value="">-- not set --</option></select>').appendTo($container);
  $.ajax(field.url, {
    dataType: 'json',
    success: function(data, textStatus, jqXHR) {
      // console.log($select, data);
      var values = [];
      for (var key in data) {
        if ($.isArray(data[key]))
          values = data[key];
      }
      values.map(function(value) {
        $('<option />').html(value.name).val(value.id).appendTo($select);
      });
    }
  });
  this.$select = $select;
};
Widgets.object.prototype.get = function() {
  return this.$select.find('option:selected').val();
};
