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
			"tag": "=tag",
			"title": "=title",
			"projectUuid": "=projectUuid"
		},
		"link": function (/*scope, iElement, iAttrs*/) {
		},
		"controller": [ '$scope', '$element', '$attrs', function( $scope, $element, $attrs ) {
			$scope.working = {
				"discussions": [],
				"loading": true
			};

			$scope.pageLimit = 100;
			$scope.page = 0;
			$scope.starting = 0;
			$scope.paging = false;
			$scope.maxPages = 100;
			$scope.descriptionTextLimit = 200;
			$scope.orderByDate = true;

			if( $attrs.pageLimit ) {
				$scope.pageLimit = parseInt($attrs.pageLimit, 10);
				$scope.page = $attrs.page || 0;
				$scope.starting = $scope.page * $scope.pageLimit;
			}

			if($attrs.orderByDate) {
				$scope.orderByDate = $attrs.orderByDate==="false"?false:true;
			}

			if($attrs.descriptionTextLimit) {
				$scope.descriptionTextLimit = parseInt($attrs.descriptionTextLimit,10);
			}

			$scope.movePage = function( amt ) {
				var maxPages = parseInt($scope.working.discussions.length / $scope.pageLimit, 10) -1;
				$scope.page = $scope.page + amt;
				$scope.page = Math.min(maxPages,$scope.page);
				$scope.page = $scope.page>=0?$scope.page:0;
				$scope.starting = $scope.page * $scope.pageLimit;
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
			$scope.generateWorkingDiscussionData = function( discussions ) {
				var dItem;
				var data = [];
				
				if( !angular.isArray(discussions) ) {
					return [];
				}

				var dis = discussions.filter(
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

				if( $scope.orderByDate && data.length>0 ) {
					console.log("ordering");
					data = data.sort( function( item1, item2 ){
						return item1.latest.id < item2.latest.id;
					});
				}

				$scope.working.loading = false;
				$scope.working.discussions = data; //$scope.data.discussions;
				if( data.length>0 && $attrs.pageLimit ) {
					$scope.paging = true;
				}
			};

			/**
			 * Watch the discussions variable for changes (deep watch)
			 */
			$scope.$watch( 'discussions', function ( nv ) {
				if( typeof(nv)!=="undefined" && nv ) {
					$scope.generateWorkingDiscussionData( nv );
				}
			}, true);

			/**
			 * Request display of a specific discussion
			 * @param  {Object} discussion Discussion item to display
			 */
			$scope.displayDiscussion = function( $event, discussion ) {
				discussionItemService.show( discussion, $scope.projectUuid );
			};

			/**
			 * Request a new discussion item
			 */
			$scope.new = function( ){
				discussionItemService.add( $scope.projectUuid );
			};

			/**
			 * Request a reply
			 * @param  {Object} discussion Parent discussion object
			 */
			$scope.reply = function( $event, discussion ){
				$event.stopPropagation();
				discussionItemService.reply( discussion, $scope.projectUuid );
			};

			/**
			 * Recieves an update that there has been a new discussion item added
			 * @param  {Event} evt
			 * @param  {Object} message  Message created by the end user
			 * @param  {Object} response Discussion item sent back from the API in response to the "message"
			 */
			$scope.$on('discussion-new-item', function ( evt, message, response ) {
				var addToList = true;
				// $scope.projectUuid can be used if there are multiple discussion lists on the page
				if( message.project_uuid && $scope.projectUuid ) {
					// Should the project Id's of the message and the dicussion list not match set addToList to false
					addToList = message.project_uuid === $scope.projectUuid;
				}
				if( addToList ) {
					$scope.discussions.push( response );
					addLastChild( message.parent_id, response );
					$scope.generateWorkingDiscussionData(  /*message.parent_id, response.id*/ );
				}
			});

			/**
			 * Used when responding to discussions, updates last child on existing array elements
			 * @param {Number} parentId Database ID of parent discussion
			 * @param {Object} newItem  Typically response from API
			 */
			var addLastChild = function( parentId, newItem ) {
				for(var i=0;i< $scope.discussions.length;i++ ) {
					if( $scope.discussions[i].id===parentId) {
						$scope.discussions[i].last_child = newItem;
					}
				}
			};
		}]
	};
}]);