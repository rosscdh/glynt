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
	/*
	$scope.working = {
		"discussions": {}
	};
	*/
	/*
	var working = {
		"dicussions": {}
	};
	*/

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

	$scope.contactUser = function( user ) {
			//window.location.href = "mailto://" + user.email, "email_window";
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
			"templateUrl": "manageTeam.html",
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

	$scope.currentUser = function() {
		return lawPalService.getCurrentUser();
	};

	$scope.isCurrentUser = function( upk ) {
		return lawPalService.getCurrentUser().pk===upk;
	};

	$scope.openProfileDialog = function( user ) {
		// profileDialogCtrl
		var modalInstance = $modal.open({
			"windowClass": "modal modal-show",
			"templateUrl": "profileDialog.html",
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