+function ($) { "use strict";

  // STEPTACULAR CLASS DEFINITION
  // ============================

  var Steptacular = function(element, options) {
    this.$element       = $(element).is('body') ? $(window) : $(element);
    this.$body          = $('body');
    this.options        = $.extend({}, Steptacular.DEFAULTS, options);
    this.$active        = null;
    this.scenes         = $([]);
    this.storage        = window.localStorage;
    this.transitioning  = null;

    this.$element.addClass('stage');

    this.$element.on('click', this.options.selector.buttons, $.proxy(this.click, this));
    this.$element.on('submit', this.options.selector.forms, $.proxy(this.submit, this));
    
    this.start();

    $(window).on('popstate', $.proxy(this.popstate, this));
  };

  Steptacular.DEFAULTS = {
    selector: {
      buttons: 'input[type=submit]',
      forms:   '.slide form',
      slides:  '.slide'
    }
  };

  Steptacular.prototype.process = function(form) {
    var self    = this;
    var $form   = $(form);
    // var scene   = this.$active.data('scene');
    var scene   = $form.data('scene');
    // var stage   = this.$active.data('stage');
    var stage   = $form.data('stage');

    var key     = stage + (scene ? '-' + scene : '');
    var storage = {};

    $form.find('input, textarea, select').each(function() {
      var $el = $(this);

      // persist the data
      if ($el.is('[type=checkbox]')) {
        if ($el.is(':checked')) {
          if (!storage[$el.attr('name')]) {
            storage[$el.attr('name')] = [];
          };

          storage[$el.attr('name')].push($el.val());
        };
      } else if ($el.is(['type=radio'])) {
        // console.log('radio');
      } else if ($el.is('[type=submit]')) {
        if ($el.attr('id') == $form.data('trigger')) {
          storage = $el.data('value');
        };
      } else {
        storage[$el.attr('name')] = $el.val();
      };

      // handle the selection of scenes
      if (stage == 'selection') {
        if ($el.data('needs-stage') && $el.is(':checked')) {
          $($el.data('needs-stage').split(',')).each(function() {
            var selector = '[data-scene="' + $el.val() + '"][data-stage="' + this + '"]';
            self.scenes.push(self.$element.find(selector));
          });
        };
      };
    });

    self.storage[key] = JSON.stringify(storage);
  };

  Steptacular.prototype.getActiveIndex = function() {
    var self = this;

    var activeIndex = null;
    $(this.scenes).each(function(index, scene) {
      if (self.$active == scene) {
        activeIndex = index;
      };
    });

    return activeIndex;
  };

  Steptacular.prototype.getSceneIndexFromId = function(id) {
    var self = this;

    var activeIndex = null;
    $(this.scenes).each(function(index, scene) {
      if (id == scene.attr('id')) {
        activeIndex = index;
      };
    });

    return activeIndex;
  };

  Steptacular.prototype.to = function(pos) {
    var activeIndex = this.getActiveIndex();

    if (pos > (this.scenes.length - 1) || pos < 0) return;

    if (activeIndex == pos) return;

    return this.show(pos > activeIndex ? 'next' : 'prev', $(this.scenes[pos]));
  };

  Steptacular.prototype.next = function() {
    if (this.transitioning) return;

    var pos = this.getActiveIndex() + 1;
    var $scene = this.scenes[pos];

    if ($scene) {
      return this.show('next', $scene);
    } else {
      return this.finish();
    };
  };

  Steptacular.prototype.prev = function() {
    if (this.transitioning) return;

    var pos = this.getActiveIndex() - 1;
    var $scene = this.scenes[pos];

    if ($scene) {
      return this.show('prev', $scene);
    } else {
      return this.start();
    };
  };

  Steptacular.prototype.show = function(type, next) {
    if (this.transitioning) return;

    var $next = next || $active[type]();

    this.transitioning = true;

    this.$active.removeClass('active');
    this.$active = null;

    var url = window.location.pathname + '#!/' + $next.attr('id');
    window.history.pushState({}, null, url);
    _gaq.push(['_trackPageview', url]);

    var percentage = '-' + parseFloat($next.index() * 100) + '%'
    this.$element.css('transform', 'translate3d(' + percentage + ', 0, 0)');

    this.$active = $next;
    this.$active.addClass('active');
    this.transitioning = false;

    return this;
  };

  Steptacular.prototype.start = function() {
    this.$active = this.$element.find(this.options.selector.slides).first();
    this.$active.addClass('active');
    this.scenes.push(this.$active);

    var hash = '#!/' + this.$active.attr('id');
    if (window.location.hash != hash) {
      var url = window.location.pathname + hash;
      window.location.href = url;
    };
  };

  Steptacular.prototype.finish = function() {
    this.$active.removeClass('active');

    var e = $.Event('finish.lp.steptacular', { formData: this.storage });
    this.$element.trigger(e);
  };

  Steptacular.prototype.click = function(e) {
    var $el   = $(e.target);
    var $form = $el.closest(this.options.selector.forms);

    $form.data('trigger', $el.attr('id'));
  };

  Steptacular.prototype.popstate = function(e) {
    var scene = window.location.hash.replace('#!/', '');

    var activeIndex = this.getActiveIndex();
    var pos = this.getSceneIndexFromId(scene);

    if (pos > (this.scenes.length - 1) || pos < 0) return;

    if (activeIndex == pos) return;

    return this.show(pos > activeIndex ? 'next' : 'prev', $(this.scenes[pos]));
  };

  Steptacular.prototype.submit = function(e) {
    var self  = this;
    var $form = $(e.target);
    // var stage = this.$active.data('stage');
    var stage = $form.data('stage');

    e.preventDefault();
    e.stopPropagation();

    var isValid = true;
    $form.find('[required]').each(function() {
      var val = $(this).val();
      if (val.replace(/^\s+/g, '').replace(/\s+$/g, '').length > 0) {
        return true;
      } else {
        isValid = false;
        return false;
      };
    });

    if (isValid) {
      self.process($form);

      var isQualified = $form.parsley('isValid');
      if (isQualified) {
        this.next();
      } else {
        if (stage == 'qualification') {
          this.finish();
        };
      };
      $form.parsley('destroy');
    };
  };


  // STEPTACULAR PLUGIN DEFINITION
  // =============================

  var old = $.fn.steptacular;

  $.fn.steptacular = function(option) {
    return this.each(function() {
      var $this   = $(this);
      var data    = $this.data('lp.steptacular');
      var options = typeof option == 'object' && option

      if (!data) $this.data('lp.steptacular', (data = new Steptacular(this, options)));
      if (typeof option == 'string') data[option]();
    });
  };

  $.fn.steptacular.Constructor = Steptacular;


  // STEPTACULAR NO CONFLICT
  // =======================

  $.fn.steptacular.noConflict = function() {
    $.fn.steptacular = old;
    return this;
  };


  // STEPTACULAR DATA-API
  // ====================

  $(window).on('load', function() {
    $('[data-ride="steptacular"]').each(function() {
      var $steptacular = $(this);
      $steptacular.steptacular($steptacular.data());
    });
  });

}(window.jQuery);