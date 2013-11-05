/**
 * Helper filter to assist with pagiation, startfrom represents a record number within an array to diaply results from
 * @return {Array} Filtered array
 */
angular.module('lawpal').filter('startFrom', function() {
    return function(input, start) {
        start = +start; //parse to int
        return input.slice(start);
    }
});