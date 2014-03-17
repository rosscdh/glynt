$(window).on('load', function() {
  // make these a bit more explicit
  $('.form-pretty input[type=checkbox], .form-pretty input[type=radio]').on('change', function() {
    var $el    = $(this);
    var $label = $el.closest('label');

    if ($el.attr('type') == 'radio') {
      $('input[name="' + $el.attr('name') + '"]').each(function() {
        $(this).closest('label').removeClass('checked');
      });
    };

    if ($el.is(':checked')) {
      $label.addClass('checked');
    } else {
      $label.removeClass('checked');
    };
  });

  // Sliders
  $('[data-toggle="slider"]').each(function() {
    var $slider = $(this);
    $slider.slider($.extend($slider.data(), { 'value': $slider.val() }));
  });

  $('input#company-founders').on('slide', function(e) {
    var $el = $('#company-founders-bind');

    $el.find('.bind-value').html(e.value);
    $el.find('.bind-desc').html($el.data(e.value == 1 ? 'single' : 'plural'));
  });

});