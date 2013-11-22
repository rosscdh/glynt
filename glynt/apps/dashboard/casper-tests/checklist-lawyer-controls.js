casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,
    function() {
        'use strict';
        /* Lawyer specific tests */
        casper.test.comment('Test for lawyer name');
        this.test.assertTextExists('Lawyer A', 'Laywer name exists');
    },
    function() {
        'use strict';
        /* Basic page title test */
        casper.test.comment('Test Page General Access and Title');
        this.test.assertHttpStatus(200);

        this.test.assertMatch(this.getTitle(), /^Checklist \—/ig);
        // --
    },
    function() {
        'use strict';
        /* Checklist create new */
        casper.waitForSelector('button.create-item',
            function success() {
                this.test.assertExists('button.create-item');
            },
            function fail() {
                this.test.assertExists('button.create-item');
            }
        );
    },
    function() {
        'use strict';
        /* Checklist categories */
        casper.waitForSelector('th.item-category',
            function success() {
                this.test.assertExists('th.item-category');
                this.test.assertSelectorHasText('th.item-category', 'Category', 'Category column exists');
              },
            function fail() {
                this.test.assertExists('th.item-category');
        });
    },
    function() {
        'use strict';
        /* Checklist categories add category button */
        casper.waitForSelector('button.create-category',
            function success() {
                this.test.assertExists('button.create-category');
              },
            function fail() {
                this.test.assertExists('button.create-category');
        });
    },
    function() {
        'use strict';
        /* Has checklist item */
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
        /* Has drop pane */
        casper.waitForSelector('.drop-pane',
            function success() {
                this.test.assertExists('.drop-pane');
            },
            function fail() {
                this.test.assertExists('.drop-pane');
        });
    },
    function() {
        'use strict';
        /* Has upload button */
        casper.waitForSelector('.upload-button',
            function success() {
                this.test.assertExists('.upload-button');
            },
            function fail() {
                this.test.assertExists('.upload-button');
        });
    },
    function() {
        'use strict';
        /* Has activity stream */
        casper.waitForSelector('.activity-stream .content[ng-switch-when="todo.status_change"]',
            function success() {
                this.test.assertExists('.activity-stream .content[ng-switch-when="todo.status_change"]');
            },
            function fail() {
                this.test.assertExists('.activity-stream .content[ng-switch-when="todo.status_change"]');
        });
    },
    function() {
        'use strict';
        /* Has attachment count */
        casper.waitForSelector('.checklist td', function() {
            casper.test.comment('Test checklist item had an attachment count of 1');
            this.test.assertSelectorHasText('td.item-details span.badge', '1', 'Attachment count exists');
        });
    }
);

helper.run();