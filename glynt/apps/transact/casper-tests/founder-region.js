casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

var btn_add_another_founders = 'fieldset[data-region-name="founders"] button#founders_add_another';

/**
 * Test to see if the founder region works.
 */
helper.scenario(casper.cli.options.url,
    function() {
        this.test.comment('Test the addition of a cloned founder region');

        this.test.assertElementCount('div.founder-group', 1);
        this.test.assertElementCount('button.delete-cloned-region', 0);

        this.click(btn_add_another_founders);
        this.test.assertElementCount('div.founder-group', 2);
        this.test.assertElementCount('button.delete-cloned-region', 1);

        this.click(btn_add_another_founders);
        this.test.assertElementCount('div.founder-group', 3);
        this.test.assertElementCount('button.delete-cloned-region', 2);

        this.echo(this.getHTML())
    }
);

helper.scenario(casper.cli.options.url,
    function() {
        this.test.comment('Test the removal of a cloned founder region');

        this.click(btn_add_another_founders);
        this.click(btn_add_another_founders);

        this.test.assertElementCount('div.founder-group', 3);
        this.test.assertElementCount('button.delete-cloned-region', 2);

        this.click('button.delete-cloned-region:first-child');
        this.test.assertElementCount('div.founder-group', 2);
        this.test.assertElementCount('button.delete-cloned-region', 1);

        this.click('button.delete-cloned-region:first-child');
        this.test.assertElementCount('div.founder-group', 1);
        this.test.assertElementCount('button.delete-cloned-region', 0);
    }
);


helper.run();