casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

helper.scenario(casper.cli.options.url,
    function() {
    	/* Elements exist */
        //this.echo(this.getHTML());
        this.viewport(1200, 800);
        //snapshotPage.call( this, 0 );
        this.test.assertHttpStatus(200);
        this.debugHTML();

        /* Test for Full Screen Button */
        casper.test.comment('Full Screen Button exists');
        this.test.assertSelectorHasText('button', 'Full Screen', 'Full Screen Button exists');

        /* Test for Delete Button */
        casper.test.comment('Delete Button exists');
        this.test.assertSelectorHasText('button', 'Delete', 'Delete Button exists');

        /* Test for Delete Button */
        casper.test.comment('Request Feedback Button exists');
        this.test.assertSelectorHasText('button', 'Request Feedback', 'Request Feedback Button exists');

        /* Iframe exists : #crocdoc-viewer-iframe*/
        casper.test.comment('Request Feedback Button exists');
        this.test.assertExists('iframe#crocdoc-viewer-iframe', 'Crocodoc iframe exists');

        /* File selector exists : h5.list-group-item-heading */
        casper.test.comment('File selector exists');
        this.test.assertExists('h5.list-group-item-heading', 'File selector exists');
    },

    function() {
    	/* Full screen button clicked  */
    	casper.test.comment('Close Full Screen Button exists');
    	this.click('button.btn-fullscreen');
    	this.test.assertSelectorHasText('button', 'Close Full Screen', 'Close Full Screen Button exists');

    	/* Full screen button clicked again */
    	casper.test.comment('Close Full Screen Button exists');
    	this.click('button.btn-fullscreen');
    	this.test.assertSelectorHasText('button', 'Full Screen', 'Full Screen Button exists');
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

function snapshotPage( num ) {
	this.capture('/tmp/page_' + num + '.png', {
        top: 0,
        left: 0,
        width: 2048,
        height: 1024
    });
}

helper.run();