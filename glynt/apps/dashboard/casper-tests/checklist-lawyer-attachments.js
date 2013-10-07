casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,
    function() {
        /* Test for attachment GUI elements */
        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist item had an attachment count of 1')
            this.test.assertSelectorHasText('td.item-details span.badge', '1', 'Attachment count exists');
        });
    }
);

helper.run();