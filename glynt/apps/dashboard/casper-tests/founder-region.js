casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test to see if the contact us modal displays.
 */
helper.scenario(casper.cli.options.url,
    function() {
        this.test.comment('Test the addition of a cloned founder region');

        // test the add founder block works
        this.test.assertElementCount('.founder-group', 1);
        this.click('button#btn_add_another');
        casper.test.assertElementCount('.founder-group', 2);
    }
);

helper.run();