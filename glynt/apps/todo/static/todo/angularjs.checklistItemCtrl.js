/**
 * @description LawPal checklist item GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').controller( 'checklistItemCtrl', [ '$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', 'toaster', function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location, toaster ) {
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

	$scope.onFileSelect = function( files ) {
		var allowedTypes = [ "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-powerpoint", "application/vnd.ms-excel" ];
		files.each( function( file ){
			var fileType = file.type;
			if( fileType && allowedTypes.indexOf(fileType)>=0 ) {
				toaster.pop("info", "Starting file upload", file.name );
				lawPalService.attachFileChecklistItem( $scope.item, file );
			} else {
				toaster.pop("error", "File type not allowed", file.name );
			}
		});
	};

	/**
	 * Recieves messages that an attachment has been added
	 * @param  {Event} e	Broadcast event
	 * @param  {Object} data Data from the update event
	 */
	$scope.$on("todo.attachment.created", function( e, data ){
		if( typeof(data)==="object" && data.instance && data.instance.name == $scope.item.name ) {
			$scope.item.num_attachments = $scope.item.num_attachments?$scope.item.num_attachments++:1;
		}
	});
}]);