casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,
    function() {
        /* Basic page title test */
        casper.test.comment('Test Page General Access and Title');
        this.test.assertHttpStatus(200);

        this.test.assertMatch(this.getTitle(), /^Checklist \—/ig);
        // --
    },
    function() {
        /* Checklist categories */
        casper.waitForSelector('#checklist-categories li a', function() {
            casper.test.comment('Test checklist categories exist');
            this.test.assertExists('ul#checklist-categories')

            casper.test.comment('Test checklist categories exist');
            this.test.assertExists('ul#checklist-categories li')

            casper.test.comment('Test for category name HTML node')
            this.test.assertExists('section h4')
               
            casper.test.comment('Test for number assigned container spans')
            this.test.assertExists('ul#checklist-categories span.num_assigned_to_user');

            casper.test.comment('Test for number of assigned tasks per category')
            this.test.assertSelectorHasText('ul#checklist-categories span.num_assigned_to_user', '1');
        });
    },
    function() {
        /* Checklist items */
        casper.test.comment('Test checklist items exist');

        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist items')
            this.test.assertExists('div#list-items')
            
            casper.test.comment('Test for open checklist item, as provided by workflow')
            this.test.assertExists('div#list-items section td .icon-state-pending')
            
            casper.test.comment('Test for to do, as provided by workflow')
            this.test.assertTextExists('My Todo')
        });
    },
    function() {
        /* Lawyer specific tests */
        casper.test.comment('Test for lawyer name')
        this.test.assertTextExists('Lawyer A', 'Laywer name exists')

        casper.test.comment('Test checklist items exist');
        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist items')
            this.test.assertExists('div#list-items')
            
            casper.test.comment('Test for open checklist item, as provided by workflow')
            this.test.assertExists('div#list-items section td .icon-state-pending')
            
            casper.test.comment('Test for to do, as provided by workflow')
            this.test.assertTextExists('My Todo')
        });

        casper.test.comment('Test checklist items options for lawyers');
        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist items create button')
            this.test.assertExists('div#list-items div#transaction-setup button.create-item')

            casper.test.comment('Test checklist items edit button exists and is visible');
            this.test.assertExists('div#list-items tr.item a.item-edit')
            this.test.assertVisible('div#list-items tr.item a.item-edit')

            casper.test.comment('Test checklist items delete button exists and is visible');
            this.test.assertExists('div#list-items tr.item a.item-delete')
            this.test.assertNotVisible('div#list-items tr.item a.item-delete')
        });
    },
    function() {
        /* Test for attachment GUI elements */
        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist item had an attachment count of 1')
            this.test.assertSelectorHasText('td.item-details span.badge', '1', 'Attachment count exists');
        });
    }
    /*,
    function() {
        // Order items
        casper.viewport(1024, 768);
        casper.test.comment('Order categories');

        casper.waitForSelector(".item-info h4 a",
            function success() {
                var secondItemText1, secondItemText2;
                // Read text in current 2nd item position
                secondItemText1 = this.getHTML('.item-info h4 a');
                // Drag and drop
                helper.snapshotPage.call( this, 11);
                helper.moveMouse.call( casper, [450,405], [450,475], 20);
                // Read text in current 2nd item position
                secondItemText2 = this.getHTML('.item-info h4 a');
                
                this.wait(1000);
                helper.snapshotPage.call( this, 12);
                // Is the text in the second category the same as before (it should not be)
                this.test.assertNotEquals( secondItemText1, secondItemText2 );
            }
        );
    }*/
);

helper.run();