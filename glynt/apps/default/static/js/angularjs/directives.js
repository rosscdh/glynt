'use strict';

angular.module('app.directives', []).
    directive('engaged', function() {
        return {
            restrict: 'E',
            transclude: true,
            scope: true,
            controller: function ($scope, $element) {
                var lawyer = $($element).attr('lawyer');
                //console.log($scope.engagements);
            },
            template: '<span class="badge btn-info badge-lawyer-engaged"><a href="#">{{ lawyer_engaged }}</a></span>',


            replace: false
        }
    });