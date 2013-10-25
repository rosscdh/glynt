var lawPalApp = angular.module('lawpal', [ 'ngResource', 'ui.bootstrap', 'Pusher', 'toaster', 'ui.sortable', 'angularFileUpload' ]);

// Filter for categories
lawPalApp.filter( 'checkListCategoryFilter', function(){
	return function( items, categoryName ) {
		if (!angular.isArray(items)) return items;

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

lawPalApp.filter('titleCase', function () {
  return function (input) {
    var words = input.split(' ');
    for (var i = 0; i < words.length; i++) {
      words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
    }
    return words.join(' ');
  }
});

lawPalApp.filter('firstLetters', function () {
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
  }
});