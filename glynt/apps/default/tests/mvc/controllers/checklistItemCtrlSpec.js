/**
 * checklistCtrl: Controller test
 */
'use strict';

/* jasmine specs for checklistItemCtrl controller */
describe('Testing checklistItemCtrl', function() {
	var $scope = {};
	var ctrl = null;
	
	beforeEach(module('lawpal'));

	beforeEach(inject(function($rootScope, $controller) {
		//create a scope object for us to use.
		$scope = $rootScope.$new();

		// run scope through controller
		// injecting any services or other injectables we need.
		ctrl = $controller('checklistItemCtrl', {
		  $scope: $scope
		});

	}));

	// Checklist item status
	it('should have item status of "new"', function() {
		// Initialise $scope.item
		$scope.item = { "status": 0 };
		expect($scope.getItemStatus()).toEqual('new');
	});

	// Checklist item status
	it('should have item status of "new"', function() {
		// Initialise $scope.item
		$scope.item = { "status": 9 };
		expect($scope.getItemStatus()).toEqual('unknown');
	});
});