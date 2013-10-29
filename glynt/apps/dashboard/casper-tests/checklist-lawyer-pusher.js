casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,

    function() {
        // Real-time tests
        casper.test.comment('New item: Real-time Pusher Mock')

        var test = {
                "comment": "Created new item \"Pushed checklist item",
                "label": "Created new item \"Pushed checklist item",
                "instance": {
                    "category": "General",
                    "project": {
                        "pk": 1
                    },
                    "is_deleted": false,
                    "status": 0,
                    "name": "Pushed checklist item: new",
                    "display_status": "New",
                    "pk": 990,
                    "slug": "new-checklist-item",
                    "uri": "/todo/b88c089da3d94337aa11fd2fcc2c4970/eWYNGcGo442oKP4fpX6Ld3/edit/"
                }
        };

        // Test new item
        casper.evaluate(function( data ) {
            // Run script in window session
            window.mock_Pusher.send_message("todo.is_new", data);
        }, test);

        this.test.assertTextExists('Pushed checklist item: new');

        // Test edit item
        casper.test.comment('Edit item: Real-time Pusher Mock');
        test.instance.name = 'Pushed checklist item: edited';

        casper.evaluate(function( data ) {
            window.mock_Pusher.send_message("todo.is_updated", data);
        }, test);
        //helper.capturePageTimelapse(10)
        // @BROKEN @LEE this seems not to be working?
        //this.test.assertTextExists('Pushed checklist item: edited');
    },
    function() {
        // Text messages
        casper.viewport(2048, 1024);
        
        //helper.snapshotPage.call(this,0);
        casper.test.comment('Test displaying messages')
        this.click('a.item-edit');

        casper.waitForText('Edit item', function() {
            //helper.snapshotPage.call(this,1);
            casper.test.comment('Test edit form displays');
            this.test.assertExists('input#id_name');

            this.fill('div.modal form', {
                name: "Modified item name"
            }, true);

            //casper.test.comment('Submit form')
            //this.click('div.modal input[type=submit]');

            casper.waitForText('Modified item name', function(){
                casper.test.comment('Wait for toaster')
                casper.waitForText('Saving changes', function(){
                    this.test.assertTextExists('Saving changes');
                });
            });
        });
    }
);

helper.run();