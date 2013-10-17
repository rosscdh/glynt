'use strict';
 
/*
 * AngularJS Toaster
 *
 * Copyright 2013 Jiri Kavulak.	
 * All Rights Reserved.	
 * Use, reproduction, distribution, and modification of this code is subject to the terms and 
 * conditions of the MIT license, available at http://www.opensource.org/licenses/mit-license.php
 *
 * Author: Jiri Kavulak
 * Related to project of John Papa and Hans Fjällemark
 */
 
angular.module('lawpal')
.service('discussionViewer', [ '$rootScope', function ($rootScope) {
		this.show = function ( discussion ) {
				this.discussion = discussion;
				$rootScope.$broadcast('discussion-show');
		};
}])
.directive('discussionViewerContainer', ['$compile', '$timeout', 'discussionViewer', '$anchorScroll',
function ($compile, $timeout, discussionViewer, $anchorScroll ) {
	return {
		'replace': true,
		'restrict': 'EAC',
		'link': function (scope/*, elm, attrs*/){
			
			function showDiscussion ( discussion ){
				scope.discussions.push(discussion);
			}
			
			scope.discussions = [];
			scope.$on('discussion-show', function () {
				showDiscussion(discussionViewer.discussion);
        $anchorScroll();
			});
		},
		'controller': function($scope/*, $element, $attrs*/) {
			
			$scope.close = function(){
				$scope.discussions = [];
			};
		},
		'template':
		'<div class="full-dialog-container">' +
			'<div ng-animate="\'animateToaster\'" ng-repeat="discussion in discussions"><div class="full-dialog-underlay"></div>' +
				'<div class="full-dialog">' +
					'<div class="container full-dialog-content">\n'+
					'	 <div class="clearfix"><button class="close" ng-click="close()">&times</button></div>\n'+
					'	 <div class="row clearfix">\n' +
          // Start: avatar column
					'		 <div class="col-lg-1">\n'+
					'			  <div class="fn fn-lg clearfix" user-mini-widget user="discussion.latest.meta.user" data-show-props="photo"></div>\n'+
					'	      <div class="time text-muted">\n'+
					'			     <i class="icon icon-time"></i>\n'+
					'			     <small ng-bind="discussion.latest.meta.timestamp | timeAgo"></small>\n'+
					'		    </div>\n'+
					'		 </div>\n'+
          // End: avatar column
          '    <div class="col-lg-11">\n'+
          '       <div class="comment" ng-bind="discussion.latest.comment"></div>\n'+
          '    </div>\n'+
          // End: comment column
					'	 </div>\n'+
					'</div>\n'+
				'</div>' +
			'</div>' +
		'</div>'
	};
}]);