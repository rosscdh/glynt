/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module("lawpal").controller( "ProjectCtrl", [ "$scope", "lawPalService", "lawPalUrls", "$location", "$anchorScroll", "angularPusher", "toaster", "$modal",
	function( $scope, lawPalService, lawPalUrls, $location, $anchorScroll, angularPusher, toaster, $modal ) {
	"use strict";
	// Load project details
	$scope.project = {};
	$scope.data = {
		"project": {},
		"users": [],
		"discussions": {},
		"discussionCategories": [ /*"issue", */"discussion" ]
	};

	$scope.loading = {
		"project": true,
		"users": true
	};

	/**
	 * Load current project
	 */
	lawPalService.currentProject().then(
		function success( project ) {
			$scope.data.project = project;
			$scope.data.users = project.users;
			$scope.loadDiscussions();
			$scope.loading.project = false;
			lawPalService.usernameSearch( $scope.data.users ).then(
				function success() {
					$scope.loading.users = false;
				},
				function error() {
					$scope.loading.users = false;
				}
			);
		},
		function error() {
			toaster.pop( "warning", "Load error", "Unable to load project details" );
		}
	);

	/**
	 * Show profile dialog
	 * @param  {Object} user User object
	 */
	$scope.contactUser = function( user ) {
		$scope.openProfileDialog( user );
	};

	/**
	 * Request team update by sending request to the API
	 * @param  {Object} updatedTeam New team object
	 */
	$scope.updateTeam = function( updatedTeam ) {
		lawPalService.updateProjectTeam(updatedTeam).then(
			function success( /*response*/ ) {
				toaster.pop( "success", "Update successful" );
			},
			function error( /*err*/ ) {
				toaster.pop( "warning", "Update error", "Unable to update team details, please try again later" );
			}
		);
	};

	/**
	 * Load discussions for the current project
	 */
	$scope.loadDiscussions = function() {
		lawPalService.discussionList().then(
			function success( results ) {
				$scope.data.discussions = results;
				//$scope.generateWorkingDiscussionData();
			},
			function error( /*err*/ ) { }
		);
	};

	/**
	 * Open manage team dialog
	 */
	$scope.openManageTeamDialog = function() {
		var modalInstance = $modal.open({
			"windowClass": "modal modal-show",
			"templateUrl": "template/lawpal/project/manageTeam.html",
			"controller": "manageTeamDialogCtrl",
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
			}
		);
	};

	/**
	 * Get current user object
	 * @return {Object} User
	 */
	$scope.currentUser = function() {
		return lawPalService.getCurrentUser();
	};

	/**
	 * Given a user_pk is that the pk of the current user?
	 * @param  {Number}  upk User PK
	 * @return {Boolean}     true if pk represents the current user
	 */
	$scope.isCurrentUser = function( upk ) {
		return lawPalService.getCurrentUser().pk===upk;
	};

	/**
	 * Display user details
	 * @param  {Object} user user object
	 */
	$scope.openProfileDialog = function( user ) {
		// profileDialogCtrl
		var modalInstance = $modal.open({
			"windowClass": "modal modal-show",
			"templateUrl": "template/lawpal/project/profileDialog.html",
			"controller": "profileDialogCtrl",
			"resolve": {
				"user": function () {
					return user;
				}
			}
		});

		modalInstance.result.then(
			function ok() {
				
			}, function cancel() {
			}
		);
	};

}]);