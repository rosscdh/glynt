'use strict';

angular.module('app.directives', []).
    directive('engaged', function() {
        return {
            restrict: 'E',
            transclude: true,
            scope: {},
            controller: function ($scope, $element, apiCall) {
                console.log($element);
            },
            template: '<span>Badge will go here...</span>',
            replace: true
        }
    });