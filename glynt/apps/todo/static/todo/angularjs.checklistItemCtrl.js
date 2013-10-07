/**
 * @description LawPal checklist item GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').controller( 'checklistItemCtrl', [ '$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location ) {
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
}]);