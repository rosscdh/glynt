casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

helper.scenario(casper.cli.options.url,
    function() {
        // Test existance of core elements
        //this.echo(this.debugHTML())
        this.test.assertHttpStatus(200);
        this.test.assertTitle('Overview');
        this.test.assertSelectorHasText('h1', 'Your LawPal Projects', 'Header Text on Page');

        helper.capturePageTimelapse( 5 );

        // Widget exists
        casper.waitForSelector(".widget.project",
            function success() {
                this.test.assertExists(".widget.project");
                // Need to test for company name
            },
            function fail() {
                this.test.assertExists(".widget.project");
        });

        // Widget heading
        casper.waitForSelector(".widget.project h3",
            function success() {
                this.test.assertExists(".widget.project h3");
                // Need to test for company name
            },
            function fail() {
                this.test.assertExists(".widget.project h3");
        });

        // Proposed state
        casper.waitForSelector(".widget .engagement-engaged",
            function success() {
                this.test.assertExists(".widget .engagement-engaged");
                this.test.assertSelectorHasText('.widget .engagement-engaged', 'Engaged');
            },
            function fail() {
                this.test.assertExists(".widget .engagement-engaged");
        });

        // Primary action displayed
        casper.waitForSelector(".project-engaged .btn-new",
            function success() {
                this.test.assertExists(".project-engaged .btn-new");
                this.test.assertSelectorHasText('.project-engaged .btn-new', 'New');
            },
            function fail() {
                this.test.assertExists(".project-engaged .btn-new");
        });

        // View link
        casper.waitForSelector(".project-engaged a",
            function success() {
                this.test.assertExists(".project-engaged a");
                this.test.assertSelectorHasText('.project-engaged a', 'View');
            },
            function fail() {
                this.test.assertExists(".project-engaged a");
        });

        // Displays discussion modal
        casper.waitForSelector(".project-engaged button.start-discussion",
            function success() {
                this.click(".project-engaged button.start-discussion");
            },
            function fail() {
                this.test.assertExists(".project-engaged button.start-discussion");
        });

        // Close modal
        casper.waitForSelector("form.form-discussion .btn-default",
            function success() {
                this.test.assertExists("form.form-discussion .btn-default");
                this.click("form.form-discussion .btn-default"); // Cancel
            },
            function fail() {
                this.test.assertExists("form.form-discussion .btn-default");
        });
    }
);

helper.run();