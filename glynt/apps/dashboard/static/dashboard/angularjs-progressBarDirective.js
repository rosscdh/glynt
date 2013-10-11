/**
 * Displays the percentage comparison between new, open, pending and closed checklist items
 * @return {Object} AngularJS directive
 */
angular.module('lawpal').directive('projectProgressBar', function () {
  return {
  	"restrict": "A",
  	"template": 
  		'<progress percent=\"percentages\" auto-type=\"true\">{[{percentages|json}]}</progress>'+
  		'<div class="row">'+
        '<h5 class="text-info col-lg-3">{[{counts.new}]} New</h5>'+
        '<h5 class="text-warning col-lg-3">{[{counts.open}]} Open</h5>'+
        '<h5 class="text-danger col-lg-3">{[{counts.awaiting}]} Pending</h5>'+
        '<h5 class="text-success col-lg-3">{[{counts.closed}]} Closed</h5>'+
        '</div>',
  	"scope": {
  		"counts": "=counts"
  	},
    "link": function (scope, iElement, iAttrs) {
    	console.log("link", scope.counts);
    },
    "controller": [ '$scope', '$element', '$attrs', function( $scope, $element, $attrs ) {
    	$scope.percentages = [];

      /**
       * Given checklist breakdown count of new, open, pending and closed calculate %'s'
       * @return {Object} JSON object { "value": percentageValue, "type": info/warning/danger/success }
       */
    	$scope.projectChecklistStack = function() {
  			var counts = $scope.counts || { "new": 0, "open": 0, "awaiting": 0, "closed": 0 };

  			var total = counts.new + counts.open + counts.awaiting + counts.closed;
  			return [
  				{ "value": (100*counts.new/total), "type": "info" },
  				{ "value": (100*counts.open/total), "type": "warning" },
  				{ "value": (100*counts.awaiting/total), "type": "danger" },
  				{ "value": (100*counts.closed/total), "type": "success" }
  			];
  		};

		  $scope.percentages = $scope.projectChecklistStack();

    	$scope.$watch('counts', function( newVal, oldVal ){
    		$scope.percentages = $scope.projectChecklistStack();
    	});

    }]
  };
});