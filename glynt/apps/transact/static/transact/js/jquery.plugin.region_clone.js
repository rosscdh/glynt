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
		num_elements_in_cloned_area: 1,
		options: {
			label: 'Add another',
			btn_remove: $('<button/>', {
				class: 'close delete-cloned-region',
				html: '&times;'
			})
		},
		region_key: null,
		element_data: {},
		form_json_data: {},
        _log: function (msg) {
            var self = this;
            if (self.options.debug === true) {
                console.log(msg)
            }
        },
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
			$.each(this.element.children().find('input, select, checkbox, radio'), function (i, elem) {
				self.add_element(elem, false)
			});

	        /**
	        * Handle the LOADED_form_json_data Event
	        * create form elements based on the data in the JSON
	        **/
	        $(document).on("LOADED_form_json_data", function (event) {
	            self.form_json_data = event.form_json_data;
	            self.ensure_key(self.form_json_data)
	            self._refresh();
	        });
		},
        _refresh: function() {
        	var self = this;
        	self._log('region_clone:_refresh');
        	/**
        	* Create all elements if they dont exist
        	*/
        	var region_ids = [];

            $.each(self.form_json_data[self.region_key], function (i, item) {
            	// var object_id = 'id_{step}-{name}'.assign({'step': self.options.current_step, 'name': item.name});
            	// var elem = $('#' + object_id);
            	var matched_count = item.id.match(/_(\d+)$/gi);
            	matched_count = (matched_count && matched_count.length) ? parseInt(matched_count[0].replace('_', '')) : 0 ;
            	region_ids.push(matched_count)

            });

			region_ids = region_ids.unique()
			$.each(region_ids, function (i, item) {
				// exclude the 0 count as that is the original cloneable region
				if (item > 0) {
					self.add_region( new Event('click'), {'region_id': item} )
				}
			});
        	/**
        	* Populate the elements, after they have been created
        	* beware this must be done seperately from the create
        	*/
            $.each(self.form_json_data[self.region_key], function (i, item) {

				var matched_count = item.id.match(/_(\d+)$/gi);

            	var object_id = 'id_{step}-{name}'.assign({'step': self.options.current_step, 'name': item.name});
            	var elem = $('#' + object_id);
            	// populate with value
            	elem.val(item.val);

				if (matched_count !== null) {
					//element_count_id = parseInt(matched_count[0].replace('_', ''));
					//console.log(elem.attr('id'))
					// var id = elem.attr('id').replace(/_(\d+)$/gi, '_{element_count_id}'.assign({'element_count_id': element_count_id}));
					// elem.attr('id', id);
					// var name = elem.attr('name').replace(/_(\d+)$/gi, '_{element_count_id}'.assign({'element_count_id': element_count_id}));
					// elem.attr('name', name);

					//console.log(elem)
					//console.log(elem.attr('name'))
				}

            });
        },
		ensure_key: function (form_json_data) {
			var self = this;
			form_json_data[this.region_key] = form_json_data[this.region_key] || {}
			self._log('ensure that the item "{region_key}" is represented in the data: {data}'.assign({'region_key': self.region_key, 'data': form_json_data[this.region_key]}))
		},
		btn_add_another: function () {
			var btn_add_another_id = '{num_elements}_add_another'.assign({'num_elements': this.num_elements})
			return $('<div id="{btn_add_another_id}"><button id="btn_add_another" class="btn btn-success pull-right">{label}</button></div>'
					.assign({
							'btn_add_another_id': btn_add_another_id,
							'label': this.options.label
					}));
		},
		add_element: function ( elem, make_new, step_count ) {
			elem = $(elem);
			var self = this;
			var make_new = (make_new == undefined);
			step_count = step_count || self.num_elements

			/**
			* Dont modify the base cloneable field
			*/
			if ( make_new === true ) {

				// append the current num to the cloned id name
				var new_id = '{id}_{current_num}'.assign({'id': elem.prop('id'), 'current_num': step_count})
				var new_name = '{name}_{current_num}'.assign({'name': elem.prop('name'), 'current_num': step_count})

				// update the id and name props
				elem.prop('id', new_id);
				elem.prop('name', new_name);
			}

			// append json_id and json_name
			elem.attr('data-json_index', step_count);
			elem.attr('data-json_id', elem.prop('id').replace(/^id_(\d+)\-/g,''));
			elem.attr('data-json_name', elem.prop('name').replace(/^(\d+)\-/g,''));

			// set the value of this element blank
			elem.val('');

			elem.on('change', function (event) {
                $.event.trigger({
                    type: "MODIFIED_CLONED_REGION_form_json_data",
                    instance: $(this),
					cloned_region_key: self.region_key
                });
			});
			return elem;
		},
		add_region: function ( event, kwargs ) {
			event.preventDefault()
			var self = this;
			var kwargs = $.extend(true, {'region_id': self.num_elements}, kwargs);
			//var current_num_cloneable_regions = $('[data-region-name={region_key}] .cloned_region'.assign({'region_key': self.region_key})).length
console.log(kwargs)
			var cloneable_html = $(this.cloneable_html).clone();

			var legend = $(cloneable_html[0]);
			var btn_remove = $(this.btn_remove.clone());

			/**
			* Update the legend
			* to consist of the current values + counter info
			*/
			legend.html('&nbsp;{label}'.assign({
				'label': legend.html(),
				'current': this.num_elements,
			}));
			// legend.prepend(btn_remove);

			/**
			* Assign change events to each input item
			* in the cloned region
			*/
			self.num_elements_in_cloned_area = 0;
			$.each(cloneable_html.find('input, select, checkbox, radio'), function (i, elem) {
				self.add_element(elem, undefined, kwargs.region_id);
				self.num_elements_in_cloned_area++;
			});

			/**
			* Insert the cloned htmlin before the "add another"
			* button
			*/
			var cloned_html = $('<div>', {
				'class': 'cloned-region',
				'html': cloneable_html,
				'data-region_key': self.region_key,
				'data-index': self.num_elements
			});

            cloned_html.prepend(btn_remove);

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

				// $('input#id_1-num_officers').val(self.num_elements);
			});

			this.num_elements += 1;

			// $('input#id_1-num_officers').val(this.num_elements);
		}
    });

});