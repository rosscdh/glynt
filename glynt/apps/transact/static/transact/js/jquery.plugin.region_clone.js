'use strict';
/**
* Clone a region of a form
* ------------------------
* 
*/
$(function() {
    // the widget definition, where "custom" is the namespace,
    // "colorize" the widget name
    $.widget( "lawpal.region_clone", {
		// default options
		num_elements: 1,
		options: {
			label: 'Add another',
			btn_remove: $('<button/>', {
				class: 'right btn btn-danger delete-cloned-region',
				html: 'x'
			})
		},
		region_key: null,
		element_data: {},
		form_json_data: {},
		// the constructor
		_create: function() {
			var self = this;

			this.element_data = this.element.data();
			this.region_key = this.element_data.regionName;

			this.cloneable_html = this.element.html();
			this.btn_remove = this.options.btn_remove.clone();

			this._btn_add_another = this.btn_add_another();
			this.element.append(this._btn_add_another);

			this._on( this._btn_add_another, {
				click: "add_region"
			});

			this._listen();
		},
		_listen: function () {
			var self = this;
            
			/**
			* Assign change events to each input item 
			* in the cloned region
			*/
			$.each($(self.cloneable_html).find('input, select, checkbox, radio'), function (i, elem) {
				self.add_element(elem, false)
			});
        
	        /**
	        * Handle the LOADED_form_json_data Event
	        **/
	        $(document).on("LOADED_form_json_data", function (event) {
	            self.form_json_data = event.form_json_data;
	            self.ensure_key(self.form_json_data)
	            self._refresh();
	        });
		},
        _refresh: function() {
        	var self = this;
            $.each(self.form_json_data[self.region_key], function (i, item) {
            	console.log('ensure that the tem is represented in the html')
            })
        },
		ensure_key: function (form_json_data) {
			form_json_data[this.region_key] = form_json_data[this.region_key] || {}
		},
		btn_add_another: function () {
			var btn_add_another_id = '{num_elements}_add_another'.assign({'num_elements': this.num_elements})
			return $('<div id="{btn_add_another_id}"><button id="btn_add_another_{num_elements}" class="btn btn-inverse">{label}</button></div>'
					.assign({
							'btn_add_another_id': btn_add_another_id, 
							'label': this.options.label
					}));
		},
		add_element: function (elem, make_new) {
			elem = $(elem);
			var self = this;
			var make_new = (make_new == undefined);

			/**
			* Dont modify the base cloneable field
			*/
			if ( make_new === true ) {
				// append the current num to the cloned id name
				var new_id = '{id}-{current_num}'.assign({'id': elem.prop('id'), 'current_num': self.num_elements})
				var new_name = '{name}-{current_num}'.assign({'name': elem.prop('name'), 'current_num': self.num_elements})

				// update the id and name props
				elem.prop('id', new_id);
				elem.prop('name', new_name);
			}

			// append json_id and json_name
			elem.attr('data-json_id', elem.prop('id').replace(/^id_(\d+)\-/g,''));
			elem.attr('data-json_name', elem.prop('name').replace(/^id_(\d+)\-/g,''));

			elem.on('change', function (event) {
                $.event.trigger({
                    type: "MODIFIED_CLONED_REGION_form_json_data",
                    cloned_region_key: self.region_key,
                    instance: $(this),
                });
			});
		},
		add_region: function ( event ) {
			event.preventDefault()
			var self = this;

			var cloneable_html = $(this.cloneable_html).clone();

			var legend = $(cloneable_html[0]);
			var btn_remove = $(this.btn_remove.clone())

			/**
			* Update the legend
			* to consist of the current values + counter info
			*/
			legend.html('&nbsp;{label}'.assign({
				'label': legend.html(), 
				'current': this.num_elements,
			}));
			legend.prepend(btn_remove);

			/**
			* Insert the cloned htmlin before the "add another"
			* button
			*/
			var cloned_html = $('<div>', {
				'class': 'cloned-region',
				'html': cloneable_html
			});

			/**
			* Assign change events to each input item 
			* in the cloned region
			*/
			$.each(cloned_html.find('input, select, checkbox, radio'), function (i, elem) {
				self.add_element(elem)
			});

			/**
			* Add the cloned HTML to the document
			* -----------------------------------
			*/
			this._btn_add_another.before(cloned_html);

			/**
			* Trigger Added Cloned Region Event
			* To allow for custom events to be assigned
			*/
			$.event.trigger({
				type: "ADD_CLONED_REGION_form_json_data",
				cloned_region: cloned_html
			});

			/**
			* Listener for the button remove
			*/
			btn_remove.on('click', function( event ) {
				event.preventDefault();
				event.stopPropagation();
				self.num_elements -= 1;
				$.event.trigger({
					type: "REMOVE_CLONED_REGION_form_json_data",
					cloned_region: $(this).closest('.cloned-region'),
					cloned_region_key: self.region_key
				});
				$(this).closest('.cloned-region').remove();
			});

			this.num_elements += 1;
		}
    });

});