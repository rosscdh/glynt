/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').controller( 'ProjectCtrl', [ '$scope', 'lawPalService', 'lawPalUrls', '$location', '$anchorScroll', 'angularPusher', 'toaster', '$modal',
	function( $scope, lawPalService, lawPalUrls, $location, $anchorScroll, angularPusher, toaster, $modal ) {

	// Load project details
	$scope.project = {};
	$scope.data = {
		"project": {},
		"users": []
	};

	/**
	 * Load current project
	 */
	lawPalService.currentProject().then(
		function success( project ) {
			$scope.data.project = project;
			$scope.data.users = project.users;
			lawPalService.usernameSearch( $scope.data.users ).then(
				function success( results ) {
					console.log( "full users", $scope.data.users );
				},
				function error( err ) {

				}
			);
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
					return $scope.data.users;
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