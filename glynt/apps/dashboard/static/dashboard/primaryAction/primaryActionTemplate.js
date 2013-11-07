/**
 * Discussion list template
 * used in conjuction with 'discussionListDirective.js'
 */
angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/project/primaryAction.html",
		'<a class="btn btn-block btn-{[{topPriority.name}]}" ng-href="{[{topPriority.url}]}"><h1 ng-bind="topPriority.value"></h1><span ng-bind="topPriority.label"></span></a>\n'+
		'\n'+
	'');
}]);