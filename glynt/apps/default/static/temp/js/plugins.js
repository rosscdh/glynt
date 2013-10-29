// +function ($) { "use strict";

    // SCENE CLASS DEFINITION
    // ======================

    // var Scene = function(element, options) {
        // this.$element       = $(element).is('body') ? $(window) : $(element);
    // }

    // Scene.DEFAULTS = {

    // };

    // Scene.prototype.show = function() {
        // var $this    = this.element;
        // var $ul      = $this.closest('ul:not(.dropdown-menu)');
        // var selector = $this.data('target');

        // if (!selector) {
            // selector = $this.attr('href');
            // selector = selector && selector.replace(/.*(?=#[^\s]*$)/, ''); //strip for ie7
        // }

        // var e = $.Event('show.bs.tab', {
            // relatedTarget: previous
        // });

        // $this.trigger(e)
    // }


    // SCENE PLUGIN DEFINITION
    // =======================

    var old = $.fn.scene

    $.fn.scene = function(option) {
        return this.each(function() {
            var $this   = $(this);
            var data    = $this.data('lp.scene');
            var options = $.extend({}, Scene.DEFAULTS, $this.data(), typeof option =='object' && option);

            if (!data) $this.data('lp.scene', (data = new Scene(this, options)));
            if (typeof option == 'string') data[option]();
        });
    }

    $.fn.scene.Constructor = Scene;


    // SCENE NO CONFLICT
    // =================

    $.fn.scene.noConflict = function() {
        $.fn.scene = old;
        return this;
    }


    // SCENE DATA-API
    // ==============

    // $(document).on('click.lp.scene.data-api', '[data-toggle="scene"]', function(e) {
        // var $this = $(e.target);
        // var $parent = $this.closest('[data-spy="scene"]');

        // alert($parent.attr('id'));

        // var $this   = $(this);
        // var href    = $this.attr('href');
        // var target
        // var option  = $.extend({}, $target.data(), $this.data());

        // var $parent = this.$element.closest('[data-toggle="buttons"]')

        // var $btn = $(e.target)
            // if (!$btn.hasClass('btn')) $btn = $btn.closest('.btn')

        // e.preventDefault();

        // alert('click');
    // });

    // $(window).on('load', function() {
        // $('[data-spy="scene"]').each(function() {
            // var $scene = $(this)
            // $scene.scene($scene.data())
        // });
    // });

}(window.jQuery);