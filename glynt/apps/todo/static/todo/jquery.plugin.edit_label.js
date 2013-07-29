'use strict';
/**
* enable dynamic editing of label items
* -------------------------------------
* 
*/
$(function() {
    // the widget definition, where "custom" is the namespace,
    // "colorize" the widget name
    $.widget( "lawpal.edit_label", {
        // default options
        list_items: null,
        options: {
            'url': null,
            'project_uuid': null,
            'edit_template': null,
            'remove_button': null,
            'target_selector': null
        },
        _log: function (msg) {
            var self = this;
            if (self.options.debug === true) {
                console.log(msg)
            }
        },
        // the constructor
        _create: function() {
            var self = this;

            self.list_items = self.element.find('[data-edit_label]');

            this._listen();
        },
        _listen: function () {
          var self = this;

            self.list_items.on('mouseover', function (event) {
                var elem = $(this);
                var target = elem.find(self.options.target_selector);
                var slug = elem.data('edit_label');

                $(document).on('keypress', {'keys': 'e', 'slug': slug, 'target': target, 'elem': elem,'self': self}, self.edit_item_label);
            });
            
            self.list_items.on('mouseout', function (event) {
                var elem = $(this);
                self.slug = null;
                $(document).unbind('keypress');
            });

            $(document).on( 'click', '[data-restore_label]', function (event) {
                self.restore_label({'elem': $(this)});
            });

        },
        restore_label: function (kwargs) {
            var elem = kwargs.elem;
            // var target = elem.parent().find('[data-update_name_url]:first');
            // target.remove();
            // var a_href = elem.parent().find('[data-restore_label]:first')
            // console.log(a_href)
            // a_href.show();
        },
        edit_item_label: function (event) {
            var self = event.data.self;
            var target = event.data.target;
            var elem = event.data.elem;
            var slug = event.data.slug;
            var url = self.options.url;

            $(document).unbind('keypress');

            url = url.assign(event.data);

            var context = $.extend(true, {
                'id': 'id_{slug}'.assign({'slug': slug}),
                'name': 'edit_label_{slug}'.assign({'slug': slug}),
                'url': url,
                'value': target.html(),
            }, event.data)

            var template = self.options.edit_template;

            template = template.assign(context)
            
            self.show_interface({'template': $(template), 'context': context, 'data': event.data});
        },
        show_interface: function (kwargs) {
            var self = kwargs.data.self;
            var elem = kwargs.data.elem;
            var target = kwargs.data.target;
            var context = kwargs.context;
            var template = kwargs.template;

            target.after(template);

            template.before($(self.options.remove_button));

            target.hide();

            template.on('change', function (event) {
                var elem = $(this);
                var url = elem.data('update_name_url');
                kwargs.val = elem.val();
                self.update_name(url, kwargs);
            });
        },
        update_name: function (url, kwargs) {
            var self = this;
            var data = {
                'name': kwargs.val,
                'project_uuid': self.options.project_uuid
            };

            $.ajax({
                type: 'PUT',
                url: url,
                data: data,
                dataType: 'application/json',
                contentType: 'application/json',
                beforeSend: function(jqXHR, settings) {
                    // Pull the token out of the DOM.
                    jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]:first').val());
                },
                success: function(data, textStatus, jqXHR) {
                    self._log('success SAVE_form_json_data')
                },
                error: function(jqXHR, textStatus, errorThrown) { 
                    self._log('error SAVE_form_json_data')
                },
                complete: function() {
                    self._log('complete SAVE_form_json_data')
                }
            });
        }
    });

});