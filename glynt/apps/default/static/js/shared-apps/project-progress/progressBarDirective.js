/**
 * Displays the percentage comparison between new, open, pending and closed checklist items
 * @return {Object} AngularJS directive
 */
angular.module('lawpal').directive('projectProgressBar', function () {
	'use strict';
	return {
		"restrict": "AC",
		"template":
			'<progress percent=\"percentages\" auto-type=\"true\">{[{percentages|json}]}</progress>'+
			'<div class="row" ng-show="showLegend">'+
				'<h5 class="text-info col-lg-3">{[{counts.new}]} New</h5>'+
				'<h5 class="text-warning col-lg-3">{[{counts.open}]} Open</h5>'+
				'<h5 class="text-danger col-lg-3">{[{counts.awaiting}]} Pending</h5>'+
				'<h5 class="text-success col-lg-3">{[{counts.closed}]} Closed</h5>'+
				'</div>',
		"scope": {
			"counts": "=counts",
			"show": "=show",
			'showLegend': "=showLegend"
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
				var counts = $scope.counts || { "new": 0, "open": 0, "awaiting": 0, "closed": 0, "pending": 0 };
				var show = ($attrs.show || "new,open,pending,closed").replace(/'/g,'').split(",");

				if( !counts.awaiting ) {
					counts.awaiting = counts.awaiting || counts.awaiting_feedback_from_user || 0;
				}

				var total = counts.total || counts.new + counts.open + counts.awaiting + counts.closed;

				var result = [];
				if( show.indexOf("new")>=0 ) {
					result.push( { "value": (100*counts.new/total), "type": "muted", "label": "new" } );
				}

				if( show.indexOf("open")>=0 ) {
					result.push( { "value": (100*counts.open/total), "type": "info", "label": "open" } );
				}

				if( show.indexOf("awaiting_feedback_from_user")>=0 ) {
					result.push( { "value": (100*counts.awaiting/total), "type": "danger", "label": "feedback" } );
				}

				if( show.indexOf("pending")>=0 ) {
					result.push( { "value": (100*(counts.pending-counts.awaiting)/total), "type": "warning", "label": "pending" } );
				}

				if( show.indexOf("closed")>=0 ) {
					result.push( { "value": (100*counts.closed/total), "type": "success", "label": "closed" } );
				}

				console.log( result );
				return result;
			};

			$scope.percentages = $scope.projectChecklistStack();

			$scope.$watch('counts', function( newVal, oldVal ){
				$scope.percentages = $scope.projectChecklistStack();
			});

		}]
	};
});