/**
 * Manage team dialog template used un conjuction with manageTeamCtrl.js
 */
angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/project/manageTeam.html",
		'<div class="modal-dialog">\n'+
		'	<div class="modal-content">\n'+
		'		<div class="modal-header">\n'+
		'			<h3>Project team</h3>\n'+
		'			<p>Primary project contacts can add and remove team members</p>\n'+
		'		</div>\n'+
		'		<div class="modal-body">\n'+
		'			<div class="row vcard team-member {[{isRemovedClass(user)}]} user-{[{user.username}]}" ng-repeat="user in team">\n'+
		'				<div class="col col-lg-12">\n'+
		'					<div class="col col-lg-1 photo">\n'+
		'						<img ng-src="{[{user.photo}]}"/>\n'+
		'					</div>\n'+
		'					<div class="col col-lg-7 details">\n'+
		'						<h5 class="fn">{[{user.full_name}]}<span ng-show="user.is_authenticated"> (you)</span></h5>\n'+
		'						<h6 class="company"><a href="/profile/{[{user.company.slug}]}">{[{user.company.name}]}</a></h6>\n'+
		'					</div>\n'+
		'					<div class="col col-lg-4 details">\n'+
		'						<p class="action pull-right" ng-show="canRemove(user)">\n'+
		'							<a href="javascript:;" ng-click="removeUser(user)" ng-show="!user.is_deleted" class="remove-link"><i class="icon icon-remove text-danger"></i> Remove</a>\n'+
		'							<a href="javascript:;" ng-click="removeUser(user)" ng-show="user.is_deleted" class="undo-remove-link"><i class="icon icon-undo"></i> Undo remove</a>\n'+
		'						</p>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'\n'+
		'			</div><!-- row //-->\n'+
		'			<form class="form-search form-horizontal">\n'+
		'				<div class="row">\n'+
		'					<div class="col col-lg-12">\n'+
		'						<h4>Add someone</h4>\n'+
		'						<p class="help-block">You can only add people that have registered with LawPal at this time.</p>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'				<div class="row">\n'+
		'					<div class="col col-lg-8">\n'+
		'						<input \n'+
		'							type="text" \n'+
		'							name="email"\n'+
		'							autocomplete="off"\n'+
		'							class="form-control search-query pull-left searching-{[{searchingEmail}]}" \n'+
		'							placeholder="Email address" \n'+
		'							typeahead="item.email for item in searchEmails($viewValue)" \n'+
		'							typeahead-wait-ms="600"\n'+
		'							typeahead-min-length="3"\n'+
		'							typeahead-loading="searchingEmail"\n'+
		'							ng-model="searchAttrs.selectedEmail" />\n'+
		'					</div>\n'+
		'					<div class="col col-lg-4">\n'+
		'						<button type="submit" class="btn btn-default" ng-click="addToProject(searchAttrs.selectedEmail, emailSearchResults)" ng-disabled="searchingEmail"><i class="icon {[{emailSearchClass(searchingEmail)}]}"></i> Add to project</button>\n'+
		'					</div>\n'+
		'						\n'+
		'				</div>\n'+
		'			</form>\n'+
		'		</div>\n'+
		'		<div class="modal-footer">\n'+
		'			<button class="btn btn-default" ng-click="cancel()">Cancel</button>\n'+
		'			<button class="btn btn-primary" ng-click="ok()">Save</button>\n'+
		'		</div>\n'+
		'	</div>\n'+
		'</div>'
	);
}]);