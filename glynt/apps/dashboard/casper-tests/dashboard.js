casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

helper.scenario('/dashboard/',
    function() {
        this.echo(this.getHTML());
        this.test.assertHttpStatus(200);
        this.test.assertTitle('Dashboard')
        this.test.assertSelectorHasText('h1', 'Your LawPal Projects', 'Header Text on Page')
        this.test.assertExists('ul#project-list')
        this.test.assertExists('a#Intercom')
        this.test.assertExists('div.proposed', 'Should be Proposed')
        this.test.assertSelectorHasText('div.proposed p.msg', 'You have been proposed to this client. Awaiting client decision.', 'Contains msg element')
    }
);

helper.run();