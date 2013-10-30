// Set up the blank defaults
window['fixed-fees'] = [];
window['intake-forms'] = [];
window['needs-qualification'] = [];
window['selected-transactions'] = [];
window['services'] = [];

// SELECTION SCENE EVENTS
// ======================
$(document).on('click', '[data-scene="selection"] .btn-next-step', function(e) {
    var $this  = $(e.target);
    var $slide = $(this).closest('section.slide');

    window['services'] = [];

    e.preventDefault();

    $slide.find('[type="checkbox"]').each(function() {
        var $element  = $(this);

        if ($element.is(':checked')) {
            window['services'].push($element.attr('name'));

            if ($element.data('fixed-fee')) {
                window['fixed-fees'].push($element.attr('name'));
            }

            if ($element.data('intake-form')) {
                window['intake-forms'].push($element.attr('name'));
            }

            if ($element.data('needs-qualification')) {
                window['needs-qualification'].push($element.attr('name'));
            }
        }
    });

    // make sure we only save things once
    window['fixed-fees'] = $.unique(window['fixed-fees']);
    window['intake-forms'] = $.unique(window['intake-forms']);
    window['needs-qualification'] = $.unique(window['needs-qualification']);
    window['services'] = $.unique(window['services']);

    // only go forward if more than one has been selected
    if (window['services'].length > 0) {
        nextStep();
    }
});

// QUALIFICATION SCENE EVENTS
// ==========================
$(document).on('click', '[data-scene="qualification"] .btn-next-step', function(e) {
    var $this  = $(e.target);
    var $slide = $this.closest('section.slide');

    e.preventDefault();

    // has the form been filled out properly?
        nextStep();
});

// FIXED FEE SCENE EVENTS
// ======================
$(document).on('click', '[data-scene="fixed-fee"] .btn-next-step', function(e) {
    var $this  = $(e.target);
    var $slide = $this.closest('section.slide');

    e.preventDefault();

    // has the form been filled out properly?
        nextStep();
});


var nextStep = function() {
    // are there any qualification steps needed?
    if (window['needs-qualification'].length > 0) {
        var nextStep = window['needs-qualification'].shift();
        return window.location.hash = "#qualification-" + nextStep;
    }

    // do we have any fixed fee services available
    if (window['fixed-fees'].length > 0) {
        var nextStep = window['fixed-fees'].shift();
        return window.location.hash = "#fixed-fee-" + nextStep;
    }
}