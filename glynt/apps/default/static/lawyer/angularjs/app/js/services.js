'use strict';

App.factory('apiCall', ['$resource', function ($resource) {
    return $resource('/api/v1/:type',
        {type: '@type'},
        {
            query: {
                method: 'GET',
                isArray: false
            }
        }
    );
}]);