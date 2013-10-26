/**
 * Multi-Progress bar
 */
(function(angular){
	'use strict';
	var multiWidgetsModule = angular.module('multi-progress-bar', []);

	multiWidgetsModule.directive('multiProgress', function() {
		
		return {
			'restrict': 'C',
			'templateUrl': 'template/progress/multi-progress.html',
			'scope': {
				'position': '=position'
			},
			'link': function( scope, iElm, iAttrs ) {
				//scope.closeable = 'close' in iAttrs || null;
				scope.position = iAttrs.position || 'bottom';
			},
			'controller': 'multiProgressCtrl'
		};
	});

	multiWidgetsModule.directive('progressBar', function() {
		
		return {
			'restrict': 'EA',
			'templateUrl': 'template/progress/progress-bar.html',
			'link': function( scope, iElm, iAttrs ) {
				scope.model = iAttrs.model || null;
			},
			'controller': 'progressCtrl'
		};
	});

	multiWidgetsModule.controller('multiProgressCtrl', [ '$scope', '$attrs', '$element', 'multiProgressService', function( $scope, $attrs, $element, multiProgressService ) {
		$scope.progressBars = multiProgressService.getProgressStates();
		$scope.$watch( 'progressBars', function(){
			console.log( "progressBars", $scope.progressBars.length );
			if($scope.progressBars.length===0) {
				$($element).css('display','none');
			} else {
				$($element).css('display','block');
			}
		}, true);
		
	}]);

	multiWidgetsModule.controller('progressCtrl', [ '$scope', '$attrs', 'multiProgressService', function( $scope, $attrs, multiProgressService ) {
		$scope.progressBars = multiProgressService.getProgressStates();
	}]);

	multiWidgetsModule.factory('multiProgressService', [ '$rootScope', function( $rootScope ) {
		// Contains all of the progress states across all controllers and views
		var progressStates = [];

		return {
			'getProgressStates': function() {
				return progressStates;
			},
			updateProgress: function( item, progress ) {
				item.percent = progress;
				$rootScope.$apply();
			},
			'push': function( details ) {
				details.id = new Date().getTime();
				progressStates.push( details );
				return progressStates[progressStates.length-1];
			},
			'remove': function( details ) {
				var id = details.id;
				var index = -1;
				for(var i=i;i<progressStates.length;i++) {
					if(progressStates[i].id===id) index = i;
				}

				if( index )
					progressStates.splice(i,1);
			}
		};
	}]);

	multiWidgetsModule.run(["$templateCache", function($templateCache) {
		$templateCache.put("template/progress/multi-progress.html",
		'<div class="multi-progress-container">\n' +
		'    <div ng-repeat="bar in progressBars" progress-bar ng-model="bar" class="multi-progress-bar"></div>\n' +
		'</div>\n'+
		'');
	}]);

	multiWidgetsModule.run(["$templateCache", function($templateCache) {
		$templateCache.put("template/progress/progress-bar.html",
		'<div class="progress-container">\n'+
		'   <div class="progress">\n' +
		'       <div class="progress-bar progress-bar-{{bar.type}}" style="width:{{bar.percent}}%"><span ng-bind="bar.label"></span></div>\n' +
		'   </div>\n'+
		'</div>\n'+
		'');
	}]);
})(window.angular);