'use strict';

angular.module('App.Services', ['ngResource']).
    factory('apiCall', function ($resource) {
        return $resource('/api/v1/:type',
            {type: '@type'},
            {
                query: {
                    method: 'GET',
                    isArray: false
                }
            }
        );
    });