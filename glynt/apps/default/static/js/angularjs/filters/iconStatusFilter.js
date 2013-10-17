/**
 * Returns a string representing the icon status class
 * @author : Lee Sinclair
 * date: 17 Oct 2013
 */
lawPalApp.filter('discussionIconStatus', function () {
	'use strict';
	return function ( statusNum ) {
		switch( statusNum ) {
			case 0:
				return "new";
			case 1:
				return "open";
			case 2:
				return "pending";
			case 3:
				return "resolved";
			default:
				return "open";
		}
	};
});