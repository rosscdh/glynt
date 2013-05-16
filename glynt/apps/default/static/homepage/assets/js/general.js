jQuery(window).load(function() {      
  // add a class so we know JavaScript is supported
  jQuery('html').addClass("js");
  jQuery('html').removeClass("no-js");
});
jQuery(document).ready(function() {


    bgImageTotal=5;

    randomNumber = Math.round(Math.random()*(bgImageTotal-1))+1;

    imgPath=('/static/homepage/assets/img/bg/landing'+randomNumber+'.jpg');

    $('body').css('background-image', ('url("'+imgPath+'")'));


$('#data-statement').click(function() {
	$('#data-statement-body').fadeToggle();	
	$('#data-statement').toggle();	

});


	// polyfill placeholder text
	if ( (jQuery('html').hasClass("oldie")) || (jQuery('html').hasClass("ie9")) ) {
	    jQuery('[placeholder]').focus(function () {
	        var input = jQuery(this);
	        if (input.val() == input.attr('placeholder')) {
	            input.val('');
	            input.removeClass('placeholder');
	        }
	    }).blur(function () {
	        var input = jQuery(this);
	        if (input.val() == '' || input.val() == input.attr('placeholder')) {
	            input.addClass('placeholder');
	            input.val(input.attr('placeholder'));
	        }
	    }).blur().parents('form').submit(function () {
	        jQuery(this).find('[placeholder]').each(function () {
	            var input = $(this);
	            if (input.val() == input.attr('placeholder')) {
	                input.val('');
	            }
	        })
	    });
	}    
});