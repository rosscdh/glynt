/**
 * @description Wraps a modal header and footer around a crispy form then invokes Angular.ui dialog 
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').factory( "lawPalDialog", [ "$q", "$http", "$modal", function( $q, $http, $modal )
	{
		return {
			/**
			 * Opens an Angular UI dialog, retrieves a HTML form using XHR, inserts the title and wraps a header and footer around the form
			 * @param  {String} title Title of dialog/form
			 * @param  {String} url   URL of HTML form to retrieve
			 * @return {Function}       promise for completion either save or cancel
			 */
			"open": function( title, url, item ) {
				var deferred = $q.defer();
				var template = '';
				var modalId = 'modal-' + new Date().getTime(); // ModalID is a class, but is also unique. A class is used because there is no method available to set the ID of the modal dialo div

				// Setup header and footer
				var templateHeader = '<div class="modal-dialog"><div class="modal-content">'+
				  '<div class="modal-header">'+
				  '<button ng-click="close(null)" class="close" aria-hidden="true">&times;</button>'+
				  '<h4>{{title}}</h4>'+
				  '</div>'+
				  '<form ng-submit="save(\'.{modalId}\')">'+
				  '<div class="modal-body">';
			   	var templateFooter = '</div>'+
				  '<div class="modal-footer">'+
				  '<input type="button" ng-click="close()" class="btn" value="Cancel" />'+
				  '<input type="submit" value="Save" class="btn btn-primary" />'+
				  '</div>'+
				  '</form>'+
				  '</div></div>';

				 // Configure modal dialog
				var dialogOptions = {
					"windowClass": "modal modal-show " + modalId,
					"backdrop": true,
					"keyboard": true,
					"dialogFade": true,
					"backdropClick": true,
					"controller": dialogController,
					"resolve": {
						"dialogsModel": function () {
						  return item;
						}
					}
				};

				title = title || "";

				// Retrieve HTML form
				$http.get( url ).success( function( html ) {
					html = html.replace("form>","span>");
					
					// Wrap the HTML inside the header and footer
					template = templateHeader + html + templateFooter;
					// Insert title
					dialogOptions.template = template.replace("{{title}}", title);
					dialogOptions.template = dialogOptions.template.replace("{modalId}", modalId);
					dialogOptions.template = dialogOptions.template.replace("data-required=\"true\"", "required data-required");

					// Open dialog
					var d = $modal.open( dialogOptions );
					d.result.then( function(result){ /* Success */
						deferred.resolve( result );
					});

				}).error( function( response ) {
					/* Error unable to load form */
					deferred.reject( response );
				});

				return deferred.promise;
			}
		};
	}
]);

/**
 * @description Wraps a modal header and footer around a crispy form then invokes Angular.ui dialog 
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').factory( "deleteCategoryConfirmDialog", [ "$q", "$modal", function( $q, $modal )
	{
		return {
			/**
			 * Opens an Angular UI dialog, retrieves a HTML form using XHR, inserts the title and wraps a header and footer around the form
			 * @param  {String} title Title of dialog/form
			 * @param  {String} url   URL of HTML form to retrieve
			 * @return {Function}       promise for completion either save or cancel
			 */
			"open": function( category ) {
				var deferred = $q.defer();
				var template = '';

				// Setup header and footer
				var templateHeader = '<div class="modal-dialog"><div class="modal-content">'+
				  '<div class="modal-header">'+
				  '<button ng-click="close(null)" class="close" aria-hidden="true">&times;</button>'+
				  '<h4 class="text-danger">Delete {[{category.info.label}]}</h4>'+
				  '</div>'+
				  '<form ng-submit="delete()">'+
				  '<div class="modal-body">';
				var templateBody = '<p><strong>Deleteing this category will also delete the following checklist items:</strong></p>'+
				  '<ul class="item-list"><li ng-repeat="item in category.items"><span ng-bind="item.name"></span></li></ul>';
			   	var templateFooter = '</div>'+
				  '<div class="modal-footer">'+
				  '<input type="button" ng-click="close()" class="btn" value="Cancel" />'+
				  '<input type="submit" value="Delete" class="btn btn-primary" id="delete-category-button" />'+
				  '</div>'+
				  '</form>'+
				  '</div></div>';

				template = templateHeader + templateBody + templateFooter;

				// Configure modal dialog
				var dialogOptions = {
					"windowClass": "modal modal-show",
					"template": template,
					"controller": simpleDialogController,
					"backdrop": true,
					"keyboard": true,
					"dialogFade": true,
					"backdropClick": false,
					"resolve": {
						"category": function () {
						  return category;
						}
					}
				};

				var modalInstance = $modal.open( dialogOptions );

				modalInstance.result.then( function(result){ /* Success */
					deferred.resolve( result );
				});

				return deferred.promise;
			}
		};
	}
]);

/**
 * This controller provides a bridget between the crispy form system and Angular
 * @param  {Object} $scope The modal forms scope object
 * @param  {dialog} dialog The dialog object, which contains references to the dom (e.g. dialog.modelEl), functions etc.
 */
var simpleDialogController = function ($scope, $modalInstance, category) {

  $scope.category = category;

  $scope.delete = function () {
    $modalInstance.close( $scope.category );
  };

  $scope.close = function () {
    $modalInstance.dismiss('cancel');
  };
};

/**
 * This controller provides a bridget between the crispy form system and Angular
 * @param  {Object} $scope The modal forms scope object
 * @param  {dialog} dialog The dialog object, which contains references to the dom (e.g. dialog.modelEl), functions etc.
 */
