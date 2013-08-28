'use strict';

$(document).ready( function () {
    /**
    * GENERIC - modal window capture
    */
    $(document).on( 'click', '[data-toggle="modal"]', function (event) {
        event.preventDefault();
        event.stopPropagation();

        var elem = $(this);
        var data = elem.data();
        var target = data.target || false;
        var is_ajax = data.is_ajax || false;

        //var selector_path = data.target_toggle_object || $.getPath(elem);

        var url = elem.data('remote') || elem.attr('href');
        
        if (target) {
            target = $(target);
        }

        var form = target.find('form:first');

        if (is_ajax === true) {
            var modal_body = target.find('.modal-body');

            target.data('is_ajax', is_ajax);
            //target.data('target_toggle_object', selector_path);

            modal_body.html('');// clear html

            modal_body.load(url, function (data) {
                modal_body.html(data);
                // fire the laod event only on successful load of url
                //target.modal('show'); // load html
            });
        } else {
            // transfer the clicked elements data values to the target

            delete data.target;
            delete data.toggle;
            delete data['bs.modal'];

            // update the froms data with all the local data
            $.each(data, function (key, value) {
                form.data(key, value);
            });
        }
    });

    /**
    * For all the data toggles capture and modify the click event
    * we want to populate the modal-body with our updated data
    */
    $('#modal-checklist-item').on('show.bs.modal', function (event) {
        var target = $(event.currentTarget);
        var title = target.find('.modal-title');
        var body = target.find('.modal-body');
        var action_button = target.find('.modal-footer .btn-success:first');

        var is_ajax = target.data('is_ajax') || false;

        // target_toggle_object is programatically tied in by using the $.getPath selector of the click event
        var target_toggle_object = target.data('target_toggle_object') || false;
        if (target_toggle_object !== false) {
            target_toggle_object = $(target_toggle_object);
        }

        if (name && name !== '') {
            title.html('Edit - {name}'.assign({'name': name}));
        } else {
            title.html('Create new item');
        }

        action_button.on('click', function (event) {
            event.preventDefault();

            var form = target.find('.modal-body form:first');
            var name = form.find('input[type=text]:first').val();

            if (is_ajax === false) {
                //console.log('submit the form')
                //console.log(form)
                form.submit();
            } else {
                //console.log('submit the form via ajax')
                $.ajax({
                    type: 'POST',
                    url: form.attr('action'),
                    data: form.serialize(),
                    beforeSend: function(jqXHR, settings) {
                        // Pull the token out of the DOM.
                        jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]:first').val());
                    },
                    success: function(data, textStatus, jqXHR){
                        var title = form.find('#id_name').val();
                        document.title = title;
                        //console.log(target_toggle_object)
                        target_toggle_object.html(title);
                    },
                    complete: function() {
                        $('#modal-checklist-item').modal('hide');
                    }
                });
            }
        });

    });

    $(document).on('hide.bs.modal', function (event) {
        var elem = $(event.target);
        elem.find('.body').html('');
    });

});