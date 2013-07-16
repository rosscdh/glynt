'use strict';
/**
* Clone a region of a form
* ------------------------
* 
*/
$(function() {
    // the widget definition, where "custom" is the namespace,
    // "colorize" the widget name
    $.widget( "lawpal.show_when", {
		// default options
		options: {
			initial_state: 'hide',
			operation: 'show'
		},
		operators: {'eq': '==',
					'eeq': '===',
					'neq': '!=',
					'gt': '>',
					'gte': '>=',
					'lt': '<',
					'lte': '<='},
		tokens: null,
		show_when: null,
		current_step: null,
		// the constructor
		_create: function () {
			//this.element.toggle()
			this.element_label = this.element.siblings('label[for={id}]'.assign({'id': this.element.prop('id')}))
			this.hide();
			this.current_step = $('#id_builder_wizard_view-current_step').val() || false;

			var e_data = this.element.data();  // get all "data" elements
			var showWhen = e_data.showWhen.replace(/^\s+|\s+$/g, '');  // trim the text element

			this.tokens = showWhen.split(/\b\s+/g).compact() // split on word-boundry and spaces
			var subject = this.form_object(this.tokens[0]);
			if (subject.length > 0) {
				console.log(subject)
				subject.trigger('change');
			}
		},
		hide: function () {
			this.element_label.hide();
			this.element.hide();
		},
		show: function () {
			this.element_label.show();
			this.element.show();
		},
		form_object: function (subject) {
			var self = this;
			var element = false;
			var test_element = null;
			var selector = null;
			$.each(['[name={subject}]', '[name={current_step}-{subject}]', '{subject}'], function (index, item) {
				selector = item.assign({
								'subject': subject, 
								'current_step': self.current_step
						});

				test_element = $(selector)

				if (test_element.length > 0) {
					element = test_element;
					self.bind_event_listener(element);
					return false; // break out of jquery loop...
				}
			})
			// check jquery object exists
			return element;
		},
		bind_event_listener: function (element) {
			var self = this;
			console.log('listening')
			element.on('change', function (event) {
				self.evaluate('"{val}"'.assign({'val': element.val()}));
			});
		},
		subject: function () {
			var self = this;
			var subject = this.tokens[0] || false;
			var element = null;
			subject = self.form_object(subject);
			if (subject && subject.length > 0) {
				subject = this.string_or_val(subject.val());
			}

			return subject || this.string_or_val(subject);
		},
		operator: function () {
			var operator = this.tokens[1] || false;
			if (Object.has(this.operators, operator)) {
				operator = this.operators[operator];
			}
			return operator;
		},
		comparator: function () {
			var comparator = this.tokens[2];
			return this.form_object(comparator) || this.string_or_val(comparator)
		},
		string_or_val: function (item) {
			console.log(jQuery.type(item))
			console.log(item)
			return (jQuery.type(item) === 'string') ? '"{item}"'.assign({'item': item}) : item;

		},
		evaluate: function (value) {
			var operation = '{value} {operation} {comparator}'.assign({
				'value': value,
				'operation': this.operator(),
				'comparator': this.comparator()
			});

			console.log(operation)

			if (eval(operation) === true) {
				this.show();
			} else {
				this.hide();
			}
		}
    });

});