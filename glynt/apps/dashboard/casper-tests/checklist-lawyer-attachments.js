casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,
    function() {
        'use strict';
        /* Open checlist item */
        casper.waitForSelector('.checklist .item:first-child td:first-child',
            function success() {
                this.test.assertExists('.checklist .item:first-child td:first-child');
                this.click('.checklist .item:first-child td:first-child');
            },
            function fail() {
                this.test.assertExists('.checklist .item:first-child td:first-child');
        });
    },
    function() {
        'use strict';
        /* Open attachment */
        casper.waitForSelector('.attachment-list li:first-child a',
            function success() {
                this.test.assertExists('.attachment-list li:first-child a');
                this.click('.attachment-list li:first-child a');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('..attachment-list li:first-child a');
        });
    },
    function() {
        'use strict';
        /* Attachment alert */
        casper.waitForSelector('.full-dialog .alert-warning',
            function success() {
                this.test.assertExists('.full-dialog .alert-warning');
                this.test.assertSelectorHasText('.full-dialog .alert-warning', 'What are your thoughts on this test...', 'Message exists');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.full-dialog .alert-warning');
        });
    },
    function() {
        'use strict';
        /* Respond button */
        casper.waitForSelector('.full-dialog .alert-warning button',
            function success() {
                this.test.assertExists('.full-dialog .alert-warning button');
                this.test.assertSelectorHasText('.full-dialog .alert-warning button', 'Respond now', 'Button exists');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.full-dialog .alert-warning button');
        });
    },
    function() {
        'use strict';
        /* Delete attachment */
        casper.waitForSelector('.full-dialog .delete-attachment-button',
            function success() {
                this.test.assertExists('.full-dialog .delete-attachment-button');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.full-dialog .delete-attachment-button');
        });
    },
    function() {
        'use strict';
        /* Close button */
        casper.waitForSelector('.full-dialog .close-button',
            function success() {
                this.test.assertExists('.full-dialog .close-button');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.full-dialog .close-button');
        });
    },
    function() {
        'use strict';
        /* Document Iframe */
        casper.waitForSelector('iframe[src="/todo/attachment/1/crocdoc/"]',
            function success() {
                this.test.assertExists('iframe[src="/todo/attachment/1/crocdoc/"]');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('iframe[src="/todo/attachment/1/crocdoc/"]');
        });
    },
    function() {
        'use strict';
        /* Open feedback dialog */
        casper.waitForSelector('.full-dialog button.respond-now',
            function success() {
                this.test.assertExists('.full-dialog button.respond-now');
                this.click('.full-dialog button.respond-now');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.full-dialog button.respond-now');
        });
    },
    function() {
        'use strict';
        /* Check dialog, question */
        casper.waitForSelector('.modal blockquote',
            function success() {
                this.test.assertExists('.modal blockquote');
                this.test.assertSelectorHasText('.modal blockquote', 'What are your thoughts on this test file with ümlauts', 'Message exists');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.modal blockquote');
        });
    },
    function() {
        'use strict';
        /* Check dialog, question */
        casper.waitForSelector('.modal .form-group textarea',
            function success() {
                this.test.assertExists('.modal .form-group textarea');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.modal .form-group textarea');
        });
    },
    function() {
        'use strict';
        /* Ok button */
        casper.waitForSelector('.modal .btn-primary',
            function success() {
                this.test.assertExists('.modal .btn-primary');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.modal .btn-primary');
        });
    },
    function() {
        'use strict';
        /* Cancel button */
        casper.waitForSelector('.modal .btn-default',
            function success() {
                this.test.assertExists('.modal .btn-default');
                this.click('.modal .btn-default');
              },
            function fail() {
                helper.snapshotPage.call( this, 9000);
                this.test.assertExists('.modal .btn-default');
        });
    }
);

helper.run();