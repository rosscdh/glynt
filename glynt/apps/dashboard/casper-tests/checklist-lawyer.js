casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

/**
* Test for the Checklist Url like: /dashboard/10a601ce31c24133939f3eced7376097/checklist/
*/
helper.scenario(casper.cli.options.url,
    function() {
        /* Basic page title test */
        casper.test.comment('Test Page General Access and Title');
        this.test.assertHttpStatus(200);

        this.test.assertMatch(this.getTitle(), /^Checklist \—/ig);
        // --
    },
    /*function() {
        // Basic User UI tests
        casper.test.comment('Company name test')
        this.test.assertTextExists('Company Incorporation', 'Company name exists')
    },*/
    function() {
        /* Checklist categories */
        casper.waitForSelector('#checklist-categories li a', function() {
	        casper.test.comment('Test checklist categories exist');
	        this.test.assertExists('ul#checklist-categories')

	        casper.test.comment('Test checklist categories exist');
	        this.test.assertExists('ul#checklist-categories li')

	        casper.test.comment('Test for category name HTML node')
	        this.test.assertExists('section h3')
	           
	        casper.test.comment('Test for number assigned container spans')
	        this.test.assertExists('ul#checklist-categories span.num_assigned_to_user');

	        casper.test.comment('Test for number of assigned tasks per category')
	        this.test.assertSelectorHasText('ul#checklist-categories span.num_assigned_to_user', '1');
        });
    },
    function() {
        /* Checklist items */
        casper.test.comment('Test checklist items exist');
        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist items')
            this.test.assertExists('div#list-items')
            
            casper.test.comment('Test for open checklist item, as provided by workflow')
            this.test.assertExists('div#list-items section td .icon-state-pending')
            
            casper.test.comment('Test for to do, as provided by workflow')
            this.test.assertTextExists('My Todo')
        });
    },
    function() {
        /* Lawyer specific tests */
        casper.test.comment('Test for lawyer name')
        this.test.assertTextExists('Lawyer A', 'Laywer name exists')

        casper.test.comment('Test checklist items exist');
        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist items')
            this.test.assertExists('div#list-items')
            
            casper.test.comment('Test for open checklist item, as provided by workflow')
            this.test.assertExists('div#list-items section td .icon-state-pending')
            
            casper.test.comment('Test for to do, as provided by workflow')
            this.test.assertTextExists('My Todo')
        });

        casper.test.comment('Test checklist items options for lawyers');
        casper.waitForSelector('div#list-items section td', function() {
            casper.test.comment('Test checklist items create button')
            this.test.assertExists('div#list-items div#transaction-setup button.create-item')

            casper.test.comment('Test checklist items edit button exists and is visible');
            this.test.assertExists('div#list-items tr.item a.item-edit')
            this.test.assertVisible('div#list-items tr.item a.item-edit')

            casper.test.comment('Test checklist items delete button exists and is visible');
            this.test.assertExists('div#list-items tr.item a.item-delete')
            this.test.assertNotVisible('div#list-items tr.item a.item-delete')
        });
    },
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

        this.test.assertTextExists('Pushed checklist item: edited');
    },
    function() {
    	// Text messages
    	//casper.viewport(2048, 1024);
    	casper.test.comment('Test displaying messages')
    	this.click('a.item-edit');

    	casper.waitForSelector('div#div_id_name', function() {
    		casper.test.comment('Test edit form displays')
    		this.test.assertExists('div#div_id_name input');

    		this.fill('div.modal form', {
                name: "Modified item name"
            }, true);

            casper.test.comment('Submit form')
            this.click('div.modal input[type=submit]');

            casper.waitForText('Modified item name', function(){
            	casper.test.comment('Wait for toaster')
	            casper.waitForText('Saving changes', function(){
	            	this.test.assertTextExists('Saving changes');
	            });
            });
    	});
    }
);

/**
 * captureRequest: Increments by one each time a capturePage request is made
 *                 this variable is used to save unique image filename for each page capture taken
 * @type {Number}
 */
var captureRequest = 0;

/**
 * capturePageTimelapse: captures the page 1 per second for numFrames (keep in mind that each test has a timeout of 5 seconds  )
 * usage:
 *                       capturePageTimelapse(4);
 * 
 * @param  {Number} numFrames Number of frames to capture
 */
function capturePageTimelapse( numFrames ) {
    for(var i=0;i<numFrames;i++) {
        capturePage();
    }
}

/**
 * capturePage: Initiates a capture request, a screen capture will be taken in n seconds where n = captureRequest * 1000
 *              images will be saved into /tmp/
 * usage:
 *              capturePage();
 */
function capturePage() {
	var wait;
	captureRequest++;
	wait = captureRequest * 1000; // wait n seconds before taking screen capture
	delayCapturePage( wait );
}

/**
 * delayCapturePage: when called invokes a screen capture in [delay] seconds
 * @param  {Number} delay Number of seconds to wait until taking the screen capture
 */
function delayCapturePage( delay ) {
	casper.wait(delay, function() {
    	this.capture('/tmp/page_' + delay + '.png', {
	        top: 0,
	        left: 0,
	        width: 2048,
	        height: 1024
	    });
    });
}

helper.run();