'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test that the lawyer can manage a projects team
 */
helper.scenario(casper.cli.options.url,
	function () {
		/* Test elements exist */
		this.test.assertSelectorHasText('h3', 'Project team');
		this.test.assertSelectorHasText('button', 'Manage team');
	},
	function () {
		/* Test for dynamic data */
		casper.waitForSelector('.vcard span', function() {
			this.test.assertSelectorHasText('.vcard h3', 'LA');
		});
	},
	function () {
		/* Test for profile: modal dialog */
		this.click('button.role-lawyer');
		casper.waitForSelector('.modal .profile-details', function() {
			this.test.assertSelectorHasText('.modal h1', 'Lawyer A');
			this.test.assertExists('.modal .btn-success');
			this.test.assertExists('.modal .btn-primary'); /* Close button */
			this.click('.modal .btn-primary');

			/* Account manager role */
			/*
			this.click('button.role-account');
			casper.waitForSelector('.modal .profile-details', function() {
				this.test.assertSelectorHasText('.modal h1', 'Yael Citro');
				this.test.assertNotVisible('.modal .btn-success');
				this.test.assertExists('.modal .btn-primary'); // Close button
				this.click('.modal .btn-primary');
			});
			*/
		});
	},
	function () {
		/* Edit team dialog: Add team member */
		this.click('div.widget.project-team button.widget-title-button');
		casper.waitForSelector('.modal h3', function() {
			/* Wait for modal to drop down */
			casper.wait(1000, function() {
			    this.test.assertSelectorHasText('.modal h3', 'Project team');
				this.test.assertSelectorHasText('.modal .form-search button', 'Add to project');
				this.test.assertExists('.modal .modal-footer button.btn-default'); /* Close button */
				this.fill('div.modal form', {
	                email: "lin"
	            }, false);

	            /* Wait for search results */
	            casper.wait(1000, function() {
	            	/* Test type ahead */
				    this.test.assertExists('.modal ul.typeahead');
				    /* Select user */
				    this.click('.modal ul.typeahead li');
				    /* Add to team */
				    this.click('.modal form button.btn-default');
				    /* Check it's been added */
				    this.test.assertSelectorHasText('.modal .vcard .fn', 'Linda Russo');
				    /* Save changes */
				    this.click('.modal .btn-primary');
				    /* Check She has been added to team */
				    this.test.assertSelectorHasText('.vcard h3', 'LR');
				});

				
			});
		});
	},
	function () {
		/* Edit team dialog: remove team member team */
		this.click('div.widget.project-team button.widget-title-button');
		casper.waitForSelector('.modal h3', function() {
			/* Wait for modal to drop down */
			casper.wait(1000, function() {
			    this.test.assertSelectorHasText('.modal h3', 'Project team');
				this.test.assertSelectorHasText('.modal .form-search button', 'Add to project');
				this.test.assertExists('.modal .modal-footer button.btn-default'); /* Close button */
				/* Click remove link */
				this.click('.modal .user-linda-russo a.remove-link');

	            /* Wait for angular data sync */
	            casper.wait(200, function() {
				    /* Save changes */
				    this.click('.modal .btn-primary');
				    /* Check She has been removed from team */
				    this.test.assertSelectorDoesntHaveText('.vcard h3', 'LR');
				});

				
			});
		});
	}
);
helper.run();