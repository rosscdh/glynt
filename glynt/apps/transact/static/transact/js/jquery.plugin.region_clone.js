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
		// the constructor
		_create: function() {
			var self = this;

			this.cloneable_html = this.element.html();
			this.btn_remove = this.options.btn_remove.clone();

			this._btn_add_another = this.btn_add_another();
			this.element.append(this._btn_add_another);

			this._on( this._btn_add_another, {
				click: "add_region"
			});
		},
		btn_add_another: function () {
			var btn_add_another_id = '{num_elements}_add_another'.assign({'num_elements': this.num_elements})
			return $('<div id="{btn_add_another_id}"><button id="btn_add_another_{num_elements}" class="btn btn-inverse">{label}</button></div>'
					.assign({
							'btn_add_another_id': btn_add_another_id, 
							'label': this.options.label
					}));
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
			this._btn_add_another.before(cloned_html);

			/**
			* Trigger Added Cloned Region Event
			* To allow for custom events to be assigned
			*/
			$.event.trigger({
				type: "region_clone_add",
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
					type: "region_clone_remove",
					cloned_region: $(this).closest('.cloned-region')
				});
				$(this).closest('.cloned-region').remove();
			});

			this.num_elements += 1;
		}
    });

});