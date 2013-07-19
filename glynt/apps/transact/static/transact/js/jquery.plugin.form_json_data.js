'use strict';
/**
* Manage the JSON data field of a form
* ------------------------------------
* 
*/
$(function() {
    // the widget definition, where "custom" is the namespace,
    $.widget( "lawpal.form_json_data", {
        // default options
        options: {
            debug: true,
            update_url: undefined,
            source_data: {} // data provided by the form being viewed
        },
        form_json_data: {},
        form: null,
        _log: function (msg) {
            if (self.options.debug === true) {
                console.log(msg)
            }
        },
        // the constructor
        _create: function () {
            var self = this;
            this.form = $(this.element).closest('form');

            this.options.source_data = JSON.parse(this.element.val()) || this.options.source_data;

            $(document).on("ready", function (event) {

                /**
                * Send off the reference to teh source data.
                * may be modified by various listeners
                */
                $.event.trigger({
                    type: "LOADED_form_json_data",
                    form_json_data: self.options.source_data
                });

                self._listen();

                self._refresh()
            });
        },
        _listen: function () {
            var self = this;
            /**
            * Capture all changes made to the source_data
            */
            if (self.options.update_url) {
                /**
                * Capture changes made to the form_json_data
                */
                $(document).on("SAVE_form_json_data", function (event) {

                    $.ajax({
                        type: 'POST',
                        url: self.options.update_url,
                        data: self.options.source_data,
                    })
                    .success(function(data, textStatus, jqXHR) {
                        self._log('success SAVE_form_json_data')
                    })
                    .error(function(jqXHR, textStatus, errorThrown) { 
                        self._log('error SAVE_form_json_data')
                    })
                    .complete(function() {
                        self._log('complete SAVE_form_json_data')
                    });

                });
            } else {
                self._log('self.options.update_url does not exist');
            }

            $(document).on("REMOVE_CLONED_REGION_form_json_data", function (event) {
                var cloned_region_key = event.cloned_region_key;

                $.each($(event.cloned_region).find('input, select, checkbox, radio'), function (i, elem) {
                    elem = $(elem);
                    var elem_id = elem.prop('id');

                    delete self.options.source_data[cloned_region_key][elem_id];
                });

                self._refresh()
            });
            /**
            * Capture changes made to Cloned Region items
            */
            $(document).on("MODIFIED_CLONED_REGION_form_json_data", function (event) {
                var elem = $(event.instance);
                var cloned_region_key = event.cloned_region_key;
                var elem_id = elem.prop('id');
                var instance_dict = {'id': elem.prop('id'), 'name': elem.prop('name'), 'val': elem.val()}

                self.options.source_data[cloned_region_key][elem_id] = instance_dict;

                self._refresh()
            });

        },
        _refresh: function() {
            console.log('_refresh')
            $(this.element).val(JSON.stringify(this.options.source_data))
            // trigger a callback/event
            this._trigger( "change" );
        },
        add_item: function (key, value) {
            var self = this;
            if (value instanceof Array) {
                // if we pass in an array it implies that the key is an array
                self.form_json_data[key] = self.form_json_data[key] || []
    console.log(self.form_json_data[key])
            } else {
                this.form_json_data[key] = value;
            }
        },
        remove_item: function (key, value) {
            
        }
    });
});