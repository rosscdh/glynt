casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,

    function() {
        var self = this;
        // Order categories
        casper.viewport(1024, 768);
        casper.test.comment('Order categories');

        casper.waitForSelector("#checklist-categories li:nth-child(2) .ng-binding:nth-child(1)",
            function success() {
                var secondItemText1, secondItemText2;
                // Read text in current 2nd item position
                secondItemText1 = this.getHTML('#checklist-categories li:nth-child(2) a span:nth-child(1)');
                // Drag and drop
                helper.moveMouse.call( casper, [150,225], [150,300], 20);
                // Read text in current 2nd item position
                secondItemText2 = this.getHTML('#checklist-categories li:nth-child(2) a span:nth-child(1)');
                
                this.wait(1000);
                // Is the text in the second category the same as before (it should not be)
                this.test.assertNotEquals( secondItemText1, secondItemText2 );
            }
        );
    },
    function() {
        'use strict';
        /* Add category */
        casper.test.comment('Add category');
        casper.waitForSelector("button.create-category",
            function success() {
                casper.test.comment('Click create button');
                this.click('button.create-category');
                // Wait for form...
                casper.waitForSelector("input#id_category",
                    function success(){
                        // Fill in form fields
                        casper.test.comment('Fill in category form');
                        this.fill('div.modal form', {
                            'category': "Test category name"
                        }, true);

                        casper.test.comment('Submit form');
                        //this.click('div.modal input[type=submit]');

                        casper.test.comment('Test for success');
                        casper.waitForText("Test category name"/* ".toast-title"*/,
                            function success(){
                                this.test.assertSelectorHasText('.toast-title', 'Success');
                            }
                        );
                    }
                );

            }
        );
    },
    function() {
        //helper.capturePageTimelapse(10);
        /* Add category */
        casper.test.comment('Delete category');

        casper.test.comment('Click remove button');
        this.test.assertSelectorExists('#checklist-categories a.category-general i.category-remove');
        this.click('#checklist-categories a.category-general i.category-remove');

        // Wait for form...
        casper.test.comment('Test for success');

        casper.waitForSelector("div.modal input[type=submit]"/* ".toast-title"*/, 
            function success(){
                this.test.assertTextExists('Delete General', 'Delete dialog exists')
            }
        );
    }
);

helper.run();