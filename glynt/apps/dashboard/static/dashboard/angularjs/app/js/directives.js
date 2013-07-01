'use strict';

var counter_template = '<div class="thumbnail"><h1 style="font-size: 80px;">{{ total }}</h1><div class="caption"><h3 class="{{ label_css_class }}" style="color: white;">{{ type_label }}</h3></div></div>';

var label_data = function label_data(count_type) {
    var data = {
        'label_css_class': '',
        'label': '',
    };
    switch (count_type)
    {
        case 'open':
            data.label_css_class = 'label-important';
            data.label = 'open items';
        break;
        case 'pending':
            data.label_css_class = 'label-warning';
            data.label = 'pending items';
        break;
        case 'closed':
            data.label_css_class = 'label-success';
            data.label = 'closed items';
        break;
    }
    return data
}

var controllerHandle = function controllerHandle($scope, $element, $attrs) {
    var count_type = $attrs.counttype;
    // console.log($scope)
    $scope.$watch('progress_count', function (data) {
        if (data !== undefined) {
            var label = label_data(count_type);
            $scope.total = data.counts[count_type] || 0;
            $scope.type_label = label.label;
            $scope.label_css_class = label.label_css_class;
        }
    });
}

App.directive('counttype', function () {
return {
    restrict: 'A',
    transclude: true,
    scope: true,
    controller: controllerHandle,
    template: counter_template,
    replace: true
}
});
