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
        this.echo(this.getTitle());
        this.test.assertMatch(this.getTitle(), /^Checklist \—/ig);
        // --
    },
    function() {
        /* Basic User UI tests */
        casper.test.comment('Company name test')
        this.test.assertTextExists('Company Incorporation', 'Company name exists')
    },
    function() {
        /* Checklist categories */
        casper.waitForSelector('#checklist-categories li a', function() {

            this.echo(this.getHTML());

            casper.test.comment('Test checklist categories exist');

            casper.test.comment('Test checklist categories exist');
            this.test.assertExists('ul#checklist-categories')

            casper.test.comment('Test checklist categories exist');
            this.test.assertExists('ul#checklist-categories li')

            casper.test.comment('Test for category name HTML node')
            this.test.assertExists('section h3')

            /*
            casper.test.comment('Test for category name')
            this.test.assertSelectorHasText('section h3,','General')
            */
           
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

            this.echo(this.getHTML());

            casper.test.comment('Test checklist items')
            this.test.assertExists('div#list-items')
            
            casper.test.comment('Test for open checklist item, as provided by workflow')
            this.test.assertExists('div#list-items section td .icon-state-pending')
            
            casper.test.comment('Test for to do, as provided by workflow')
            this.test.assertTextExists('My Todo')
        });
        /*
        casper.wait(1000, function() {
            casper.test.comment('Test checklist categories exist');
            this.test.assertExists('ul#checklist-categories')
            
            this.test.assertExists('ul#checklist-categories li')

            casper.test.comment('Test checklist items')
            casper.test.assertExists('div#list-items')
            casper.test.comment('Test checklist items create button')
            casper.test.assertExists('div#list-items section div#transaction-setup button.create-item')
            
            casper.test.comment('Test checklist items exist');

            this.test.assertExists('tr.item')
            this.test.assertExists('button.create-item')

            casper.test.comment('Test checklist items edit button exists and is visible');
            this.test.assertExists('tr.item a.item-edit')
            this.test.assertVisible('tr.item a.item-edit')

            casper.test.comment('Test checklist items delete button exists and is not visible');
            this.test.assertExists('tr.item a.item-delete')
            this.test.assertNotVisible('tr.item a.item-delete')
        
            casper.test.comment('Test checklist feedback request indicator is working');

            // the general cat has the span with the right class
            this.test.assertExists('li[data-category="general"] span.num_assigned_to_user');
            // the span contains the value
            this.test.assertSelectorHasText('li[data-category="general"] span.num_assigned_to_user', '1');
            // test we have the little span indicator
            this.test.assertExists('li[data-category="general"] span.num_assigned_to_user i.icon-state-pending');
            
        });
        */
    },
    function() {
        /* Lawyer specific tests */
        casper.test.comment('Test for lawyer name')
        this.test.assertTextExists('Lawyer A', 'Laywer name exists')

        casper.test.comment('Test checklist items exist');
        casper.waitForSelector('div#list-items section td', function() {

            this.echo(this.getHTML());

            casper.test.comment('Test checklist items')
            this.test.assertExists('div#list-items')
            
            casper.test.comment('Test for open checklist item, as provided by workflow')
            this.test.assertExists('div#list-items section td .icon-state-pending')
            
            casper.test.comment('Test for to do, as provided by workflow')
            this.test.assertTextExists('My Todo')
        });

        casper.test.comment('Test checklist items options for lawyers');
        casper.waitForSelector('div#list-items section td', function() {

            this.echo(this.getHTML());

            casper.test.comment('Test checklist items create button')
            this.test.assertExists('div#list-items div#transaction-setup button.create-item')

            casper.test.comment('Test checklist items edit button exists and is visible');
            this.test.assertExists('div#list-items tr.item a.item-edit')
            this.test.assertVisible('div#list-items tr.item a.item-edit')

            casper.test.comment('Test checklist items delete button exists and is visible');
            this.test.assertExists('div#list-items tr.item a.item-delete')
            this.test.assertNotVisible('div#list-items tr.item a.item-delete')
        });
    }
);

helper.run();