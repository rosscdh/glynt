angular.module('lawpal').run(["$templateCache", function($templateCache) {
	'use strict';
	$templateCache.put("template/lawpal/project/profileDialog.html",
		'<link href="/static/css/theme/lawyer-profile.css" rel="stylesheet" />\n'+
		'<div class="modal-dialog">\n'+
		'	<div class="modal-content">\n'+
		'		<div class="modal-body">\n'+
		'			<button type="button" class="close" ng-click="cancel()" aria-hidden="true">×</button>\n'+
		'			<div id="hero-mini">\n'+
		'				<div class="container container-main">\n'+
		'					<!-- starts carousel -->\n'+
		'					<div class="row profile-details">\n'+
		'						<div class="col col-lg-4 text-center">\n'+
		'							<div class="avatar text-center">\n'+
		'								<img ng-src="{[{user.photo}]}" alt="{[{user.full_name}]}" />\n'+
		'							</div>\n'+
		'						</div>\n'+
		'						<div class="col col-lg-8">\n'+
		'							<h1>{[{user.full_name}]}</h1>\n'+
		'							<h5 style="text-info">\n'+
		'								<span ng-bind="user.role | titleCase"></span>\n'+
		'							</h5>\n'+
		'							<div class="firm">\n'+
		'								<h2 style="text-info">\n'+
		'									<span ng-show="user.years_practiced">{[{user.years_practiced}]} Years Practicing</span>\n'+
		'								</h2>\n'+
		'							</div>\n'+
		'							<ul class="list-unstyled">\n'+
		'								<li ng-show="user.phone">\n'+
		'									<i class="icon-phone"></i> {[{user.phone}]}\n'+
		'								</li>\n'+
		'							</ul>\n'+
		'							<div id="buttons">\n'+
		'								<span ng-show="user.is_lawyer">\n'+
		'									<a class="btn btn-success btn-large" ng-show="user.is_authenticated" href="/lawyers/profile/setup/">\n'+
		'										<i class="icon-pencil"></i>\n'+
		'										Edit profile\n'+
		'									</a>\n'+
		'								</span>\n'+
		'								<span ng-show="user.is_customer">\n'+
		'									<a class="btn btn-success btn-large" ng-show="user.is_authenticated" href="/customers/setup">\n'+
		'										<i class="icon-pencil"></i>\n'+
		'										Edit profile\n'+
		'									</a>\n'+
		'								</span>\n'+
		'							</div>\n'+
		'						</div>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'			</div>\n'+
		'			<div class="container profile">\n'+
		'				<div class="row">\n'+
		'					<div class="col col-lg-12">\n'+
		'						<p class="lead attorney-quote" ng-bind="user.summary" ng-show="user.summary"></p>\n'+
		'					</div>  \n'+
		'				</div>\n'+
		'				<div ng-show="user.practice_locations">\n'+
		'					<div class="row">\n'+
		'						<div class="col col-9 col-offset-1">\n'+
		'							<h2><i class="glyphicon glyphicon-map-marker text-success"></i>Location</h2>\n'+
		'						</div>\n'+
		'						<div ng-show="user.practice_locations" class="col col-lg-6" ng-repeat="location in user.practice_locations" style="background:url(\'//maps.googleapis.com/maps/api/staticmap?size=450x100&amp;markers=color:blue%7Clabel:S%7C{[{location}]}&amp;sensor=false\');height:100px;background-position:center;"></div>\n'+
		'					</div>\n'+
		'				</div>\n'+
		'				\n'+
		'			</div>\n'+
		'		</div>\n'+
		'		<div class="modal-footer">\n'+
		'			<button class="btn btn-primary" ng-click="cancel()">Close</button>\n'+
		'		</div>\n'+
		'	</div>\n'+
		'</div>'
	);
}]);