/**
 * @author : Lee Sinclair
 * date 17 Oct 2013
 */
angular.module('lawpal').controller( 'newDiscussionDialogCtrl', [ '$scope', '$modalInstance', 'parent',
	function ($scope, $modalInstance, parent) {
		'use strict';
		$scope.message = {
			"tags": [ "project", "discussion" ],
			"comment": null,
			"subject": null,
			"type": "discussion",
			"parent_id": parent && parent.id?parent.id:null
		};

		$scope.hasParent = parent && parent.id?true:false; // USed to determine if to show subject field
		$scope.title = !$scope.hasParent?"New discussion":"Respond"; // Dialog title
		
		/**
		 * User clicked the OK/Save button
		 */
		$scope.ok = function () {
			$modalInstance.close($scope.message);
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