'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test that the lawyer can manage a projects team
 */
helper.scenario(casper.cli.options.url,
    function () {
        var self = this;
    }
);
helper.run();