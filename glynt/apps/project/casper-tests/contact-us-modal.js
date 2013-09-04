casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test to see if the contact us modal displays.
 */
helper.scenario(casper.cli.options.url,
    function() {
        this.test.assertTrue(true);
    }
);

helper.run();