<script type="text/javascript"x>
$(document).ready(function(){
  // create new default date
  var c = new Date();
  // convert it to utc time, as we calculate all relative to UTC
  c = moment.utc(new Date(c.getUTCFullYear(), c.getUTCMonth(), c.getUTCDate(), c.getUTCHours(), c.getUTCMinutes(), c.getUTCSeconds()));
  // find all dates to be humanized and then do it
  $.each($('{{ selector }}'), function(index, item){
    var t = new Date($(item).attr('data-humanize-date')*1000)
    // convert the date to urc
    var d = moment.utc(Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), t.getUTCDate(), t.getUTCHours(), t.getUTCMinutes(), t.getUTCSeconds()));
    // set its value
    $(item).html(c.from(d));
  });
});
</script>