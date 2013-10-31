/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module("lawpal").controller( "projectsOverviewCtrl", [ "$scope", "lawPalService", "lawPalUrls", "$location", "$anchorScroll", "angularPusher", "toaster", "$modal", "$window",
	function( $scope, lawPalService, lawPalUrls, $location, $anchorScroll, angularPusher, toaster, $modal, $window ) {
	"use strict";
	// Load project details
	$scope.project = {};
	$scope.data = {
		"projects": [],
		"users": [],
		"discussions": {},
		"discussionCategories": [ /*"issue", */"discussion" ]
	};

	/**
	 * Load an array of projects for which the current user has an association
	 */
	$scope.loadProjects = function() {
		lawPalService.getUsersProjects().then(
			function success( projects ) {
				// Calculate user Engagement string for easier template usage
				for(var i=0;i<projects.length;i++) {
					projects[i].currentUserEngagement = $scope.engagement(projects[i]);
					projects[i].discussions = [];
					projects[i].discussionItemNum = 0;
					$scope.loadProjectDiscussions( projects[i] );
				}
				
				$scope.data.projects = projects;
			}
		);
	};

	/**
	 * Load discussions for a speicfic project
	 * @param  {Object} project project object
	 */
	$scope.loadProjectDiscussions = function( project ) {
		var user = lawPalService.getCurrentUser();
		lawPalService.getRecentDiscussions( project.id, user.pk ).then(
			function success( discussions ) {
				project.discussions = discussions;
			}
		);
	};

	/**
	 * Determine the project engagement status for a specific project for the current user
	 * @param  {Object} project Project Object
	 * @return {String}         'Engaged' / 'Proposed'
	 */
	$scope.engagement = function( project ) {
		var engagementStatus = "Proposed";
		var user = lawPalService.getCurrentUser();

		var lawyers = project.lawyers || [];
		engagementStatus = lawyers.filter( function( lawyer ){
			return lawyer.user_pk===user.pk;
		})[0].status.name;

		return engagementStatus;
	};

	$scope.loadProjects();

	/**
	 * Display profile details
	 * @param  {Object} user User profile object
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

	/**
	 * Display checklist view
	 * @param  {String} baseUrl Base URL string
	 * @param  {Object} project Project object
	 */
	$scope.viewChecklist = function( baseUrl, project ) {
		$window.location.href = baseUrl + project.uuid + '/';
	};
}]);
