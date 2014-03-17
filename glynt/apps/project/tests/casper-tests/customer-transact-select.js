'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test the qualified intake form
 */
helper.scenario(casper.cli.options.url,
    function () {
        this.waitFor(function waitForJQuery() {
            return this.evaluate(function() {
                return typeof(window.$) !== 'undefined';
            });
        });
        this.waitFor(function check() {
            return this.evaluate(function() {
                return document.querySelectorAll('.slide.active').length == 1;
            });
        });
    },
    function () {
        this.test.comment('Test the selection page');

        this.test.assertExists('.slide[data-stage="selection"].active');

        // test validation
        this.click('.slide.active button[type="submit"]');
        this.test.assertExists('.slide[data-stage="selection"].active');

        this.click('input[name="services"][value="incorporation"]');
        this.click('input[name="services"][value="financing"]');
        this.click('input[name="services"][value="intellectual-property"]');
        this.click('.slide.active button[type="submit"]');
    },
    function () {
        this.test.comment('Test the qualification page');

        this.test.assertExists('.slide[data-scene="incorporation"][data-stage="qualification"].active');

        // test validation
        this.click('.slide.active button[type="submit"]');
        this.test.assertExists('.slide[data-scene="incorporation"][data-stage="qualification"].active');

        this.fill('.slide[data-scene="incorporation"][data-stage="qualification"] form', {
            'company_founders': 3,
            'company_founders_location': 'inside',
            'company_incorporated': 'no',
            'company_paperwork': 'no'
        });

        this.click('.slide.active button[type="submit"]');
    },
    function () {
        this.test.comment('Test the incorporation services page');

        this.test.assertExists('.slide[data-scene="incorporation"][data-stage="services"].active');
        this.test.assertExists('.slide.active input[type="submit"]#submit-btn-CS');
        this.test.assertExists('.slide.active input[type="submit"]#submit-btn-CSP');

        this.click('.slide.active input[type="submit"]#submit-btn-CS');
    },
    function () {
        this.test.comment('Test the financing services page');

        this.test.assertExists('.slide[data-scene="financing"][data-stage="services"].active');
        this.test.assertExists('.slide.active input[type="submit"]#submit-btn-SF');
        this.test.assertExists('.slide.active input[type="submit"]#submit-btn-ES');

        this.click('.slide.active input[type="submit"]#submit-btn-ES');
    },
    function () {
        this.test.comment('Test the redirect after project creation');

        this.waitForUrl(/dashboard/, function success() {
            this.test.assertUrlMatch(/dashboard/);
        });
    }
);

/**
 * Test the unqualified intake form
 */
helper.scenario(casper.cli.options.url,
    function () {
        this.waitFor(function check() {
            return this.evaluate(function() {
                return document.querySelectorAll('.slide.active').length == 1;
            });
        });
    },
    function () {
        this.test.comment('Test the selection page');

        this.test.assertExists('.slide[data-stage="selection"].active');

        // test validation
        this.click('.slide.active button[type="submit"]');
        this.test.assertExists('.slide[data-stage="selection"].active');

        this.click('input[name="services"][value="incorporation"]');
        this.click('input[name="services"][value="financing"]');
        this.click('input[name="services"][value="intellectual-property"]');
        this.click('.slide.active button[type="submit"]');
    },
    function () {
        this.test.comment('Test the qualification page');

        this.test.assertExists('.slide[data-scene="incorporation"][data-stage="qualification"].active');

        // test validation
        this.click('.slide.active button[type="submit"]');
        this.test.assertExists('.slide[data-scene="incorporation"][data-stage="qualification"].active');

        this.fill('.slide[data-scene="incorporation"][data-stage="qualification"] form', {
            'company_founders': 4,
            'company_founders_location': 'outside',
            'company_incorporated': 'yes',
            'company_paperwork': 'yes'
        });

        this.click('.slide.active button[type="submit"]');
    },
    function () {
        this.test.comment('Test the redirect after project creation');

        this.waitForUrl(/dashboard/, function success() {
            this.test.assertUrlMatch(/dashboard/);
        });
    }
);

helper.run();