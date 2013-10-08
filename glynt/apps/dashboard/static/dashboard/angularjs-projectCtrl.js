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
			$scope.project.checklist.percentageStack = $scope.projectChecklistStack();
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

	$scope.projectChecklistStack = function() {
		if(!$scope.project.checklist)
			$scope.project.checklist = {};
		
		var counts = $scope.project.checklist.counts || { "new": 0, "open": 0, "awaiting": 0, "closed": 0 };

		var total = counts.new + counts.open + counts.awaiting + counts.closed;
		return [
			{ "value": (100*counts.new/total), "type": "info" },
			{ "value": (100*counts.open/total), "type": "warning" },
			{ "value": (100*counts.awaiting/total), "type": "danger" },
			{ "value": (100*counts.closed/total), "type": "success" }
		];
	};

	$scope.project.checklist.percentageStack = $scope.projectChecklistStack();

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