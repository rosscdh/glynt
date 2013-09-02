var lawPalApp = angular.module('lawpal', [ 'ngResource' ]);

// Filter for categories
lawPalApp.filter( 'checkListCategoryFilter', function(){
	return function( items, categoryName ) {
		debugger;
		if (!angular.isArray(items)) return items;

		debugger;

		arrayToReturn = [];
		for ( var i = 0; i < items.length; i++)
			{
				item = items[0];
				if( item.category === categoryName )
					{
						arrayToReturn.push( item );
					}
			}
	}
});

// Adjust template markup for Django
lawPalApp.config( [ '$interpolateProvider', '$httpProvider', function( $interpolateProvider, $httpProvider ) {
	// AngularJS Handlebar templates
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');

	// Add CSRF challenge codes
	$httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
	$httpProvider.defaults.headers.put['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
	$httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
	$httpProvider.defaults.headers.common['Content-Type']='application/json';
}]);