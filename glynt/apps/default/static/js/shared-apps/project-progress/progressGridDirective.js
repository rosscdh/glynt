/**
 * Displays the percentage comparison between new, open, pending and closed checklist items
 * @return {Object} AngularJS directive
 */
angular.module('lawpal').directive('projectProgressGrid', function () {
	'use strict';
	return {
		"restrict": "AC",
		"template":
				'<div class="col-lg-2" tooltip="New"><button class="btn btn-block btn-link"><span class="text-muted">{[{counts.new}]}</span></button></div>'+
				'<div class="col-lg-2" tooltip="Open"><button class="btn btn-block btn-link">{[{counts.open}]}</button></div>'+
				'<div class="col-lg-2" tooltip="Your Feedback required"><button class="btn btn-block btn-link"><span class="text-danger">{[{counts.awaiting}]}</span></button></div>'+
				'<div class="col-lg-2" tooltip="Feedback required"><button class="btn btn-block btn-link"><span class="text-warning">{[{counts.pending}]}</span></button></div>'+
				'<div class="col-lg-2" tooltip="Closed"><button class="btn btn-block btn-link"><span class="text-success">{[{counts.closed}]}</span></button></div>'+
				'',
		"scope": {
			"counts": "=counts",
			"show": "=show"
		},
		"link": function (scope, iElement, iAttrs) {
			console.log("link", scope.counts);
		},
		"controller": [ '$scope', '$element', '$attrs', function( $scope, $element, $attrs ) {
			$scope.adjustedCounts = {};

			/**
			 * Given checklist breakdown count of new, open, pending and closed calculate %'s'
			 * @return {Object} JSON object { "value": percentageValue, "type": info/warning/danger/success }
			 */
			$scope.adjustCounts = function() {
				var counts = $scope.counts || { "new": 0, "open": 0, "awaiting": 0, "closed": 0, "pending": 0 };

				if( !counts.awaiting ) {
					counts.awaiting = counts.awaiting_feedback_from_user || 0;
				}

				var total = $scope.counts.total || counts.new + counts.open + counts.awaiting + counts.closed;

				var result = {
					"new": counts.new,
					"open": counts.open,
					"feedback": counts.awaiting,
					"pending": counts.pending,
					"closed": counts.closed
				};
				return result;
			};

			$scope.calculateDisplays = function( ) {
				var showArr = ($attrs.show || "new,open,pending,feedback,closed").replace(/'/g,'').split(",");
				var show = {};
				for(var i=0;i<showArr;i++) {
					show[ showArr[i] ] = true;
				}

				$scope.show = show;
			};

			$scope.adjustedCounts = $scope.adjustCounts($scope.counts);
			$scope.adjustedCounts = $scope.calculateDisplays();

			$scope.$watch('counts', function( newVal, oldVal ){
				$scope.adjustedCounts = $scope.adjustCounts(nv);
			});

		}]
	};
});