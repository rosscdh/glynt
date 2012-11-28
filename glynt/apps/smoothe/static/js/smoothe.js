/**
* Handlebars helpers that assist in the creation of document variables
* generally the output html that allows us to bind DOM events
*/
// var docVarBase = function docVarBase(params) {
//     self = this;
//     self.param_required = ['name'];
//     self.param_optional = [];
//     self.valid_params = null;
// 
//     self.init = function init(params) {
//         console.log(params)
//         self.valid_params = self.param_required + self.param_optional;
//         $.each(params, function(key, value){
//             if (self.valid_params.indexOf(key) > -1) {
//                 self[key] = value;
//             }
//         });
//     }
//     self.init(params)
// };

Handlebars.registerHelper('doc_var', function(options) {

    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_var requires a unique "name"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var field_type = 'text';
    var has_initial = (options.hash.initial === undefined) ? false : true;
    var value = null;
    var html_return = '<span class="{type} edit" data-has_initial="{has_initial}" data-doc_var="{variable_name}">{value}</span>';

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
    // wrap the value in our detailed html to allow UX interaction
    html_return = html_return.assign({ 'variable_name': var_name, 'value': value, 'type': 'doc_var', 'has_initial': has_initial });

    options.hash.field_type = field_type;
    options.hash.html_return = html_return;

    // set the context
    app.helper_context[var_name] = options.hash;

    // make it safe so hb does not mess with it
    return new Handlebars.SafeString(html_return);
});


Handlebars.registerHelper('doc_choice', function(options) {
    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_choice requires a unique "name"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var choices = options.hash.choices;
    var html_return = '';
console.log(options.hash.choices)
    // set the context
    app.helper_context[var_name] = options.hash;

    // make it safe so hb does not mess with it
    return new Handlebars.SafeString(html_return);
});


Handlebars.registerHelper('doc_select', function(options) {
    if (options.hash.name === undefined || options.hash.name === '') {
        throw new Error('doc_select requires a unique "name"');
    }
    var app = (options.hash.app === undefined) ? window.app : eval('window.'.format(options.hash.app)) ;
    var var_name = options.hash.name;
    var title = options.hash.name;
    var can_toggle = (options.hash.can_toggle === undefined) ? false: options.hash.can_toggle;
    var html_return = '';
    var content = options.fn(this);
    options.hash.select_options = [];
    select_options = content.split('{option}');// splti by the {option} seperator
    for (var i = 0; i < select_options.length; i++) {
        options.hash.select_options.push({
            'text': select_options[i],
            'selected': false,
            'index': i
        });
    }

    html_return = Handlebars.compile('<ul id="{{id}}" data-can_toggle="{{can_toggle}}" data-multi="{{multi}}" class="doc_select {{class}}">{{#each select_options}}<li data-option_index="{{index}}" class="{{#if selected}}selected{{/if}}">{{text}}</li>{{/each}}</ul>');

    // set the context
    app.helper_context[var_name] = options.hash;

    // make it safe so hb does not mess with it
    return html_return(options.hash);
});