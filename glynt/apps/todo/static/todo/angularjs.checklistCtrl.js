/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').controller( 'checklistCtrl', [ '$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', '$anchorScroll', function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location, $anchorScroll ) {

	// Data is stored within a JavaSCript object to avoid any nasty scope overides
	$scope.model = {
		'project': { 'uuid': null }, // Project details
		'categories': [], // Array of checklist categories
		'feedbackRequests': [],
		'alerts': [], // Used to display alerts at the top of the page
		'checklist': [], // Contains all checklist items
		'usertype': lawPalService.getUserType(), // is_lawyer, is_customer
		'showDeletedItems': false // If true deleted items are displayed also
	};

	// When the controller is ready ng-init calls initialise, with project details such as uuid
	$scope.initalise = function( options ){
		// If there are no options
		if(options) {
			// Set project details
			if( options.project ) {
				$scope.model.project = options.project;
			}
			// Load data
			$scope.loadCategories();
			$scope.loadChecklist();
			$scope.loadFeedbackRequests();
		} else {
			$scope.addAlert( "Unable to load items at this this, please try again later", "error" );
		}
	};

	/**
	 * Create new checklist item
	 * @param  {String} category Full category name, under which the new checklist item will be saved
	 */
	$scope.createItem = function( category ) {
		// open dialog
		var url = lawPalUrls.checklistItemCreateFormUrl( $scope.model.project.uuid, category.label );
		
		// Open edit form + dialog
		lawPalDialog.open( "Create item", url, {} ).then( 
			function(result) { /* Success */
				var item = result;
				var csrf = null;
				/* Update model */
				if( result && result.name )  {
					csrf= result.csrfmiddlewaretoken || null;
					delete item.csrf;

					$scope.saveItem( item, csrf );
				}
			}
		);
	};

	/**
	 * Saves item through API
	 * @param  {Object} item JSON object representation of checklist item
	 * @param  {String} csrf CSRF string for checking validity
	 */
	$scope.saveItem = function( item, csrf ) {
		if( item && item.name ) {
			/* Update item update */
			var promise = lawPalService.updateChecklistItem( item, csrf );
			promise.then(
				function( results ) { /* Success */
					$scope.addAlert( "Item updated", "success" );
				},
				function( details ) { /* Error */
					$scope.addAlert( "Unable to updated item", "error" );
				}
			);
		} else {

		}
	};

	$scope.assignedPerCategory = function( category ) {
		var numAssigned = 0;
		var categoryLabel = category.label.unescapeHTML(); /* sugar.js */
		var checkListItems = $scope.model.checklist.filter(function( item ){
			/* .filter is sugar.js */
			return item.category === categoryLabel;
		});
		var assigned;
		var item;

		for(var i=0;i<checkListItems.length;i++) {
			item = checkListItems[i];
			assigned = $scope.isChecklistItemAssigned( item );
			if(assigned)
				numAssigned++;
		}

		return numAssigned || ""; 
	};

	$scope.isChecklistItemAssigned = function( item ) {
		var assigned = false;
		var feedbackRequests = $scope.model.feedbackRequests;
		var itemSlug = item.slug || null;

		if( feedbackRequests[itemSlug] ) {
			assigned = (feedbackRequests[itemSlug].length>0);
		}

		return assigned;
	};

	/**
	 * Remove alert from display
	 * @param  {Number} index Index of alert to remove
	 */
	$scope.closeAlert = function( index ) {
		$scope.model.alerts.splice(index, 1);
	};

	/**
	 * Display alert on page and scroll to it
	 * @param {String} message Message to display
	 * @param {String} type    type of alert to display e.g. error, success, worning, info
	 */
	$scope.addAlert = function( message, type ) {
		type = type || "info";
		$scope.model.alerts.push({ "type": type, "message": message });
		$("html, body").animate({ scrollTop: 0 }, 600);
	};

	/**
	 * Untility function to remove item from checklist array (within this scope only)
	 * @param  {Object} item JSON object representing a checklist item
	 */
	$scope.removeItemFromArray = function( item ) {
		var index = $scope.findItemIndex( item );
		if( index !== null )
			$scope.model.checklist.splice( index, 1 );
	};

	/**
	 * Locate a specific item in the checklist
	 * @param  {Object} item JSON object representing a checklist item
	 * @return {Number}      Index in the array or -1
	 */
	$scope.findItemIndex = function( item ) {
		var list = $scope.model.checklist;
		for( var i=0; i<list.length; i++) {
			if( list[i].id === item.id )
				return i;
		}

		return -1;
	};

	/**
	 * Load categories from service
	 */
	$scope.loadCategories = function() {
		// Load initial categories
		var promise = lawPalService.getCategories().then( 
			function( results ) { /* Success */
				$scope.model.categories = results;
			},
			function( details ) { /* Error */
			}
		);
	};

	/**
	 * Load checklist items using service
	 */
	$scope.loadChecklist = function() {
		// Load initial checklist items
		var promise = lawPalService.getChecklist( 'sort_position_by_cat' );
		promise.then( 
			function( results ) { /* Success */
				$scope.model.checklist = results;
			},
			function( details ) { /* Error */
			}
		);
	};

	$scope.loadFeedbackRequests = function() {
		// Load initial checklist items
		var promise = lawPalService.getFeedbackRequests();
		promise.then( 
			function( results ) { /* Success */
				$scope.model.feedbackRequests = results;
			},
			function( details ) { /* Error */
			}
		);
	};

}]);

/**
 * This controller provides a bridget between the crispy form system and Angular
 * @param  {Object} $scope The modal forms scope object
 * @param  {dialog} dialog The dialog object, which contains references to the dom (e.g. dialog.modelEl), functions etc.
 */
function dialogController( $scope, dialog ) {
	$scope.formData = {};

	/**
	 * Close the modal dialog no further action required
	 */
	$scope.close = function() {
		dialog.close( null, $scope );
	};

	$scope.save = function( nodeId ) {
		// result needs to be built up in order to map the form data to JSON
		var result = {};

		// The below code is writter such as to provide the critical bridge between static HTML forms and AngularJS objects
		$.map( $(nodeId + " form").serializeArray(), function( item, i ) {
			result[ item.name ] = item.value;
		});

		// Proceed to call the success function(s) with the newly calculated JSON data
		dialog.close( result, $scope );
	};
}