"use strict"; // jshint ;_;
/**
* Handlebars helpers that assist in the creation of document variables
* generally the output html that allows us to bind DOM events
*/

Handlebars.registerHelper('doc_var', function(options) {
    var app = window.app || eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name.compact();
    // wrap the value in our detailed html to allow UX interaction
    var html_return = Handlebars.partials['doc_var-partial'];

    if (app.context[var_name] === undefined) {
        if (options.hash.name === undefined || options.hash.name === '') {
            throw new Error('doc_var requires a unique "name"');
        }
        var field_type = 'text';
        var has_initial = (options.hash.initial === undefined) ? false : true;
        var value = null;

        if (options.hash.field_type !== undefined && options.hash.field_type === '') {
            field_type = options.hash.field_type;
        }
        // see if this options.name is already defined in the app context (to get user populated data)
        if (has_initial === false) {
            options.hash.has_initial = has_initial;
            options.hash.initial = options.fn(this).compact();
            console.log('name: {name},initial: {initial}'.assign({initial:options.hash.initial, name:var_name}))
        }

        value = (options.hash.initial !== undefined) ? options.hash.initial : '' ;
        value = (app.context[var_name] === undefined) ? value : app.context[var_name].value.compact() ;
        value = value.compact();

        options.hash.type = 'doc_var';
        options.hash.field_type = field_type;
        options.hash.variable_name = var_name;
        options.hash.value = value;

        // set the context
        options.hash.id = MD5(String(var_name + app.context.length+1));
        options = app.instance_count(options, var_name);
        app.context[var_name] = options.hash;
    }
    // make it safe so hb does not mess with it
    return html_return(app.context[var_name]);
});


Handlebars.registerHelper('doc_choice', function(options) {
    var app = window.app || eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name.compact();
    // wrap the value in our detailed html to allow UX interaction
    var html_return = Handlebars.partials['doc_choice-partial'];

    if (app.context[var_name] === undefined) {
        if (options.hash.name === undefined || options.hash.name === '') {
            throw new Error('doc_choice requires a unique "name"');
        }

        if (options.hash.choices === undefined || options.hash.choices.length <= 0) {
            console.log('"{name}" is a doc_choice element and requires a "choices" list i.e. "a,b,c"]'.assign({'name': options.hash.name}));
            options.hash.choices = [];
            options.hash.initial = '[Error] You must provide a set of choices';
        } else {
            options.hash.choices = options.hash.choices.split(',');
        }
        var app = window.app || eval('window.'.format(options.hash.app)) ;
        var value = null;
        var var_name = options.hash.name;
        var choices = options.hash.choices;

        var has_initial = (options.hash.initial === undefined) ? false : true;
        if (has_initial === false) {
            options.hash.initial = options.fn(this);
        }
        value = (options.hash.initial !== undefined) ? options.hash.initial : '' ;
        value = (app.context[var_name] === undefined || app.context[var_name].value === "") ? value : app.context[var_name].value ;
        options.hash.value = value;

        options.hash.type = 'doc_choice';

        // set the context
        options.hash.id = MD5(String(var_name + app.context.length+1));
        options = app.instance_count(options, var_name);

        app.context[var_name] = options.hash;
    }
    return html_return(options.hash);
});


