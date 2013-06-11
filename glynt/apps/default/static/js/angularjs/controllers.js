'use strict';

angular.module('app.controllers', []).
    controller('MarketplaceCtrl', function ($scope, apiCall) {
        apiCall.get({
            type: 'engagement',
            engagement_status__in: '0,1'
        }, function(data) {
            $scope.engagements = data.objects;
        });
    });