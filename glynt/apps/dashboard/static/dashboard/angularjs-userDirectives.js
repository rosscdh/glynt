/**
 * Displays the percentage comparison between new, open, pending and closed checklist items
 * @return {Object} AngularJS directive
 */
angular.module('lawpal').directive('userMiniWidget', function () {
  return {
  	"restrict": "A",
  	"template": 
  		'<div class="vcard user-mini-profile"><img class="user-photo photo" ng-src="{[{user.photo}]}" class="photo">'+
  		'<h5 class="fn">'+
        '<span class="user-firstname" ng-bind="user.firstName"></span> '+
        '<span class="user-lastname" ng-bind="user.lastName"></span>'+
      '</h5><a ng-show="!hasContact()" class="icon icon-envelope clickable" tooltip="Contact {[{ user.firstName | titleCase }]}" tooltip-append-to-body="true" ng-click="contactUser()" href="javascript:;"></a></div>',
  	"scope": {
  		"user": "=user"
  	},
    "link": function (scope, iElement, iAttrs) {
    },
    "controller": [ '$scope', '$element', '$attrs', function( $scope, $element, $attrs ) {
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