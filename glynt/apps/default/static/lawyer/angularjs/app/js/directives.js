'use strict';

angular.module('App.Directives', []).
    directive('engaged', function () {
        return {
            restrict: 'E',
            transclude: true,
            scope: true,
            controller: function ($scope, $element, $attrs) {
                var lawyer = $attrs.lawyer;
                $scope.hide = 'hide';
                $scope.$watch('engagements', function (data) {
                    if (data !== undefined) {
                        var ele = data[lawyer];
                        if (ele && parseInt(ele) !== NaN) {
                            $scope.lawyer_engaged = 'Already Contacted';
                            $scope.enagagement_url = ele.absolute_url;
                            $scope.hide = '';
                        }
                    }
                });
            },
            template: '<span class="badge btn-info badge-lawyer-engaged {{ hide }}"><a href="{{ enagagement_url }}">{{ lawyer_engaged }}</a></span>',
            replace: false
        }
    });