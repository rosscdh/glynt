/**
 * @description LawPal checklist GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').controller( 'checklistCtrl', [ '$scope', '$rootScope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', 'deleteCategoryConfirmDialog', '$location', '$anchorScroll', 'angularPusher', 'toaster',
	function( $scope, $rootScope, lawPalService, lawPalUrls, lawPalDialog, deleteCategoryConfirmDialog, $location, $anchorScroll, angularPusher, toaster ) {
		'use strict';
		$scope.loadStatus = 0;

		/**
		 * Data is stored within a JavaSCript object to avoid any nasty scope overides
		 * @type {Object} project		Project details
		 * @type {Array} categories	Array of category objects (from API directly), the JSON object contains:
		 *								{String} slug, {String} label

		 * @type {Array} checklist		Array of checklist items (from API directly), the JSON object contains:
		 *						{String} category, {String} date_created. {String} date due, {String} date modified
		 *						{String} description, {String} display_status, {String} id, {Boolean} is_deleted
		 *						{String} name, {Number} project, {String} slug, {Number} sort_position
		 *						{Number} sort_position_by_cat, {Number} status
		 * @type
		 */
		$scope.model = {
			'project': { 'uuid': null }, // 
			'categories': [],
			'filters': {
				'on': false,
				'category': {
					'label': null,
					'buttonLabel': 'Category'
				} 
			},
			'checklist': [], // from API: Contains all checklist items
			'selectedAttachments': [],
			'workingChecklist': [],
			/*'data': [],	// Working copy of the data*/
			'feedbackRequests': [],
			'alerts': [], // Used to display alerts at the top of the page
			'usertype': lawPalService.getUserType(), // is_lawyer, is_customer
			'showDeletedItems': false, // If true deleted items are displayed also
			'ignoreChecklistUpdate': false
		};

		$scope.categories = [];

		$scope.config = {
			'pusher': {},
			'categorySort': {
				'axis': 'y'
			 },
			'itemSort': {
				'filtered': false,
				'axis': 'y',
				'updatePending': false
			 }
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

				if( options.pusher ) {
					$scope.config.pusher = options.pusher;
					var key = options.pusher.key;
					var channel = options.pusher.channel;
					angularPusher( key, channel );
				}
			} else {
				$scope.addAlert( "Unable to load items at this this, please try again later", "warning", "Error!" );
			}
		};

		$scope.categoryFilter = function( category ) {
			var checklist = $scope.model.checklist;
			//debugger;
			if( typeof(category)!=='undefined') {
				// Get button label
				$scope.model.filters.category = category || {};
				$scope.model.filters.category.buttonLabel = category?category.label:'Category';
				// If a category has been provided, then filter the working checklist
				if( category ) {
					var workingChecklist = [];
					// filter checklist checklist
					for(var i=0;i<checklist.length;i++) {
						if(checklist[i].category===category.label) {
							workingChecklist.push( checklist[i] );
						}
					}
					$scope.model.workingChecklist = $scope.getUndeleted(workingChecklist);
					// Ignore this change to the working checklist
					$scope.model.filters.on = true;
				} else {
					// Reset to full checklist
					$scope.model.workingChecklist = $scope.getUndeleted(checklist);
					//$scope.model.workingChecklist = checklist;
					$scope.model.filters.on = false;
				}

				$scope.model.ignoreChecklistUpdate = true;
				
			} else {
				return $scope.model.filters.category;
			}
		};

		$scope.updateWorkingList = function() {
			var checklist = $scope.model.checklist;
			if($scope.model.filters.on) {
				if($scope.model.filters.category.label) {
					$scope.categoryFilter($scope.model.filters.category);
				} else {
					$scope.model.workingChecklist = $scope.getUndeleted(checklist);
				}
			} else {
				$scope.model.workingChecklist = $scope.getUndeleted(checklist);
			}
		};

		$scope.getUndeleted = function( checklist ) {
			var workingChecklist = [];
			for(var i=0;i<checklist.length;i++) {
				if( checklist[i].is_deleted!==true) {
					workingChecklist.push( checklist[i] );
				}
			}

			return workingChecklist;
		};
		/**
		 * Create new checklist category, opens a dialog asking for a category name
		 */
		$scope.createCategory = function() {
			// open dialog
			var url = lawPalUrls.checklistCategoryCreateFormUrl( $scope.model.project.uuid );

			// Open edit form + dialog
			lawPalDialog.open( "Create category", url, {} ).then(
				function(result) { /* Success */
					var item = result;
					var promise;
					
					if( result && result.category )  {
						/* Data is valied enough */
						promise = lawPalService.addCategory( item, true );
						promise.then(
							function( response ) { /* success */
								$scope.model.categories.push( response ); /* required data : { "label": String, "slug": String } */
								$scope.insertCategory( response, [] );
								$scope.addAlert( "New category added", "success", "Success!" );
							},
							function( /*error*/ ) { /* error */
								$scope.addAlert( "Unable to add category", "warning", "Error!" );
							}
						);
					}
				},
				function(result) { /* Error */
					console.log( result );
				}
			);
		};

		/**
		 * Remove category, 
		 * @param {Object} category JSON object containing the category to be deleted
		 * @return {Object} category object
		 */
		$scope.removeCategory = function( category ) {
			if( category && category.items && category.items.length>0) {
				deleteCategoryConfirmDialog.open( category ).then(
					function( /*cat*/ ) {
						/* Yes delete */
						lawPalService.removeCategory( category ).then(
							function(){
								var index = $scope.findCategoryIndex(category.info.label);
								/* Use index >=0 instead of is true */
								if(index>=0) {
									$scope.categories.splice(index, 1);
								}

								$scope.addAlert( "Category removed", "success", "Success!" );
							},
							function(){
								$scope.addAlert( "Unable to remove category", "warning", "Error!" );
							}
						);
					}
				);
			} else {
				/* No checklist items: just delete it */
				lawPalService.removeCategory( category ).then(
					function(){
						var index = $scope.findCategoryIndex(category.info.label);
						if(index>=0) {
							$scope.categories.splice(index, 1);
						}

						$scope.addAlert( "Category removed", "success", "Success!" );
					},
					function(){
						$scope.addAlert( "Unable to remove category", "warning", "Error!" );
					}
				);
			}
		};

		/**
		 * Create new checklist item
		 * @param  {String} category Full category name, under which the new checklist item will be saved
		 */
		$scope.createItem = function( category ) {
			// open dialog
			var url = lawPalUrls.checklistItemCreateFormUrl( $scope.model.project.uuid, category.label || 'General' );
			
			// Open edit form + dialog
			lawPalDialog.open( "Create item", url, {} ).then(
				function(result) { /* Success */
					var item = result;
					// Put item at bottom of list in sort order
					item.sort_position = $scope.model.checklist.length + 1;

					/* Start save process i.e. POST to API */
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
						$scope.updateWorkingList();
					},
					function( /*details*/ ) { /* Error */
						$scope.addAlert( "Unable to updated item", "warning", "Error!" );
					}
				);
			} else {

			}
		};
		/**
		 * Adds a checklist item to the checklist
		 * @param {Object} item item to add to checklist array
		 */
		$scope.addItemToChecklist = function( item ) {
			// 1. Push item into main checklist array
			$scope.model.checklist.push( item );

			// 2. Add item into 
			var category = $scope.findCategoryByLabel( item.category );
			category.items.push( item );
		};

		/**
		 * Given a label find the working category JSON object
		 * @param  {String} label category label
		 * @return {Object}		category object
		 */
		$scope.findCategoryByLabel = function( label ) {
			var categories = $scope.categories;
			var category = {
				"info": { "label": label },
				"items": []
			};
			angular.forEach( categories, function( cat/*, index*/ ) {
				if( cat.info.label == label ) {
					category = cat;
				}
			});

			return category;
		};

		/**
		 * Given a label find index of a category
		 * @param  {String} label category label
		 * @return {Number}		index of category object
		 */
		$scope.findCategoryIndex = function( label ) {
			var categories = $scope.categories;
			var i = -1;
			angular.forEach( categories, function( cat, index ) {
				if( cat.info.label == label ) {
					i = index;
				}
			});
			return i;
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

		/**
		 * Returns true if a specific checklist item
		 * @param  {Object}  item JSON checklist item
		 * @return {Boolean}		true if has assigned items
		 */
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
		 * @param {String} type	type of alert to display e.g. error, success, worning, info
		 */
		$scope.addAlert = function( message, type, title ) {
			type = type || "info";
			if( typeof(title)==="undefined" ) {
				title = "Update";

				if( type=="Error" )
					title = "Error";
			}

			toaster.pop( type, title, message );
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
			$rootScope.$broadcast('close-sidebar', 1);
			$scope.updateWorkingList();
		};

		/**
		 * Locate a specific item in the checklist
		 * @param  {Object} item JSON object representing a checklist item
		 * @return {Number}		Index in the array or -1
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
		 * @return {Number}		Index in the array or -1
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
			lawPalService.getCategories().then(
				function( results ) { /* Success */
					$scope.model.categories = results;
					//$scope.mergeChecklistCategories();
				}
			);
		};
		/*
		$scope.mergeChecklistCategories = function() {
			var categories, checklist;
			$scope.loadStatus++;
			if( $scope.loadStatus === 2) {
				categories = $scope.model.categories;
				checklist = $scope.model.checkListItems;
				
				angular.forEach( categories, function( item, index ) {
					$scope.insertCategory( item, $scope.checklistItemsByCategory( item ) );
				});
			}
		};
		*/

		/**
		 * Insert category into working array of categories, this might occur when a response is received from the API notifing that a new category has been inserted
		 * @param  {Object} category JSON category object
		 * @param  {Array} items	Array of checklist items to add
		 */
		$scope.insertCategory = function( category, items ) {
			$scope.categories.push(
				{
					"info": category,
					"items": items
				}
			);
		};

		/**
		 * Return a list of checlist items for a specific category
		 * @param  {Object} category JSON category object
		 * @return {Array}			an array of checklist items assigned to a specific category
		 */
		$scope.checklistItemsByCategory = function( category ) {
			var items = [], checkListItems = $scope.model.checklist;
			for( var i=0; i<checkListItems.length; i++ ) {
				if( checkListItems[i].category === category.label && !checkListItems[i].is_deleted ) {
					items.push(checkListItems[i]);
				}
			}

			return items;
		};

		/**
		 * Watch for changes in the order of items
		 * @param  {Object} nv New value, the updated value that has been changed
		 * @param  {Object} ov Old value what it used to look like
		 */
		$scope.$watch('categories', function( nv, ov ){
			var nv_items = [], ov_items = [];
			// Find out if order has changed
			var hasChanged_Category = ov.some( function( item, idx ){ return item.info.slug!=nv[idx].info.slug; } );

			if(hasChanged_Category) {
				// Save order change
				$scope.saveCategoryOrder();
			} else {
				// Find out if the order of items has been changed
				for(var i=0;i<ov.length;i++) {
					nv_items = nv_items.union( nv[i].items );
					ov_items = ov_items.union( ov[i].items );
				}

				var hasChanged_Items = ov_items.some( function( item, idx ){ return item.slug!=nv_items[idx].slug; } );
				if(hasChanged_Items) {
					// Save order change
					$scope.saveItemOrder();
				}
			}
		}, true);

		$scope.$watch('model.workingChecklist', function( nv, ov ){
			
			if(!$scope.model.ignoreChecklistUpdate) {
				var nv_items = [], ov_items = [];
				// Find out if the order of items has been changed
				for(var i=0;i<ov.length;i++) {
					nv_items = nv_items.union( nv[i] );
					ov_items = ov_items.union( ov[i] );
				}

				var hasChanged_Items = ov_items.some( function( item, idx ){ 
					if(!nv_items[idx]) {
						return false;
					} else {
						if(item.slug!==nv_items[idx].slug) {
							debugger;
						}
						return item.slug!==nv_items[idx].slug;
					}
				} );
				if(hasChanged_Items) {
					// Save order change
					if($scope.model.filters.on) {
						// If filtered then re-organise the original list
						sortInList( $scope.model.checklist,  $scope.model.workingChecklist);
					}
					$scope.saveItemOrder();
				}
			}
			$scope.model.ignoreChecklistUpdate = false;

			function findOriginalIndex( original, category, starting ) {
				for(var j=starting;j<original.length;j++) {
					if( original[j].category === category) { return j; }
				}
				return -1;
			}
			function sortInList( original, sorted ) {
				var availableSpot = 0;
				for(var i=0;i<sorted.length;i++) {
					availableSpot = findOriginalIndex( original, sorted[i].category, availableSpot);
					if(availableSpot>=0){
						original[availableSpot]=sorted[i];
						availableSpot = availableSpot+1;
					}
				}
			}
		}, true);

		/**
		 * Event triggered by releasing drag when re-organising categories
		 * @param  {Event} evt	event that incepted this action
		 * @param  {DOMNode} uiItem DOM node that this action was performed on
		 */
		$scope.saveCategoryOrder = function( /*evt, uiItem*/ ){
			var categories = $.map($scope.categories, function( cat ){
				return cat.info;
			});
			var promise = lawPalService.updateCategoryOrder( categories );
			promise.then(
				function( /*results*/ ) { /* Success */
					$scope.addAlert( "Categories re-ordered", "success", "Update complete" );
				},
				function( /*details*/ ) { /* Error */
					$scope.addAlert( "Unable to save order of categories", "warning", "Error!" );
				}
			);
		};

		/**
		 * Post changes to the order of checklist categories to the API
		 * @param  {Event} evt	Event that was fired
		 * @param  {uiItem} uiItem DOM node
		 */
		$scope.saveItemOrder = function( /*evt, uiItem*/ ) {
			var items = $scope.model.checklist;

			// Is there a filter?
			if( $scope.model.filters.category.label !== null ) {
				//debugger;
			}

			lawPalService.updateChecklistItemOrder( items ).then(
				function( /*results*/ ) { /* Success */
					$scope.addAlert( "Items re-ordered", "success", "Update complete" );
				},
				function( /*details*/ ) { /* Error */
					$scope.addAlert( "Unable to save order of items", "warning", "Error!" );
				}
			);
		};

		/**
		 * Load checklist items using service
		 */
		$scope.loadChecklist = function() {
			// Load initial checklist items
			lawPalService.getChecklist( 'sort_position_by_cat' ).then(
				function( results ) { /* Success */
					
					$scope.model.checklist = results;
					$scope.model.workingChecklist = $scope.getUndeleted(results);
					//$scope.mergeChecklistCategories();
				}
			);
		};

		$scope.loadFeedbackRequests = function() {
			// Load initial checklist items
			lawPalService.getFeedbackRequests().then(
				function( results ) { /* Success */
					$scope.model.feedbackRequests = results;
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
					for( var key in newData ) {
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
		 * Starts the process of viewing an item in the sidebar
		 * @param  {Object} item  Checklist item
		 * @param  {Number} index The layout area to slide into view
		 */
		$scope.selectChecklistItem = function( item, index ) {
			console.log( item );
			for(var i=0;i<$scope.model.checklist.length;i++) {
				$scope.model.checklist[i].selected = false;
			}
			item.selected = true;
			$scope.loadAttachments( item );
			$scope.getFeedbackStatus( item );
			$rootScope.$broadcast('open-sidebar', index);
		};

		$scope.loadAttachments = function( item ) {
			item.loadingAttachments = true;
			lawPalService.getCheckListItemAttachments( item ).then(
				function success( attachments ) {
					if( attachments && attachments.results ) {
						//adjustScollPos($(".options-container .item-container"));
						$rootScope.$broadcast('adjust-sidebar');
						for(var i=0;i<attachments.results.length;i++) {
							attachments.results[i].is_deleted = attachments.results[i].is_deleted?true:false;
							attachments.results[i].todo_slug = item.slug;
						}
						item.attachments = attachments.results;
						item.loadingAttachments = false;
					}
				},
				function error( err ) {
					console.log( err );
					item.loadingAttachments = false;
				}
			);
		};

		$scope.getFeedbackStatus = function( item ) {
			var options = {
				'id': null, /* attachment ID */
				'todo_slug': item.slug
			};

			clearFeedbackRequired();
			window.item = item;

			lawPalService.feedbackStatus( options ).then(
				function success( response ) {
					var feedbackItem, attachment;
					if( response.results && response.results.length>0 ) {
						var feedbackItems = response.results;
						for(var i=0;i<feedbackItems.length;i++) {
							feedbackItem = feedbackItems[i];
							
							if(feedbackItem.status<4 && feedbackItem.assigned_to_current_user ) {
								attachment = findAttachment(feedbackItem);
								if(attachment) {
									attachment.feedbackRequired = true;
									attachment.has_feedback = true;
									attachment.feedbackItem = feedbackItem;
								}
							} else if (feedbackItem.status<4) {
								attachment = findAttachment(feedbackItem);
								if(attachment) {
									attachment.has_feedback = true;
									attachment.feedbackRequired = false;
									attachment.feedbackItem = feedbackItem;
								}
							}
						}
					}
				},
				function error( err ) {
					console.log( 'error', err );
				}
			);

			function findAttachment( feebackItem ) {
				if( item ) {
					for(var j=0;j<item.attachments.length;j++) {
						if(item.attachments[j].id===feebackItem.attachment) {
							return item.attachments[j];
						}
					}
					return null;
				}
			}

			function clearFeedbackRequired(  ) {
				for(var j=0;j<item.attachments;j++) {
					item.attachments[j].feedbackRequired = false;
				}
			}
		};

		/**
		 * Recieves messages to update one of the existing checklist items
		 * @param  {Event} e	Broadcast event
		 * @param  {Object} data Data from the update event
		 */
		$scope.$on("todo.is_updated", function( e, data ){
			if( typeof(data)==="object" && data.instance ) {
				$scope.partialItemUpdate( data.instance, data.comment );
			}
		});

		/**
		 * Recieves mesages to remove items from the checklist (is_deleted = true ), in fact this is the same as an update message
		 * @param  {Event} e	Broadcast event
		 * @param  {Object} data Data from the new checklist item event
		 */
		$scope.$on("todo.is_deleted", function( e, data ){
			if( typeof(data)==="object" && data.instance ) {
				$scope.partialItemUpdate( data.instance, data.comment );
			}
		});

		/**
		 * Recieves messages to add new todo items
		 * @param  {Event} e	Broadcast event
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
		 * @param  {Event} e	Broadcast event
		 * @param  {Object} data Data from the pusher, containing details about the action
		 */
		$scope.$on("action.created", function( e, data){
			var slug = null;
			var user = lawPalService.getCurrentUser();

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

		$scope.$on("feedbackrequest.opened", function( e, data ){
			if(data.status) {
				if( data.instance && data.instance.slug ) {
					var slug = data.instance.slug||null;
					if( slug ) {
						// Add request for feedback
						$scope.model.feedbackRequests[slug] = [ { "todo_slug": slug} ];
						$scope.$apply();
						$scope.addAlert( "Feedback requested", "info", "Feedback" );
					}
				}
			}
		});

		$scope.$on("feedbackrequest.cancelled", function( e, data ){
			if(data.status) {
				if( data.instance && data.instance.slug ) {
					var slug = data.instance.slug||null;
					if( slug ) {
						// Add request for feedback
						delete $scope.model.feedbackRequests[slug];
						$scope.$apply();
						$scope.addAlert( "Feedback cancelled", "info", "Feedback" );
					}
				}
			}
		});

		// feedbackrequest.cancelled

}]);