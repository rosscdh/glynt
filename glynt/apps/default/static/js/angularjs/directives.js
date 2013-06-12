'use strict';

angular.module('app.directives', []).
    directive('engaged', function () {
        return {
            restrict: 'E',
            transclude: true,
            scope: true,
            controller: function ($scope, $element) {
                var lawyer = $($element).attr('lawyer');
                $scope.$watch('engagements', function (data) {
                    if (data !== undefined) {
                        $.each(data, function (i, engagement) {
                            if (parseInt(lawyer) === engagement.lawyer_id) {
                                $scope.lawyer_engaged = 'Already Contacted';
                                $scope.enagagement_url = engagement.absolute_url;
                                $scope.hide = '';
                                return false
                            } else {
                                $scope.hide = 'hide';
                            }
                        });
                    }
                });

            },
            template: '<span class="badge btn-info badge-lawyer-engaged {{ hide }}"><a href="{{ enagagement_url }}">{{ lawyer_engaged }}</a></span>',


            replace: false
        }
    });