module.exports = (function() {
    var first_scenario = true;

    function opt(name, dfl) {
        if (casper.cli.options.hasOwnProperty(name))
            return casper.cli.options[name];
        else
            return dfl;
    }

    function inject_cookies() {
        var m = opt('url-base').match(/https?:\/\/([^:]+)(:\d+)?\//);
        var domain = m ? m[1] : 'localhost';

        for (var key in casper.cli.options) {
            if (key.indexOf('cookie-') === 0) {
                var cn = key.substring('cookie-'.length);
                var c = phantom.addCookie({
                    name: cn,
                    value: opt(key),
                    domain: domain
                });
            }
        }
    }

    function scenario() {
        var base_url = opt('url-base');
        var start_url = base_url + arguments[0];
        var i;

        if (first_scenario) {
            inject_cookies();

            var viewports = {
              'smartphone_portrait': {width: 320, height: 480},
              'smartphone_landscape': {width: 480, height: 320},
              'tablet_portrait': {width: 768, height: 1024},
              'tablet_landscape': {width: 1024, height: 768},
              'desktop_standard': {width: 1280, height: 1024}
            };

            casper.options.clientScripts = [
                                                casper.cli.options.STATIC_PATH + 'js/jquery.min.js',
                                                casper.cli.options.STATIC_PATH + 'js/jquery.getPath.js',
                                                casper.cli.options.STATIC_PATH + 'js/angularjs/mocks/PusherMock.js'
                                            ];

            casper.options.viewportSize = viewports.desktop_standard;
            casper.options.timeout = casper.cli.options.timeout || 30000;
            casper.options.onTimeout = function() {
                casper.die("Timed out after "+ casper.options.timeout/1000 +" seconds.", 1);
            };

            casper.start(start_url, arguments[1]);
            first_scenario = false;
        } else {
            casper.thenOpen(start_url, arguments[1]);
        }

        for (i = 2; i < arguments.length; i++) {
            casper.then(arguments[i]);
        }
    }

    function run() {
        casper.run(function() { this.test.done(); });
    }

    function assertAbsUrl(rel_url, str_msg) {
        var regex_str = '^' + casper.cli.options['url-base'] + rel_url.replace(/\?/g, '\\?') + '$';
        casper.test.assertUrlMatch(new RegExp(regex_str), str_msg);
    }

    function qunit (url) {
        scenario(url, function() {
            casper.waitFor(function() {
                return casper.evaluate(function() {
                    var el = document.getElementById('qunit-testresult');
                    return el && el.innerText.match('completed');
                });
            }, function() {
                casper.echo("Test output: " + casper.evaluate(function(){
                    return document.getElementById('qunit-testresult').innerText;
                }), 'INFO');
                casper.test.assertEquals(
                    casper.evaluate(function(){
                        return document.getElementById('qunit-testresult')
                            .getElementsByClassName('failed')[0].innerText;
                    }), "0");
            });
        });
    }

    /**
     * Drag and drop from x,y position to a,b position
     * @param  {Array} origin      [x,y]
     * @param  {Array} destination [x,y]
     * @param  {Number} steps       Number > 0
     */
    function moveMouse( origin, destination, steps ) {
        //steps = (steps && steps>0) || 20;
        var stepx = parseInt((destination[0] - origin[0]) / steps);
        var stepy = parseInt((destination[1] - origin[1]) / steps);
        var x = origin[0];
        var y = origin[1];

        casper.page.sendEvent("mousedown", x, y, "left");

        for(var i=0;i<steps;i++) {
            this.page.sendEvent("mousemove", x + (stepx*i), y + (stepy*i));
        }

        casper.page.sendEvent("mouseup", x + (stepx*i), y + (stepy*i));
    }

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

    function snapshotPage(num ) {
        this.capture('/tmp/page_' + num + '.png', {
            top: 0,
            left: 0,
            width: 2048,
            height: 1024
        });
    }

    return {
        scenario: scenario,
        run: run,
        assertAbsUrl: assertAbsUrl,
        qunit: qunit,
        // Custom
        moveMouse: moveMouse,
        capturePageTimelapse: capturePageTimelapse,
        capturePage: capturePage,
        delayCapturePage: delayCapturePage,
        snapshotPage: snapshotPage
    };
})();