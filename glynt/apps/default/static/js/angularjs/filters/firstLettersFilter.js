/**
 * Returns the first letter of each word in a string
 * @author Lee Sinclair
 * @deprecated : Oct 17 2013
 */
lawPalApp.filter('firstLetters', function () {
	'use strict';
	return function (input) {
		if( typeof input=== "string") {
			var stringEls = input.split(" ");
			var letters = "";
			for(var i=0;i<stringEls.length;i++)
				letters+=(stringEls[i].length>0?stringEls[i][0]:"");
			return letters;
		}
		else
			return null;
	};
});