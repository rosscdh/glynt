'use strict';

App.controller('TransactBuilderCtrl', function ($scope, apiCall) {
    apiCall.query({
        type: 'todo/count',
    }, function (data) {
        var progress_count = {};

        // get the current users data
        if (data.objects[0] !== undefined) {
            progress_count = $.extend(true, {}, data.objects[0])
        }

        $scope.progress_count = progress_count;
    });
});

