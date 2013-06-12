'use strict';

describe('controllers', function () {
    //beforeEach(module('App.Controllers'));
    beforeEach(
        module('App', ['App.Controllers', 'App.Directives', 'App.Services'])
    );

    describe('MarketplaceCtrl', function () {
        var scope, ctrl, $httpBackend;

        beforeEach(inject(function (_$httpBackend_, $rootScope, $controller) {
            $httpBackend = _$httpBackend_;
            $httpBackend.expectGET('/api/v1/engagement?engagement_status__in=0,1').
                respond([]);
            scope = $rootScope.$new();
            /* Why is MarketplaceCtrl not working? :( */
            ctrl = $controller('MarketplaceCtrl', {$scope: scope});
        }));

        it('should have a MarketplaceCtrl controller', (function () {
            expect(ctrl).not.to.equal(null);
        }));
    });
});


