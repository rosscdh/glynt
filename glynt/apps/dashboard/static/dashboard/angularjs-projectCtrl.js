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
		"users": [],
		"discussions": {},
		"discussionCategories": [ "issue", "discussion" ]
	};

	/**
	 * Load current project
	 */
	lawPalService.currentProject().then(
		function success( project ) {
			$scope.data.project = project;
			$scope.data.users = project.users;
			console.log( "users", $scope.data.users );
			$scope.loadDiscussions();
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

	$scope.loadDiscussions = function() {
		lawPalService.discussionList().then(
			function success( results ) {
				$scope.data.discussions = results;
			},
			function error( err ) {

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

	/**
	 * Open manage team dialog
	 */
	$scope.openDiscussionDialog = function() {
		var modalInstance = $modal.open({
			"windowClass": "modal modal-show",
			"templateUrl": 'newDiscussion.html',
			"controller": 'newDiscussionDialogCtrl'
		});

		modalInstance.result.then(
			function ok( message ) {
				$scope.newDiscussion( message );
			}, function cancel() {
				console.info('Modal dismissed at: ' + new Date());
			}
		);
	};

	$scope.newDiscussion = function( message ) {
		var userPk = lawPalService.getCurrentUser().pk;
		var messageDetails = {
			"object_pk": $scope.data.project.uuid, 
			"title": message.subject, 
			"comment": message.comment, 
			"user": userPk, 
			"content_type_id": lawPalService.projectContentTypeId(),
			"parent_id": null
		};

		console.log( "messageDetails", messageDetails );

		lawPalService.addDiscussion( messageDetails).then(
			function success( results ) {
				toaster.pop( "success", "Discussion item added" );
			},
			function error( err ) {
				toaster.pop( "warning", "Error", "Unable to post discussion item" );
			}
		);
	};

}]);