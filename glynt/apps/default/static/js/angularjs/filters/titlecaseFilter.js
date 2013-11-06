/**
 * Converts string into title case
 * @author Lee Sinclair
 * date: 17 Oct 2013
 */
lawPalApp.filter('titleCase', function () {
	'use strict';
	return function (input) {
		var words = input.split(' ');
		for (var i = 0; i < words.length; i++) {
			words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
		}
		return words.join(' ');
	};
});