jQuery(window).load(function() {      
  // add a class so we know JavaScript is supported
  jQuery('html').addClass("js");
  jQuery('html').removeClass("no-js");
});
jQuery(document).ready(function() {

	// get reveal and expose inner
	jQuery('.reveal').each(function(index) {
		var getHeight = (jQuery(this).height()/2);
		var $current = jQuery(this);
		
		jQuery('hgroup',this).css("margin-top" , getHeight);
		
		// jQuery('.reveal-inner',$current).hide();
				// 
		// jQuery(this).hover(
		//   function () {
		//     jQuery('hgroup',this).animate({
		//         marginTop: 0
		//       }, 100, function() {
		//         jQuery('.reveal-inner',$current).addClass("show");
		//         jQuery('.reveal-inner',$current).fadeIn(100);
		//       });
		//   },
		//   function () {
		//   	jQuery('.reveal-inner',$current).fadeOut(100, function() {
		//   	    jQuery('hgroup',$current).animate({
		//   	        marginTop: getHeight
		//   	      }, 100, function() {
		//   	      });
		//   	  });
		//   }
		// );
		
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