$(document).ready(function(){
    orGroup = function orGroup(params) {
        var self = this;
        this.name = params.name;
        this.current = params.current;
        this.items = params.items;
        this.length = params.items.length;
        this.add_item = function add_item(item) {
            self.items.add(item);
            self.length = self.items.length;
        }
    };

    window.app = $.sammy(function() {
        var self = this;
        self.default_data = $.parseJSON($('script#document-default_data').html());
        self.context = {};
        self.helper_context = {
            'or_groups': {}
        };
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
          self.dispatch('handle_doc_or', {});
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

            if (self.context[doc_var] === undefined) {
                self.context[doc_var] = null;
            };

            if (self.context[doc_var] != doc_var_value) {
                update_fields = true;    
            };

            self.context[doc_var] = doc_var_value;

            if (update_fields) {
                $.each($('[data-doc_var="'+ doc_var +'"]'), function(index, element){
                    if (notify_user) { $(element).fadeOut('fast'); };
                    $(element).html(self.context[doc_var]);
                    if (notify_user) { $(element).fadeIn('fast'); };
                });
            };
        };
        self.handle_doc_or = function handle_doc_or() {
            // loop over ors and ensure only 1 is showing at one time
            // ensure that the appropriate one is handled and displayed 
            // from user selected data
            var found = Object.merge(self.helper_context.or_groups, {});
            $.each($('[data-doc_or]'), function(index, element) { 
                var e = $(element);
                var doc_group = e.attr('data-doc_or');
                if ((Object.has(found, doc_group)) == false) {
                    e.show();
                    found[doc_group] = new orGroup({name: doc_group, current: index, items: [e]});
                } else {
                    e.hide();
                    found[doc_group].add_item(e);
                };
            });
            self.helper_context.or_groups = Object.merge(self.helper_context.or_groups, found);
            // when we want to replace the current doc or value use
            // $('#document').find('[data-doc_or=group_1]').html($(app.helper_context.or_groups.group_1.items[1]).html());
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
            $.each($('[data-has_initial=true]'), function(index, element){
                var doc_var_name = $(this).attr('data-doc_var')
                var doc_val = $(this).html();
                self.dispatch('bind_data', {'doc_var': doc_var_name, 'value': doc_val, 'notify': false});
            });

        };

        self.init = function init() {
            // setup the data from defaults
            self.setup_data();

            // load the smooth helpers
            $.getScript("{{ STATIC_URL }}js/smoothe.js")
            .done(function(script, textStatus) {
                // register callbacks
                self.registerCallback('bind_data', self.bind_data);
                self.registerCallback('handle_doc_or', self.handle_doc_or);

                // output html so we can bind events
                self.render();
                // bind events
                self.init_interface();
            })
            .fail(function(jqxhr, settings, exception) {
                console.log('could not load smoothe.js, there will be no document!');
                console.log(jqxhr);
                console.log(settings);
                console.log(exception);
            });
        };

       self.init();
    });

    // start the application
    window.app.run('#/');
});

