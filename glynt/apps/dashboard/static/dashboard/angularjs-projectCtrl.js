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


angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/project/manageTeam.html",
		'<div class="modal-dialog">\n'+
		'	<div class="modal-content">\n'+
		'		<div class="modal-header">\n'+
		'			<h3>Project team</h3>\n'+
		'			<p>Primary project contacts can add and remove team members</p>\n'+
		'		</div>\n'+
		'		<div class="modal-body">\n'+
		'			<div class="row vcard team-member {[{isRemovedClass(user)}]} user-{[{user.username}]}" ng-repeat="user in team">\n'+
		'				<div class="col col-lg-12">\n'+
		'					<div class="col col-lg-1 photo">\n'+
		'						<img ng-src="{[{user.photo}]}"/>\n'+
		'					</div>\n'+
		'					<div class="col col-lg-7 details">\n'+
		'						<h5 class="fn">{[{user.full_name}]}<span ng-show="user.is_authenticated"> (you)</span></h5>\n'+
		'						<h6 class="company"><a href="/profile/{[{user.company.slug}]}">{[{user.company.name}]}</a></h6>\n'+
		'					</div>\n'+
		'					<div class="col col-lg-4 details">\n'+
		'						<p class="action pull-right" ng-show="canRemove(user)">\n'+
		'							<a href="javascript:;" ng-click="removeUser(user)" ng-show="!user.is_deleted" class="remove-link"><i class="icon icon-remove text-danger"></i> Remove</a>\n'+
		'							<a href="javascript:;" ng-click="removeUser(user)" ng-show="user.is_deleted" class="undo-remove-link"><i class="icon icon-undo"></i> Undo remove</a>\n'+
		'						</p>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'\n'+
		'			</div><!-- row //-->\n'+
		'			<form class="form-search form-horizontal">\n'+
		'				<div class="row">\n'+
		'					<div class="col col-lg-12">\n'+
		'						<h4>Add someone</h4>\n'+
		'						<p class="help-block">You can only add people that have registered with LawPal at this time.</p>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'				<div class="row">\n'+
		'					<div class="col col-lg-8">\n'+
		'						<input \n'+
		'							type="text" \n'+
		'							name="email"\n'+
		'							autocomplete="off"\n'+
		'							class="form-control search-query pull-left searching-{[{searchingEmail}]}" \n'+
		'							placeholder="Email address" \n'+
		'							typeahead="item.email for item in searchEmails($viewValue)" \n'+
		'							typeahead-wait-ms="600"\n'+
		'							typeahead-min-length="3"\n'+
		'							typeahead-loading="searchingEmail"\n'+
		'							ng-model="searchAttrs.selectedEmail" />\n'+
		'					</div>\n'+
		'					<div class="col col-lg-4">\n'+
		'						<button type="submit" class="btn btn-default" ng-click="addToProject(searchAttrs.selectedEmail, emailSearchResults)" ng-disabled="searchingEmail"><i class="icon {[{emailSearchClass(searchingEmail)}]}"></i> Add to project</button>\n'+
		'					</div>\n'+
		'						\n'+
		'				</div>\n'+
		'			</form>\n'+
		'		</div>\n'+
		'		<div class="modal-footer">\n'+
		'			<button class="btn btn-default" ng-click="cancel()">Cancel</button>\n'+
		'			<button class="btn btn-primary" ng-click="ok()">Save</button>\n'+
		'		</div>\n'+
		'	</div>\n'+
		'</div>'
	);
}]);