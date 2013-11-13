+function ($) { "use strict";

  // STEPTACULAR CLASS DEFINITION
  // ============================

  var Steptacular = function(element, options) {
    this.$element       = $(element).is('body') ? $(window) : $(element);
    this.$body          = $('body');
    this.options        = $.extend({}, Steptacular.DEFAULTS, options);
    this.storage        = $.sessionStorage;

    this.$active        = null;
    this.data           = null;
    this.progress       = null;
    this.scenes         = null;
    this.$slides        = null;
    this.transitioning  = null;

    this.refresh();
    this.init();
  };

  Steptacular.DEFAULTS = {
    selector: {
      buttons: 'input[type=submit]',
      forms:   '.slide form',
      slides:  '.slide'
    }
  };

  Steptacular.prototype.init = function() {
    var hash = window.location.hash.replace('#!/', '');
    if (hash) {
      this.to(hash);
    } else {
      this.start();
    };

    this.$element.addClass('stage');

    this.$element.on('click', this.options.selector.buttons, $.proxy(this.click, this));
    this.$element.on('submit', this.options.selector.forms, $.proxy(this.submit, this));

    $(window).on('popstate', $.proxy(this.popstate, this));
  };

  Steptacular.prototype.refresh = function() {
    var self      = this;

    this.data     = {};
    if (this.storage.getItem('data')) {
      this.data   = JSON.parse(this.storage.getItem('data'));
    };

    this.$slides  = $([]);
    this.$element
      .find(this.options.selector.slides)
      .each(function() {
        self.$slides.push(this);
      });

    this.scenes   = [];
    if (this.storage.getItem('scenes')) {
      this.scenes = $(JSON.parse(this.storage.getItem('scenes')));
    } else {
      this.scenes.push(this.$slides.first().attr('id'));
    };

    this.progress = this.storage.getItem('progress');
  };

  Steptacular.prototype.process = function(form) {
    var self    = this;
    var $form   = $(form);
    var key     = this.$active.attr('id');
    var stage   = this.$active.data('stage');

    var data    = {};
    $form.find('input, textarea, select').each(function() {
      var $el = $(this);

      // persist the data
      if ($el.is('[type=checkbox]')) {
        if ($el.is(':checked')) {
          if (!data[$el.attr('name')]) {
            data[$el.attr('name')] = [];
          };

          data[$el.attr('name')].push($el.val());
        };
      } else if ($el.is(['type=radio'])) {
        // console.log('radio');
      } else if ($el.is('[type=submit]')) {
        if ($el.attr('id') == $form.data('trigger')) {
          data = $el.data('value');
        };
      } else {
        data[$el.attr('name')] = $el.val();
      };
    });

    this.data[key] = data;
    this.storage.setItem('data', JSON.stringify(this.data));

    // handle the selection of scenes
    if (stage == 'selection') {
      var scenes = [this.$active.attr('id')];
      $form.find('input[type="checkbox"][data-needs-stage]:checked').each(function() {
        var $el = $(this);

        $($el.data('needs-stage').split(',')).each(function() {
          var selector = '[data-scene="' + $el.val() + '"][data-stage="' + this + '"]';
          var $element = self.$element.find(selector);

          scenes.push($element.attr('id'));
        });
      });

      this.storage.setItem('scenes', JSON.stringify(scenes));
    };

    this.refresh();
  };

  Steptacular.prototype.getActiveIndex = function() {
    var active = (this.$active) ? this.$active.attr('id') : null;

    var activeIndex = null;
    $(this.scenes).each(function(index, scene) {
      if (active == scene) {
        activeIndex = index;
      };
    });

    return activeIndex;
  };

  Steptacular.prototype.getSceneIndex = function(id) {
    var self = this;

    var sceneIndex = null;
    $(this.scenes).each(function(index, scene) {
      if (id == scene) {
        sceneIndex = index;
      };
    });

    return sceneIndex;
  };

  Steptacular.prototype.getSlide = function(scene) {
    var self = this;

    var slide = null;
    this.$slides.each(function() {
      var $el = $(this);
      if (scene == $el.attr('id')) {
        slide = $el;
      };
    });

    return slide;
  };

  Steptacular.prototype.to = function(scene) {
    var activeIndex = this.getActiveIndex();
    var pos         = this.getSceneIndex(scene);
    var progress    = this.getSceneIndex(this.progress);

    if (pos > (this.scenes.length - 1) || pos < 0) return;

    if (activeIndex == pos) return;

    if (pos > progress) return this.start();

    return this.show(pos > activeIndex ? 'next' : 'prev', this.scenes[pos]);
  };

  Steptacular.prototype.next = function() {
    if (this.transitioning) return;

    var pos = this.getActiveIndex() + 1;
    var scene = this.scenes[pos];

    if (scene) {
      return this.show('next', scene);
    } else {
      return this.finish();
    };
  };

  Steptacular.prototype.prev = function() {
    if (this.transitioning) return;

    var pos = this.getActiveIndex() - 1;
    var scene = this.scenes[pos];

    if (scene) {
      return this.show('prev', scene);
    } else {
      return this.start();
    };
  };

  Steptacular.prototype.show = function(type, scene) {
    if (this.transitioning) return;

    var $next = this.getSlide(scene);

    this.transitioning = true;

    if (this.$active) {
      this.$active.removeClass('active');
      this.$active = null;
    };

    var url = window.location.pathname + '#!/' + $next.attr('id');
    window.history.pushState({}, null, url);
    _gaq.push(['_trackPageview', url]);

    if (this.getSceneIndex(scene) > this.getSceneIndex(this.progress)) {
      this.storage.setItem('progress', scene);
      this.refresh();
    };

    var percentage = '-' + parseFloat($next.index() * 100) + '%';
    this.$element.css('transform', 'translate3d(' + percentage + ', 0, 0)');

    this.$active = $next;
    this.$active.addClass('active');

    this.transitioning = false;

    return this;
  };

  Steptacular.prototype.start = function() {
    return this.to(this.scenes[0]);
  };

  Steptacular.prototype.finish = function(isQualified) {
    var self        = this;
    var isQualified = isQualified || true;
    var pos         = this.getSceneIndex(this.$active.attr('id'));

    var data = {};
    $(this.scenes).each(function(index, scene) {
      if (index <= pos) {
        data[scene] = self.data[scene];
      };
    });

    this.$active.removeClass('active');
    this.storage.clear();

    var e = $.Event('finish.lp.steptacular', { formData: data, isQualified: isQualified });
    this.$element.trigger(e);
  };

  Steptacular.prototype.click = function(e) {
    var $el   = $(e.target);
    var $form = $el.closest(this.options.selector.forms);

    $form.data('trigger', $el.attr('id'));
  };

  Steptacular.prototype.popstate = function(e) {
    return this.to(window.location.hash.replace('#!/', ''));
  };

  Steptacular.prototype.submit = function(e) {
    var $form = $(e.target);
    var stage = this.$active.data('stage');

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
      this.process($form);

      var isQualified = $form.parsley('isValid');
      if (isQualified) {
        this.next();
      } else {
        if (stage == 'qualification') {
          this.finish(false);
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