{% if PROJECT_ENVIRONMENT == 'test' %}
<!-- load the mock if were in the testing environment -->
<script type="text/javascript" src="{{ STATIC_URL }}js/angularjs/mocks/PusherMock.js" id="pusher-test-env-mock-script"></script>
{% else %}
<script type="text/javascript" src="{{ STATIC_URL }}js/pusher.2.1.2.min.js" id="pusher-live-script"></script>
{% endif %}
<script type="text/javascript" id="pusher-object">
/**
* The Pusher.log object
* Available when debug is True
*/
// Enable pusher logging - don't include this in production
{% if DEBUG %}
Pusher.log = function (message) {
    if (window.console && window.console.log) {
        window.console.log(message);
    }
};
{% endif %}
</script>