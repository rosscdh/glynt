'use strict';

describe('Controllers', function () {
    var $scope = null;
    var $controller = null;
    var $httpBackend = null;

    beforeEach(function () {
        this.addMatchers({
            // we need to use toEqualData because the Resource has extra properties
            // which make simple .toEqual not work.
            toEqualData: function (expect) {
                return angular.equals(expect, this.actual);
            }
        });
    });

    //you need to indicate your module in a test
    beforeEach(module('App'));

    // read: http://docs.angularjs.org/api/ngMock.$httpBackend
    beforeEach(inject(function ($rootScope, _$controller_, _$httpBackend_) {
        $scope = $rootScope.$new();
        $controller = _$controller_;
        $httpBackend = _$httpBackend_;
    }));

    // use console.log(JSON.stringify(engagements)); in controllers.js
    var desired_result = {"44":{"absolute_url":"/engage/ed71d690bf273a9fb7e74dc4faf7b254b27310cc/","engagement_status":0,"lawyer_id":44,"status":"new"},"49":{"absolute_url":"/engage/0330ace35cc7345351a8a40f0770ead8ffd16fa1/","engagement_status":0,"lawyer_id":49,"status":"new"}};

    it('It should exist', function () {
        // Expect that the resource (or http) makes a request.
        $httpBackend.expect('GET', '/api/v1/engagement?engagement_status__in=0,1').respond(
            {
                meta: {
                    limit: 20,
                    next: null,
                    offset: 0,
                    previous: null,
                    total_count: 2
                },
                objects: [
                    {
                        absolute_url: "/engage/0330ace35cc7345351a8a40f0770ead8ffd16fa1/",
                        engagement_status: 0,
                        lawyer_id: 49,
                        status: "new"
                    },
                    {
                        absolute_url: "/engage/ed71d690bf273a9fb7e74dc4faf7b254b27310cc/",
                        engagement_status: 0,
                        lawyer_id: 44,
                        status: "new"
                    }
                ]
            }
        );

        // create controller which will cause Project.query which in turn does $http
        var ctrl = $controller('MarketplaceCtrl', {$scope: $scope});

        // At this point the Project.query() returns empty array since the server
        // did not respond.
        expect($scope.engagements).toEqual();

        // Simulate server response.
        $httpBackend.flush();

        // The projects now has actual data.
        // we need to use toEqualData because the Resource hase extra properties
        // which make simple .toEqual not work.
        expect($scope.engagements).toEqualData(desired_result);
    });
});


