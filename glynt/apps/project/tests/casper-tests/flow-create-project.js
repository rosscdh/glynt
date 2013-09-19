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
    /*function() {
        // Basic User UI tests
        casper.test.comment('Company name test')
        this.test.assertTextExists('Company Incorporation', 'Company name exists')
    },*/
    function() {
        /* Checklist categories */
        casper.waitForSelector('#checklist-categories li a', function() {
            casper.test.comment('Test checklist categories exist');
            this.test.assertExists('ul#checklist-categories')

            casper.test.comment('Test checklist categories exist');
            this.test.assertExists('ul#checklist-categories li')

            casper.test.comment('Test for category name HTML node')
            this.test.assertExists('section h3')
               
            casper.test.comment('Test for number assigned container spans')
            this.test.assertExists('ul#checklist-categories span.num_assigned_to_user');

            casper.test.comment('Test for number of assigned tasks per category')
            this.test.assertSelectorHasText('ul#checklist-categories span.num_assigned_to_user', '1');
        });
    },
);

helper.run();