'use strict';

describe('directives', function () {
    var elm, scope, lawyer_data;

    beforeEach(module('App'));

    beforeEach(inject(function ($rootScope, $compile) {
        elm = angular.element(
            '<engaged lawyer="1"></engaged>');

        scope = $rootScope;
        scope.engagements = lawyer_data;
        $compile(elm)(scope);
        scope.$digest();
    }));

    it('should create a span with correct classes', inject(function($compile, $rootScope) {
        var badge = $(elm[0]).find('span.badge-lawyer-engaged');
        expect(badge.attr('class')).toBe('badge btn-info badge-lawyer-engaged hide')
    }));

    beforeEach(function() {
        lawyer_data = {"1":{"absolute_url":"/testURL/","engagement_status":0,"lawyer_id":1,"status":"new"}};
        scope.$digest();
    });

    it('should remove hide class when lawyer matches pk', inject(function($compile, $rootScope) {
        var badge = $(elm[0]).find('span.badge-lawyer-engaged');
        expect(badge.attr('class')).toBe('badge btn-info badge-lawyer-engaged ')
    }));

    it('should populate href with the absolute_url', inject(function($compile, $rootScope) {
        var anchor = $(elm[0]).find('span.badge-lawyer-engaged a');
        expect(anchor.attr('href')).toBe("/testURL/");
    }));
});