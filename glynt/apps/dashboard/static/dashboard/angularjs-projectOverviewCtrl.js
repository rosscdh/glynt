/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module("lawpal").controller( "projectsOverviewCtrl", [ "$scope", "lawPalService", "lawPalUrls", "$location", "$anchorScroll", "angularPusher", "toaster", "$modal",
	function( $scope, lawPalService, lawPalUrls, $location, $anchorScroll, angularPusher, toaster, $modal ) {
	"use strict";
	// Load project details
	$scope.project = {};
	$scope.data = {
		"projects": [],
		"users": [],
		"discussions": {},
		"discussionCategories": [ /*"issue", */"discussion" ]
	};

	$scope.loadProjects = function() {
		var projects = LawPal.overview.projects.results;
		for(var i=0;i<projects.length;i++) {
			projects[i].currentUserEngagement = $scope.engagement(projects[i]);
		}
		
		return projects;
	};

	$scope.contactUser = function( user ) {
			//window.location.href = "mailto://" + user.email, "email_window";
			$scope.openProfileDialog( user );
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

	$scope.currentUser = function() {
		return lawPalService.getCurrentUser();
	};

	$scope.isCurrentUser = function( upk ) {
		return lawPalService.getCurrentUser().pk===upk;
	};

	$scope.engagement = function( project ) {
		var engagementStatus = "Proposed";
		var user = LawPal.user;

		var lawyers = project.lawyers || [];
		engagementStatus = lawyers.filter( function( lawyer ){
			return lawyer.user_pk===user.pk;
		})[0].status.name;

		return engagementStatus;
	};

	$scope.data.projects = $scope.loadProjects();
	debugger;

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
/*
angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/project/manageTeam.html",
		''
	);
}]);
*/