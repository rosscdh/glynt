/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').controller( 'ProjectCtrl', [ '$scope', 'lawPalService', 'lawPalUrls', '$location', '$anchorScroll', 'angularPusher', 'toaster', '$modal',
	function( $scope, lawPalService, lawPalUrls, $location, $anchorScroll, angularPusher, toaster, $modal ) {

	// Load project details
	$scope.project = {
		"checklist": {}
	};

	/**
	 * Load current project
	 */
	lawPalService.currentProject().then(
		function success( project ) {
			$scope.project = project;
			$scope.project.users = $scope.project.users || [];
		},
		function error( err ) {
			toaster.pop( "warning", "Load error", "Unable to load project details" );
		}
	);

	/**
	 * Request team update by sending request to the API
	 * @param  {Object} updatedTeam New team object
	 */
	$scope.updateTeam = function( updatedTeam ) {
		console.log("updated team", updatedTeam );
		lawPalService.updateProjectTeam(updatedTeam).then(
			function success( response ) {
				toaster.pop( "success", "Update successful" );
			},
			function error( err ) {
				toaster.pop( "warning", "Update error", "Unable to update team details, please try again later" );
			}
		);
	};

	/**
	 * Open manage team dialog
	 */
	$scope.openManageTeamDialog = function() {
		var modalInstance = $modal.open({
			"windowClass": "modal modal-show",
			"templateUrl": 'manageTeam.html',
			"controller": 'manageTeamDialogCtrl',
			"resolve": {
				"team": function () {
					return $scope.project.users;
				}
			}
		});

		modalInstance.result.then(
			function ok( updatedTeam ) {
				$scope.updateTeam( updatedTeam );
			}, function cancel() {
				console.info('Modal dismissed at: ' + new Date());
			}
		);
	};

}]);