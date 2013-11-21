/**
 * @author : Lee Sinclair
 * date 17 Oct 2013
 */
angular.module('lawpal').controller( 'feedbackRequestCtrl', [ '$scope', '$modalInstance', 'attachment', 'feedbackItem', 'lawPalService',
	function ($scope, $modalInstance, attachment, feedbackItem, lawPalService ) {
		'use strict';
		$scope.attachment = attachment;
		$scope.feedbackItem = feedbackItem;
		$scope.oppositeUser = lawPalService.getOppositeUser();
		$scope.currentUser = lawPalService.getCurrentUser();

		$scope.data = {
			"comment": null,
			"complete": false
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