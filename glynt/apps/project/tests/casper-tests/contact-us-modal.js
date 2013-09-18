'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test to see if the contact us modal displays.
 */
helper.scenario(casper.cli.options.url,
    function () {
        var self = this;
        casper.test.comment('Test Custom Package Contact Us Invalid Click Event')

        casper.then(function() {
            // Click on 1st result link
            this.test.assertExists('button#contact-us-btn');
            this.test.assertExists('div#custom-package-modal[class="modal fade"]');

            casper.then(function() {
                self.click('button#contact-us-btn');

                casper.waitForSelector('div#custom-package-modal[class="modal fade in"]', function() {
                    this.test.pass('Modal is open');

                    this.test.assertVisible('form#contact-us-form');

                    // test the name has been prefilled in
                    var form_values = this.getFormValues('form#contact-us-form');
                    this.test.assertEquals('Customer A', form_values.name);
                    this.test.assertEquals('customer+test@lawpal.com', form_values.email);

                    // complete a message
                    self.fill('form#contact-us-form', {
                        message: ""
                    }, true);

                    var form_values = this.getFormValues('form#contact-us-form');
                    this.echo(JSON.stringify(form_values));
                    // submit the form
                    this.click('#send-contact-us-modal');

                    // ensure modal is visible still
                    this.test.assertExists('form#contact-us-form');
                    this.test.assertVisible('form#contact-us-form');

                    // a message should be presented
                    this.test.assertSelectorHasText('div#div_id_message ul.parsley-error-list li', 'This value is required.');
                });
            });
        });
    },
    function () {
        var self = this;
        casper.test.comment('Test Custom Package Contact Us Valid Click Event')

        casper.then(function() {
            // Click on 1st result link
            self.click('button#contact-us-btn');

            // wait for modal to show
            casper.waitForSelector('div#custom-package-modal[class="modal fade in"]', function() {
                // complete a message
                self.fill('form#contact-us-form', {
                    message: "This is my test message, are you getting it"
                }, true);

                // submit the form
                self.click('#send-contact-us-modal');

                // hide the modal
                casper.waitForSelector('div#custom-package-modal[class="modal fade in"]', function() {
                    this.test.pass('Modal is closed');
                });

                // a message should be presented
                casper.waitForText('Thanks, your message has been sent');
            });
        });
    }
);
helper.run();