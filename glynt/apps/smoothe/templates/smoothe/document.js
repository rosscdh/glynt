$(document).ready(function(){

    window.app = $.sammy(function() {
        var self = this;
        self.default_data = $.parseJSON($('script#document-default_data').html());
        self.context = {
            'progress': null,
            'help': {},
            'notes': {}
        };
        self.helper_context = {
            'or_groups': {}
        };
        // ---- OBSERVER -----
        self.observer = new argosPanOptia();

        self.views = $('div.view');
        self.nav = $('ul.nav-list li a');

        self.doc_view = Handlebars.compile($('script#document-hb').html());

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
          self.render_doc();
          $('div#sidebar').height($('div#document').height());
          $('div#sidebar').css('top', $('div.navbar').position().top + $('div.navbar').height());
          $('ul#glynt_progress').height($('div#document').height());
        };
        self.render_doc = function render_steps() {
          $( "div#document" ).html(self.doc_view({}));
        };

        self.setup_data = function setup_data() {
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
            $('body').glynt_progress();

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

