// ----- JQUEY PLUGINS -----
// select jquery UI plugin
(function($) {
  "use strict"; // jshint ;_;

  /* GLYNT_TOGGLE PUBLIC CLASS DEFINITION
   * ================================= */
        var GlyntToggle = function (options) {
            this.options = $.extend({
                in_admin: false
            }, options)
            this.select_element = this.options.select_element;
            this.$container = $(this.select_element.element);
            this.$button = false;
            this.$show_button = $('<button>', {
                                class: 'btn btn-success',
                                html: '+'
                            });
            this.init();
            this.listen();
        }
        GlyntToggle.prototype = {
            constructor: GlyntToggle
            ,init: function () {
                self = this;
                self.$button = self.$container.find('button.toggle_state:first');
                self.first_selecta = self.select_element.context.select_options[0].selecta.$element;

                $('body').append(self.$show_button);
                self.$show_button.hide();
            }
            ,listen: function () {
                self.$show_button.on('click', function(){
                    self.$container.show();
                    self.$show_button.hide();
                });
                self.$button.on('click', function(event){
                    self.$container.hide();
                    self.$show_button.show();
                    self.$show_button.offset(self.first_selecta.offset());
                    console.log(self.$show_button)
                });
            }
            ,inject_show: function() {

            }
        }
    /* GLYNT_INCREMENTOR PUBLIC CLASS DEFINITION
     * ================================= */
        var GlyntIncrementor = function (options) {
            this.options = $.extend({
                in_admin: false
            }, options)
            this.select_element = this.options.select_element;
            this.$container = $(this.select_element.element);
            this.$button = false;
            this.first_row = false;
            this.init();
            this.listen();
        }
        GlyntIncrementor.prototype = {
            constructor: GlyntIncrementor
            ,init: function () {
                self = this;
                this.$button = this.$container.find('button.incrementor:first');
                this.first_row = self.select_element.context.select_options[0];
            }
            ,listen: function () {
                self.$button.on('click', function(event){
                    // increment the first row
                    console.log(self.select_element.context.select_options)
                    console.log(self);//.increment();
                });
            }
            ,increment: function () {
                var copy = $.extend(true, {}, this.first_row);
                copy.index = self.select_element.context.select_options.length;
                var from = '-{index}'.assign({index: this.first_row.index});
                var to = '-{index}'.assign({index: copy.index});
                copy.id = copy.id.replace(from, to);
                self.select_element.context.select_options.push(copy);
            }
        }

  /* GLYNT_PROGRESS PUBLIC CLASS DEFINITION
   * ================================= */
    var GlyntProgress = function (options) {
        this.options = $.extend({
            in_admin: false
        }, options)
        this.num_elements = 0
        this.completed_elements = 0
        this.$element = $(this.options.element).appendTo(this.options.target_element)
        this.init()
        this.listen()
        this.render()
    }
   GlyntProgress.prototype = {
     constructor: GlyntProgress
     ,init: function () {
         var self = this;

        if (self.options.in_admin === false) {
            this.options.target_element.css('top', $('div.navbar').position().top + $('div.navbar').height());
        } else {
            this.options.target_element.css('top', 0);
        }

        var percent_indicator_li = $('<li/>', {
                html: '<strong><span id="percent-complete">{complete}</span>%</strong>'.assign({complete: 0})
                ,mouseover: function() {
                }
                ,mouseout: function() {
                }
                ,click: function() {
                }
            });
         //self.$element.prepend(percent_indicator_li);

         $.each(self.options.items, function(index, item){

             if (index != 'self.app.context.progress' && item) {
                // types: select, choice, var
                var item_class = item.type.replace('doc_', '');
                var icon_css_class = self.icon_css_class(item_class);
                var icon = $('<i>', {class: icon_css_class + ' icon-align-left', title: item_class.replace('_', ' ')});
                var content = $('<a/>',{href: '#', html: icon});
                var title = (!item.initial) ? item.name.replace('_', ' ') : item.initial;
                var element = $('#' + item.id);

                var li = $('<li/>', {
                        html: content
                        ,'data-var_name': item.name
                        ,'data-instance_count': item.instance_count
                        ,'title': title
                        ,'class': item_class
                        ,mouseover: function() {
                            $(this).attr('title',item.value);
                        }
                        ,mouseout: function() {
                            $(this).attr('title',title);
                        }
                        ,click: function() {
                            $('html, body').animate({
                                scrollTop: element.offset().top - $('.navbar').height()
                            }, 200);
                        }
                    });

                li.tooltip({
                    placement: 'right'
                });

                self.$element.append(li);
                self.num_elements++;
             }
         });
     }
     ,increment_percent_complete: function() {
         this.completed_elements++;
         this.update_percent()
     }
     ,decrement_percent_complete: function() {
         this.completed_elements--;
         this.update_percent()
     }
     ,update_percent: function() {
         //console.log('100/{num} * {complete}'.assign({num: this.num_elements, complete: this.completed_elements}))
         var percent = (100/this.num_elements)*this.completed_elements;
         //console.log(percent)
         $('#percent-complete').text(Math.round(percent,0));
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
     ,setPos: function() {
        // var self = this;
        // var doc_top = $('#document').position().top;
        // var wide = self.$element.width()/1.2;
        // //var pos = $('#document').offset().left - wide;
        // var pos = 5;
        // self.$element.offset($('#document').offset());
        // self.$element.css('left', pos+'px');
     }
     ,listen: function () {
         var self = this;

         self.$element.find('li').on('mouseover', function(event) {
             event.preventDefault();
             $(this).addClass('toggle-on')
         });
         self.$element.find('li').on('mouseout', function(event) {
             $(this).removeClass('toggle-on')
         });

         var navbar_height = $('div.navbar').height();

        self.$element.trigger('unfreeze');

        $(window).resize(function() {
            self.setPos();
        });

     }
     ,render: function () {
         var self = this;
         self.setPos();
     }
   }
   // GLYNT_PROGRESS ui_widget
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
           console.log('self.app.context.progress')
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
            self.$target.attr('class','span3')
            self.listen();
        }
        , listen: function () {
            var self = this;
        }
        , help_pos: function () {
            var self = this;
            var element_pos = self.$selector.position();
            var element_width = self.$selector.width();
            var doc_pos = $('#document').position();
            return {
                //'left': doc_pos.left + $('#document').width()*1.15,
                'left': element_pos.left + element_width
                ,'top': element_pos.top
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
      options: {}
      ,$element: null
      ,_create: function() {
          var self = this;
          self.app = window.app;
          self.id = $(self.element).attr('id');
          self.variable_name = $(self.element).attr('data-doc_var');
          self.context = self.app.context[self.variable_name];
          self.$element = $(self.element);
          self.listen();
          self.$element.trigger('change', {'initial': true});
      }
      ,handle_value_change: function(e, data) {
          var self = this;
          var val = e.text();

          if (val == '' || val == self.context.initial) {
                e.removeClass('done');// make it yellow
                // setthe value back to the initial value
                e.html(self.context.initial);
                // only issue the decrement if its an actual user change
                // and not the initial load
                if (data === undefined || data.initial !== true) {
                    // issue element done event
                    $.Queue('percentCompleteDecrement').publish({'element':e});
                }
          }else{
              if (e.hasClass('done') == false) {
                  e.addClass('done');   // make it green
                  $.Queue('percentCompleteIncrement').publish({'element':e});
              }
          }
      }
      ,listen: function () {
          var self = this;
          // apply the hallo editor
          self.$element.hallo({
              // plugins: {
              //     'halloformat': {}
              // },
              editable: true
              ,showAlways: true
          });

          // GlyntTypeAhead
          if (self.$element.hasClass('doc_choice') === false) {// only if were NOT looking at a choice element
              self.$element.glynt_typeahead({
                  source: ['something','you typed','before']
              });
          }

          // events
          self.$element.on('blur', function(event){
              var doc_var_name = $(this).attr('data-doc_var')
              var doc_val = $(this).html();
              if (self.app.context[doc_var_name].value != doc_val) {
                  self.app.dispatch('bind_data', {'doc_var': doc_var_name, 'value': doc_val});
              }
              $(this).trigger('change');
          });

          /**
          * Handle changing of edit value
          * NOTE: these are not fields.. there is no .val() etc
          */
          self.$element.on('change', function(event, data){
              var e = $(this);
              self.handle_value_change(e, data);
          });

          /**
          * Capture return (13)
          * 13: tabs to the next item
          */
          self.$element.on('keydown', function(event){
            var key = event.keyCode || event.which;
            if (key === 13) {
                event.preventDefault();
                $(this).trigger('keypress', {which: 9})
            }
          });

          self.$element.on('click', function(event){
              self.select_inner_text(this);
              event.preventDefault();
              event.stopPropagation();
              
          });
          self.$element.on('focus', function(event){
              event.preventDefault();
              event.stopPropagation();
              self.select_inner_text(this);
              self.app.context.help[self.variable_name].show();
          });
          self.$element.on('blur', function(event){
            self.app.context.help[self.variable_name].hide();
          });
          self.$element.on('mouseenter', function(event){
            self.app.context.help[self.variable_name].show();
          });
      }
      ,clear_if_initial_text: function(element) {
        var self = this;
        var element = $(element);
        var val = element.text();
        console.log(val)
        if (val == self.context.initial) {
            element.text('');
        }
      }
      ,select_inner_text: function(element) {
        this.clear_if_initial_text(element);

        var range = document.createRange();
        var sel = window.getSelection();

        range.setStartBefore(element.firstChild);
        range.setEndAfter(element.lastChild);
        sel.removeAllRanges();
        sel.addRange(range);
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
            self.set_selected_status();
            self.position(self.pos());
        }
        , set_selected_status: function() {
            var self = this;
            if (self.select_option.selected === true) {
                self.select_option.selected = true;
                self.$element.addClass('btn-primary');
                self.$element.find('i').removeClass('icon-star-empty')
                self.$element.find('i').addClass('icon-star')
                self.$target.addClass('selected');
            } else {
                self.select_option.selected = false;
                self.$element.removeClass('btn-primary');
                self.$element.find('i').removeClass('icon-star')
                self.$element.find('i').addClass('icon-star-empty')
                self.$target.removeClass('selected');
            }
        }
        , toggle_selected_status: function() {
            var self = this;
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
        }
        , listen: function () {
            var self = this;

            self.$element.on('click', function(event){
                event.preventDefault();
                self.toggle_selected_status();
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
                'left': parent_pos.left - (self.$element.width()*5),
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
            self.can_increment = self.context.can_increment;

            self.html_selecta = Handlebars.partials['doc_select-selecta-partial'];
            // add selecta widgets to each li
            $.each(self.context.select_options, function(index, option){
                if (option.text.string.length > 0) {
                    self.context.select_options[index].selecta = new Selecta({
                        'widget': self,
                        'index': index,
                        'item': option,
                        'html': self.html_selecta
                    });
                }

            });

            // listen for "incrementor" functionality
            if (self.can_increment === true) {
                // create new GlyntIncrementor
                self.incrementor = new GlyntIncrementor({select_element: self})
            }

            // listen for "can_toggle" functionality
            if (self.can_toggle === true) {
                // create new GyntToggle
                self.toggle = new GlyntToggle({select_element: self})
            }

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
            self.is_static = self.app.context[var_name].is_static;

            element.glynt_typeahead({
                'source': self.choices
            });

            element.popover({
                trigger: 'hover',
                placement: 'top',
                title: (self.is_static) ? 'Required Choice Info' : 'Choice Info',
                content: (self.is_static) ? 'Valid choices are: "{choices}"'.assign({'choices': self.choices}) : 'Some valid choices are: "{choices}"'.assign({'choices': self.choices})
            });

            element.on('blur', function(event){
                if (self.is_static) {
                    // if is static (required to have one of the specified values)
                    var val = $(this).html();

                    if (self.app.context[var_name].choices.indexOf(val) == -1) {
                        $(this).html('');
                    }
                }
            });

            element.on('mouseover', function(event){
                event.preventDefault();
                $(this).css('cursor', 'pointer')
            });
            element.on('mouseout', function(event){
                event.preventDefault();
                $(this).css('cursor', 'auto')
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