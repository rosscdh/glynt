/**
 * @author : Lee Sinclair
 * date 17 Oct 2013
 */
lawPalApp.filter('timeAgo', function () {
	'use strict';
	var minute = 60000;
	var hour = minute * 60;
	var day = hour * 24;
	return function ( timeStamp ) {
		var now = new Date().getTime(),diff;
		timeStamp = parseInt(timeStamp, 10);
		if( timeStamp < now/1000 ) {
			timeStamp = timeStamp * 1000; // Convert unix timestamp to milliseconds
		}

		if( timeStamp ) {
			if( now - timeStamp < minute ) {
				return "Just now";
			}
			if( now - timeStamp < minute * 60 ) {
				diff = parseInt(( now - timeStamp )/minute,10);
				return	diff + "m"/* + (diff>1?"s":"") + " ago"*/;
			}
			if( now - timeStamp < day ) {
				diff = parseInt(( now - timeStamp )/hour, 10);
				return	diff + "h"/* + (diff>1?"s":"") + " ago"*/;
			}
			diff = parseInt(( now - timeStamp )/day, 10);
			return diff + "d"/* + (diff>1?"s":"") + " ago"*/;
		}
		return "";
	};
});