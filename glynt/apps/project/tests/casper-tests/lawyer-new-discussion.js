'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test that the lawyer can add new discussions
 */
helper.scenario(casper.cli.options.url,
	function () {
		/* Test add discussion button */
		casper.waitForSelector(".discussion-list button.widget-title-button", /* + New (button) */
			function success() {
				this.test.assertExists(".discussion-list button.widget-title-button");
				this.click(".discussion-list button.widget-title-button");
			},
			function fail() {
				this.test.assertExists(".discussion-list button.widget-title-button");
			}
		);
	},
	function () {
		/* Wait for dialog to open */
		casper.waitForSelector("form input#discussionSubject",
			function success() {
				helper.snapshotPage.call( this, 0 );
				this.test.assertExists("form input#discussionSubject");
				this.click("form input#discussionSubject");
			},
			function fail() {
				this.test.assertExists("form input#discussionSubject");
			}
		);
	},
	function () {
		/* Test title */
		casper.waitForSelector(".modal-dialog.discussion-modal h3",
			function success() {
				this.test.assertExists(".modal-dialog.discussion-modal h3");
			},
			function fail() {
				this.test.assertExists(".modal-dialog.discussion-modal h3");
			}
		);
	},
	function () {
		/* Add title to form */
		casper.waitForSelector("input#discussionSubject",
			function success() {
				this.sendKeys("input#discussionSubject", "Test title");
			},
			function fail() {
				this.test.assertExists("input#discussionSubject");
			}
		);
	},
	function () {
		/* Add comment to form */
		casper.waitForSelector("textarea#discussionComment",
			function success() {
				this.sendKeys("textarea#discussionComment", "Test message");
			},
			function fail() {
				this.test.assertExists("textarea#discussionComment");
			}
		);
	},
	function () {
		// Submit form
		this.fill('form.form-discussion', {
			'discussionSubject':'Test subject',
			'discussionComment':'Test message'
		}, true);

		/* Wait for success message */
		casper.waitForText("Discussion item saved",
			function success() {
				this.test.assertExists(".comment-column p");
				this.test.assertSelectorHasText('.discussion-list', 'Test subject');
				this.test.assertSelectorHasText('.discussion-list', 'Test message');
			},
			function fail() {
				this.test.assertSelectorHasText('.discussion-list', 'Test subject');
			}
		);
	},
	function () {
		// Test response button
		casper.waitForSelector(".comment-column button.btn-respond",
		    function success() {
		        this.test.assertExists(".comment-column button.btn-respond");
		        this.click(".comment-column button.btn-respond");
		    },
		    function fail() {
		        this.test.assertExists(".comment-column button.btn-respond");
		});
	},
	function () {
		// Test response form
		this.fill('form.form-discussion', {
			'discussionComment':'Test response'
		}, true);
		/* Wait for success message */
		casper.waitForText("Discussion item saved",
			function success() {
				this.test.assertExists(".comment-column p");
				this.test.assertSelectorHasText('.discussion-list', 'Test subject');
				this.test.assertSelectorHasText('.discussion-list', 'Test response'); // Updated discussion content on page
			},
			function fail() {
				this.test.assertTextExists('Discussion item saved');
			}
		);
	},
	function () {
		// Open full view
		casper.waitForSelector(".comment-column",
		    function success() {
		        this.test.assertExists(".comment-column");
		        this.click(".comment-column");
		    },
		    function fail() {
		        this.test.assertExists(".comment-column");
		});
	},
	function () {
		// Check items in full view
		casper.waitForSelector(".full-dialog h3",
		    function success() {
		        this.test.assertExists(".full-dialog h3");
		        this.test.assertSelectorHasText('.full-dialog h3', 'Test subject');	// Subject line
		        this.test.assertSelectorHasText('.full-dialog .comment', 'Test message'); // Original message
		        this.test.assertSelectorHasText('.full-dialog .comment', 'Test response'); // Response message
		        this.click(".full-dialog-toolbar button.btn-primary"); // Close Dialog
		    },
		    function fail() {
		        this.test.assertExists(".comment-column");
		});
	}
	//
);
helper.run();

/*
// submit form
casper.waitForSelector(".discussion-list.ng-isolate-scope h3",
	function success() {
		this.test.assertExists(".discussion-list.ng-isolate-scope h3");
		this.click(".discussion-list.ng-isolate-scope h3");
	},
	function fail() {
		this.test.assertExists(".discussion-list.ng-isolate-scope h3");
});
casper.waitForSelector(".table.table-striped .byme-true:nth-child(1) p:nth-child(1) .ng-binding",
	function success() {
		this.test.assertExists(".table.table-striped .byme-true:nth-child(1) p:nth-child(1) .ng-binding");
		this.click(".table.table-striped .byme-true:nth-child(1) p:nth-child(1) .ng-binding");
	},
	function fail() {
		this.test.assertExists(".table.table-striped .byme-true:nth-child(1) p:nth-child(1) .ng-binding");
});
casper.waitForSelector("form .btn.btn-info.pull-right",
	function success() {
		this.test.assertExists("form .btn.btn-info.pull-right");
		this.click("form .btn.btn-info.pull-right");
	},
	function fail() {
		this.test.assertExists("form .btn.btn-info.pull-right");
});
casper.waitForSelector("#discussionComment",
	function success() {
		this.test.assertExists("#discussionComment");
		this.click("#discussionComment");
	},
	function fail() {
		this.test.assertExists("#discussionComment");
});
casper.waitForSelector("textarea#discussionComment",
	function success() {
		this.sendKeys("textarea#discussionComment", "test response");
	},
	function fail() {
		this.test.assertExists("textarea#discussionComment");
});
casper.waitForSelector("form .form-discussion.ng-dirty.ng-valid.ng-valid-required .btn.btn-primary",
	function success() {
		this.test.assertExists("form .form-discussion.ng-dirty.ng-valid.ng-valid-required .btn.btn-primary");
		this.click("form .form-discussion.ng-dirty.ng-valid.ng-valid-required .btn.btn-primary");
	},
	function fail() {
		this.test.assertExists("form .form-discussion.ng-dirty.ng-valid.ng-valid-required .btn.btn-primary");
});
// submit form

casper.then(function() {
	this.test.comment("Response added");
});

casper.waitForSelector("form .btn.btn-primary.pull-right",
	function success() {
		this.test.assertExists("form .btn.btn-primary.pull-right");
		this.click("form .btn.btn-primary.pull-right");
	},
	function fail() {
		this.test.assertExists("form .btn.btn-primary.pull-right");
});
casper.waitForSelector("#content",
	function success() {
		this.test.assertExists("#content");
		this.click("#content");
	},
	function fail() {
		this.test.assertExists("#content");
});
 */