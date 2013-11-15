/**
 * Manageteam dialog controller
 * @param  {Object} $scope         	Modal $scope
 * @param  {Object} $modalInstance 	Modal object instance, allow it to close itself etc
 * @param  {Array} team           	List of team users
 * @param  {Object} lawPalService 	List of methods used to acccess the LawPAl API
 * @param  {Object} $q				Promise library
 */
angular.module('lawpal').controller( 'manageTeamDialogCtrl', [ '$scope', '$modalInstance', 'team', 'process', 'lawPalService', '$q', 'toaster',
	function ($scope, $modalInstance, team, process, lawPalService, $q, toaster) {
		'use strict';
		$scope.revert = [];
		$scope.emailSearchStr = null;
		$scope.team = team;
		$scope.emailSearchResults = [];
		$scope.selectedEmail = null;
		$scope.searchingEmail = "";
		$scope.processType = process; // 'manage' team or 'sign'

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

		$scope.toggleSign = function( user ) {
			user.is_signing = user.is_signing===true?false:true;
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