$(document).ready(function(){
    app = $.sammy(function() {
        var self = this;

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
        };

        self.init = function init() {
            $.getScript("{{ STATIC_URL }}js/smooth.js")
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
    app.run('#/');
});