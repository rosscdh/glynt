Handlebars.registerHelper('doc_var', function(context, options) {
  var app = (context.hash.app == undefined) ? window.app : eval('window.'.format(context.hash.app)) ;
  var var_name = '';
  var field_type = 'text';
  if (context.hash.name == undefined || context.hash.name == '') {
    throw 'doc_var requires a "name"';
  } else {
    var_name = context.hash.name;
    app.helper_context[var_name] = context.hash;
  };
  if (context.hash.field_type != undefined && context.hash.field_type == '') {
    field_type = context.hash.field_type;
  }
  // see if this context.name is already defined in the app context (to get user populated data)
  var value = (app.context[var_name] == undefined) ? '_____'.repeat(2) : app.context[var_name] ;
  if (app.context[var_name] == undefined) {
    // set to nul because we know it is undefined; assert positive
    app.context[var_name] = null;
  };
  // wrap the value in our detailed html to allow UX interaction
  var html_return = '<span class="{type} edit" rel="{variable_name}">{value}</span>'.assign({ variable_name: var_name, value: value, type: 'doc_var' });
  // make it safe so hb does not mess with it
  return new Handlebars.SafeString(html_return);
});