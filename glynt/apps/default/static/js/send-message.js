$(document).ready(function() {
   // Load message modal
    $("#send-message").click(function(ev) {
        ev.preventDefault();
        var url = $(this).attr('href');
        $("#send-message-modal").load(url, function() {
            $(this).modal('show');
        });
        return false;
    });

    // Activate parsley form validation when the modal has finished loading
    $('#send-message-modal').live('shown', function() {
        $('#send-message-form').parsley();
    });

    // Simulate input submit
    $('#submit-modal-message').live('click', function() {
        $('#send-message-form').submit();
    });

    // Submit form
    $('#send-message-form').live('submit', function(event) {
        event.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            context: this,
            success: function(data, status) {
                GlyntJsMessages.add_message(data.message);
            },
            error: function(jsdata, data, status) {
                GlyntJsMessages.add_message(data.message, 'error');
            },
            complete: function(){
                $("#send-message-modal").modal('hide');
                GlyntJsMessages.show();
            }
        });
        return false;
    });
});