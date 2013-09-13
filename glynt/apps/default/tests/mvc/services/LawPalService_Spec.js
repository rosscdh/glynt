/**
 * checklistCtrl: Controller test
 */
'use strict';

/* jasmine specs for lawPalService factory */
describe('lawPalService tests', function () {
	var svc,
		httpBackend;
	
	beforeEach(function (){	
		//load the module.
		module('lawpal');
		
		//get your service, also get $httpBackend
		//$httpBackend will be a mock, thanks to angular-mocks.js
		inject(function($httpBackend, lawPalService) {
			svc = lawPalService;
		});

		jasmine.Clock.useMock();
	});

	it('should send the msg and return the response.', function (){
		var test = {
	      handler: function(data) {}
	    };

	    spyOn(test, 'handler');

		//make the call.
		var returnedPromise = svc.getCategories();
		
		//use the handler you're spying on to handle the resolution of the promise.
		returnedPromise.then( test.handler() );
		
		//check your spy to see if it's been called with the returned value.	
		expect(test.handler).toHaveBeenCalled();
	});	
});