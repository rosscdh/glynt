'use strict';

angular.module('app.services', ['ngResource']).
    factory('apiCall', function ($resource) {
        return $resource('/api/v1/:type',
            {type: '@type'},
            {
                query: {
                    method: 'GET',
                    isArray: false,
                    cache : true
                }
            }
        );
    });