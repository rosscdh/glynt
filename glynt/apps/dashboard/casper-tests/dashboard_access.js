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
    },
    function() {
        // Test discussions
        // Start discussion
        casper.waitForSelector(".discussion-list button.start-discussion",
            function success() {
                this.test.assertExists(".discussion-list button.start-discussion");
                this.click(".discussion-list button.start-discussion");
            },
            function fail() {
                this.test.assertExists(".discussion-list button.start-discussion");
        });

        // Enter data
        // Subject
        casper.waitForSelector("form input[name='discussionSubject']",
            function success() {
                this.test.assertExists("form input[name='discussionSubject']");
                this.click("form input[name='discussionSubject']");
            },
            function fail() {
                this.test.assertExists("form input[name='discussionSubject']");
        });

        casper.waitForSelector("input[name='discussionSubject']",
            function success() {
                this.sendKeys("input[name='discussionSubject']", "Test subject");
            },
            function fail() {
                this.test.assertExists("input[name='discussionSubject']");
        });

        // Message
        casper.waitForSelector("#discussionComment",
            function success() {
                this.test.assertExists("#discussionComment");
                this.click("#discussionComment");
            },
            function fail() {
                this.test.assertExists("#discussionComment");
        });
        casper.waitForSelector("textarea[name='discussionComment']",
            function success() {
                this.sendKeys("textarea[name='discussionComment']", "Test message");
            },
            function fail() {
                this.test.assertExists("textarea[name='discussionComment']");
        });

        // Submit form
        casper.waitForSelector(".form-discussion .btn-primary",
            function success() {
                this.test.assertExists(".form-discussion .btn-primary");
                this.click(".form-discussion .btn-primary");
            },
            function fail() {
                this.test.assertExists(".form-discussion .btn-primary");
        });
        

        // Check text has been added
        casper.waitForSelector(".discussion-item .discussion-title",
            function success() {
                // Subject
                this.test.assertExists(".discussion-item .discussion-title");
                this.test.assertSelectorHasText('.discussion-item .discussion-title', 'Test subject');

                // Comment
                this.test.assertExists(".discussion-item .discussion-comment");
                this.test.assertSelectorHasText('.discussion-item .discussion-comment', 'Test message');
                this.click(".discussion-item .discussion-comment"); // Open discussion
            },
            function fail() {
                this.test.assertExists(".discussion-item .discussion-comment");
        });

        // Test item is displayed
        casper.waitForSelector("#discussionComment",
            function success() {
                this.test.assertExists("#discussionComment");
                this.click("#discussionComment");
            },
            function fail() {
                this.test.assertExists("#discussionComment");
        });

        // Test response
        casper.waitForSelector("textarea[name='discussionComment']",
            function success() {
                this.sendKeys("textarea[name='discussionComment']", "Test response A");
            },
            function fail() {
                this.test.assertExists("textarea[name='discussionComment']");
        });

        // Submit response
        casper.waitForSelector(".form-discussion [type='submit']",
            function success() {
                // Subject
                this.test.assertExists(".form-discussion [type='submit']");
                this.click(".form-discussion [type='submit']"); // Open discussion
            },
            function fail() {
                this.test.assertExists(".form-discussion [type='submit']");
        });        
    },
    function() {
        // Submit response
        casper.waitForSelector(".discussion-item .discussion-title",
            function success() {
                // Subject
                this.test.assertExists(".discussion-item .discussion-title");
                this.test.assertSelectorHasText('.discussion-item .discussion-comment', 'Test response A');
            },
            function fail() {
                this.test.assertExists(".discussion-item .discussion-title");
        });
    }
);

helper.run();