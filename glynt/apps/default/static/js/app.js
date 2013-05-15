// Little function which will show the next input field 

$('.new-input').hide();

$(".swaptoinput").change(function () {
	var str = "";
	$("select option:selected").each(function () {
	    str += $(this).attr('class') + " ";
	  });
	if (str.indexOf("new") >= 0){
		
		$(this).css("display", "none");
	  	$(this).next(".new-input").fadeIn();
	}
})
.trigger('change');


// Additional little function for new Property row we are adding

$('.new-property').hide();

$(".add-new-property").click(function() {
	$('.new-property').show();
})

$('input[title]').tooltip({trigger: 'focus', placement: 'top'});
$('.tip').tooltip({trigger: 'focus', placement: 'top'});