Handlebars.registerHelper('doc_select', function(options) {
    var app = window.app || eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name.compact();
    // wrap the value in our detailed html to allow UX interaction
    var html_return = Handlebars.partials['doc_select-partial'];

    if (app.context[var_name] === undefined) {
        if (options.hash.name === undefined || options.hash.name === '') {
            throw new Error('doc_select requires a unique "name"');
        }
        var app = window.app || eval('window.'.format(options.hash.app)) ;
        var var_name = options.hash.name;
        var label = (options.hash.label === undefined) ? false: options.hash.label;
        var can_toggle = (options.hash.can_toggle === undefined) ? false: options.hash.can_toggle;
        var multi = (options.hash.multi === undefined) ? false: options.hash.multi;
        var can_increment = (options.hash.can_increment === undefined) ? false: options.hash.can_increment;
        var extended_html = (options.hash.extended_html === undefined) ? Array(): Array(options.hash.extended_html);
        var default_selected_items =  (options.hash.selected === undefined) ? Array(): Array(options.hash.selected.split(","));

        options.hash.label = label;
        options.hash.variable_name = var_name;
        options.hash.multi = multi;
        options.hash.id = MD5(String(var_name + app.context.length+1));
        options.hash.type = 'doc_select';
        options.hash.can_toggle = can_toggle;
        options.hash.can_increment = can_increment;

        // get the inner content
        var content = options.fn(this);
        // split it based on the {option} seperator as per our docs
        options.hash.select_options = [];
        var select_options = content.split('{option}');// splti by the {option} seperator
        var has_selected_item = false;
        // setup the partial list
        for (var i = 0; i < select_options.length; i++) {
            // handle this ugly nastiness from submitting json obejct and having it converted into an abomination
            var selected = '{var_name}[{index}][selected]'.assign({var_name:var_name, index:i})
            if (app.document_data[selected] !== undefined){
                selected = (app.document_data[selected] == 'true')
            }
            // used for setting defaults
            if (has_selected_item == false && selected === true) {
                has_selected_item = true;
            }

            options.hash.select_options.push({
                'id': '{id}-{index}'.assign({'id': options.hash.id, 'index': i}),
                'text': new Handlebars.SafeString(select_options[i]),
                'handle': 'Select',
                'target': options.hash.id,
                'selected': selected,
                'index': i
            });
        }
        if (has_selected_item === false) {
            // set defaults, but only we if have no values
            $.each(options.hash.select_options, function(index,item){
                var i = index + 1; // the spec is 1 based
                if (default_selected_items.indexOf(i) >= 0) {
                    item.selected = true;
                }
            })
        }

        // set the context
        options = app.instance_count(options, var_name);
        app.context[var_name] = options.hash;

        if (can_increment == true) {
            var incrementor = Handlebars.partials['incrementor-partial'];
            var incrementor_hash = {
              'incrementor_for': var_name,
              'text': 'Add'
            };
            extended_html.push(incrementor(incrementor_hash));
        }

        if (can_toggle == true) {
            var toggle = Handlebars.partials['toggle-partial'];
            var show_toggle = (app.context[var_name] === undefined || app.context[var_name].show_toggle === undefined || app.context[var_name].show_toggle === true) ? true : false;
            var toggle_hash = {
                'toggle_for': var_name,
                'label': label,
                'text': (show_toggle == false) ? 'Show': 'Hide'
            };
            extended_html.push(toggle(toggle_hash));
        }
        options.hash.extended_html = new Handlebars.SafeString(extended_html.join(''));
    }

    return html_return(options.hash);
});


Handlebars.registerHelper('help_for', function(options) {
    if (options.hash.varname === undefined || options.hash.varname === '') {
        throw new Error('help_for requires a "varname"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    try{
        var var_name = options.hash.varname;
    } catch(e) {
        console.log(e)
    }
    var content = options.fn(this).compact();

    if (app.context[var_name] === undefined || typeof app.context[var_name] !== 'object') {
        throw new Error('There is no variable named "{varname}" that is an "object" in the app.context'.assign({'varname': var_name}));
    }else{
        app.context[var_name].help_text = content;
    }
});


Handlebars.registerHelper('doc_note', function(options) {
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var content = options.fn(this);
    content = content.split('{note}');
    var note = content[1].compact();
    content = content[0].compact();

    options.hash.id = MD5(note + app.context.notes.length+1);
    app.context.notes[options.hash.id] = note;

    var html_return = Handlebars.partials['doc_note-partial'];
    return html_return({'id': options.hash.id, 'note': note, 'content': content});
});
