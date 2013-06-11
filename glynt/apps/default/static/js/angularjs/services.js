'use strict';

angular.module('api_v1', ['ngResource']).
    factory('apiCall', function ($resource) {
        return $resource('/api/v1/:type/:id',
            {type: '@type', id: '@id'},
            {
                get: {method: 'GET'}
            }
        );
    });