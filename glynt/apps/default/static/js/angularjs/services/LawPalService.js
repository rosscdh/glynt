/**
 * @description LawPal API interface
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').factory("lawPalService", ['$q', '$timeout', '$resource', '$http', function ($q, $timeout, $resource, $http) { /* Load the LawPal local interface */
	var lawPalInterface = LawPal;
	var userType = "is_customer";
	var checklist = [];
	var getEndpoint = (lawPalInterface.getEndpoint ? lawPalInterface.getEndpoint() : null);
	var data = {
		"project": {},
		"users": []
	};

	/* Define API interfaces for check list items */
	var checkListItemResources = {
		"remove": $resource("/api/v1/todo/:id", {}, 
			/* This is done to ensure the content type of PATCH is sent through */
			{ "save": { "method": "PATCH", headers: { "Content-Type": "application/json" } } 
		}),
		"update": 
			$resource("/api/v1/todo/:id\\/", {},
				{ "save": { "method": "PUT", headers: { "Content-Type": "application/json" } } 
			}),
		"create": 
			$resource("/api/v1/todo\\/", {},
				{ "save": { "method": "POST", headers: { "Content-Type": "application/json" } } 
			}),
		"reorder": $resource("/api/v1/project/:id/checklist/sort\\/", {}, 
			/* This is done to ensure the content type of PATCH is sent through */
			{ "save": { "method": "PATCH", headers: { "Content-Type": "application/json" }, "isArray": true } 
		})
	};

	var checkListCategories = {
		"reorder": $resource("/api/v1/project/:id/checklist/categories/sort\\/", {}, 
			/* This is done to ensure the content type of PATCH is sent through */
				{ "save": { "method": "PATCH", headers: { "Content-Type": "application/json" }, "isArray": true } 
			}),
		"add": $resource( "/projects/:id/category\\/", {},
				{ "save": { "method": "POST", "headers" : {'Content-Type': 'application/x-www-form-urlencoded'}, "transformRequest": transformToFormData } 
			}),
		"delete": $resource( "/projects/:id/category\\/", {},
				{ "save": { "method": "DELETE", "headers" : { "Content-Type": "application/json" } } 
			})
	};

	var projectResource = {
		"details": $resource("/api/v2/project/:uuid\\/", {}, 
				{ 
					"get": { "method": "GET", "headers": { "Content-Type": "application/json" } },
					"patch": { "method": "PATCH", "headers": { "Content-Type": "application/json" } } 
				}
			),
		"team": $resource("/api/v2/project/:uuid/team\\/", {}, 
				{ 
					"update": { "method": "PATCH", "headers": { "Content-Type": "application/json" }, "isArray": true } 
				}
			)
	};

	var transformToFormData = function(data){
		// Convert JSON to form post
        return $.param(data);
    }

	var checkList = {};

	return {
		/**
		 * Retreive current project
		 * @return {Function} promise
		 */
		"currentProject": function() {
			var deferred = $q.defer();
			var projectDetails = {};
			var projectUuid = this.getProjectUuid();
			var _this = this;

			if (lawPalInterface && typeof(lawPalInterface.project)==="function") {
				projectDetails = lawPalInterface.project();
			}

			// Get lawpal object
			projectResource.details.get( { "uuid": projectUuid },
				function success( results ) {
					projectDetails = Object.merge( projectDetails, results );
					data.project = projectDetails;
					data.project.users = _this.mergedProjectTeam( projectDetails );
					deferred.resolve( projectDetails );
				},
				function error( err ) {
					deferred.reject( err );
				}
			);

			return deferred.promise;
		},

		/**
		 * Merge different user types into a single array for the purpose of displaying them in a list
		 * @return {Array} Array of users
		 */
		"mergedProjectTeam": function( project ) {
			//
			var users = [];
			if( angular.isArray( project.lawyers ) ) {
				users = project.lawyers.map( function(item) {
					return Object.merge( item, {
						"role": "lawyer"
					});
				});
			}

			if( project.customer ) {
				project.customer.role = "client";
				users.push( project.customer );
			}

			return users;
		},

		"updateProjectTeam": function( team ) {
			var deferred = $q.defer();
			// Update lawyers
			var options = { "id": this.getProjectUuid() };

			debugger;

			projectResource.team.update( options, team, 
				function success( response ) {
					// Return project details
					deferred.resolve(response);
				},
				function error( err ) {
					deferred.reject( err );
				}
			);

			// Update customers
			

			return deferred.promise;
		},

		/**
		 * Request the list of categories
		 * @return {Function} promise for categories
		 */
		"getCategories": function () {
			// Set up a promise, because this method might retrieve information from the API directly in the future
			var deferred = $q.defer();
			var categories = [];

			$timeout(function () {
				if (lawPalInterface && lawPalInterface.checklist_categories) {
					// Retrieve items
					var loadedCategories = lawPalInterface.checklist_categories();
					// Remove unclean categories if needed
					categories = onlyCleanCategories( loadedCategories );
					// Return categories
					deferred.resolve(categories);
				} else {
					deferred.reject(categories);
				}
			}, 100);

			return deferred.promise;
		},

		/**
		 * Sends a PATCH request to update the category order
		 * @param  {Array} reOrderedCategories Array of catgeory names
		 * @return {Function}                  promise
		 */
		"updateCategoryOrder": function( reOrderedCategories ) {
			var projectId = this.getProjectUuid();
			var options = { "id": projectId };
			var cats = reOrderedCategories.map( 
				function( item, i ) { 
					//return  { "label": item.label.unescapeHTML(), "order": i }; 
					return  item.label.unescapeHTML(); 
				}
			);
			var data = { "project": projectId, "categories": cats };
			var deferred = $q.defer();

			checkListCategories.reorder.save(options, data.categories, function (results) { /* Success */
					deferred.resolve(results);
				}, function (results) { /* Error */
					deferred.reject(results);
				}
			);

			return deferred.promise;
		},

		"addCategory": function( details ) {
			var deferred = $q.defer();

			var projectId = this.getProjectUuid();
			var url = "/projects/" + projectId  + "/category/";

			if( details && details.category ) {
				$http.post(url, details, {
			        "headers": { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
			        "transformRequest": transformToFormData
			    }).success(function(response) {
			        //do stuff with response
			        if( response && response.instance && response.instance.category ) {
			        	if( !response.instance.category.label )
			        		response.instance.category.label = response.instance.category.name;
			        	deferred.resolve(response.instance.category);
			        } else {
			        	deferred.reject(response);
			        }
			    }).error(function(err){
			    	deferred.reject(err);
			    });
			}

			return deferred.promise;
		},

		"removeCategory": function( details ) {
			var deferred = $q.defer();

			var projectId = this.getProjectUuid();
			var options = { "id": projectId };

			if( details && details.info.label ) {
				var data = { "category": details.info.label };
				checkListCategories.delete.save(options, data, function (results) { /* Success */
						deferred.resolve(results);
					}, function (results) { /* Error */
						deferred.reject(results);
					}
				);
			}

			return deferred.promise;
		},

		/**
		 * Posts the new checklist item order to the API
		 * @param  {Array} categories array of categories (with nested checklist items)
		 * @return {Function}            promise
		 */
		"updateChecklistItemOrder": function( categories ) {
			var projectId = this.getProjectUuid();
			var slugItems = [];
			var options = { "id": projectId };
			var data = { "slugs": [] };
			var deferred = $q.defer();

			angular.forEach( categories, function( item, index ) {
				var items = item.items;
				for( var i=0; i<items.length; i++ ) {
					data.slugs.push( items[i].slug );
				}
			});

			checkListItemResources.reorder.save(options, data.slugs, function (results) { /* Success */
					deferred.resolve(results);
				}, function (results) { /* Error */
					deferred.reject(results);
				}
			);

			return deferred.promise;
		},

		/**
		 * Returns the list of check list items, ordered by the sort by parameter
		 * @param  {String} 	sortByProperty used to dermine which attribute to sort the data by
		 * @return {Function}   Promise
		 */
		"getChecklist": function (sortByProperty) {
			// Set up a promise, because this method might retrieve information from the API directly in the future
			var deferred = $q.defer();
			var checklist = [];

			$timeout(function () {
				if (lawPalInterface && lawPalInterface.checklist_data) {
					// Retrieve checklist items
					checklist = lawPalInterface.checklist_data();
					// Sort checklist
					checklist = sortChecklist( checklist );
					// Return checklist
					deferred.resolve(checklist);
				} else {
					// Ohh nooo! an error
					deferred.reject(checklist);
				}
			}, 100);

			return deferred.promise;
		},

		/**
		 * Returns the list of feedback requests
		 * @return {Function}   Promise
		 */
		"getFeedbackRequests": function (sortByProperty) {
			// Set up a promise, because this method might retrieve information from the API directly in the future
			var deferred = $q.defer();
			var feedbackRequests = [];

			$timeout(function () {
				if (lawPalInterface && lawPalInterface.feedback_requests) {
					// Retrieve checklist items
					feedbackRequests = lawPalInterface.feedback_requests() || {};
					// Return checklist
					deferred.resolve(feedbackRequests);
				} else {
					// Ohh nooo! an error
					deferred.reject(feedbackRequests);
				}
			}, 100);

			return deferred.promise;
		},

		/**
		 * Get current users profile type
		 * @return {String} "is_lawyer" or "_is_customer"
		 */
		"getUserType": function () {
			if (lawPalInterface.is_lawyer) return "is_lawyer";
			else return userType;
		},

		/**
		 * Makes a HTTP POST request to update 
		 * @param  {[type]} item [description]
		 * @param  {String} csrf [description]
		 * @return {Function}	  promise for AJAX request
		 */
		"updateChecklistItem": function( item, pusherConfig ) {
			//
			var deferred = $q.defer();

			delete item.csrfmiddlewaretoken;

			if( pusherConfig && pusherConfig.channel )
				item.pusher_id = pusherConfig.channel;

			item = angular.fromJson(angular.toJson(item));
				
			if( item.id ) {
				var options = {
					"id": item.id
				};

				checkListItemResources.update.save(options, item, function (results) { /* Success */
					deferred.resolve(results);
				}, function (results) { /* Error */
					deferred.reject(results);
				});
			} else {
				checkListItemResources.create.save({}, item, function (results) { /* Success */
					deferred.resolve(results);
				}, function (results) { /* Error */
					deferred.reject(results);
				});
			}

			return deferred.promise;
		},

		/**
		 * Deletes item from checklist
		 * @param  {Object} 	item JSON object representing the check list item to remove
		 * @return {Function}   promise to delete item
		 */
		"deleteChecklistItem": function (item) {
			var deferred = $q.defer();
			var options = {
				"id": item.id
			};

			var actionDetails = {
				"is_deleted": true
			};

			checkListItemResources.remove.save(options, actionDetails, function (results) { /* Success */
				deferred.resolve(results);
			}, function (results) { /* Error */
				deferred.reject(results);
			});

			return deferred.promise;
		},

		/**
		 * Get current project ID if available
		 * @return {Number} project Id
		 */
		"getProjectId": function() {
			return LawPal.project.id;
		},

		"getProjectUuid": function() {
			if( typeof(LawPal.project)==="function")
				return LawPal.project().uuid;
			else
				return LawPal.project.uuid;
		},

		/**
		 * Get current user
		 * @return {Object} Current user
		 */
		"getCurrentUser": function() {
			return (LawPal.user && LawPal.user.is_authenticated?LawPal.user:null);
		},

		"emailSearch": function( str ) {
			var deferred = $q.defer();

			$timeout(function () {
				var results = lawPalInterface._mockSearch(str);
				deferred.resolve(results);
			}, 1500);

			return deferred.promise;
		}
	};

	/**
	 * Filters out categories that are invalid
	 * @param  {Array} categories Array of category objects
	 * @return {Array}			Array of clean categories
	 */
	function onlyCleanCategories( categories ) {
		if( !categories || !angular.isArray(categories) )
			return [];

		var cleanCats = [];

		if (angular.isArray(categories) && categories.length > 0) {
			for (var i = 0; i < categories.length; i++){
				var cat = categories[i];
				if (cat && cat.label !== "") {
					cat.label = cat.label.unescapeHTML();
					cleanCats.push(cat);
				}
			}
		}

		return cleanCats;
	}

	/**
	 * Sorts a checklist if this request has been made
	 * @param  {Array} checklist	  Array of checlist items
	 * @param  {String} sortByProperty String representing the prooperty to do the sort on
	 * @return {Array}				Array of sorted checklist items
	 */
	function sortChecklist( checklist, sortByProperty ) {
		if( !checklist || !angular.isArray(checklist) )
			return [];

		if (angular.isArray(checklist) && sortByProperty) {
			// Sort list
			checklist = checklist.sort(function (item1, item2) {
				return item1[sortByProperty] - item2[sortByProperty];
			});
		}

		return checklist;
	}
}]);