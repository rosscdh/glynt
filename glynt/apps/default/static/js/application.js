!function ($) {
    $(function() {
        var $window = $(window)

        // affix sidebar
        setTimeout(function () {
            $('.sidebar').affix({
                offset: {
                    top: function () { return $window.width() <= 980 ? 290 : 210 },
                    bottom: 270
                }
            });
        }, 100);
    });
}(window.jQuery);

// setTimeout(function () {
      // $('.bs-sidebar').affix({
        // offset: {
          // top: function () { return $window.width() <= 980 ? 290 : 210 }
        // , bottom: 270
        // }
      // })
    // }, 100)