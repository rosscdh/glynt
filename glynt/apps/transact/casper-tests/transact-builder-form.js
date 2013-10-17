casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

var btn_add_another_founders = 'fieldset[data-region-name="founders"] button#founders_add_another';

/**
 * Test to see if the founder region works.
 */
helper.scenario(casper.cli.options.url,
    function() {
        this.test.comment('Test that the forms fields exist and can be populated and the form submitted');

        //this.echo(this.getHTML())
        this.test.assertExists('form#builder-form');
        this.test.assertExists('#id_1-founder_name');
        this.test.assertExists('#id_1-founder_email');
        this.test.assertExists('#id_1-incubator');
        this.test.assertExists('#id_1-profile_website');
        this.test.assertExists('#id_1-description');
        this.test.assertExists('#id_1-target_states_and_countries');
        this.test.assertExists('#id_1-num_officers');
        this.test.assertExists('#id_1-ip_nolonger_affiliated');
        this.echo(this.getCurrentUrl())

        this.fill('form#builder-form', {
            '1-founder_name': 'Monkey',
            '1-founder_email': 'Number1',
            '1-incubator': 'Founders Den',
            '1-profile_website': 'http://lawpal.com/',
            '1-description': 'We are LawPal.com',
            '1-target_states_and_countries': 'Mönchengladbach',
            '1-num_officers': 2,
            '1-ip_nolonger_affiliated': true,
        }, true);
    }
);

helper.run();
