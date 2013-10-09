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
  	debugger;
  	console.log( statusNum )
  	switch( statusNum ) {
  		case 0: 
  			return "icon-state-new icon-circle-blank";
  			break;
  		case 1: 
  			return "icon-state-open icon-adjust";
  			break;
  		case 2: 
  			return "icon-warning-sign";
  			break;
  		case 3: 
  			return "icon-state-resolved icon-ok";
  			break;

  		default:
  			return "icon-state-open icon-adjust"
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

  	if( timeStamp ) {
  		console.log(now - timeStamp);
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