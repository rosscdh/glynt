<script>
$(document).ready(function(){
  $('.submit_comment').live('click', function(event){
    event.preventDefault();
    var self = $(this);
    var form = $(this).closest('form');

    $.ajax({
      type: 'POST',
      url: form.attr('action'),
      data: form.serialize(),
    })
    .success(function(data, textStatus, jqXHR) {
      var base_form = self.closest('div#comment-form');
      var base_comment_ul = $('ul#comments');
      var comment_ul = $(data).find('ul#comments');
      var new_li = comment_ul.find('li:first');
      base_comment_ul.prepend(new_li);
      base_form.find('#id_comment').val('')
      base_form.find('#id_comment').select();
    })
    .error(function(jqXHR, textStatus, errorThrown) { 
    })
    .complete(function() {
    });
  });
});
</script>