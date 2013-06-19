'use strict';

var App = angular.module('App', ['ngResource' /*', ngMockE2E'*/]);


/** MOCK API FOR E2E TESTING IN ANGULAR  **/

/*
App.run(function ($httpBackend) {
    $httpBackend.whenGET('/api/v1/engagement?engagement_status__in=0,1').respond(
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
});
*/