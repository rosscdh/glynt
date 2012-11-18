$(document).ready(function(){
    window.app = $.sammy(function() {
        var self = this;
        self.context = {};
        self.helper_context = {};
        // ---- OBSERVER -----
        self.observer = new argosPanOptia();

        self.views = $('div.view');
        self.nav = $('ul.nav-list li a');

        self.doc_view = Handlebars.compile($('script#document-hb').html());

        // ---- VIEWS -----
        this.get('#/', function() {
        });

        // ---- RENDER VIEWS -----
        self.render = function render() {
          self.render_doc();
        };
        self.render_doc = function render_steps() {
          $( "div#document" ).html(self.doc_view({}));
        };

        // ---- BIND METHODS -----
        self.bind_data = function bind_data(data){
            var update_fields = false;
            var doc_var = data.doc_var;
            var doc_var_value = data.value;

            if (self.context[doc_var] === undefined) {
                self.context[doc_var] = null;
            };

            if (self.context[doc_var] != doc_var_value) {
                update_fields = true;    
            };

            self.context[doc_var] = doc_var_value;

            if (update_fields) {
                $.each($('[data-doc_var="'+ doc_var +'"]'), function(index, element){
                    $(element).fadeOut('fast');
                    $(element).html(self.context[doc_var]);
                    $(element).fadeIn('fast');
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
        self.init_interface = function init_interface() {
            /**
            * Setup the editable items
            */
            $('.edit').hallo({
                plugins: {
                    'halloformat': {}
                },
                editable: true,
                showAlways: true
            });

            $('.edit').live('blur', function(event){
                var doc_var_name = $(this).attr('data-doc_var')
                var doc_val = $(this).html();
                self.dispatch('bind_data', {'doc_var': doc_var_name, 'value': doc_val});
            });

        };

        self.init = function init() {
            // load the smooth helpers
            $.getScript("{{ STATIC_URL }}js/smoothe.js")
            .done(function(script, textStatus) {
                // register callbacks
                self.registerCallback('bind_data', self.bind_data);

                // output html so we can bind events
                self.render();
                // bind events
                self.init_interface();
            })
            .fail(function(jqxhr, settings, exception) {
                console.log('could not load smoothe.js, there will be no document!');
            });
        };

       self.init();
    });

    // start the application
    window.app.run('#/');
});

