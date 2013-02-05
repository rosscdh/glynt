{% load i18n %}
$(document).ready(function(){

    window.app = $.sammy(function() {
        var self = this;
        self.default_data = null;
        self.document_data = null;

        self.context = {
            'progress': null,
            'help': {},
            'notes': {}
        };
        self.helper_context = {};

        // ---- OBSERVER -----
        self.observer = new argosPanOptia();
        self.markdownConverter = new Markdown.Converter();
        self.message = new GlyntMessage({});

        self.views = $('div.view');
        self.nav = $('ul.nav-list li a');

        self.doc_view = Handlebars.compile($('script#document-hb').html());

        Handlebars.registerPartial("toggle-partial", Handlebars.compile($("script#toggle-partial").html()));
        Handlebars.registerPartial("incrementor-partial", Handlebars.compile($("script#incrementor-partial").html()));

        Handlebars.registerPartial("doc_var-partial", Handlebars.compile($("script#doc_var-partial").html()));
        Handlebars.registerPartial("doc_select-partial", Handlebars.compile($("script#doc_select-partial").html()));
        Handlebars.registerPartial("doc_select-selecta-partial", Handlebars.compile($("script#doc_select-selecta-partial").html()));
        Handlebars.registerPartial("doc_choice-partial", Handlebars.compile($("script#doc_choice-partial").html()));
        Handlebars.registerPartial("doc_note-partial", Handlebars.compile($("script#doc_note-partial").html()));

        // ---- VIEWS -----
        this.notFound = function(){
        };
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
            if ($('div#sidebar').length > 0) {
                $('div#sidebar').height($('div#document').height());
                $('div#sidebar').css('top', $('div.navbar').position().top + $('div.navbar').height());
            }
            if ($('ul#glynt_progress').length > 0) {
                // $('ul#glynt_progress').height($('div#document').height());
            }
        };
        self.render_doc = function render_steps() {
            if ($("div#document").length > 0) {
                $("div#document").html(self.renderMarkdown(self.doc_view({})));
            } else {
                console.log('Can not output to undefined div#document')
            }
        };
        self.renderMarkdown = function renderMarkdown(md) {
          return self.markdownConverter.makeHtml(md);
        };

        self.setup_data = function setup_data(params) {
            var data = $('script#document-document_data').html();
            if (data == null || data == '') {
                data = "{}";
            }
            self.document_data = $.parseJSON(data);
        };

        // ---- BIND METHODS -----
        self.bind_data = function bind_data(data){
            var update_fields = false;
            var notify_user = (data.notify == undefined) ? true: data.notify;
            var doc_var = data.doc_var;
            var doc_var_value = data.value;

            if (self.context[doc_var].value != doc_var_value) {
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
            if (self.document_data !== null) {
                $.each(self.context, function(key, item){
                    if (item && self.document_data[key]) {
                        self.dispatch('bind_data', {'doc_var': key, 'value': self.document_data[key], 'notify': false});
                    }
                });
            }

            $('.edit').glynt_edit();
            $('.doc_select').glynt_select({});
            $('.doc_choice').glynt_choice({target_element: $('#element_help_text')});
            $('.note').glynt_note({target_element: $('#element_help_text')});
            $('body').help_text({target_element: $('#element_help_text')});
            $('body').glynt_progress();

            $('form#document-form button.submit').on('click', function(event){
                event.preventDefault();
                var button = $(this);
                button.show();
                var offset = button.closest('form').offset();
                button.toggle();

                var data = {
                    csrfmiddlewaretoken: "{{ csrf_raw_token }}"
                };
                // extract just the value from context
                $.each(self.context, function(index, item) {
                    if (item.type == 'doc_select') {
                        var select_item = []
                        // extract the item index and its selected value
                        $.each(item.select_options, function(i,item){
                            select_item.push({
                                'selected': item.selected
                                ,'index': item.index
                            });
                        });
                        data[item.name] = select_item;
                    } else {
                        data[item.name] = item.value;
                    }
                });

                $.ajax({
                    type: 'POST'
                    ,url: $(this).closest('form').attr('href')
                    ,contentType : 'application/json'
                    ,data: data
                })
                .success(function(data, textStatus, jqXHR) {
                    if (window.location.pathname !== data.url) {
                        document.location = data.url;
                    }else{
                        // congrats maybe show a message?
                        self.message.place(offset).show('{% trans "Updated your Document" %}');
                    }
                })
                .error(function(jqXHR, textStatus, errorThrown) {
                    var data = $.parseJSON(jqXHR.responseText);
                    // oh oh maybe show a message?
                    self.message.place(button.offset()).show_error(data.errors);
                })
                .complete(function(jqXHR, textStatus, errorThrown) {
                    button.toggle();
                });
            });
        };

        self.init = function init() {

            // load the smooth helpers
            $.getScript("{{ STATIC_URL }}smoothe/js/smoothe.js")
            .done(function(script, textStatus) {
                $.getScript("{{ STATIC_URL }}smoothe/js/jquery.plugins.js")
                .done(function(script, textStatus) {
                    // initialize
                    self.setup_data();
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

