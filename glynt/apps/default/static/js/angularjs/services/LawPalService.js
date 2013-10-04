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

	var transformToFormData = function(data){
		console.log("data", data);
        return $.param(data);
    }

	var checkList = {};

	return {
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
			return LawPal.project.uuid;
		},

		/**
		 * Get current user
		 * @return {Object} Current user
		 */
		"getCurrentUser": function() {
			return (LawPal.user && LawPal.user.is_authenticated?LawPal.user:null);
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