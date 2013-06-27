function founder_form(type) {

    if (type === "save") {
        var founder_name = $('input#id_founders-first_name').val() + ' ' + $('input#id_founders-last_name').val();
        var founder_list = $('.founder-list');
        founder_list.removeClass('hide').append('<dd><a href="#" class="edit-founder">' + founder_name + '</a></dd>');
        $('form')[0].reset();
        $('form').parsley( 'destroy' );
    }

    else if (type === "edit") {
        // pre populate fields
    }

    else if (type === "remove") {
        // delete founder
    }
}

$(document).ready(function () {
    $('.add-field').click(function (e) {
        e.preventDefault();
        var target = $(this).attr('data-target-field');
        var elm = $('div#div_' + target).last();
        elm.clone().insertAfter(elm).find('input').val('');
    });

    $('.save-founder').live('click', function (e) {
        e.preventDefault();
        var test_form = $('form').parsley('validate');
        if (test_form === true) {
            founder_form('save');
            $('body, html').animate({ scrollTop: 0 }, 700);
        }
        return false;
    });

});