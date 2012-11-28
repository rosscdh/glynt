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

Handlebars.registerHelper('doc_var', function(context, options) {

    if (context.hash.name === undefined || context.hash.name === '') {
        throw 'doc_var requires a unique "name"';
    }
    var app = (context.hash.app === undefined) ? window.app : eval('window.'.format(context.hash.app)) ;
    var var_name = context.hash.name;
    var field_type = 'text';
    var has_initial = null;
    var value = null;
    var html_return = '<span class="{type} edit" data-has_initial="{has_initial}" data-doc_var="{variable_name}">{value}</span>';

    if (context.hash.field_type !== undefined && context.hash.field_type === '') {
        field_type = context.hash.field_type;
    }
    // see if this context.name is already defined in the app context (to get user populated data)
    try{
        // context.hash.initial = context.call(this);
    }catch(e){
        // as we set the hash initial based on html_inner above we need do nothing
        // except catch the error
    }

    has_initial = (context.hash.initial === undefined) ? false : true;
    value = (context.hash.initial !== undefined) ? context.hash.initial : '_____'.repeat(2) ;
    value = (app.context[var_name] === undefined) ? value : app.context[var_name] ;

    // add value to context
    if (app.context[var_name] === undefined) {
        // set to nul because we know it is undefined; assert positive
        app.context[var_name] = null;
    }
    // wrap the value in our detailed html to allow UX interaction
    html_return = html_return.assign({ 'variable_name': var_name, 'value': value, 'type': 'doc_var', 'has_initial': has_initial });

    context.hash.field_type = field_type;
    context.hash.html_return = html_return;

    // set the context
    app.helper_context[var_name] = context.hash;

    // make it safe so hb does not mess with it
    return new Handlebars.SafeString(html_return);
});


Handlebars.registerHelper('doc_choice', function(context, options) {
    console.log(context)
    if (context.hash.name === undefined || context.hash.name === '') {
        throw 'doc_choice requires a unique "name"';
    }
    var app = (context.hash.app === undefined) ? window.app : eval('window.'.format(context.hash.app)) ;
    var var_name = context.hash.name;
    var choices = context.hash.choices;
    console.log(this.name)
    var html_return = '';

    // set the context
    app.helper_context[var_name] = context.hash;

    // make it safe so hb does not mess with it
    return new Handlebars.SafeString(html_return);
});


Handlebars.registerHelper('doc_select', function(context, options) {
    if (context.hash.name === undefined || context.hash.name === '') {
        throw 'doc_select requires a unique "name"';
    }
    var app = (context.hash.app === undefined) ? window.app : eval('window.'.format(context.hash.app)) ;
    var var_name = context.hash.name;
    //var content = context.call(this);
    //content = content.split('{option}');// splti by the {option} seperator

    var html_return = '';

    // set the context
    app.helper_context[var_name] = context.hash;

    // make it safe so hb does not mess with it
    return new Handlebars.SafeString(html_return);
});