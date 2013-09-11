casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
 * Test to see if the contact us modal displays.
 */
helper.scenario(casper.cli.options.url,
    function() {
        casper.test.comment('Test for valid form submission');
        this.test.assertHttpStatus(200);

        this.click('button.custom-package-button');

        this.waitUntilVisible('div#custom-package', function() {
            this.test.pass('Modal is open');

            this.fill('form#contact-us-form', {
                message: "Hello world!"
            }, true);

            // test the name has been prefilled in
            this.test.assertEquals('Customer A', this.getFormValues('form#contact-us-form').name);

            this.click('input#submit-id-send');

            this.waitWhileVisible('div#custom-package', function() {
                this.test.pass('Modal is closed');
            });
        });
    }
);

helper.scenario(casper.cli.options.url,
    function() {
        this.echo('Test for invalid form submission');
        this.test.assertHttpStatus(200);

        this.click('button.custom-package-button');

        this.waitUntilVisible('div#custom-package', function() {
            this.test.pass('Modal is open');

            // test the name has been prefilled in
            this.test.assertEquals('Customer A', this.getFormValues('form#contact-us-form').name);

            this.click('input#submit-id-send');

            this.test.assertVisible('div#custom-package');
            this.test.assertSelectorHasText('div#div_id_message ul.parsley-error-list li', 'This value is required.');
        });
    }
);

helper.run();