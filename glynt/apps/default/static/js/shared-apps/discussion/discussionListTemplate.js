/**
 * Discussion list template
 * used in conjuction with 'discussionListDirective.js'
 */
angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/discussion/list.html",
		'<button class="btn btn-link btn-small pull-right widget-title-button" ng-click="new(null)">\n'+
		'	<i class="icon icon-plus"></i>\n'+
		'		&nbsp;New\n'+
		'</button>\n'+
		'<h3>Discussions and Issues</h3>\n'+
		'<span ng-show="working.loading" class="text-muted"><i class="icon icon-spinner icon-spin"></i> Loading discussions</span>\n'+
		'<p ng-show="working.discussions.length==0" class="text-muted"><button class="btn btn-link" ng-click="new(null)">Start a discussion</button></p>\n'+
		'<table class="table table-striped">\n'+
		'	<tr ng-repeat="discussion in working.discussions  | orderBy:\'latest.id\':true" class="byme-{[{byMe(discussion.latest.meta.user.pk)}]}"  ng-click="displayDiscussion( $event, discussion)">\n'+
		'		<td class="status-column clickable">\n'+
		'			<i class="icon icon-comment nest">\n'+
		'				<small class="nested text-primary" ng-bind="discussion.original.count">1</small>\n'+
		'			</i>\n'+
		'		</td>\n'+
		'		<td class="vcard-column clickable">\n'+
		'			<div class="fn fn-large vcard" user-mini-widget user="discussion.latest.meta.user" data-show-props="photo"></div>\n'+
		'			<div class="time text-muted">\n'+
		/*'				<i class="icon icon-time"></i>\n'+*/
		'				<small ng-bind="discussion.latest.meta.timestamp | timeAgo"></small>\n'+
		'			</div>\n'+
		'		</td>\n'+
		'		<td class="comment-column">\n'+
		'			<div class="comment clickable">\n'+
		'			    <p ng-show="discussion.original.title"><strong ng-bind="discussion.original.title | characters:50"></strong></p>\n'+
		'			    <p ng-bind="discussion.latest.comment | characters:200"></p>\n'+
		'			</div>\n'+
		'			<div><button type="button" class="btn btn-link btn-small pull-right" tooltip="Respond now" ng-click="reply( $event, discussion.original)">\n'+
		'				<i class="icon icon-reply"></i> Respond\n'+
		'			</button></div>\n'+
		'		</td>\n'+
		'		<td class="more-column clickable">\n'+
		'			<i class="icon icon-chevron-right text-muted"></i>\n'+
		'		</td>\n'+
		'	</tr>\n'+
		'</table>\n'
	);
}]);