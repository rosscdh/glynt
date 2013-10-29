/**
 * Returns the first letter of each word in a string
 * @author Lee Sinclair
 * @deprecated : Oct 17 2013
 */
lawPalApp.filter('plainTextToParagraphs', function () {
	'use strict';
	return function (input) {
		if( typeof input=== "string") {
			return input.replace(/\n/g,'<br />');
		}
		else
			return null;
	};
});