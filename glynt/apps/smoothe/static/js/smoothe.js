/**
* Handlebars helpers that assist in the creation of document variables
* generally the output html that allows us to bind DOM events
*/

Handlebars.registerHelper('doc_var', function(options) {

    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_var requires a unique "name"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var field_type = 'text';
    var has_initial = (options.hash.initial === undefined) ? false : true;
    var value = null;
    var html_return = null;

    if (options.hash.field_type !== undefined && options.hash.field_type === '') {
        field_type = options.hash.field_type;
    }
    // see if this options.name is already defined in the app context (to get user populated data)
    if (has_initial === false) {
        options.hash.initial = options.fn(this);
    }

    value = (options.hash.initial !== undefined) ? options.hash.initial : '' ;
    value = (app.context[var_name] === undefined) ? value : app.context[var_name] ;

    // add value to context
    if (app.context[var_name] === undefined) {
        // set to nul because we know it is undefined; assert positive
        app.context[var_name] = null;
    }
    options.hash.type = 'doc_var';
    options.hash.field_type = field_type;
    options.hash.variable_name = var_name;
    options.hash.value = value;
    options.hash.has_initial = has_initial;

    // wrap the value in our detailed html to allow UX interaction
    html_return = Handlebars.partials['doc_var-partial'];

    // set the context
    options.hash.id = MD5(String(var_name + app.context.length+1));
    app.context[var_name] = options.hash;

    // make it safe so hb does not mess with it
    return html_return(options.hash);
});


Handlebars.registerHelper('doc_choice', function(options) {
    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_choice requires a unique "name"');
    }
    if (options.hash.choices === undefined || options.hash.choices.length <= 0) {
        console.log('"{name}" is a doc_choice element and requires a "choices" list i.e. ["a","b","c"]'.assign({'name': options.hash.name}));
        options.hash.choices = [];
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var choices = options.hash.choices;
    var html_return = '';
//console.log(options.hash.choices)
    // set the context
    options.hash.id = MD5(String(var_name + app.context.length+1));
    app.context[var_name] = options.hash;

    // make it safe so hb does not mess with it
    return new Handlebars.SafeString(html_return);
});


Handlebars.registerHelper('doc_select', function(options) {
    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_select requires a unique "name"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var label = (options.hash.label === undefined) ? false: options.hash.label;
    var can_toggle = (options.hash.can_toggle === undefined) ? false: options.hash.can_toggle;
    var html_return = '';
    // get the inner content
    var content = options.fn(this);
    // split it based on the {option} seperator as per our docs
    options.hash.select_options = [];
    select_options = content.split('{option}');// splti by the {option} seperator
    // setup the partial list
    for (var i = 0; i < select_options.length; i++) {
        options.hash.select_options.push({
            'text': select_options[i].compact(),
            'selected': false,
            'index': i
        });
    }

    html_return = Handlebars.partials['doc_select-partial'];

    // set the context
    options.hash.id = MD5(String(var_name + app.context.length+1));
    app.context[var_name] = options.hash;

    if (can_toggle == true) {
        var toggle = Handlebars.partials['toggle-partial'];
        var show_toggle = (app.context[var_name] === undefined || app.context[var_name].show_toggle === undefined || app.context[var_name].show_toggle === true) ? true : false;
        toggle_hash = {
            'toggle_for': var_name,
            'label': label,
            'text': (show_toggle == false) ? 'Show': 'Hide'
        };
        return html_return(options.hash) + toggle(toggle_hash);
    } else {
        return html_return(options.hash);
    }
});


Handlebars.registerHelper('help_for', function(options) {
    if (options.hash.varname === undefined || options.hash.varname === '') {
        throw new Error('help_for requires a "varname"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.varname;
    var content = options.fn(this);

    if (app.context[var_name] === undefined || typeof app.context[var_name] !== 'object') {
        throw new Error('There is no variable named "{varname}" that is an "object" in the app.context'.assign({'varname': varname}));
    }else{
        app.context[var_name].help_text = content;
    }
});

Handlebars.registerHelper('doc_note', function(options) {
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var content = options.fn(this);
    content = content.split('{note}');
    var note = content[1];
    content = content[0];

    options.hash.id = MD5(note);
    app.context.notes[options.hash.id] = note;

    var html_return = Handlebars.partials['doc_note-partial'];
    return html_return({'id': options.hash.id, 'note': note, 'content': content});
});


// ----- JQUEY PLUGINS -----
// select jquery UI plugin
(function($) {
    $.widget("ui.glynt_select", {
        options: {
            context_name: null,
            multi: false,
            can_toggle: false,
            location: "bottom",
            color: "#fff",
            backgroundColor: "#000"
        },
        _create: function() {
            var self = this;
            self.app = window.app;
            self.multi = ($(self.element).attr('data-multi') !== '') ? true: false;
            self.can_toggle = ($(self.element).attr('data-can_toggle') !== '') ? true: false;
        }
    });
})(jQuery);