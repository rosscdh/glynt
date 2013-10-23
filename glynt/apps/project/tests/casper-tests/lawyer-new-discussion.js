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
		});
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
		});
	},
	function () {
		/* Test title */
		casper.waitForSelector(".modal-dialog.discussion-modal.ng-scope h3",
			function success() {
				this.test.assertExists(".modal-dialog.discussion-modal.ng-scope h3");
			},
			function fail() {
				this.test.assertExists(".modal-dialog.discussion-modal.ng-scope h3");
		});
	},
	function () {
		/* Add title to form */
		casper.waitForSelector("input#discussionSubject",
			function success() {
				this.sendKeys("input#discussionSubject", "Test title");
			},
			function fail() {
				this.test.assertExists("input#discussionSubject");
		});
	},
	function () {
		/* Add comment to form */
		casper.waitForSelector("textarea#discussionComment",
			function success() {
				this.sendKeys("textarea#discussionComment", "Test message");
			},
			function fail() {
				this.test.assertExists("textarea#discussionComment");
		});
	},
	function () {
		// Submit form
		casper.waitForSelector(".modal form .btn.btn-primary",
			function success() {
				helper.snapshotPage.call( this, 1 );
				this.test.assertExists(".modal form .btn.btn-primary");
				this.click(".modal form .btn.btn-primary");
			},
			function fail() {
				this.test.assertExists(".modal form .btn.btn-primary");
		});
	}
);
helper.run();