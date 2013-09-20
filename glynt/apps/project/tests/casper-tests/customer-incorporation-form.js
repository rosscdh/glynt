"use strict";

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

var btn_submit_form = 'button#submit-builder';
var btn_add_another_founders = 'fieldset[data-region-name="founders"] button#founders_add_another';

/**
* Test for the Checklist Url like: /transact/build/925f383b4dde40fa91f03ef99e3b08d9/CS/1/
*/
helper.scenario(casper.cli.options.url,
    function() {
        /* Basic page title test */
        casper.test.comment('Test Page General Access and Title');
        this.test.assertHttpStatus(200);

        this.test.assertEqual(this.getTitle(), 'Your Company Profile');
    },
    function() {
        // Basic User UI tests
        casper.test.comment('Test all the javascript HTML elements are present');

        this.test.assertTextExists('Your Company Profile');
        this.test.assertTextExists('Enter some basic details about your company');

        // fieldset legends
        this.test.assertTextExists('Founding Team');
        this.test.assertTextExists('About your Startup');

        // submit button
        this.test.assertExists(btn_submit_form);
        this.test.assertSelectorHasText(btn_submit_form, 'Continue');

        // region-clone add button
        this.test.assertExists(btn_add_another_founders);
        this.test.assertSelectorHasText(btn_add_another_founders, 'Add another');

        // json_data field is present
        this.test.assertExists('input[name="1-form_json_data"][type="hidden"]');
        
    },
    function() {
        /* Form Functionality */
        var self = this;
        casper.test.comment('Test the form can be completed');

        this.fill('form#builder-form', {
            '1-founder_name': "Ross Crawford",
            '1-founder_email': "ross@lawpal.com",
            '1-incubator': "FoundersDen",
            '1-profile_website': "http://angel.com/lawpal"
        }, false);

        casper.test.comment('Test the Add another button works');

        this.test.assertElementCount('button.close.delete-cloned-region', 0);

        this.test.assertElementCount('input#id_1-founder_email_1', 0);
        this.click(btn_add_another_founders);
        this.test.assertExists('button#region-clone-remove_1')
        this.test.assertElementCount('input#id_1-founder_email_1', 1);

        this.test.assertElementCount('button.close.delete-cloned-region', 1);


        casper.test.comment('Test the Add a third button works');
        this.test.assertElementCount('input#id_1-founder_email_2', 0);
        this.click(btn_add_another_founders);
        this.test.assertExists('button#region-clone-remove_2')
        this.test.assertElementCount('input#id_1-founder_email_2', 1);
        this.test.assertElementCount('button.close.delete-cloned-region', 2);

        // add a test delete item
        casper.test.comment('Test theat we can delete region clones items');
        this.test.assertElementCount('input#id_1-founder_email_3', 0);
        this.click(btn_add_another_founders);
        this.test.assertExists('button#region-clone-remove_3')
        this.test.assertElementCount('input#id_1-founder_email_3', 1);

        this.test.assertElementCount('button.close.delete-cloned-region', 3);
        this.click('button#region-clone-remove_3'); // 2 and not 3 because its 0 based and there should only be 2 showing at this point
        this.test.assertElementCount('button.close.delete-cloned-region', 2);

        this.fill('form#builder-form', {
            '1-founder_name_1': "Alex Halliday",
            '1-founder_email_1': "alex@lawpal.com",
            '1-founder_name_2': "Yael Citaro",
            '1-founder_email_2': "yael@lawpal.com",
        }, false);

        casper.test.comment('Test the form has been filled');

        var form_values = this.getFormValues('form#builder-form');
        this.test.assertEqual(form_values['1-founder_name_1'], 'Alex Halliday')
        this.test.assertEqual(form_values['1-founder_email_1'], 'alex@lawpal.com')
        this.test.assertEqual(form_values['1-founder_name_2'], 'Yael Citaro')
        this.test.assertEqual(form_values['1-founder_email_2'], 'yael@lawpal.com')

        casper.test.comment('Test the form can be submitted and we are redirected');

        this.click(btn_submit_form);
    }
);

helper.run();