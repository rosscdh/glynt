$(document).ready(function () {
    $('.add-field').click(function (e) {
        e.preventDefault();
        var target = $(this).attr('data-target-field');
        var elm = $('div#div_'+target).last();
        elm.clone().insertAfter(elm).find('input').val('');
    });


    $('.save-founder').click(function (e) {
        e.preventDefault();
        var form = $('form');
        $.ajax({
            type: form.attr('method'),
            url: $(this).attr('data-url'),
            data: form.serialize(),
            context: this,
            success: function(data, status) {
                console.log('SUCCESS');
            },
            error: function(jsdata, data, status) {
                console.log('FAIL');
            },
            complete: function(){
                console.log('COMPLETE');
            }
        });
        return false;
    });
});