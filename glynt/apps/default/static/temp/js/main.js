// set up the blank defaults
window['fixed-fees']            = [];
window['intake-forms']          = [];
window['needs-qualification']   = [];
window['selected-transactions'] = {};
window['services']              = [];

// SELECTION SCENE EVENTS
// ======================
$(document).on('click', '[data-scene="selection"] .btn-next-step', function(e) {
    var $this  = $(e.target);
    var $slide = $this.closest('section.slide');

    var fixedFees          = [];
    var intakeForms        = [];
    var needsQualification = [];
    var services           = [];

    e.preventDefault();

    $slide.find('[type="checkbox"]').each(function() {
        var $element = $(this);

        if ($element.is(':checked')) {
            services.push($element.attr('name'));

            if ($element.data('fixed-fee')) {
                fixedFees.push($element.attr('name'));
            }

            if ($element.data('intake-form')) {
                intakeForms.push($element.attr('name'));
            }

            if ($element.data('needs-qualification')) {
                needsQualification.push($element.attr('name'));
            }
        }
    });

    // make sure we only save things once
    window['fixed-fees'] = $.unique(fixedFees);
    window['intake-forms'] = $.unique(intakeForms);
    window['needs-qualification'] = $.unique(needsQualification);
    window['services'] = $.unique(services);

    // only go forward if more than one has been selected
    if (window['services'].length > 0) {
        nextStep();
    }
});

// QUALIFICATION SCENE EVENTS
// ==========================
$(document).on('click', '[data-scene="qualification"] .btn-next-step', function(e) {
    var $this  = $(e.target);

    e.preventDefault();

    // has the form been filled out properly?
        nextStep();
});

// FIXED FEE SCENE EVENTS
// ======================
$(document).on('click', '[data-scene="fixed-fee"] .btn-next-step', function(e) {
    var $this  = $(e.target);
    var $node = $this.closest('.transaction-choice');
    var $slide = $this.closest('section.slide');

    var transaction = $node.attr('data-transaction');
    var transactionType = $slide.attr('data-transaction-type');

    e.preventDefault();

    window['selected-transactions'][transactionType] = transaction;

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

    // no more steps to show
    var $form  = $('form#transaction-form');
    var $input = $form.find('#id_transaction_type');

    var selectedTransactions = [];
    $.each(window['selected-transactions'], function(key, value) {
        selectedTransactions.push(value);
    });
    $input.attr('value', selectedTransactions);

    $form.submit();
}