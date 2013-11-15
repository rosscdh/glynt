/**
 * @description LawPal checklist item GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').controller( 'checklistItemCtrl', [ '$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', "$modal", function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location, $modal ) {
	'use strict';
	/**
	 * Removes an item from the checklist
	 * @param  {Object} item JSON object representing a checklist item
	 */
	$scope.deleteItem = function() {
		var item = $scope.item;
		var promise = lawPalService.deleteChecklistItem( item );
		promise.then(
			function( results ) { /* Success */
				$scope.removeItemFromArray( item );
				//$scope.addAlert( "Item removed", "success" );
			},
			function( details ) { /* Error */
				$scope.addAlert( "Unable to remove item", "error" );
			}
		);
	};

	/**
	 * Determines the checklist item status of an item
	 * @return {String} status name
	 */
	$scope.getItemStatus = function() {
		var item = $scope.item;
		switch( item.status )
		{
			case 0: return "new";
			case 1: return "open";
			case 2: return "pending";
			case 3: return "resolved";
			case 4: return "closed";
		}

		return "unknown";
	};

	$scope.pendingFeedback = function() {
		var item = $scope.item;
		var slug = item.slug;

		return $scope.isChecklistItemAssigned(item)?"pending-feedback":"";
		
	};

	/**
	 * Determines the checklist item display status of an item
	 * @return {String} status name for display
	 */
	$scope.getItemDisplayStatus = function() {
		var item = $scope.item;
		switch( item.status )
		{
			case 0: return "New";
			case 1: return "Open";
			case 2: return "Pending";
			case 3: return "Resolved";
			case 4: return "Closed";
		}

		return "Unknown";
	};

	/**
	 * Determine if checklist item is assigned to the current user
	 * @return {Boolean} true if assigned
	 */
	$scope.getAssignedStatus = function() {
		var item = $scope.item;

		return $scope.isChecklistItemAssigned(item);
	};

	/**
	 * Show detail view of checklist item
	 */
	$scope.viewItem = function() {
		var item = $scope.item;
		var url = lawPalUrls.checklistItemDetailUrl( $scope.model.project.uuid, item, true );
		if( url )
			window.location.href = url;
	};

	/**
	 * Incepts the edit process
	 */
	$scope.editItem = function() {
		var item = $scope.item;
		// Get URL to request edit form HTML
		var url = lawPalUrls.checklistItemFormUrl( $scope.model.project.uuid, item );

		// Open edit form + dialog
		lawPalDialog.open( "Edit item", url, item ).then(
			function(result) { /* Success */
				/* Update model */
				if( result && result.name )  {
					item.name = result.name;

					$scope.saveItem( item );
				}
			},
			function(result) { /* Error */
				/* Update model */
				console.error(result);
			}
		);
	};

	/**
	 * Incepts the process of showing a modal to select team members
	 * @param  {Number} documentId      Document ID from the DB
	 * @param  {Array} possibleSignees Team member sof the project
	 */
	$scope.findSignees = function( documentId, possibleSignees ) {
		var modalInstance = $modal.open({
			"windowClass": "modal modal-show",
			"templateUrl": "template/lawpal/project/manageTeam.html",
			"controller": "manageTeamDialogCtrl",
			"resolve": {
				"team": function () {
					return possibleSignees;
				},
				"process": function() {
					return 'sign';
				}
			}
		});
		// Show dialog
		modalInstance.result.then(
			function ok( updatedTeam ) {
				var signees = [];
				if( updatedTeam && angular.isArray(updatedTeam) ) {
					// @ROSS Call 'lawPalService.updateProjectTeam(updatedTeam)' if you want to add people to the project if they have been added to the dialog
					signees = updatedTeam.filter( function(user){
						return user.is_signing;
					});
					lawPalService.assignSignees( documentId, signees );
				}
			}, function cancel() {
			}
		);
	};

	// Recieves message to display document
	// @TODO remove once this feature is merge into the single view
	$scope.$on( 'signDocument', function( ev, documentId ){
		// Load project team members
		lawPalService.currentProject().then(
			function success( project ) {
				var users = project.users;
				// Load ful user details
				lawPalService.usernameSearch( users ).then(
					function success() {
						$scope.findSignees(documentId, users);
					},
					function error() {
						$scope.findSignees(documentId, users);
					}
				);
			}
		);
		
	});
}]);