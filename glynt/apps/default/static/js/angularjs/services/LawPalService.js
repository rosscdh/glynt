/**
 * @description LawPal API interface
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').factory('lawPalService', ['$q', '$timeout', '$resource', '$http', function ($q, $timeout, $resource, $http) { /* Load the LawPal local interface */
	'use strict';
	var lawPalInterface = LawPal;
	var userType = 'is_customer';
	var data = {
		'project': {},
		'users': []
	};

	/* Define API interfaces for check list items */
	var checkListItemResources = {
		'remove': $resource('/api/v1/todo/:id', {},
			/* This is done to ensure the content type of PATCH is sent through */
			{ 'save': { 'method': 'PATCH', headers: { 'Content-Type': 'application/json' } }
		}),
		'update':
			$resource('/api/v1/todo/:id/?format=json', {},
				{ 'save': { 'method': 'PUT', headers: { 'Content-Type': 'application/json' } }
			}),
		'create':
			$resource('/api/v1/todo/?format=json', {},
				{ 'save': { 'method': 'POST', headers: { 'Content-Type': 'application/json' } }
			}),
		'reorder': $resource('/api/v1/project/:id/checklist/sort/?format=json', {},
			/* This is done to ensure the content type of PATCH is sent through */
			{ 'save': { 'method': 'PATCH', headers: { 'Content-Type': 'application/json' }, 'isArray': true }
		})
	};

	var checkListCategories = {
		'reorder': $resource('/api/v1/project/:id/checklist/categories/sort/?format=json', {},
			/* This is done to ensure the content type of PATCH is sent through */
				{ 'save': { 'method': 'PATCH', headers: { 'Content-Type': 'application/json' }, 'isArray': true }
			}),
		'add': $resource( '/projects/:id/category\\/', {},
				{ 'save': { 'method': 'POST', 'headers' : {'Content-Type': 'application/x-www-form-urlencoded'}, 'transformRequest': transformToFormData }
			}),
		'delete': $resource( '/projects/:id/category\\/', {},
				{ 'save': { 'method': 'DELETE', 'headers' : { 'Content-Type': 'application/json' } }
			})
	};

	var projectResource = {
		'details': $resource('/api/v2/project/:uuid/?format=json', {}, /* use ?format=json to avoid trailing slash issues*/
				{
					'get': { 'method': 'GET', 'headers': { 'Content-Type': 'application/json' } },
					'patch': { 'method': 'PATCH', 'headers': { 'Content-Type': 'application/json' } }
				}
			),
		'team': $resource('/api/v2/project/:uuid/team/?format=json', {},
				{
					'update': { 'method': 'PATCH', 'headers': { 'Content-Type': 'application/json' } },
					'get': { 'method': 'GET', 'headers': { 'Content-Type': 'application/json' } }
				}
			)
	};

	var userResource = {
		'email': $resource( '/api/v2/user/?email=:searchFor', {},
				{
					'search': { 'method': 'GET', 'headers': { 'Content-Type': 'application/json' } }
				}
			),
		'username': $resource( '/api/v1/user/profile/?username__in=:searchFor', {},
				{
					'search': { 'method': 'GET', 'headers': { 'Content-Type': 'application/json' } }
				}
			)

		// loadFullProfileDetails
	};

	var discussionResource = {
		'project': $resource( '/api/v2/project/:uuid/discussion/?format=json', {},
				{
					'get': { 'method': 'GET', 'headers': { 'Content-Type': 'application/json' } },
					'save': { 'method': 'POST', 'headers': { 'Content-Type': 'application/json' } }
				}
			),
		"discussion": $resource( '/api/v2/project/:uuid/discussion/:pk/?format=json', {},
				{
					'get': { 'method': 'GET', 'headers': { 'Content-Type': 'application/json' } }
				}
			)
	};

	var transformToFormData = function(data){
		// Convert JSON to form post
		return $.param(data);
	};

	return {
		/**
		 * Retreive current project
		 * @return {Function} promise
		 */
		'currentProject': function() {
			var deferred = $q.defer();
			var projectDetails = {};
			var projectUuid = this.getProjectUuid();
			var _this = this;
			if (lawPalInterface && typeof(lawPalInterface.project)==='function') {
				projectDetails = lawPalInterface.project();
			}

			// Get lawpal object
			projectResource.details.get( { 'uuid': projectUuid },
				function success( results ) {
					projectDetails = Object.merge( projectDetails, results );
					data.project = projectDetails;
					_this.loadProjectTeamMembers( projectDetails ).then(
						function success( team ) {
							data.project.users = _this.mergedProjectTeam( projectDetails, team );
							deferred.resolve( projectDetails );
						},
						function error() {
							deferred.resolve( projectDetails );
						}
					);
					
				},
				function error( err ) {
					deferred.reject( err );
				}
			);

			return deferred.promise;
		},

		'loadProjectTeamMembers': function( ) {
			var projectUuid = this.getProjectUuid();
			var deferred = $q.defer();

			projectResource.team.get( { 'uuid': projectUuid },
				function success( results ) {
					deferred.resolve( results.team );
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
		'mergedProjectTeam': function( project, team ) {
			//
			var user;
			var users = team || [];
			var currentUser = this.getCurrentUser();

			for (var i=0;i<team.length;i++) {
				user = team[i];

				if( user.username == currentUser.username ) {
					user.is_authenticated = true;
				}
				if(!user.is_deleted)
					user.is_deleted = false;

				if( user.is_lawyer ) user.role = "lawyer";
				if( user.is_customer ) user.role = "client";

				if( user.id ) user.pk = user.id;

				if( user.username == data.project.customer.username ) user.primary = true;
				if( data.project.lawyers[0] && user.username == data.project.lawyers[0].username ) user.primary = true;
			}

			return users;
		},

		'updateProjectTeam': function( team ) {
			var deferred = $q.defer();
			// Update lawyers
			var options = { 'uuid': this.getProjectUuid() };
			var updatedTeam = team.filter( function( user ){
				return user.is_deleted !== true;
			});
			var data = updatedTeam.map( function( item ) {
				return item.pk || item.id;
			});

			data = data.filter( function( id ) {
				return id !==null && id>=0;
			});

			var obj = { 'team': data };

			projectResource.team.update( options, obj,
				function success( response ) {
					// Return project details
					deferred.resolve(response);
				},
				function error( err ) {
					deferred.reject( err );
				}
			);

			return deferred.promise;
		},

		/**
		 * Request the list of categories
		 * @return {Function} promise for categories
		 */
		'getCategories': function () {
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
		 * @return {Function}				  promise
		 */
		'updateCategoryOrder': function( reOrderedCategories ) {
			var projectId = this.getProjectUuid();
			var options = { 'id': projectId };
			var cats = reOrderedCategories.map(
				function( item ) {
					return  item.label.unescapeHTML();
				}
			);
			var data = { 'project': projectId, 'categories': cats };
			var deferred = $q.defer();

			checkListCategories.reorder.save(options, data.categories, function (results) { /* Success */
					deferred.resolve(results);
				}, function (results) { /* Error */
					deferred.reject(results);
				}
			);

			return deferred.promise;
		},

		'addCategory': function( details ) {
			var deferred = $q.defer();

			var projectId = this.getProjectUuid();
			var url = '/projects/' + projectId  + '/category/';

			if( details && details.category ) {
				$http.post(url, details, {
					'headers': { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
					'transformRequest': transformToFormData
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

		'removeCategory': function( details ) {
			var deferred = $q.defer();

			var projectId = this.getProjectUuid();
			var options = { 'id': projectId };

			if( details && details.info.label ) {
				var data = { 'category': details.info.label };
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
		 * @return {Function}			promise
		 */
		'updateChecklistItemOrder': function( categories ) {
			var projectId = this.getProjectUuid();
			var options = { 'id': projectId };
			var data = { 'slugs': [] };
			var deferred = $q.defer();

			angular.forEach( categories, function( item ) {
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
		 * Returns the list of projects for the current user
		 * @return {Function}	Promise
		 */
		'getUsersProjects': function () {
			// Set up a promise, because this method might retrieve information from the API directly in the future
			var deferred = $q.defer();
			var projects = [];

			$timeout(function () {
				if (lawPalInterface && lawPalInterface.overview) {
					// Retrieve checklist items
					projects = lawPalInterface.overview.projects.results;
					// Return checklist
					deferred.resolve(projects);
				} else {
					// Ohh nooo! an error
					deferred.reject(projects);
				}
			}, 10);

			return deferred.promise;
		},

		/**
		 * Returns the list of projects for the current user
		 * @return {Function}	Promise
		 */
		'getRecentDiscussions': function ( projectId, userId ) {
			// Set up a promise, because this method might retrieve information from the API directly in the future
			var deferred = $q.defer();
			var discussions = [];
			var workingDiscussions = [];

			$timeout(function () {
				if (lawPalInterface && lawPalInterface.overview) {
					// Retrieve discussion items
					workingDiscussions = lawPalInterface.overview.discussions;
					// Merge discussions
					if( angular.isArray(workingDiscussions) && workingDiscussions.length>1 ) {
						discussions = workingDiscussions[0].results;
						for(var i=1;i<workingDiscussions.length;i++) {
							discussions = discussions.union(workingDiscussions[i].results);
						}
					} else if ( angular.isArray(workingDiscussions) && workingDiscussions.length==1 ) {
						discussions = workingDiscussions[0];
						if(discussions.results) {
							discussions = discussions.results;
						}
					}

					// Filter dicussions by project
					if( projectId ) {
						discussions = discussions.filter( function(item){
							return parseInt(item.object_pk,10)===projectId;
						});
					}

					// Standardise last_child, so that it can be referenced easily
					for(var di=0;di<discussions.length;di++) {
						if( !discussions[di].last_child ) {
							discussions[di].last_child = Object.clone(discussions[di]);
						}
					}

					discussions = discussions.sort(function(item1,item2){
						// If item1 has the current user and the second itesm does not switch them in order
						return item1.last_child.id > item2.last_child.id;
					});

					if( userId ) {
						// Sort discussions that need responding to first to the top
						var myDiscussions = discussions.filter(function(item){
							// If item1 has the current user and the second itesm does not switch them in order
							return item.last_child.meta.user.pk === userId;
						});

						var theirDiscussions = discussions.filter(function(item){
							// If item1 has the current user and the second itesm does not switch them in order
							return item.last_child.meta.user.pk !== userId;
						});

						discussions = [].union(theirDiscussions, myDiscussions);
					}

					// Return checklist
					deferred.resolve(discussions);
				} else {
					// Ohh nooo! an error
					deferred.reject(discussions);
				}
			}, 10);

			return deferred.promise;
		},

		/**
		 * Returns the list of check list items, ordered by the sort by parameter
		 * @param  {String}		sortByProperty used to dermine which attribute to sort the data by
		 * @return {Function}	Promise
		 */
		'getChecklist': function () {
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
		'getFeedbackRequests': function () {
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
		 * @return {String} 'is_lawyer' or '_is_customer'
		 */
		'getUserType': function () {
			if (lawPalInterface.is_lawyer) return 'is_lawyer';
			else return userType;
		},

		/**
		 * Makes a HTTP POST request to update 
		 * @param  {[type]} item [description]
		 * @param  {String} csrf [description]
		 * @return {Function}	  promise for AJAX request
		 */
		'updateChecklistItem': function( item, pusherConfig ) {
			//
			var deferred = $q.defer();

			delete item.csrfmiddlewaretoken;

			if( pusherConfig && pusherConfig.channel )
				item.pusher_id = pusherConfig.channel;

			item = angular.fromJson(angular.toJson(item));
				
			if( item.id ) {
				var options = {
					'id': item.id
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
		 * @param  {Object}		item JSON object representing the check list item to remove
		 * @return {Function}   promise to delete item
		 */
		'deleteChecklistItem': function (item) {
			var deferred = $q.defer();
			var options = {
				'id': item.id
			};

			var actionDetails = {
				'is_deleted': true
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
		'getProjectId': function() {
			return LawPal.project.id;
		},

		/**
		 * Returns the current project UUID
		 * @return {String} Project UUID
		 */
		"getProjectUuid": function() {
			return LawPal.project.uuid;
		},

		/**
		 * Returns the content type ID for the project content type
		 * @return {Number} Project content type ID
		 */
		'projectContentTypeId': function() {
			if( typeof(LawPal.project)==='function')
				return LawPal.project().content_type_id;
			else
				return LawPal.project.content_type_id || 14;
		},

		/**
		 * Get current user
		 * @return {Object} Current user
		 */
		'getCurrentUser': function() {
			return (LawPal.user && LawPal.user.is_authenticated?LawPal.user:null);
		},

		/**
		 * Given an array of usernames search for full user profiles
		 * @param  {Array} users Array of usernames
		 * @return {Function}       promise
		 */
		'usernameSearch': function( users ) {
			var deferred = $q.defer();
			var userList = [];
			var searchList  = '';
			var retreivedUsers = [];
			var user, updatedUser;

			if( angular.isArray( users ) ) {
				userList = users.map( function( user ){
					return user.username;
				});

				searchList = userList.join(',');
			} else {
				searchList= users;
			}

			var options = { 'searchFor': searchList };

			userResource.username.search( options,
				function success( data ) {
					if( data.objects || data.results ) {
						retreivedUsers = data.objects || data.results;
						for( var i=0; i<retreivedUsers.length; i++ ) {
							for( var j=0; j<users.length; j++ ) {
								if(retreivedUsers[i].username===users[j].username) {
									user = users[j];
									updatedUser = retreivedUsers[i];
									user.practice_locations = updatedUser.practice_locations;
									user.companies = updatedUser.companies;
									user.is_active = updatedUser.is_active;
									user.is_customer = updatedUser.is_customer;
									user.is_lawyer = updatedUser.is_lawyer;
									user.summary = updatedUser.summary;
									user.years_practiced = updatedUser.years_practiced;
									user.phone = updatedUser.phone;
									user.firm = updatedUser.firm;
								}
							}
						}
						deferred.resolve( data.objects );
					} else {
						deferred.reject( data );
					}
				},
				function error( err ) {
					deferred.reject( err );
				}
			);

			return deferred.promise;
		},

		/**
		 * Search for users using their email addresses
		 * @param  {String} str Email address partial
		 * @return {Function}     promise
		 */
		'emailSearch': function( str ) {
			var deferred = $q.defer();

			var options = { 'searchFor': str };

			userResource.email.search( options,
				function success( data ) {
					if( data.results ) {
						deferred.resolve( data.results );
					} else {
						deferred.reject( data );
					}
				},
				function error( err ) {
					deferred.reject( err );
				}
			);

			return deferred.promise;
		},

		/**
		 * Retrieve discussions for a specific project
		 * @return {Function} promise
		 */
		'discussionList': function() {
			var deferred = $q.defer();
			var projectUuid = this.getProjectUuid();
			var options = { 'uuid': projectUuid };

			discussionResource.project.get( options,
				function success( data ) {
					deferred.resolve(data.results);
				},
				function error( err ) {
					deferred.reject(err);
				}
			);

			return deferred.promise;
		},

		/**
		 * Retrieve a full discussion for a specific discussion base
		 * @param  {Number} discussionId discussion ID
		 * @param  {String} pUuid        project UUID (optinal)
		 * @return {Function}              promise
		 */
		'fullDiscussion': function( discussionId, pUuid ) {
			var deferred = $q.defer();
			var projectUuid = pUuid || this.getProjectUuid();
			var options = { 'uuid': projectUuid, 'pk': discussionId };

			if(projectUuid) {
				discussionResource.discussion.get( options,
					function success( data ) {
						deferred.resolve(data);
					},
					function error( err ) {
						deferred.reject(err);
					}
				);
			}

			return deferred.promise;
		},

		/**
		 * Post discussion to API
		 * @param  {Object} message Discussion object
		 * @param  {String} pUuid   Project UUID (optional)
		 * @return {Function}         promise
		 */
		'addDiscussion': function( message, pUuid ) {
			var deferred = $q.defer();
			var projectUuid = pUuid || this.getProjectUuid();
			var options = { 'uuid': projectUuid };

			discussionResource.project.save( options, message,
				function success( result ) {
					deferred.resolve(result);
				},
				function error( err ) {
					deferred.reject(err);
				}
			);

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
				if (cat && cat.label !== '') {
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