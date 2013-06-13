'use strict';

App.controller('MarketplaceCtrl', function ($scope, apiCall) {
    apiCall.query({
        type: 'engagement',
        engagement_status__in: '0,1'
    }, function (data) {
        var engagements = {};
        $.each(data.objects, function (i, engagement) {
            engagements[engagement.lawyer_id] = engagement
        });
        //console.log(JSON.stringify(engagements)); /* Helpful for testing */
        $scope.engagements = engagements;
    });
});

