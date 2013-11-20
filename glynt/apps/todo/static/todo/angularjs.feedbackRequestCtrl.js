/**
 * @author : Lee Sinclair
 * date 17 Oct 2013
 */
angular.module('lawpal').controller( 'feedbackRequestCtrl', [ '$scope', '$modalInstance', 'attachment',
	function ($scope, $modalInstance, attachment) {
		'use strict';
		$scope.data = {
			"comment": null,
		};

		/**
		 * User clicked the OK/Save button
		 */
		$scope.ok = function () {
			$modalInstance.close($scope.data);
		};

		/**
		 * User clicked the cancel button, reset team to original state
		 * @return {[type]} [description]
		 */
		$scope.cancel = function () {
			$modalInstance.dismiss('cancel');
		};
	}]
);