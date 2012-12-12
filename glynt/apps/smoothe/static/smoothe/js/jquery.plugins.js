// ----- JQUEY PLUGINS -----
// select jquery UI plugin
(function($) {
  "use strict"; // jshint ;_;

  /* GLYNT_PROGRESS PUBLIC CLASS DEFINITION
   * ================================= */
   var GlyntProgress = function (options) {
     this.options = $.extend({}, options)
     this.$element = $(this.options.element).appendTo(this.options.target_element)
     this.init()
     this.listen()
     this.render()
   }

   GlyntProgress.prototype = {
     constructor: GlyntProgress
     ,init: function () {
         var self = this;
         // insert elements into the ul
         // self.$element.parent().height($('#document').height())
         // self.$element.height(self.$element.parent().height())
         this.options.target_element.top = $('div.navbar').position().top + $('div.navbar').height()
         this.$element.attr('top', this.options.target_element.top);
         this.$element.attr('top', 0);
         $.each(self.options.items, function(index, item){
             if (item) {
                // types: select, choice, var
                var item_class = item.type.replace('doc_', '');
                var icon_css_class = self.icon_css_class(item_class);
                var icon = $('<i>', {class: icon_css_class + ' icon-align-left', title: item_class.replace('_', ' ')})
                var content = $('<a/>',{href: '#', html: icon})
                var li = $('<li/>', {
                    html: content
                    ,'data-var_name': item.name
                    ,'data-instance_count': item.instance_count
                    ,'title': (!item.initial) ? item.name.replace('_', ' ') : item.initial
                    ,'class': item_class
                })
                li.tooltip({
                    placement: 'top'
                });
                self.$element.append(li);
             }
         });
     }
     ,icon_css_class: function (item_class) {
         var icon_css_class = 'icon-font'
         if (item_class == 'choice') {
             icon_css_class = 'icon-plus-sign';
         } else if (item_class == 'select') {
             icon_css_class = 'icon-th-list';
         }
         return icon_css_class;
     }
     ,listen: function () {
         var self = this;
         self.$element.find('li').on('mouseover', function(event) {
             event.preventDefault();
             $(this).addClass('toggle-on')
             // var num = $(this).attr('data-instance_count')
             // var html = $(this).html();
             // html = html + ' ' + num;
             // $(this).html(html);
         });
         self.$element.find('li').on('mouseout', function(event) {
             $(this).removeClass('toggle-on')
         });
     }
     ,render: function () {
         var self = this;
         console.log('render')
     }
   }
   $.widget("ui.glynt_progress", {
       options: {
           target_element: $('#progress'),
           element: $('<ul/>', {id: 'glynt_progress'}),
       },
       _create: function() {
           var self = this;
           self.app = window.app;
           self.options.items = Object.clone(self.app.context);
           delete self.options.items.notes
           delete self.options.items.progress
           delete self.options.items.help

           var options = $.extend({}, self.options);
           self.app.context.progress = new GlyntProgress(options);
       }
   });

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
            self.$selector = (self.options.selector !== undefined) ? $(self.options.selector) : self.$element;
            self.$target = $(self.options.help_target);
            self.listen();
        }
        , listen: function () {
            var self = this;

            self.$selector.on('mouseover mouseout', function(event){
                self.toggle(event);
            });
        }
        , help_pos: function () {
            var self = this;
            var element_pos = self.$selector.position();
            return {
                'left': $('#document').width()*1.1,
                'top': element_pos.top
            }
        }
        , show: function () {
            var self = this;
            var pos = self.help_pos();
            var icon = $('<i/>', {class:'icon-info-sign icon-align-left'});
            var info = $('<div/>', {class:'info-text'}).append('&nbsp;' + self.options.item.help_text)

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
                self.show();
            } else {
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
                if(item && item.help_text !== undefined) {
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
            self.note_icon = $(self.element).find('.note:first');
            var item = {
                'id': self.note_id,
                'help_text': self.app.context.notes[self.note_id]
            };

            self.app.context.notes[self.note_id] = new HelpText({'selector': self.note_icon, 'item': item, 'help_target': self.options.target_element});
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