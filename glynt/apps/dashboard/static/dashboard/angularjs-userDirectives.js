/**
 * Displays the percentage comparison between new, open, pending and closed checklist items
 * @return {Object} AngularJS directive
 */
angular.module('lawpal').directive('userMiniWidget', function () {
  'use strict';
	return {
		"restrict": "AC",
		"template":
			'<div class="vcard user-mini-profile"><img class="user-photo photo" ng-src="{[{user.photo}]}" class="photo" ng-show="show.photo">'+
			'<h5 class="fn" ng-bind="user.full_name" ng-show="show.name"></h5>'+
			'</div>',
			/*'<a ng-show="!hasContact()" class="icon icon-envelope clickable" tooltip="Contact {[{ user.firstName | titleCase }]}" tooltip-append-to-body="true" ng-click="contactUser()" href="javascript:;"></a>*/
		"scope": {
			"user": "=user"
		},
		/*
		"link": function (scope, iElement, iAttrs) {
		},
		*/
		"controller": [ '$scope', '$element', '$attrs', function( $scope, $element, $attrs ) {

			$scope.show = {
				"name": false,
				"photo": false
			};

			if( $attrs.showProps ) {
				var showProps = $attrs.showProps.split(',');
				for(var i=0;i<showProps.length;i++) {
					$scope.show[showProps[i]]=true;
				}
			} else {
				for(var key in $scope.show) {
					$scope.show[key]=true;
				}
			}
			$scope.contactUser = function() {
				console.log("Contact user");
			};

			$scope.hasContact = function() {
				// return true if user has an email address
				return (typeof($scope.user.email) === "string" );
			};
		}]
	};
});