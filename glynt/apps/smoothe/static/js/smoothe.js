/**
* Handlebars helpers that assist in the creation of document variables
* generally the output html that allows us to bind DOM events
*/

Handlebars.registerHelper('doc_var', function(context, options) {
  if (context.hash.name == undefined || context.hash.name == '') {
    throw 'doc_var requires a unique "name"';
  };
  var app = (context.hash.app == undefined) ? window.app : eval('window.'.format(context.hash.app)) ;
  var var_name = context.hash.name;
  var field_type = 'text';

  if (context.hash.field_type != undefined && context.hash.field_type == '') {
    field_type = context.hash.field_type;
  }
  // see if this context.name is already defined in the app context (to get user populated data)
  var has_initial = (context.hash.initial == undefined) ? false : true;
  var value = (context.hash.initial != undefined) ? context.hash.initial : '_____'.repeat(2) ;
  value = (app.context[var_name] == undefined) ? value : app.context[var_name] ;

  if (app.context[var_name] == undefined) {
    // set to nul because we know it is undefined; assert positive
    app.context[var_name] = null;
  };
  // wrap the value in our detailed html to allow UX interaction
  var html_return = '<span class="{type} edit" data-has_initial="{has_initial}" data-doc_var="{variable_name}">{value}</span>'.assign({ variable_name: var_name, value: value, type: 'doc_var', has_initial: has_initial });

  context.hash.field_type = field_type;
  context.hash.html_return = html_return;
  // set the context
  app.helper_context[var_name] = context.hash;

  // make it safe so hb does not mess with it
  return new Handlebars.SafeString(html_return);
});


Handlebars.registerHelper('doc_or', function(context, options) {
  if (context.hash.name == undefined || context.hash.name == '') {
    throw 'doc_or requires a unique "name"';
  };
  var app = (context.hash.app == undefined) ? window.app : eval('window.'.format(context.hash.app)) ;
  var var_name = context.hash.name;
  var html = context.call(this);
  // wrap the value in our detailed html to allow UX interaction
  var html_return = '<span class="{type}" data-doc_or="{variable_name}">{html}</span>'.assign({ variable_name: var_name, html: html, type: 'doc_or' });
  return new Handlebars.SafeString(html_return);
});