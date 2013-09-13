/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').controller( 'checklistCtrl', [ '$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', '$anchorScroll', 'angularPusher', 'toaster',
	function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location, $anchorScroll, angularPusher, toaster ) {

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

	$scope.config = {
		'pusher': {}
	}

	/*
	// @@ remove: quick async test and intermediate test to see if socket style updates will work
	setTimeout( function(){
		//debugger;
		$scope.model.feedbackRequests["1dfefcfe4f86d49254cd2ddd57331b17deff2295"] = [{"todo_slug":"1dfefcfe4f86d49254cd2ddd57331b17deff2295"}];
		$scope.$apply();
	}, 2000);
	*/

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

			if( options.pusher ) {
				$scope.config.pusher = options.pusher;
				var key = options.pusher.key;
				var channel = options.pusher.channel;
				console.log( $scope.config );
				angularPusher( key, channel );
			}
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
				/* Update model */
				if( result && result.name )  {
					$scope.saveItem( item, true );
				}
			},
			function(result) { /* Error */
				console.log( result );
			}
		);
	};

	/**
	 * Saves item through API
	 * @param  {Object} item JSON object representation of checklist item
	 */
	$scope.saveItem = function( item, isNewItem ) {
		if( item && item.name ) {
			/* Ensure project is allocated properly, esp for new items */
			var projectId = lawPalService.getProjectId();
			item.project = (projectId?projectId:item.project);
			/* Update item update */
			var promise = lawPalService.updateChecklistItem( item, $scope.config.pusher );
			promise.then(
				function( results ) { /* Success */
					$scope.addAlert( "Updating: " + item.name , (isNewItem?"success":"info"), "Saving changes" );
					var newItem = results;
					if( $scope.findItemIndex( newItem ) === -1 )
						{
							$scope.addItemToChecklist( newItem );
						}
				},
				function( details ) { /* Error */
					$scope.addAlert( "Unable to updated item", "error" );
				}
			);
		} else {

		}
	};

	$scope.addItemToChecklist = function( item ) {
		//
		$scope.model.checklist.push( item );
	};

	/**
	 * Watch for changed to feed Requests and update category details
	 */
	$scope.$watch('model.feedbackRequests', function(){
		// Create the list ok feedback_requests keys
		var itemSlugs = Object.keys($scope.model.feedbackRequests);

		if( angular.isArray(itemSlugs) ) {
			// For each key (slug) find the corresponding checklist item
			itemSlugs.forEach( function( slug ){
				var item = $scope.itemBySlug(slug);
				if( item && item.category ) {
					// Locate the corresponding category
					var category = $scope.model.categories.find( function(cat){
						return cat.label == item.category;
					});

					// Update number of assigned items in this category
					$scope.assignedPerCategory( category );
				}
			});
		}
	}, true);

	/**
	 * Increments a numeric value, representing the number of feedback items assigned to the current user
	 * @param  {Object} category Category object
	 *
	 * @todo : change count to an array of slugs, then use .length in view
	 */
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

		category.numAssigned = numAssigned;
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

	$scope.delayedAlertClose = function( alert ) {
		setTimeout( function() {
			var alerts = $scope.model.alerts;
			for(var i=0;i<alerts.length;i++) {
				if(alerts[i].timeStamp===alert.timeStamp) $scope.closeAlert( i );
			}

			$scope.$apply();
		}, 6000);
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
	$scope.addAlert = function( message, type, title ) {
		type = type || "info";
		if( typeof(title)==="undefined" ) {
			title = "Update";

			if( type=="Error" )
				title = "Error";
		}

		toaster.pop( type, title, message );
		/*
		alert = { "type": type, "message": message, "timeStamp": new Date().getTime() };

		$scope.model.alerts.push( alert );
		$("html, body").animate({ scrollTop: 0 }, 600);
		if( type==="success" ) {
			$scope.delayedAlertClose( alert );
		}
		*/
	};

	/**
	 * Untility function to remove item from checklist array (within this scope only)
	 * @param  {Object} item JSON object representing a checklist item
	 */
	$scope.removeItemFromArray = function( item ) {
		/*
		var index = $scope.findItemIndex( item );
		if( index !== null )
			$scope.model.checklist.splice( index, 1 );
		*/
		if( item ) {
			item.is_deleted = true;
		}
	};

	/**
	 * Locate a specific item in the checklist
	 * @param  {Object} item JSON object representing a checklist item
	 * @return {Number}      Index in the array or -1
	 */
	$scope.findItemIndex = function( item ) {
		var list = $scope.model.checklist;
		for( var i=0; i<list.length; i++) {
			if( list[i].slug === item.slug )
				return i;
		}

		return -1;
	};

	/**
	 * Locate a specific item in the checklist
	 * @param  {Object} item JSON object representing a checklist item
	 * @return {Number}      Index in the array or -1
	 */
	$scope.itemBySlug = function( slug ) {
		var list = $scope.model.checklist;
		for( var i=0; i<list.length; i++) {
			if( list[i].slug === slug )
				return list[i];
		}

		return null;
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

	/**
	 * Given a JSON object update an existing checklist item with new data
	 * @param  {Object} newData Object containg new data
	 */
	$scope.partialItemUpdate = function( newData, successMsg ){
		if( newData.slug ) {
			// find checklist item
			var checklistItem = $scope.itemBySlug( newData.slug );
			// update details
			if( typeof(checklistItem)==="object" ) {
				for( key in newData ) {
					checklistItem[key] = newData[key];
				}

				if( successMsg )
					$scope.addAlert( successMsg, "success", "Item updated" );

				// As this event has not been invoked through the normal angular channels update the scope
				$scope.$apply();
			}
		}
	};

	/**
	 * Recieves messages to update one of the existing checklist items
	 * @param  {Event} e    Broadcast event
	 * @param  {Object} data Data from the update event
	 */
	$scope.$on("todo.is_updated", function( e, data ){
		if( typeof(data)==="object" && data.instance ) {
			$scope.partialItemUpdate( data.instance, data.comment );
		}
	});

	/**
	 * Recieves mesages to remove items from the checklist (is_deleted = true ), in fact this is the same as an update message
	 * @param  {Event} e    Broadcast event
	 * @param  {Object} data Data from the new checklist item event
	 */
	$scope.$on("todo.is_deleted", function( e, data ){
		if( typeof(data)==="object" && data.instance ) {
			$scope.partialItemUpdate( data.instance, data.comment );
		}
	});

	/**
	 * Recieves messages to add new todo items
	 * @param  {Event} e    Broadcast event
	 * @param  {Object} data Data from the new checklist item event
	 */
	$scope.$on("todo.is_new", function( e, data ){
		var newItem = null;

		if( typeof(data)==="object" && data.instance ) {
			newItem = data.instance;

			if( $scope.findItemIndex( newItem ) === -1 )
				{
					$scope.addItemToChecklist( newItem );
					$scope.addAlert( newItem.name , "success", "New item" );
					$scope.$apply();
				}
		}
	});

	/**
	 * Recieves messages to modify the feedback status of checklist items
	 * @param  {Event} e    Broadcast event
	 * @param  {Object} data Data from the pusher, containing details about the action
	 */
	$scope.$on("action.created", function( e, data){
		var slug = null;
		var user = lawPalService.getCurrentUser();
		var action = {};

		if( user && data.status ) {
			if(data.status==="Pending"){
				// Feedback requested
				if( angular.isArray(data.assigned.to) && data.assigned.to.indexOf(user.pk)>=0) {
					slug = data.instance.slug||null;
					if( slug ) {
						// Add request for feedback
						$scope.model.feedbackRequests[slug] = [ { "todo_slug": slug} ];
						$scope.$apply();
					}
				}
			} else if( data.instance && data.instance.slug ) {
				//Feedback request removed
				slug = data.instance.slug||null;
				if( slug ) {
					// remove request from feedback object
					delete $scope.model.feedbackRequests[slug];
					$scope.$apply();
				}
			}
		}
	});

}]);

/**
 * This controller provides a bridget between the crispy form system and Angular
 * @param  {Object} $scope The modal forms scope object
 * @param  {dialog} dialog The dialog object, which contains references to the dom (e.g. dialog.modelEl), functions etc.
 */
function dialogController( $scope, dialog, dialogsModel ) {
	$scope.formData = {};

	var key;

    // hook the passed data to the popin scope
    for (key in dialogsModel) {
        $scope[key] = dialogsModel[key];
    }

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

		result = Object.clone(result);
		// Proceed to call the success function(s) with the newly calculated JSON data
		dialog.close( result, $scope );
	};
}