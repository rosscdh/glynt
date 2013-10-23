/**
 * Displays a discussion list
 * @author : Lee Sinclair
 * date 17 Oct 2013
 */
angular.module('lawpal').directive('discussionList', [ 'lawPalService', 'toaster', '$modal', 'discussionItemService', function ( lawPalService, toaster, $modal, discussionItemService ) {
	'use strict';
	return {
		"restrict": "AC",
		"templateUrl":'template/lawpal/discussion/list.html',
		"scope": {
			"discussions": "=discussion",
			"tag": "=tag"
		},
		"link": function (/*scope, iElement, iAttrs*/) {
		},
		"controller": [ '$scope', '$element', '$attrs', function( $scope/*, $element, $attrs*/ ) {
			var working = {
				"dicussions": {}
			};

			$scope.working = {
				"discussions": {},
				"loading": true
			};
			
			/**
			 * Returns true if the discussion item was last responded to by the current user
			 * @param  {Integer} pk Primary key of the user who write the discussion item/response
			 * @return {Boolean}	tre if writter by current user
			 */
			$scope.byMe = function( pk ) {
				var userPk = lawPalService.getCurrentUser().pk;
				return userPk && userPk === pk;
			};

			/**
			 * Generate working copy of discission list. includes original and lastest response data
			 * @param  {Integer} parentId PK of comment of the parent (optional)
			 * @param  {Integer} childId  PK of the child comment (optional)
			 */
			$scope.generateWorkingDiscussionData = function() {
				var dItem;
				var data = [];
				
				if( !angular.isArray($scope.discussions) ) {
					return [];
				}

				var dis = $scope.discussions.filter(
					function( item ) {
						return item.parent_id===null;
					}
				);

				for( var i=0; i<dis.length;i++) {
					dItem = {
						"original": dis[i],
						"latest": dis[i].last_child || dis[i]
					};

					data.push(dItem);
				}

				$scope.working.loading = false;
				$scope.working.discussions = data; //$scope.data.discussions;
			};

			/**
			 * Watch the discussions variable for changes (deep watch)
			 */
			$scope.$watch( 'discussions', function () {
				$scope.generateWorkingDiscussionData();
			}, true);

			/**
			 * Request display of a specific discussion
			 * @param  {Object} discussion Discussion item to display
			 */
			$scope.displayDiscussion = function( discussion ) {
				discussionItemService.show( discussion );
			};

			/**
			 * Request a new discussion item
			 */
			$scope.new = function( ){
				discussionItemService.add();
			};

			/**
			 * Request a reply
			 * @param  {Object} discussion Parent discussion object
			 */
			$scope.reply = function( discussion ){
				discussionItemService.reply( discussion );
			};

			/**
			 * Recieves an update that there has been a new discussion item added
			 * @param  {Event} evt
			 * @param  {Object} message  Message created by the end user
			 * @param  {Object} response Discussion item sent back from the API in response to the "message"
			 */
			$scope.$on('discussion-new-item', function ( evt, message, response ) {
				$scope.discussions.push( response );
				addLastChild( message.parent_id, response );
				$scope.generateWorkingDiscussionData(  /*message.parent_id, response.id*/ );
			});

			var addLastChild = function( parentId, newItem ) {
				for(var i=0;i< $scope.discussions.length;i++ ) {
					if( $scope.discussions[i].id===parentId) {
						$scope.discussions[i].last_child = newItem;
					}
				}
			};

			/**
			 * Given and Object attempt to find it quickly, uses object keys for speed. If an object is not passed through then the working list is generated.
			 * Please note that working is not in $scope. This is to avoid angular watching for changes and reducing page speed
			 * @param  {Array/String} obj Array of discussion items or a look up string
			 * @return {Object}	 Discussion item
			 */
			/*
			function discussionLookup( obj ) {
				if(angular.isArray(obj)) {
					for (var i=0;i<obj.length;i++) {
						working.dicussions[obj[i].id] = obj[i];
					}
				}
				else {
					return working.dicussions[obj]||null;
				}
			}
			*/
		}]
	};
}]);

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
		'	<tr ng-repeat="discussion in working.discussions  | orderBy:\'latest.id\':true" class="byme-{[{byMe(discussion.latest.meta.user.pk)}]}">\n'+
		'		<td class="status-column">\n'+
		'			<i class="icon icon-comment nest">\n'+
		'				<small class="nested text-primary" ng-bind="discussion.original.count">1</small>\n'+
		'			</i>\n'+
		'		</td>\n'+
		'		<td class="vcard-column">\n'+
		'			<div class="fn fn-large vcard" user-mini-widget user="discussion.latest.meta.user" data-show-props="photo"></div>\n'+
		'			<div class="time text-muted">\n'+
		'				<i class="icon icon-time"></i>\n'+
		'				<small ng-bind="discussion.latest.meta.timestamp | timeAgo"></small>\n'+
		'			</div>\n'+
		'		</td>\n'+
		'		<td class="comment-column">\n'+
		'			<p class="comment clickable" ng-bind="discussion.latest.comment | characters:200" ng-click="displayDiscussion(discussion)"></p>\n'+
		'			<div><button type="button" class="btn btn-link btn-small pull-right" tooltip="Respond now" ng-click="reply(discussion.original)">\n'+
		'				<i class="icon icon-reply"></i> Respond\n'+
		'			</button></div>\n'+
		'		</td>\n'+
		'		<td class="more-column clickable">\n'+
		'			<i class="icon icon-chevron-right text-muted" ng-click="displayDiscussion(discussion)"></i>\n'+
		'		</td>\n'+
		'	</tr>\n'+
		'</table>\n'
	);
}]);