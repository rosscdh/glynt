/**
 * 
 */

angular.module('lawpal').controller( 'checklistCtrl', [ '$scope', 'lawPalService', /*'$dialog' ,*/function( $scope, lawPalService, $dialog ) {

	$scope.model = {
		'project': { 'uuid': null },
		'checklist': [],
		'usertype': lawPalService.getUserType(),
		'manage': { 'create':'#', 'edit': '#', 'delete': '#' },
		'dialogOpts': {}
	};

	// Load initial items
	var promise = lawPalService.getChecklist( 'sort_position_by_cat' )
	promise.then( 
		function( results ) {
			/* Success */
			$scope.model.checklist = results;
			console.log($scope.model.checklist);
		},
		function( details ) {
			/* Error */
		}
	);
	/*
	$scope.openDialog = function( category, url ) {
		$scope.dialogOpts = {
			'backdrop': true,
			'keyboard': true,
			'backdropClick': true,
			'templateUrl': url,
			'controller': 'dialogController'
		};

		debugger;

		var d = $dialog.dialog( $scope.dialogOpts )
		d.open().then( function( result ){
			if(result)
		      {
		        console.log('dialog closed with result: ' + result);
		      }
		});
	};
	*/

	$scope.deleteItem = function( item ) {
		//
		var promise = lawPalService.deleteItem( item );
		promise.then( 
			function( results ) {
				/* Success */
				console.log( results );
				$scope.removeItemFromList( item );
			},
			function( details ) {
				/* Error */
				console.error( details );
			}
		);
	};

	$scope.getItemStatus = function( item ) {
		switch( item.status )
		{
			case 0: return "new";
			case 1: return "open";
			case 2: return "pending";
			case 3: return "resolved";
			case 4: return "closed";
		}
	};

	$scope.removeItemFromList = function( item ) {
		var index = $scope.findItemIndex( item );
		if( index !== null )
			$scope.model.checklist.splice( index, 1 );
	};

	$scope.findItemIndex = function( item ) {
		var list = $scope.model.checklist;
		for( var i=0; i<list.length; i++) {
			if( list[i].id === item.id )
				return i;
		}

		return null;
	};

	$scope.initalise =function( options ){
		if(!options) return;

		if( options.project ) {
			$scope.model.project = options.project;
		}

		if( options.manage ) {
			$scope.model.manage = options.manage;
		}
	};

}]);

function dialogController( $scope, dialog ) {
	$scope.close = function( result ) {
		// This dialog is not yet an angular based dialog
		dialog.close( result );
	};
}