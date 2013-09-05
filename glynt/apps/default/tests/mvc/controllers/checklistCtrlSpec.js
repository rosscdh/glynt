/**
 * checklistCtrl: Controller test
 */
'use strict';

/* jasmine specs for checklistCtrl controller */
describe('Testing checklistCtrl', function() {
	var $scope = {};
	var ctrl = null;
	
	beforeEach(module('lawpal'));

	beforeEach(inject(function($rootScope, $controller) {
		//create a scope object for us to use.
		$scope = $rootScope.$new();

		// run scope through controller
		// injecting any services or other injectables we need.
		ctrl = $controller('checklistCtrl', {
		  $scope: $scope
		});

	}));

	// Test project ID
	it('should have project uuid of 1234567890', function() {
		// Initialise project ID
		$scope.initalise( { "project": { "uuid": "1234567890" } } );
		expect($scope.model.project.uuid).toEqual('1234567890');
	});

	// Test checklist items assigned to the current user #1
	it('should return true, items is assigned', function() {
		// Initialise basic checklist
		var item = { "slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295" };
		// Initialise basic feedback object
		$scope.model.feedbackRequests = { "1dfefcfe4f86d49254cd2ddd57331b17deff2295": [ { "slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295" } ] };
		// There should only be one
		expect($scope.isChecklistItemAssigned(item)).toBeTruthy();
	});

	// Test checklist items assigned to the current user #1
	it('should return false, items is not assigned', function() {
		// Initialise basic checklist
		var item = { "slug": "a different slug" };
		// Initialise basic feedback object
		$scope.model.feedbackRequests = { "1dfefcfe4f86d49254cd2ddd57331b17deff2295": [ { "slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295" } ] };
		// There should only be one
		expect($scope.isChecklistItemAssigned(item)).toBeFalsy();
	});

	// Test checklist items assigned to the current user #1
	it('should return 1 items in a category', function() {
		// Initialise category to search on
		var category = { "label": "Qualification to do business" };
		// Initialise basic checklist
		$scope.model.checklist = [ { "category": "Qualification to do business", "slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295" } ];
		// Initialise basic feedback object
		$scope.model.feedbackRequests = { "1dfefcfe4f86d49254cd2ddd57331b17deff2295": [ { "slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295" } ] };
		// Make request to update numAssigned
		$scope.assignedPerCategory(category);
		// There should only be one
		expect(category.numAssigned).toEqual(1);
	});

	// Test checklist items assigned to the current user #2
	it('should return 0 items in a category', function() {
		// Initialise category to search on
		var category = { "label": "Qualification to do business" };
		// Initialise basic checklist
		$scope.model.checklist = [ { "category": "Qualification to do business", "slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295" } ];
		// Initialise basic feedback object
		$scope.model.feedbackRequests = { "a different slug": [ { "slug": "a different slug" } ] };
		// Make request to update numAssigned
		$scope.assignedPerCategory(category);
		// There should only be one
		expect(category.numAssigned).toEqual(0);
	});

	// Test checklist items assigned to the current user #2
	it('should return 1 items matching slug', function() {
		// Initialise basic checklist
		var slug = "1dfefcfe4f86d49254cd2ddd57331b17deff2295";
		$scope.model.checklist = [ { "slug": slug } ];
		// Make request to update numAssigned
		var item = $scope.itemBySlug(slug);
		// There should only be one
		expect(item.slug).toEqual(slug);
	});

	// Test checklist items assigned to the current user #2
	it('should return 1 items matching slug', function() {
		// Initialise basic checklist
		var slug = "1dfefcfe4f86d49254cd2ddd57331b17deff2295";
		$scope.model.checklist = [ { "slug": slug } ];
		// Make request to update numAssigned
		var item = $scope.itemBySlug("123");
		// There should only be one
		expect(item).toEqual(null);
	});

	// Test checklist items assigned to the current user #2
	it('should return 1 alert with message "Hello World"', function() {
		// Make request to update numAssigned
		$scope.addAlert( "Hello World" );
		var count = $scope.model.alerts.count( function( alert ) {
			return alert.message === "Hello World" && alert.type === "info";
		});
		// There should only be one
		expect(count).toEqual(1);
	});

	// Test checklist items assigned to the current user #2
	it('should return 1 alert with message "Hello World" with type "warning"', function() {
		// Make request to update numAssigned
		$scope.addAlert( "Hello World", "warning" );
		var count = $scope.model.alerts.count( function( alert ) {
			return alert.message === "Hello World" && alert.type === "warning";
		});
		// There should only be one
		expect(count).toEqual(1);
	});
});