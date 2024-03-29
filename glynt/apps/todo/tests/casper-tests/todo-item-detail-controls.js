'use strict';
casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

helper.scenario(casper.cli.options.url,
	function() {
		/* Elements exist */
		//this.echo(this.getHTML());
		this.viewport(1200, 800);
		//helper.snapshotPage.call( this, 0 );
		this.test.assertHttpStatus(200);
		//this.debugHTML();
		//
		casper.waitForSelector('.btn-fullscreen', function() {
            /* Test for Full Screen Button */
			casper.test.comment('Full Screen Button exists');
			this.test.assertSelectorHasText('button', 'Full Screen', 'Full Screen Button exists');

			/* Test for Delete Button */
			casper.test.comment('Delete Button exists');
			this.test.assertSelectorHasText('button', 'Delete', 'Delete Button exists');

			/* Test for Delete Button */
			casper.test.comment('Request Feedback Button exists');
			this.test.assertSelectorHasText('button', 'Request Feedback', 'Request Feedback Button exists');

			/* Iframe exists : #crocdoc-viewer-iframe*/
			casper.test.comment('Request Feedback Button exists');
			this.test.assertExists('iframe#crocdoc-viewer-iframe', 'Crocodoc iframe exists');

			/* File selector exists : h5.list-group-item-heading */
			casper.test.comment('File selector exists');
			this.test.assertExists('h5.list-group-item-heading', 'File selector exists');
        });
	},

	function() {
		/* Full screen button clicked  */
		casper.test.comment('Close Full Screen Button exists');
		this.click('button.btn-fullscreen');

        this.wait(1000, function() {
            this.test.assertSelectorHasText('button', 'Close Full Screen', 'Close Full Screen Button exists');

            casper.test.comment('Close Full Screen Button exists');
            this.click('button.btn-fullscreen');

            this.wait(1000, function() {
                /* Full screen button clicked again */
                this.test.assertSelectorHasText('button', 'Full Screen', 'Full Screen Button exists');
            });
        });
	},

	function() {
		//snapshotPage.call(this,0);
		/* Change item status */
		casper.evaluate(function() {
			// Run script in window session
			window.updateChecklistItemStatus({ "instance": { "status": 0 } });
		});

		this.test.assertSelectorHasText('#checklist_item_status_label', 'New', 'Checklist item status changed');

		casper.evaluate(function() {
			// Run script in window session
			window.updateChecklistItemStatus({ "instance": { "status": 1 } });
		});

		this.test.assertSelectorHasText('#checklist_item_status_label', 'Open', 'Checklist item status changed');
	}
);

helper.run();