var dialogController = function( $scope, $modalInstance, dialogsModel ) {
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
		$modalInstance.close( null, $scope );
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
		$modalInstance.close( result, $scope );
	};
};

/**
 * Manageteam dialog controller
 * @param  {Object} $scope         	Modal $scope
 * @param  {Object} $modalInstance 	Modal object instance, allow it to close itself etc
 * @param  {Array} team           	List of team users
 * @param  {Object} lawPalService 	List of methods used to acccess the LawPAl API
 * @param  {Object} $q				Promise library
 */
angular.module('lawpal').controller( 'manageTeamDialogCtrl', [ '$scope', '$modalInstance', 'team', 'lawPalService', '$q', 'toaster',
	function ($scope, $modalInstance, team, lawPalService, $q, toaster) {
		$scope.revert = [];
		$scope.emailSearchStr = null;
		$scope.team = team;
		$scope.emailSearchResults = [];
		$scope.selectedEmail = null;
		$scope.searchingEmail = "";

		$scope.searchAttrs = {
			"selectedEmail": null,
		};

		angular.copy( team, $scope.revert );

		$scope.canRemove = function( user ) {
			if(!user.role)
				user.role = "";
			return !user.is_authenticated && ( user.role!=="account manager") && !user.primary;
		};

		/**
		 * Set user as deleted
		 * @param  {Object} user JSON object containing the user details
		 */
		$scope.removeUser = function( user ) {
			user.is_deleted = !user.is_deleted;
		};

		/**
		 * Determine removed DOM class
		 * @param  {Object}  user [description]
		 * @return {String}      remove or ""
		 */
		$scope.isRemovedClass = function( user ) {
			return user.is_deleted?"remove":"";
		};

		/**
		 * Sets the animation class so the the spinner is spinning
		 * @param  {Boolean} searchStatus Is the search form currently searching
		 * @return {String}              Incon classes
		 */
		$scope.emailSearchClass = function( searchStatus ) {
			return searchStatus?"icon-refresh icon-spin":"icon-plus";
		};

		/**
		 * Perform a search on user emails
		 * @param  {String} searchStr partial email address
		 * @return {Function}           Promise
		 */
		$scope.searchEmails = function(searchStr) {
			searchStr = searchStr || null;
			var deferred = $q.defer();
			
			lawPalService.emailSearch(searchStr).then(
				function success( results ) {
					$scope.emailSearchResults = results;
					deferred.resolve(results)
				},
				function error( err ) {
					$scope.emailSearchResults = [];
					deferred.reject( err );
				}
			);

			return deferred.promise;
		};

		/**
		 * Add selected user to team
		 * @param {String} selectedEmail User email address
		 * @param {Array} results       List of results from the most recent user search
		 */
		$scope.addToProject = function( selectedEmail, results ) {
			var selectedUser = results.filter(
				function(item){
					return (item.email === selectedEmail) || (item.username === selectedEmail);
				})[0] || null;

			if( selectedUser.profile_photo )
				selectedUser.photo = selectedUser.profile_photo;

			if( selectedUser.name )
				selectedUser.full_name = selectedUser.name;

			selectedUser.is_deleted = false;

			var exisingUser = $scope.team.filter(
				function( user ) {
					return (user.email === selectedUser.email);
				}
			);

			if( selectedUser && exisingUser.length <= 0 )
				$scope.team.push( selectedUser );
			else
				toaster.pop("info", "Team management", selectedUser.full_name + " Has already been added");

			$scope.searchAttrs.selectedEmail = "";
		};

		/**
		 * User clicked the OK/Save button
		 */
		$scope.ok = function () {
			$modalInstance.close($scope.team);
		};

		/**
		 * User clicked the cancel button, reset team to original state
		 * @return {[type]} [description]
		 */
		$scope.cancel = function () {

			var team = $scope.team;
			var originals = $scope.revert;

			for(var i=0;i<team.length;i++) {
				if(originals[i]) {
					// Reset primary and deleted flags to original state
					team[i].primary = originals[i].primary;
					team[i].is_deleted = originals[i].is_deleted;
				} else {
					// Remove users added to team
					team.splice(i,1);
				}
			}

			$modalInstance.dismiss('cancel');
		};
	}]
);

angular.module('lawpal').controller( 'newDiscussionDialogCtrl', [ '$scope', '$modalInstance', 'parent', 'lawPalService', '$q',
	function ($scope, $modalInstance, parent, lawPalService, $q) {
		$scope.message = {
			"subject": null,
			"comment": null,
			"type": "discussion",
			"parent_id": parent && parent.id?parent.id:null
		};
		/**
		 * User clicked the OK/Save button
		 */
		$scope.ok = function () {
			$modalInstance.close($scope.message);
		};

		/**
		 * User clicked the cancel button, reset team to original state
		 * @return {[type]} [description]
		 */
		$scope.cancel = function () {
			$modalInstance.dismiss('cancel');
		};
	}]
);

/**
 * Manageteam dialog controller
 * @param  {Object} $scope         	Modal $scope
 * @param  {Object} $modalInstance 	Modal object instance, allow it to close itself etc
 * @param  {Array} team           	List of team users
 * @param  {Object} lawPalService 	List of methods used to acccess the LawPAl API
 * @param  {Object} $q				Promise library
 */
angular.module('lawpal').controller( 'profileDialogCtrl', [ '$scope', '$modalInstance', 'user', 'lawPalService', '$q', 'toaster',
	function ($scope, $modalInstance, user, lawPalService, $q, toaster) {
		$scope.user = user;

		$scope.ok = function () {
			$modalInstance.close($scope.user);
		};

		$scope.cancel = function () {
			$modalInstance.dismiss('cancel');
		};
	}]
);