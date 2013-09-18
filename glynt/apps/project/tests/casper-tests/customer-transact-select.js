'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,
    function () {
        /* Basic page title test */
        casper.test.comment('Test Page General Access and Title');
        this.test.assertHttpStatus(200);
        this.test.assertEqual(this.getTitle(), 'Select a Transaction')
        // --
    },
    function () {
        casper.test.comment('Test Page for appropriate HTML containers')

        // we have the primary container that contains the packages
        this.test.assertExists('div.container.packages-view')

        /**
        * Test we have 3 data-transactions available
        * but only 1 callout-info - 3 transaction and 1 contact us
        */
        this.test.assertElementCount('div.transaction-choice[data-transaction]', 3)
        this.test.assertElementCount('div.transaction-choice[data-transaction] button.btn', 3)
        this.test.assertElementCount('div#custom-package.callout-info', 1)
        this.echo(this.debugHTML());

        /**
        * Inspect the contact us div
        */
        this.test.assertSelectorHasText('div#custom-package.callout-info h4', 'Need something else?')
        this.test.assertSelectorHasText('div#custom-package.callout-info p:nth-child(3)', 'Just give us the details and we will get back to you ASAP.')
        this.test.assertExists('div#custom-package.callout-info button.custom-package-button i.icon-envelope')
        this.test.assertSelectorHasText('div#custom-package.callout-info button#contact-us-btn.custom-package-button', 'Contact us')

        // check for the modal settings
        this.getElementAttribute('div#custom-package.callout-info button.custom-package-button[data-toggle]', 'modal')
        this.getElementAttribute('div#custom-package.callout-info button.custom-package-button[data-target]', '#custom-package-modal')

        // has the modal div
        this.test.assertExists('div#custom-package-modal')
        // has the form
        this.test.assertExists('div#custom-package-modal form#contact-us-form')
        // has appropriate form fields
        this.test.assertExists('div#custom-package-modal form#contact-us-form input#id_name')
        this.test.assertExists('div#custom-package-modal form#contact-us-form input#id_email[type=hidden]')
        this.test.assertExists('div#custom-package-modal form#contact-us-form textarea#id_message')

        // and the fields have values
        var form_values = this.getFormValues('form#contact-us-form');
        this.test.assertNotEquals(form_values.name, '') // must have a value
        this.test.assertNotEquals(form_values.email, '') // must have a value
        this.test.assertEquals(form_values.message, '') // must NOT have a value
        // test actual values
        this.test.assertEquals('Customer A', form_values.name);
        this.test.assertEquals('customer+test@lawpal.com', form_values.email);

        // submit button
        this.test.assertExists('div#custom-package-modal .modal-footer input.btn.btn-primary')
        this.getElementAttribute('div#custom-package-modal .modal-footer input.btn.btn-primary[value]', 'Send')
    },
    function () {
        casper.test.comment('Test Transaction Types')

        this.test.assertExists('button#CS-select');
        this.test.assertSelectorHasText('button#CS-select', 'Add package')

        this.test.assertExists('button#SF-select');
        this.test.assertSelectorHasText('button#SF-select', 'Add package')

        this.test.assertExists('button#ES-select');
        this.test.assertSelectorHasText('button#ES-select', 'Add package')
    },
    function () {
        casper.test.comment('Test Selection matrix of transactions')
        // select incorporation and 1 other of the Seed Financing
        this.click('button#CS-select')
        // is set to active
        this.test.assertExists('button#CS-select.active');

        this.click('button#SF-select')
        // is set to active
        this.test.assertExists('button#SF-select.active');

        this.click('button#ES-select')
        // is set to active
        this.test.assertExists('button#ES-select.active');
        // but the original SF-select.active is REMOVED
        this.test.assertNotExists('button#SF-select.active');

        this.click('button#SF-select')
        // is set to active
        this.test.assertExists('button#SF-select.active');
        // but the original SF-select.active is REMOVED
        this.test.assertNotExists('button#ES-select.active');
    },
    function () {
        var self = this;
        casper.test.comment('Test Custom Package Contact Us Click Event')

        casper.then(function() {
            // Click on 1st result link
            self.click('button#contact-us-btn');

            // wait for modal to show
            casper.waitForSelector('div#custom-package-modal form#contact-us-form', function() {
                // complete a message
                self.fill('form#contact-us-form', {
                    message: "This is my test message, are you getting it"
                }, true);

                // submit the form
                self.click('div#custom-package-modal .modal-footer input.btn.btn-primary[value]');

                // hide the modal
                self.test.assertNotVisible('div#custom-package-modal');

                // a message should be presented
                casper.waitForText('Thanks, your message has been sent');
            });

        });

    }
);

helper.run();