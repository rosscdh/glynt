/**
* Handlebars helpers that assist in the creation of document variables
* generally the output html that allows us to bind DOM events
*/

Handlebars.registerHelper('doc_var', function(options) {

    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_var requires a unique "name"');
    }
    var app = window.app || eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var field_type = 'text';
    var has_initial = (options.hash.initial === undefined) ? false : true;
    var value = null;
    var html_return = null;

    if (options.hash.field_type !== undefined && options.hash.field_type === '') {
        field_type = options.hash.field_type;
    }
    // see if this options.name is already defined in the app context (to get user populated data)
    if (has_initial === false) {
        options.hash.initial = options.fn(this);
    }

    value = (options.hash.initial !== undefined) ? options.hash.initial : '' ;
    value = (app.context[var_name] === undefined) ? value : app.context[var_name] ;

    // add value to context
    if (app.context[var_name] === undefined) {
        // set to nul because we know it is undefined; assert positive
        app.context[var_name] = null;
    }
    options.hash.type = 'doc_var';
    options.hash.field_type = field_type;
    options.hash.variable_name = var_name;
    options.hash.value = value;
    options.hash.has_initial = has_initial;

    // wrap the value in our detailed html to allow UX interaction
    html_return = Handlebars.partials['doc_var-partial'];

    // set the context
    options.hash.id = MD5(String(var_name + app.context.length+1));
    app.context[var_name] = options.hash;

    // make it safe so hb does not mess with it
    return html_return(options.hash);
});


Handlebars.registerHelper('doc_choice', function(options) {
    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_choice requires a unique "name"');
    }

    if (options.hash.choices === undefined || options.hash.choices.length <= 0) {
        console.log('"{name}" is a doc_choice element and requires a "choices" list i.e. "a,b,c"]'.assign({'name': options.hash.name}));
        options.hash.choices = [];
        options.hash.initial = '[Error] You must provide a set of choices';
    } else {
        options.hash.choices = options.hash.choices.split(',');
    }
    var app = window.app || eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var choices = options.hash.choices;
    var has_initial = (options.hash.initial === undefined) ? false : true;
    if (has_initial === false) {
        options.hash.initial = options.fn(this);
    }
    value = (options.hash.initial !== undefined) ? options.hash.initial : '' ;
    value = (app.context[var_name] === undefined) ? value : app.context[var_name] ;
    options.hash.value = value;

    var html_return = Handlebars.partials['doc_choice-partial'];

    // set the context
    options.hash.id = MD5(String(var_name + app.context.length+1));
    app.context[var_name] = options.hash;

    // make it safe so hb does not mess with it
    return html_return(options.hash);
});


Handlebars.registerHelper('doc_select', function(options) {
    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_select requires a unique "name"');
    }
    var app = window.app || eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var label = (options.hash.label === undefined) ? false: options.hash.label;
    var can_toggle = (options.hash.can_toggle === undefined) ? false: options.hash.can_toggle;
    var multi = (options.hash.multi === undefined) ? false: options.hash.multi;

    options.hash.label = label;
    options.hash.variable_name = var_name;
    options.hash.can_toggle = can_toggle;
    options.hash.multi = multi;
    options.hash.id = MD5(String(var_name + app.context.length+1));

    var html_return = '';
    // get the inner content
    var content = options.fn(this);
    // split it based on the {option} seperator as per our docs
    options.hash.select_options = [];
    select_options = content.split('{option}');// splti by the {option} seperator
    // setup the partial list
    for (var i = 0; i < select_options.length; i++) {
        options.hash.select_options.push({
            'id': '{id}-{index}'.assign({'id': options.hash.id, 'index': i}),
            'text': new Handlebars.SafeString(select_options[i]),
            'handle': 'Select',
            'target': options.hash.id,
            'selected': false,
            'index': i
        });
    }

    // set the context
    app.context[var_name] = options.hash;

    html_return = Handlebars.partials['doc_select-partial'];

    if (can_toggle == true) {
        var toggle = Handlebars.partials['toggle-partial'];
        var show_toggle = (app.context[var_name] === undefined || app.context[var_name].show_toggle === undefined || app.context[var_name].show_toggle === true) ? true : false;
        toggle_hash = {
            'toggle_for': var_name,
            'label': label,
            'text': (show_toggle == false) ? 'Show': 'Hide'
        };
        return html_return(options.hash) + toggle(toggle_hash);
    } else {
        return html_return(options.hash);
    }
});


