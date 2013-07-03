var form_mode = 'new';
var active_customer = '';

function save_to_localstorage(tag, data) {
    localStorage.setItem(tag, data.serialize());
    founder_list()
}

function delete_from_localstorage(tag) {
    localStorage.removeItem(tag);
    founder_list()
    $('form')[0].reset()
}

function populate_form(tag) {
    $('form').deserialize(localStorage.getItem(tag));
}

function founder_list() {
    var founder_list = $('.customer-list');
    founder_list.find('dd').remove();
    for (var key in localStorage) {
        if (key.indexOf("founder-") !== -1) {
            key = key.replace('founder-', '');
            founder_list.removeClass('hide').append('<dd><span>' + key + '</span><a href="#" class="btn edit-founder">Edit</a> <a href="#" class="btn remove-founder">Delete</a></dd>');
        }
    }
}

function save_founder() {
    var form = $('form');
    var founder_name = $('input#id_customers-first_name').val() + ' ' + $('input#id_customers-last_name').val();
    save_to_localstorage('founder-' + founder_name, form);
    form[0].reset();
    form.parsley('destroy');

    if (form_mode === 'edit' && founder_name != active_founder) {
        delete_from_localstorage('founder-' + active_founder);
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
        var no_errors = $('form').parsley('validate');
        if (no_errors === true) {
            save_founder();
            $('body, html').animate({ scrollTop: 0 }, 700);
        }
        return false;
    });

    $('.edit-founder').live('click', function (e) {
        e.preventDefault();
        form_mode = 'edit';
        var name = $(this).parent().find('span').text();
        active_customer = name;
        populate_form('founder-' + name);
    });

    $('.remove-founder').live('click', function (e) {
        e.preventDefault();
        var name = $(this).parent().find('span').text();
        delete_from_localstorage('founder-' + name);
    });

    $('.customer-submit').click(function (e) {
        e.preventDefault();
        $('form').submit();
        return false;
    });
});