angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/attachment/feedback.html",
		'	<div class="modal-dialog">\n'+
		'		<div class="modal-content">\n'+
		'			<div class="modal-header">\n'+
		'				<h3>Feedback</h3>\n'+
		'			</div>\n'+
		'			<form class="form-discussion" ng-submit="ok()">\n'+
		'				<div class="modal-body">\n'+
		'					<div class="form-group">\n'+
		'						<textarea ng-model="data.comment" class="form-control" placeholder="Enter a feedback request comment"></textarea>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'				<div class="modal-footer">\n'+
		'					<button class="btn btn-default" ng-click="cancel()">Cancel</button>\n'+
		'					<button class="btn btn-primary" type="submit">Ok</button>\n'+
		'				</div>\n'+
		'			</form>\n'+
		'		</div>\n'+
		'	</div>'
	);
}]);