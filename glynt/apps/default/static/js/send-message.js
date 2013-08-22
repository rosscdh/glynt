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
    $(document).on( 'shown', '#send-message-modal', function (event) {
        $('#send-message-form').parsley();
    });

    // Simulate input submit
    $(document).on( 'click', '#submit-modal-message', function (event) {
        $('#send-message-form').submit();
    });

    // Submit form
    $(document).on( 'submit', '#send-message-form', function (event) {
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