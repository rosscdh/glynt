var lawPalApp = angular.module('lawpal', [ 'ngResource', 'ui.bootstrap', 'Pusher', 'toaster', 'ui.sortable', 'angularFileUpload', 'multi-progress-bar' ]);

// Filter for categories
lawPalApp.filter( 'checkListCategoryFilter', function(){
	'use strict';
	return function( items, categoryName ) {
		var arrayToReturn = [], item;
		
		if (!angular.isArray(items)) return items;

		for ( var i = 0; i < items.length; i++)
			{
				item = items[0];
				if( item.category === categoryName )
					{
						arrayToReturn.push( item );
					}
			}
	};
});

// Adjust template markup for Django
lawPalApp.config( [ '$interpolateProvider', '$httpProvider', function( $interpolateProvider, $httpProvider ) {
	'use strict';
	// AngularJS Handlebar templates
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');

	// Add CSRF challenge codes
	$httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
	$httpProvider.defaults.headers.put['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
	$httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
	$httpProvider.defaults.headers.common['Content-Type']='application/json';
}]);



lawPalApp.filter('openStatus', function () {
	'use strict';
	return function ( items, statusLevel ) {
		var filtered = [];
		if( angular.isArray(items) ) {
			//debugger;
			filtered = items.filter(
				function(item) {
					return item.status <= statusLevel;
				}
			);
		}
		return filtered;
	};
});

angular.module("template/modal/window.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("template/modal/window.html",
    "<div class=\"modal {{ windowClass }}\" ng-class=\"{in: animate}\" ng-style=\"{'z-index': 1050 + index*10}\" ng-transclude></div>");
}]);
