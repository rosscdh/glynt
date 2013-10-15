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

	$scope.working = {
		"discussions": {}
	};

	var working = {
		"dicussions": {}
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
				$scope.generateWorkingDiscussionData();
			},
			function error( /*err*/ ) { }
		);
	};

	function discussionLookup( obj ) {
		if(angular.isArray(obj)) {
			for (var i=0;i<obj.length;i++) {
				working.dicussions[obj[i].id] = obj[i];
			}
		}
		else {
			return working.dicussions[obj]||null;
		}
	}

	$scope.generateWorkingDiscussionData = function( parentId, childId ) {
		var discussionItem;
		var data = [];

		discussionLookup($scope.data.discussions);
		
		if( !angular.isArray($scope.data.discussions) ) {
			return [];
		}

		var dis = $scope.data.discussions.filter(
			function( item ) {
				return item.parent_id===null;
			}
		);

		for( var i=0; i<dis.length;i++) {
			if( parentId && childId && parentId===dis[i].id ) {
				dis[i].last_child = childId;
			}
			discussionItem = { "original": dis[i], "latest": discussionLookup(dis[i].last_child) || dis[i] };

			data.push(discussionItem);
		}

		$scope.working.discussions = data; //$scope.data.discussions;
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

	/**
	 * Open manage team dialog
	 */
	$scope.openDiscussionDialog = function( parent ) {
		var modalInstance = $modal.open({
			"windowClass": "modal modal-show",
			"templateUrl": "newDiscussion.html",
			"controller": "newDiscussionDialogCtrl",
			"resolve": {
				"parent": function(){
					return parent;
				}
			}
		});

		modalInstance.result.then(
			function ok( message ) {
				$scope.newDiscussion( message );
			}, function cancel() {
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
			"parent_id": message.parent_id
		};

		lawPalService.addDiscussion( messageDetails).then(
			function success( response ) {
				$scope.data.discussions.push( response );
				toaster.pop( "success", "Discussion item added" );
				$scope.generateWorkingDiscussionData(  message.parent_id, response.id );
			},
			function error( /*err*/ ) {
				toaster.pop( "warning", "Error", "Unable to post discussion item" );
			}
		);
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