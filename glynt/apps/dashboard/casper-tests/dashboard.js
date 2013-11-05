casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

helper.scenario(casper.cli.options.url,
    function() {
        // Test existance of core elements
        //this.echo(this.debugHTML())
        //this.test.assertHttpStatus(200);
        this.test.assertTitle('Overview');
        this.test.assertSelectorHasText('h1', 'Your LawPal Projects', 'Header Text on Page');

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
                // Test for company name
                this.test.assertSelectorHasText('.widget.project h3', 'Test Company');
            },
            function fail() {
                this.test.assertExists(".widget.project h3");
        });

        // Proposed state
        casper.waitForSelector(".widget .engagement-proposed",
            function success() {
                this.test.assertExists(".widget .engagement-proposed");
                this.test.assertSelectorHasText('.widget .engagement-proposed', 'Proposed');
            },
            function fail() {
                this.test.assertExists(".widget .engagement-proposed");
        });
    },
    function () {
        // Displays customer name
        casper.waitForSelector(".project-proposed .user-mini-widget h5",
            function success() {
                this.test.assertExists(".project-proposed .user-mini-widget h5");
                this.test.assertSelectorHasText('.project-proposed .user-mini-widget h5', 'Customer A');
            },
            function fail() {
                this.test.assertExists(".project-proposed .user-mini-widget h5");
        });

        // Displays client caption
        casper.waitForSelector(".project-proposed .client",
            function success() {
                this.test.assertExists(".project-proposed .client");
                this.test.assertSelectorHasText('.project-proposed .client', 'Client');
            },
            function fail() {
                this.test.assertExists(".project-proposed .user-mini-widget h5");
        });

        // Displays discussion modal
        casper.waitForSelector(".project a[data-toggle='modal']",
            function success() {
                this.click(".project a[data-toggle='modal']");
            },
            function fail() {
                this.test.assertExists(".project a[data-toggle='modal']");
        });

        // Close modal
        casper.waitForSelector("#overview-modal .close",
            function success() {
                this.test.assertExists("#overview-modal .close");
                this.click("#overview-modal .close");
            },
            function fail() {
                this.test.assertExists("#overview-modal .close");
        });
    }
);

helper.run();