/**
 * Discussion list template
 * used in conjuction with 'discussionListDirective.js'
 */
angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/discussion/list.html",
		'<button class="btn btn-link btn-small pull-right widget-title-button" ng-click="new(null)" ng-show="title">\n'+
		'	<i class="icon icon-plus"></i>\n'+
		'		&nbsp;New\n'+
		'</button>\n'+
		'<h3 ng-show="title" ng-bind="title">Discussions and Issues</h3>\n'+
		'<span ng-show="working.loading" class="text-muted"><i class="icon icon-spinner icon-spin"></i> Loading discussions</span>\n'+
		'<em ng-show="paging">\n'+
		'  <span class="text-muted">Discussion {[{starting+1}]}/{[{working.discussions.length}]}</span>\n'+
		'  <button ng-click="movePage(-1)" href="javascript:;" class="btn-link" ng-disabled="starting==0">&lt; previous</button>\n'+
		'  <button ng-click="movePage(+1)" href="javascript:;" class="btn-link" ng-disabled="starting==working.discussions.length-1">next &gt;</button>\n'+
		'  <button ng-click="new(null)" href="javascript:;" class="btn-link pull-right">+ new</button>\n'+
		'</em>\n'+
		'<p ng-show="working.discussions.length==0"><button class="btn btn-link" ng-click="new(null)">Start a discussion</button></p>\n'+
		'<table class="table table-striped">\n'+
		'	<tr ng-repeat="discussion in working.discussions | startFrom: starting | limitTo: pageLimit" class="byme-{[{byMe(discussion.latest.meta.user.pk)}]} discussion-item"  ng-click="displayDiscussion( $event, discussion)">\n'+
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
		'			    <p class="discussion-title"><strong ng-bind="discussion.original.title | characters:50">&nbsp;</strong></p>\n'+
		'			    <p class="discussion-comment" ng-bind="discussion.latest.comment | characters:descriptionTextLimit"></p>\n'+
		'			</div>\n'+
		'		</td>\n'+
		'		<td class="more-column clickable" tooltip="Respond now" tooltip-append-to-body="true" ng-click="reply( $event, discussion.original)">\n'+
		'			<button type="button" class="btn btn-link btn-small pull-right btn-respond">\n'+
		'				<i class="icon icon-reply"></i><br /> Respond\n'+
		'			</button>\n'+
		/*'			<i class="icon icon-chevron-right text-muted"></i>\n'+*/
		'		</td>\n'+
		'	</tr>\n'+
		'</table>\n'+
	'');
}]);