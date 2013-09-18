'use strict';

casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test to see if the contact us modal displays.
 */
helper.scenario(casper.cli.options.url,
    function() {
        casper.test.comment('Test for valid form submission');
        this.test.assertHttpStatus(200);

        this.click('button#contact-us-btn');

        casper.waitUntilVisible('div#custom-package-modal', function() {
            this.test.pass('Modal is open');

            // test the name has been prefilled in
            var form_values = this.getFormValues('form#contact-us-form');
            this.test.assertEquals('Customer A', form_values.name);
            this.test.assertEquals('customer+test@lawpal.com', form_values.email);

            this.fill('form#contact-us-form', {
                message: "Hello world!"
            }, true);

            this.click('#send-contact-us-modal');

            this.capture('/tmp/wtf.png')
            this.test.assertNotVisible('div#custom-package-modal');
        });
    }
);

helper.scenario(casper.cli.options.url,
    function() {
        this.echo('Test for invalid form submission');
        this.test.assertHttpStatus(200);

        this.click('button#contact-us-btn');

        this.waitUntilVisible('div#custom-package-modal', function() {
            this.test.pass('Modal is open');

            // ensure the message field is EMPTY for this test
            this.fill('form#contact-us-form', {
                message: ""
            }, true);

            // test the name has been prefilled in
            var form_values = this.getFormValues('form#contact-us-form');
            this.test.assertEquals('Customer A', form_values.name);
            this.test.assertEquals('customer+test@lawpal.com', form_values.email);

            this.click('#send-contact-us-modal');

            // test the modal is still present
            this.test.assertVisible('div#custom-package-modal');

            // do we see the parsley message specific to the message input
            this.test.assertSelectorHasText('div#div_id_message ul.parsley-error-list li', 'This value is required.');
        });
    }
);

helper.run();