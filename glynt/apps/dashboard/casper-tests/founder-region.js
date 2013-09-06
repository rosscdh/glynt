casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test to see if the founder region works.
 */
helper.scenario(casper.cli.options.url,
    function() {
        this.test.comment('Test the addition of a cloned founder region');

        this.test.assertElementCount('.founder-group', 1);
        this.test.assertElementCount('button.delete-cloned-region', 0);

        this.click('button#btn_add_another');
        this.test.assertElementCount('.founder-group', 2);
        this.test.assertElementCount('button.delete-cloned-region', 1);

        this.click('button#btn_add_another');
        this.test.assertElementCount('.founder-group', 3);
        this.test.assertElementCount('button.delete-cloned-region', 2);
    }
);

helper.scenario(casper.cli.options.url,
    function() {
        this.test.comment('Test the removal of a cloned founder region');

        this.click('button#btn_add_another');
        this.click('button#btn_add_another');

        this.test.assertElementCount('.founder-group', 3);
        this.test.assertElementCount('button.delete-cloned-region', 2);

        this.click('button.delete-cloned-region:first-child');
        this.test.assertElementCount('.founder-group', 2);
        this.test.assertElementCount('button.delete-cloned-region', 1);

        this.click('button.delete-cloned-region:first-child');
        this.test.assertElementCount('.founder-group', 1);
        this.test.assertElementCount('button.delete-cloned-region', 0);
    }
);

helper.run();