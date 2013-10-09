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
      '</h5></div>',
  	"scope": {
  		"user": "=user"
  	},
    "link": function (scope, iElement, iAttrs) {
    },
    "controller": [ '$scope', '$element', '$attrs', function( $scope, $element, $attrs ) {
    }]
  };
});