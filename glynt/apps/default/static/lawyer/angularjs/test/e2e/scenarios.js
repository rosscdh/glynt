describe('Lawyer App', function () {

    /* Needs ngMockE2E added to App */

    describe('Marketplace', function () {
        beforeEach(function () {
            browser().navigateTo('/lawyers/');
        });

        it('should display 10 lawyer engaged badges', function () {
            expect(element('.badge-lawyer-engaged').count()).toBe(10);
        });

        it('should display 2 visible lawyer engaged badges', function () {
            expect(element('.badge-lawyer-engaged:visible').count()).toBe(2);
        });

        it('should link to engagement if visible', function () {
            expect(element('.badge-lawyer-engaged:visible a').attr('href')).toContain('engage');
        });
    });

});