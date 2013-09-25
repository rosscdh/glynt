casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

helper.scenario(casper.cli.options.url,
    function() {
        //this.echo(this.getHTML());
        this.test.assertHttpStatus(200);
        this.debugHTML();
        this.test.assertTitle('Overview')
        this.test.assertSelectorHasText('h1', 'Your LawPal Projects', 'Header Text on Page')
    }
);

helper.run();