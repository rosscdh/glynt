/**
 * Primary action directive
 * @author : Lee Sinclair
 * date 3- Oct 2013
 */
angular.module('lawpal').directive('projectPrimaryAction', [ function ( ) {
	'use strict';
	return {
		"restrict": "AC",
		"templateUrl":'template/lawpal/project/primaryAction.html',
		"scope": {
			"counts": "=",
			"projectUuid": "=projectUuid",
			"baseUrl": "=baseUrl"
		},
		"link": function (/*scope, iElement, iAttrs*/) {
		},
		"controller": [ '$scope', '$element', '$attrs', function( $scope/*, $element, $attrs*/ ) {
			console.log( "s", $scope );
			var counts = $scope.counts;
			$scope.weightings = [
				{ "name": "awaiting_feedback_from_user", "weighting": ( counts.awaiting_feedback_from_user?1:0 ) * 5, "value": counts.awaiting_feedback_from_user, "label": "Feedback" },
				{ "name": "pending", "weighting": ( counts.pending?1:0 ) * 4, value: counts.pending, "label": "Pending" },
				{ "name": "open", "weighting": ( counts.open?1:0 ) * 3, "value": counts.open, "label": "Open" },
				{ "name": "new", "weighting": ( counts.new?1:0 ) * 2, "value": counts.new, "label": "New" },
				{ "name": "closed", "weighting": ( counts.closed?1:0 ) * 1, "value": counts.closed, "label": "Closed" }
			];

			$scope.weightings = $scope.weightings.sort( function( item1, item2 ){
				return item1.weighting < item2.weighting;
			});

			console.log($scope.weightings);

			$scope.topPriority = $scope.weightings[0];
			$scope.topPriority.url = $scope.baseUrl + $scope.projectUuid + '/checklist/#' + $scope.topPriority.label;

		}]
	};
}]);