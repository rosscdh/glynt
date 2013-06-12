'use strict';

angular.module('app.directives', []).
    directive('engaged', function () {
        return {
            restrict: 'E',
            transclude: true,
            scope: true,
            controller: function ($scope, $element) {
                var lawyer = $($element).attr('lawyer');
                $scope.hide = 'hide';
                $scope.$watch('engagements', function (data) {
                    if (data !== undefined) {
                        var ele = data[$element.attr('lawyer')];
                        if (ele) {
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