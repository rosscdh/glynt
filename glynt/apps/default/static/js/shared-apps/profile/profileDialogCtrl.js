/**
 * Manageteam dialog controller
 * @param  {Object} $scope         	Modal $scope
 * @param  {Object} $modalInstance 	Modal object instance, allow it to close itself etc
 * @param  {Array} team           	List of team users
 * @param  {Object} lawPalService 	List of methods used to acccess the LawPAl API
 * @param  {Object} $q				Promise library
 */
angular.module('lawpal').controller( 'profileDialogCtrl', [ '$scope', '$modalInstance', 'user',
	function ($scope, $modalInstance, user) {
		'use strict';
		$scope.user = user;

		$scope.ok = function () {
			$modalInstance.close($scope.user);
		};

		$scope.cancel = function () {
			$modalInstance.dismiss('cancel');
		};
	}]
);