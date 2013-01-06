$(document).ready(function(){

    window.app = $.sammy(function() {
        var self = this;
        self.default_data = null;

        self.context = {
            'progress': null,
            'help': {},
            'notes': {}
        };
        self.helper_context = {};

        // ---- OBSERVER -----
        self.observer = new argosPanOptia();

        self.views = $('div.view');
        self.nav = $('ul.nav-list li a');

        self.doc_view = null;

        Handlebars.registerPartial("toggle-partial", Handlebars.compile($("script#toggle-partial").html()));
        Handlebars.registerPartial("doc_var-partial", Handlebars.compile($("script#doc_var-partial").html()));
        Handlebars.registerPartial("doc_select-partial", Handlebars.compile($("script#doc_select-partial").html()));
        Handlebars.registerPartial("doc_select-selecta-partial", Handlebars.compile($("script#doc_select-selecta-partial").html()));
        Handlebars.registerPartial("doc_choice-partial", Handlebars.compile($("script#doc_choice-partial").html()));
        Handlebars.registerPartial("doc_note-partial", Handlebars.compile($("script#doc_note-partial").html()));

        // ---- VIEWS -----
        this.get('#/', function() {
        });


        // ---- CONTEXT MODIFIERS -----
        self.instance_count = function instance_count(options, var_name) {
            // method increments the instance count of each variable
            // for use in the progress meter
            if (!self.context[var_name]) {
                options.hash.instance_count = 1;
            } else {
                self.context[var_name].instance_count++;
                options.hash.instance_count = self.context[var_name].instance_count;// = options.hash.instance_count+1;
            }
            return options;
        }

        // ---- RENDER VIEWS -----
        self.render = function render() {
            if ($("div#document").length > 0) {
                self.doc_view = self.get_doc_view();
                $("div#document").html(self.doc_view({}));
            } else {
                console.log('Can not output to undefined div#document')
            }
        };

        self.get_doc_view = function get_doc_view() {
            return Handlebars.compile($('#id_body').val());
        }
        self.get_default_data = function get_default_data() {
            return {};
        };

        self.setup_data = function setup_data() {
            self.default_data = self.get_default_data();
            self.context = Object.merge(self.default_data, self.context);
        };

        // ---- BIND METHODS -----
        self.bind_data = function bind_data(data){
            var update_fields = false;
            var notify_user = (data.notify == undefined) ? true: data.notify;
            var doc_var = data.doc_var;
            var doc_var_value = data.value;

            if (self.context[doc_var] != doc_var_value) {
                update_fields = true; 
            };

            self.context[doc_var].value = doc_var_value;

            if (update_fields) {
                $.each($('[data-doc_var="'+ doc_var +'"]'), function(index, element){
                    if (notify_user) { $(element).fadeOut('fast'); };
                    // set all elements related to this field to have the new updated value
                    $(element).html(self.context[doc_var].value);
                    if (notify_user) { $(element).fadeIn('fast'); };
                });
            };
        };

        // ---- DISPATCH -----
        self.registerCallback = function registerCallback(event_name, callback) {
          self.observer.registerCallback(event_name, callback);
        };
        self.dispatch = function dispatch(event_name, value) {
          self.observer.dispatch(event_name, value);
        };

        // ---- INTERFACE EVENTS -----
        self.listen = function listen() {
            /**
            * Setup the editable items
            */
            $.each($('[data-has_initial=true]'), function(index, element){
                self.dispatch('bind_data', {'doc_var': $(this).attr('data-doc_var'), 'value': $(this).html(), 'notify': false});
            });

            $('.edit').glynt_edit();
            $('.doc_select').glynt_select({});
            $('.doc_choice').glynt_choice({target_element: $('#element_help_text')});
            $('.note').glynt_note({target_element: $('#element_help_text')});
            $('body').help_text({target_element: $('#element_help_text')});
            $('body').glynt_progress({in_admin: true});

            $('#id_body').on('change', function(event){
                self.render();
            });
        };

        self.init = function init() {
            // setup the data from defaults
            self.setup_data();

            // load the smooth helpers
            $.getScript("{{ STATIC_URL }}smoothe/js/smoothe.js")
            .done(function(script, textStatus) {
                $.getScript("{{ STATIC_URL }}smoothe/js/jquery.plugins.js")
                .done(function(script, textStatus) {
                    // register callbacks
                    self.registerCallback('bind_data', self.bind_data);

                    // output html so we can bind events
                    self.render();

                    // bind events
                    self.listen();
                })
                .fail(function(jqxhr, settings, exception) {
                    console.log('Could not load jquery.plugins.js, {exception}'.assign({'exception': exception}));
                });
            })
            .fail(function(jqxhr, settings, exception) {
                console.log('Could not load smoothe.js, {exception}'.assign({'exception': exception}));
            });
        };

       self.init();
    });

    // start the application
    window.app.run('#/');
});

