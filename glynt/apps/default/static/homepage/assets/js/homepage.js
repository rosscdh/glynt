jQuery(window).load(function() {      
  // add a class so we know JavaScript is supported
  jQuery('html').addClass("js");
  jQuery('html').removeClass("no-js");
});
jQuery(document).ready(function() {


    
	randomNumber=Math.floor(Math.random()*3);
    imgPath=('/static/homepage/assets/img/bg/landing'+randomNumber+'.jpg');

    $('#hero').css('background-image', ('url("'+imgPath+'")'));

    // $('#hero').css({'height':(($(window).height())-182)+'px'});

    $(window).resize(function(){
   		// $('#hero').css({'height':(($(window).height())-182)+'px'});
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

	$('.hideme').each( function(i){
            
                $(this).animate({'opacity':'0'},100);
        }); 

	$('a').click(function(){
	    $('html, body').animate({
	        scrollTop: $('[name="' + $.attr(this, 'href').substr(1) + '"]').offset().top
	    }, 500);
	    return false;
	});
    /* Every time the window is scrolled ... */
    $(window).scroll( function(){
    
        /* Check the location of each desired element */
        $('.hideme').each( function(i){
            
            var bottom_of_object = $(this).position().top + $(this).outerHeight();
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            
            /* If the object is completely visible in the window, fade it it */
            if( bottom_of_window > bottom_of_object ){
                
                $(this).animate({'opacity':'1'},1500);
                    
            }
            
        }); 
    
    });
    
});