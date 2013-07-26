'use strict';
/**
* Filter a specified list by certain status
* -----------------------------------------
* 
*/
$(function() {
    // the widget definition, where "custom" is the namespace,
    // "colorize" the widget name
    $.widget( "lawpal.filter_status", {
        // default options
        filterable_items: [],
        options: {
            'state_modifier': null
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

            self.filterable_items = self.element.find('[data-status]');
            self.state_modifier = self.options.state_modifier;

            this._listen();
        },
        _listen: function () {
            var self = this;
            /**
            * Normalise the names all lowercase
            */
            $.each(self.state_modifier.find('[data-status]'), function (i, elem) {
                var elem = $(elem);
                elem.attr('data-status', elem.data('status').toLowerCase());
            });
            /**
            * Find all clickable elements within the parent
            * that has a data-modifier element
            */
            self.state_modifier.find('[data-modifier]').on('click', function (event) {
                var elem = $(this);
                var action = elem.data('modifier');
                self.apply_filter(action);
            });

            /**
            * Find all badge elements that have a modifier_type
            * count the number of items and update the badge html
            */
            $.each(self.state_modifier.find('.badge[data-modifier_type]'), function (i, elem) {
                elem = $(elem);
                elem.hide();
                var modifier_type = elem.data('modifier_type').toLowerCase();
                if ( modifier_type == 'all' ) {
                    var selector = '[data-status]';
                } else {
                    var selector = '[data-status={modifier_type}]'.assign({'modifier_type': modifier_type});
                }
                var num_items = $(selector).length;
                elem.html(num_items.toString());
                elem.show();
            });
        },
        apply_filter: function (action) {
            var self = this;

            action = action.toLowerCase();

            $.each(self.filterable_items, function (i, item) {
                item = $(item)
                var element_status = item.data('status').toLowerCase();

                if ( element_status == 'all') {
                    self['_all'](item);

                } else if ( element_status != action ) {
                    self['_{action}'.assign({'action': action})](item);

                }

            });
        },
        _all: function (item) {
            item.show();
        },
        _closed: function (item) {
            item.hide();
        }
    });

});