Handlebars.registerHelper('help_for', function(options) {
    if (options.hash.varname === undefined || options.hash.varname === '') {
        throw new Error('help_for requires a "varname"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.varname;
    var content = options.fn(this).compact();

    if (app.context[var_name] === undefined || typeof app.context[var_name] !== 'object') {
        throw new Error('There is no variable named "{varname}" that is an "object" in the app.context'.assign({'varname': varname}));
    }else{
        app.context[var_name].help_text = content;
    }
});

Handlebars.registerHelper('doc_note', function(options) {
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var content = options.fn(this);
    content = content.split('{note}');
    var note = content[1];
    content = content[0];

    options.hash.id = MD5(note);
    app.context.notes[options.hash.id] = note;

    var html_return = Handlebars.partials['doc_note-partial'];
    return html_return({'id': options.hash.id, 'note': note, 'content': content});
});


// ----- JQUEY PLUGINS -----
// select jquery UI plugin
(function($) {
  "use strict"; // jshint ;_;

    var HelpText = function (options) {
    this.options = $.extend({}, options)
    this.init()
    this.listen()
    }

    HelpText.prototype = {
        constructor: HelpText
        , element: null
        , target: null
        , init: function () {
            var self = this;
            self.$element = $('#{id}'.assign({'id': self.options.item.id}));
            self.$target = $(self.options.help_target);
            self.listen();
        }
        , listen: function () {
            var self = this;

            self.$element.on('mouseover mouseout', function(event){
                self.toggle(event);
            });
        }
        , help_pos: function () {
            var self = this;
            var element_pos = self.$element.position();
            return {
                'left': $('#document').width()*1.1,
                'top': element_pos.top
            }
        }
        , show: function () {
            var self = this;
            var pos = self.help_pos();
            var icon = $('<i/>', {class:'icon-info-sign icon-align-left'});
            var info = $('<div/>', {class:'info-text'}).append(self.options.item.help_text)

            self.$target.css({'left': pos.left + 'px', 'top': pos.top + 'px'});
            info.prepend(icon);
            self.$target.html(info);
            self.$target.css('display', 'block');
        }
        , hide: function () {
            var self = this;
            self.$target.html('');
            self.$target.css('display', 'none');
        }
        , toggle: function (event) {
            var self = this;
            var target = self.options.help_target;

            if (event.type == 'mouseover' ) {
                console.log('show')
                self.show();
            } else {
                console.log('hide')
                self.hide();
            }

        }
    };
    $.widget("ui.help_text", {
        options: {
            help_target: $('#element_help_text')
        },
        _create: function() {
            var self = this;
            self.app = window.app;
            $.each(self.app.context, function(index, item){
                if(item.help_text !== undefined) {
                    self.app.context.help[item.name] = new HelpText({'item': item, 'help_target': self.options.help_target});
                }
            });
        }
    });

    // all editable widgets
    $.widget("ui.glynt_edit", {
      options: {},
      _create: function() {
          var self = this;
          self.app = window.app;
          self.id = $(self.element).attr('id');
          self.variable_name = $(self.element).attr('data-doc_var');
          self.context = self.app.context[self.variable_name];

          // apply the hallo editor
          $(self.element).hallo({
              plugins: {
                  'halloformat': {}
              },
              editable: true,
              showAlways: true
          });
          // GlyntTypeAhead
          if ($(self.element).hasClass('doc_choice') === false) {// only if were NOT looking at a choice element
              $(self.element).glynt_typeahead({
                  source: ['something','you typed','before']
              });
          }

          // events
          $(self.element).on('blur', function(event){
              var doc_var_name = $(this).attr('data-doc_var')
              var doc_val = $(this).html();
              if (self.app.context[doc_var_name].value != doc_val) {
                  self.app.dispatch('bind_data', {'doc_var': doc_var_name, 'value': doc_val});
              }
          });
          $(self.element).on('click', function(event){
              event.preventDefault();
              if (this.firstChild) {
                  var range = document.createRange();
                  var sel = window.getSelection();
                  range.setStartBefore(this.firstChild);
                  range.setEndAfter(this.lastChild);
                  sel.removeAllRanges();
                  sel.addRange(range);
              }
          });
      }
    });

      var Selecta = function (options) {
        //this.$element = $(element)
        this.options = $.extend({}, options)
        this.init()
        this.listen()
      }

      Selecta.prototype = {

        constructor: Selecta

        , init: function () {
            var self = this;

            // create html
            self.selecta_html = self.options.html(self.options.item);
            // appendhtml
            $('body').append(self.selecta_html);
            // set element
            self.$element = $('#{id}'.assign({'id': self.options.item.id}))

            self.widget = self.options.widget;
            self.context = self.options.widget.context;

            self.options.$parent = $("#content-{target}".assign({'target': self.options.item.id}));

            self.$target = self.options.$parent;
            self.select_options = self.widget.context.select_options;
            self.select_option = self.select_options[self.options.index];
            self.other_options = self.select_options.findAll({
                id: function(id){
                    return id !== self.select_option.id
                }
            });
            
            self.position(self.pos());
        }
        , listen: function () {
            var self = this;

            self.$element.on('click', function(event){
                event.preventDefault();
                if (self.select_option.selected === false) {
                    self.select_option.selected = true;
                    self.$element.addClass('btn-primary');
                    self.$element.find('i').removeClass('icon-star-empty')
                    self.$element.find('i').addClass('icon-star')
                } else {
                    self.select_option.selected = false;
                    self.$element.removeClass('btn-primary');
                    self.$element.find('i').removeClass('icon-star')
                    self.$element.find('i').addClass('icon-star-empty')
                }
                self.$target.toggleClass('selected');
                self.handle_is_multi();
            });

            $(window).on('resize', function() {
                self.position(self.pos());
            });
        }
        , handle_is_multi: function () {
            // if not is_multi then ensure no other items in this option_set are selected
            var self = this;
            if (self.context.multi === false) {
                $.each(self.other_options, function(index, item){
                    // content element
                    item.selecta.$target.removeClass('selected');
                    // select elemnt
                    item.selecta.select_option.selected = false;
                    item.selecta.$element.removeClass('btn-primary');
                    item.selecta.$element.find('i').removeClass('icon-star')
                    item.selecta.$element.find('i').addClass('icon-star-empty')
                });
            }
        }
        , position: function (pos) {
            // set the position of this element
            // can pass in a {left:x, top: x}
            var self = this;
            self.$element.css({'left': pos.left + 'px', 'top': pos.top + 'px' });
        }
        , pos: function () {
            // get the approximate position of the element
            // relative to its parent
            var self = this;
            var parent_pos = self.options.$parent.offset();
            return {
                'left': parent_pos.left - (self.$element.width()*3),
                'top': parent_pos.top + (self.options.$parent.height()/3.2) - (self.$element.height()/4.2)
            }
        }
      }

    $.widget("ui.glynt_select", {
        options: {},
        _create: function() {
            var self = this;
            self.app = window.app;
            self.id = $(self.element).attr('id');
            self.variable_name = $(self.element).attr('data-doc_var');
            self.context = self.app.context[self.variable_name];

            self.multi = self.context.multi;
            self.can_toggle = self.context.can_toggle;

            self.html_selecta = Handlebars.partials['doc_select-selecta-partial'];

            $.each(self.context.select_options, function(index, option){
                if (option.text.string.length > 0) {

                    self.context.select_options[index].selecta = new Selecta({
                        'widget': self,
                        'index': index,
                        'item': option,
                        'html': Handlebars.partials['doc_select-selecta-partial']
                    });
                }

            });
        }
    });

    $.widget("ui.glynt_choice", {
        options: {
            target_element: null
        },
        _create: function() {
            var self = this;
            self.app = window.app;
            var var_name = $(self.element).attr('data-doc_var');
            self.choices = self.app.context[var_name].choices;
            var element = $(self.element);

            element.glynt_typeahead({
                'source': self.choices
            });

            element.on('mouseover', function(event){
                event.preventDefault();
                $(this).css('cursor', 'pointer')
                self.options.target_element.html('Valid choices include "{choices}"'.assign({'choices': self.choices}));
            });
            element.on('mouseout', function(event){
                event.preventDefault();
                $(this).css('cursor', 'auto')
                self.options.target_element.html('');
            });
        }
    });

    $.widget("ui.glynt_note", {
        options: {
            target_element: null
        },
        _create: function() {
            var self = this;
            self.app = window.app;
            self.has_note_id = ($(self.element).attr('data-note_id') !== '') ? true: false;
            self.note_id = $(self.element).attr('data-note_id');
            self.note = self.app.context.notes[self.note_id];
            self.note_icon = $(self.element).find('.note:first');

            self.note_icon.on('mouseover', function(event){
                event.preventDefault();
                $(this).css('cursor', 'pointer')
                self.options.target_element.html(self.note);
            });
            self.note_icon.on('mouseout', function(event){
                event.preventDefault();
                $(this).css('cursor', 'auto')
                self.options.target_element.html('');
            });
        }
    });
})(jQuery);


!function($){

  "use strict"; // jshint ;_;


 /* GLYNT_TYPEAHEAD PUBLIC CLASS DEFINITION
  * ================================= */

  var GlyntTypeahead = function (element, options) {
    this.$element = $(element)
    this.options = $.extend({}, $.fn.glynt_typeahead.defaults, options)
    this.matcher = this.options.matcher || this.matcher
    this.sorter = this.options.sorter || this.sorter
    this.highlighter = this.options.highlighter || this.highlighter
    this.updater = this.options.updater || this.updater
    this.$menu = $(this.options.menu).appendTo('body')
    this.source = this.options.source
    this.shown = false
    this.listen()
  }

  GlyntTypeahead.prototype = {

    constructor: GlyntTypeahead

  , select: function () {
      var val = this.$menu.find('.active').attr('data-value')
      this.$element
        .html(this.updater(val))
        .change()
      return this.hide()
    }

  , updater: function (item) {
      return item
    }

  , show: function () {
      var pos = $.extend({}, this.$element.offset(), {
        height: this.$element[0].offsetHeight
      })

      this.$menu.css({
        top: pos.top + pos.height
      , left: pos.left
      })

      this.$menu.show()
      this.shown = true
      return this
    }

  , hide: function () {
      this.$menu.hide()
      this.shown = false
      return this
    }

  , lookup: function (event) {
      var items

      this.query = this.$element.html()

      if (!this.query || this.query.length < this.options.minLength) {
        return this.shown ? this.hide() : this
      }

      items = $.isFunction(this.source) ? this.source(this.query, $.proxy(this.process, this)) : this.source

      return items ? this.process(items) : this
    }

  , process: function (items) {
      var that = this

      items = $.grep(items, function (item) {
        return that.matcher(item)
      })

      items = this.sorter(items)

      if (!items.length) {
        return this.shown ? this.hide() : this
      }

      return this.render(items.slice(0, this.options.items)).show()
    }

  , matcher: function (item) {
      return ~item.toLowerCase().indexOf(this.query.toLowerCase())
    }

  , sorter: function (items) {
      var beginswith = []
        , caseSensitive = []
        , caseInsensitive = []
        , item

      while (item = items.shift()) {
        if (!item.toLowerCase().indexOf(this.query.toLowerCase())) beginswith.push(item)
        else if (~item.indexOf(this.query)) caseSensitive.push(item)
        else caseInsensitive.push(item)
      }

      return beginswith.concat(caseSensitive, caseInsensitive)
    }

  , highlighter: function (item) {
      var query = this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&')
      return item.replace(new RegExp('(' + query + ')', 'ig'), function ($1, match) {
        return '<strong>' + match + '</strong>'
      })
    }

  , render: function (items) {
      var that = this

      items = $(items).map(function (i, item) {
        i = $(that.options.item).attr('data-value', item)
        i.find('a').html(that.highlighter(item))
        return i[0]
      })

      items.first().addClass('active')
      this.$menu.html(items)
      return this
    }

  , next: function (event) {
      var active = this.$menu.find('.active').removeClass('active')
        , next = active.next()

      if (!next.length) {
        next = $(this.$menu.find('li')[0])
      }

      next.addClass('active')
    }

  , prev: function (event) {
      var active = this.$menu.find('.active').removeClass('active')
        , prev = active.prev()

      if (!prev.length) {
        prev = this.$menu.find('li').last()
      }

      prev.addClass('active')
    }

  , listen: function () {
      this.$element
        .on('blur',     $.proxy(this.blur, this))
        .on('keypress', $.proxy(this.keypress, this))
        .on('keyup',    $.proxy(this.keyup, this))

      if (this.eventSupported('keydown')) {
        this.$element.on('keydown', $.proxy(this.keydown, this))
      }

      this.$menu
        .on('click', $.proxy(this.click, this))
        .on('mouseenter', 'li', $.proxy(this.mouseenter, this))
    }

  , eventSupported: function(eventName) {
      var isSupported = eventName in this.$element
      if (!isSupported) {
        this.$element.setAttribute(eventName, 'return;')
        isSupported = typeof this.$element[eventName] === 'function'
      }
      return isSupported
    }

  , move: function (e) {
      if (!this.shown) return

      switch(e.keyCode) {
        case 9: // tab
        case 13: // enter
        case 27: // escape
          e.preventDefault()
          break

        case 38: // up arrow
          e.preventDefault()
          this.prev()
          break

        case 40: // down arrow
          e.preventDefault()
          this.next()
          break
      }

      e.stopPropagation()
    }

  , keydown: function (e) {
      this.suppressKeyPressRepeat = !~$.inArray(e.keyCode, [40,38,9,13,27])
      this.move(e)
    }

  , keypress: function (e) {
      if (this.suppressKeyPressRepeat) return
      this.move(e)
    }

  , keyup: function (e) {
      switch(e.keyCode) {
        case 40: // down arrow
        case 38: // up arrow
        case 16: // shift
        case 17: // ctrl
        case 18: // alt
          break

        case 9: // tab
        case 13: // enter
          if (!this.shown) return
          this.select()
          break

        case 27: // escape
          if (!this.shown) return
          this.hide()
          break

        default:
          this.lookup()
      }

      e.stopPropagation()
      e.preventDefault()
  }

  , blur: function (e) {
      var that = this
      setTimeout(function () { that.hide() }, 150)
    }

  , click: function (e) {
      e.stopPropagation()
      e.preventDefault()
      this.select()
    }

  , mouseenter: function (e) {
      this.$menu.find('.active').removeClass('active')
      $(e.currentTarget).addClass('active')
    }

  }


  /* GLYNTTYPEAHEAD PLUGIN DEFINITION
   * =========================== */

  $.fn.glynt_typeahead = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('glynt_typeahead')
        , options = typeof option == 'object' && option
      if (!data) $this.data('glynt_typeahead', (data = new GlyntTypeahead(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.glynt_typeahead.defaults = {
    source: []
  , items: 8
  , menu: '<ul class="typeahead dropdown-menu"></ul>'
  , item: '<li><a href="#"></a></li>'
  , minLength: 1
  }

  $.fn.glynt_typeahead.Constructor = GlyntTypeahead


 /*   GLYNTTYPEAHEAD DATA-API
  * ================== */

  $(document).on('focus.glynt_typeahead.data-api', '[data-provide="glynt_typeahead"]', function (e) {
    var $this = $(this)
    if ($this.data('glynt_typeahead')) return
    e.preventDefault()
    $this.glynt_typeahead($this.data())
  })

}(window.jQuery);