'use strict';

var counter_template = '<div class="thumbnail"><h1 style="font-size: 80px;">{{ total }}</h1><div class="caption"><h3 class="label-important" style="color: white;">{{ type_label }}</h3></div></div>';

App.directive('numopen', function () {
return {
    restrict: 'E',
    transclude: true,
    scope: true,
    controller: function ($scope, $element, $attrs) {
        console.log($attrs)
        $scope.hide = 'hide';
    },
    template: counter_template,
    replace: true
}
});

App.directive('numpending', function () {
return {
    restrict: 'E',
    transclude: true,
    scope: true,
    controller: function ($scope, $element, $attrs) {
        console.log($attrs)
        $scope.hide = 'hide';
    },
    template: counter_template,
    replace: true
}
});

App.directive('numclosed', function () {
return {
    restrict: 'E',
    transclude: true,
    scope: true,
    controller: function ($scope, $element, $attrs) {
        console.log($attrs)
        $scope.hide = 'hide';
    },
    template: counter_template,
    replace: true
}
});

