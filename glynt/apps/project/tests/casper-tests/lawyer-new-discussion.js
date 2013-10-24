'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test that the lawyer can add new discussions
 */
helper.scenario(casper.cli.options.url,
	function () {
		/* Test add discussion button */
		casper.waitForSelector(".discussion-list button.widget-title-button",
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
		casper.waitForSelector("form.form-discussion .btn.btn-primary",
			function success() {
				helper.snapshotPage.call( this, 1 );
				this.test.assertExists("form.form-discussion .btn.btn-primary");
				this.fill('form.form-discussion', {
					'discussionSubject':'Test subject',
					'discussionComment':'Test message'
				}, true);
			},
			function fail() {
				this.test.assertExists("form.form-discussion .btn.btn-primary");
			}
		);
	}
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