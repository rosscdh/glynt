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

        // ---- RENDER VIEWS -----
        this.get('#/', function() {
        });

        // ---- RENDER VIEWS -----
        self.render = function render() {
          self.render_doc();
        };
        self.render_doc = function render_steps() {
          $( "div#document" ).html(self.doc_view({}));
        };

        self.init_interface = function init_interface() {
            $('.edit').hallo({});
            console.log($('.edit'))
            $('.edit').bind('hallomodified', function(event, data) {
            console.log(data)
            });
        };

        self.init = function init() {
            $.getScript("{{ STATIC_URL }}js/smoothe.js")
            .done(function(script, textStatus) {
                self.init_interface();
                self.render();
            })
            .fail(function(jqxhr, settings, exception) {
                alert('could not load smoothe.js, there will be no document!');
            });
        };

       self.init();
    });

    // start the application
    window.app.run('#/');
});

