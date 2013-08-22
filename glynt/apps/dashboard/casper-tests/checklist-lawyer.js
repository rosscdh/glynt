casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,
    function() {
        casper.test.comment('Test Page General Access and Title');
        //this.echo(this.getHTML());
        this.echo(this.getTitle());
        this.test.assertHttpStatus(200);

        this.test.assertMatch(this.getTitle(), /^Checklist for\:/ig, 'Title contains Checklist for:');
        // --
    },
    function() {
        casper.test.comment('Test checklist categories exist');

        this.test.assertExists('ul#checklist-categories')
        this.test.assertExists('ul#checklist-categories li')
    },
    function() {
        casper.test.comment('Test checklist items exist');

        this.test.assertExists('tr.item')
        this.test.assertExists('button.create-item')

        casper.test.comment('Test checklist items edit button exists and is visible');
        this.test.assertExists('tr.item a.item-edit')
        this.test.assertVisible('tr.item a.item-edit')

        casper.test.comment('Test checklist items delete button exists and is not visible');
        this.test.assertExists('tr.item a.item-delete')
        this.test.assertNotVisible('tr.item a.item-delete')
        
    },
    function() {
        casper.test.comment('Test checklist feedback request indicator is working');

        // the general cat has the span with the right class
        this.test.assertExists('li[data-category="general"] span.num_assigned_to_user');
        // the span contains the value
        this.test.assertSelectorHasText('li[data-category="general"] span.num_assigned_to_user', '1');
        // test we have the little span indicator
        this.test.assertExists('li[data-category="general"] span.num_assigned_to_user i.icon-state-pending');

    }
    // function() {
    //     var self = this;
    //     casper.test.comment('Test edit item shows modal');

    //     this.evaluate(function() {
    //         var selector = $('tr.item a.item-edit:first');
    //         selector.trigger('click');
    //     });

    //     casper.waitFor(function check() {
    //         return this.evaluate(function() {
    //             return $('#modal-checklist-item').length > 0;
    //         });
    //     }, function then() {
    //         this.capture('/tmp/modal_click.png')
    //         this.captureSelector('/tmp/yoursitelist.png', 'div#modal-checklist-item');
    //     });
    // }
);

helper.run();