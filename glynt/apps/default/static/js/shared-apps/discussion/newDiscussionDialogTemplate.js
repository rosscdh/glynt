angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/discussion/newDiscussion.html",
		'	<div class="modal-dialog discussion-modal">\n'+
		'		<div class="modal-content">\n'+
		'			<div class="modal-header">\n'+
		'				<h3 ng-bind="title"></h3>\n'+
		'			</div>\n'+
		'			<form class="form-discussion" ng-submit="ok()">\n'+
		'				<div class="modal-body">\n'+
		'					<div class="form-group" ng-show="!hasParent">\n'+
		'						<label for="discussionSubject" class="sr-only">Subject</label>\n'+
		'						<input type="text" id="discussionSubject" ng-model="message.subject" class="form-control" />\n'+
		'					</div>\n'+
		'					<div class="form-group">\n'+
		'						<label for="discussionComment" class="sr-only">Message</label>\n'+
		'						<textarea id="discussionComment" required="true" ng-model="message.comment" class="form-control" rows="5"></textarea>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'				<div class="modal-footer">\n'+
		'					<button class="btn btn-default" ng-click="cancel()">Cancel</button>\n'+
		'					<button class="btn btn-primary" type="submit">Save</button>\n'+
		'				</div>\n'+
		'			</form>\n'+
		'		</div>\n'+
		'	</div>'
	);
}]);