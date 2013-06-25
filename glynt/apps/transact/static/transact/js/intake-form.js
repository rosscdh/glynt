$(document).ready(function () {
    $('.add-field').click(function (e) {
        e.preventDefault();
        var target = $(this).attr('data-target-field');
        var elm = $('div#div_'+target).last();
        elm.clone().insertAfter(elm).find('input').val('');
    });
});