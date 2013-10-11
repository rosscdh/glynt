var lawPalApp = angular.module('lawpal', [ 'ngResource', 'ui.bootstrap', 'Pusher', 'toaster', 'ui.sortable' ]);

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

lawPalApp.filter('discussionIconStatus', function () {
  return function ( statusNum ) {
  	switch( statusNum ) {
  		case 0: 
  			return "new";
  			break;
  		case 1: 
  			return "open";
  			break;
  		case 2: 
  			return "pending";
  			break;
  		case 3: 
  			return "resolved";
  			break;
  		default:
  			return "open"
  	}
  }
});

lawPalApp.filter('openStatus', function () {
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
  }
});

lawPalApp.filter('timeAgo', function () {
  var minute = 60000;
  var hour = minute * 60;
  var day = hour * 24;
  return function ( timeStamp ) {
  	var now = new Date().getTime(),diff;
  	timeStamp = parseInt(timeStamp);
  	if( timeStamp < now/1000 ) {
  		timeStamp = timeStamp * 1000;
  	}

  	if( timeStamp ) {
  		if( now - timeStamp < minute ) {
  			return "Just now";
  		}
  		if( now - timeStamp < minute * 60 ) {
  			diff = parseInt(( now - timeStamp )/minute,10);
  			return  diff + " minute" + (diff>1?"s":"") + " ago";
  		}
  		if( now - timeStamp < day ) {
  			diff = parseInt(( now - timeStamp )/hour);
  			return  diff + " hour" + (diff>1?"s":"") + " ago";
  		}
  		diff = parseInt(( now - timeStamp )/day);
  		return diff + " day" + (diff>1?"s":"") + " ago";
  	}
    return "";
  }
});