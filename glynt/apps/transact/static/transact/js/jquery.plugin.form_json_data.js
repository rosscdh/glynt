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
            source_data: {}, // data provided by the form being viewed
            dataType: 'application/json',
            contentType: "application/json"
        },
        form_json_data: {},
        form: null,
        _log: function (msg) {
            var self = this;
            if (self.options.debug === true) {
                console.log(msg)
            }
        },
        // the constructor
        _create: function () {
            var self = this;
            this.form = $(this.element).closest('form');

            var source_data = this.element.val() || this.options.source_data;
            this.option.source_data = (typeof source_data === 'string') ? JSON.parse(source_data) : source_data ;

            self._listen();
        },
        _listen: function () {
            var self = this;
            $(document).on("ready", function (event) {

                /**
                * Send off the reference to teh source data.
                * may be modified by various listeners
                */
                $.event.trigger({
                    type: "LOADED_form_json_data",
                    form_json_data: self.options.source_data
                });
                self._refresh()
            });

            /**
            * Capture all changes made to the source_data
            */
            $(document).on("REMOVE_CLONED_REGION_form_json_data", function (event) {
                var cloned_region_key = event.cloned_region_key;

                $.each(event.cloned_region.find('input, select, checkbox, radio'), function (i, elem) {
                    elem = $(elem);
                    var json_id = elem.prop('id').replace(/^id_(\d+)\-/g,'');
                    console.log(elem.data())
                    /**
                    * Remove the object
                    */
                    delete self.options.source_data[cloned_region_key][json_id];
                    console.log(self.options.source_data[cloned_region_key])
                    console.log(json_id)
                });

                self._refresh()

                /**
                * Save the data to the specified url
                */
                $.event.trigger({
                    type: "SAVE_form_json_data",
                });

            });
            /**
            * Capture changes made to Cloned Region items
            */
            $(document).on("MODIFIED_CLONED_REGION_form_json_data", function (event) {
                var elem = $(event.instance);
                var cloned_region_key = event.cloned_region_key;

                var elem_id = elem.data('json_id');

                var instance_dict = {
                    'id': elem.data('json_id'),
                    'name': elem.data('json_name'),
                    'val': elem.val()
                }

                self.options.source_data[cloned_region_key][elem_id] = instance_dict;

                self._refresh()
                /**
                * Save the data to the specified url
                */
                $.event.trigger({
                    type: "SAVE_form_json_data",
                });

            });

            /**
            * Capture changes made to the form_json_data
            */
            $(document).on("SAVE_form_json_data", function (event) {

                self._send(self.options.source_data);

            });

        },
        _refresh: function() {
            this._log('_refresh');
            var json_data = JSON.stringify(this.options.source_data);
            $(this.element).val(json_data)
        },
        _send: function (data) {            
            var self = this;
            /**
            * Prepare for structure that we are saving as
            * {data: {}}
            */
            data = {'data': data}
            var json_data = JSON.stringify(data);

            if (self.options.update_url) {
                self._log('Save DAta URL: {url} send: {data}'.assign({'url': self.options.update_url, 'data': data}))
                /**
                * Capture changes made to the form_json_data
                */
                $.ajax({
                    type: 'PUT',
                    url: self.options.update_url,
                    data: json_data,
                    dataType: self.options.dataType,
                    contentType: self.options.contentType,
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

            } else {

                self._log('self.options.update_url does not exist');

            }
        }
    });
});