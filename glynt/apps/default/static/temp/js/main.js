// Set up the blank defaults
window['fixed-fees'] = [];
window['intake-forms'] = [];
window['needs-qualification'] = [];
window['services'] = [];

// $.blah('section#intake-form-financing', {
    // validate: function(e) {
        // var $this = $(e.target);
        // var $slide = $this.closest('section.slide');
    // }
// });

// $('data-spy="scene"').scene();

// how to handle the individual slides and all the submissions
    // events?
        // pre/post submission
        // add in validation and these custom controls that way?!?!

// $(document).on('submit.lp.slide.data-api')

// blah
// use all the scene crack
    // sets up the onclick of the btn-next-step

$(document).on('click', 'section#selection .btn-next-step', function(e) {
    var $this    = $(e.target);
    var $slide   = $this.closest('section.slide');

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

    // only go forward if one has been selected
        nextStep();
});

$(document).on('click', 'section#qualification-incorporation .btn-next-step', function(e) {
    // var $this    = $(e.target);
    // var $slide   = $this.closest('section.slide');

    e.preventDefault();

    // has the form been filled out properly?
        nextStep();
});

$(document).on('click', 'section#fixed-fee-incorporation .btn-next-step', function(e) {
    // var $this    = $(e.target);
    // var $slide   = $this.closest('section.slide');

    e.preventDefault();

    // has the form been filled out properly?
        nextStep();
});

$(document).on('click', 'section#fixed-fee-financing .btn-next-step', function(e) {
    // var $this    = $(e.target);
    // var $slide   = $this.closest('section.slide');

    e.preventDefault();

    // has the form been filled out properly
        nextStep();
});

$(document).on('click', 'section#intake-form-incorporation .btn-next-step', function(e) {
    // var $this    = $(e.target);
    // var $slide   = $this.closest('section.slide');

    e.preventDefault();

    // has the form been filled out properly
        nextStep();
});

$(document).on('click', 'section#intake-form-financing .btn-next-step', function(e) {
    // var $this    = $(e.target);
    // var $slide   = $this.closest('section.slide');

    e.preventDefault();

    // has the form been filled out properly
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

    // do we have any intake questions?
    if (window['intake-forms'].length > 0) {
        var nextStep = window['intake-forms'].shift();
        return window.location.hash = "#intake-form-" + nextStep;
    }

    return window.location.hash = '#finished';
}