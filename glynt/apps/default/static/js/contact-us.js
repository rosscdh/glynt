$(document).ready( function() {

    // Load modal
    $("a.contact-us").click(function(ev) {
        ev.preventDefault();
        var url = $(this).attr('href');
        $("#contactModal").load(url, function() {
            $(this).modal('show');
        });
        return false;
    });

    // Simulate input submit
    $('#submitMessage').live('click', function() {
       $('#contact-us-form').submit();
    });

    // Submit form
    $('#contact-us-form-modal').live('submit', function() {
        $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            context: this,
            success: function(data, status) {
                $('#contactModal').html(data);
            }
        });
        return false;
    });

});