/**
 * Displays a full page dialog containing an entire discussion exchange
 * 1. requries a tag on the page somewhere
 *   <div class="discussion-viewer-container"></div>
 * 2. Recieves a broadcast message to display a specific discussion item (most likely a parent)
 *
 * Discussion objects are expected in the following format:
 *   { "original": {}, "lastest": {} }
 */
angular.module('lawpal').directive('discussionViewer', ['$compile', '$timeout', 'discussionItemService', '$anchorScroll', '$location',
  function ($compile, $timeout, discussionItemService, $anchorScroll, $location ) {
    'use strict';
    return {
      'replace': true,
      'restrict': 'EAC',
      'templateUrl':'template/lawpal/discussion/viewConversation.html',
      'link': function ( /*scope , elm, attrs*/ ) {
      },
      'controller': function ($scope /*, $element, $attrs*/ ) {
        // Contains the original discussion, it's an array so the we can take advantage of ngAnimate later
        $scope.discussions = [];
        // An array of replies for the current discussion
        $scope.replies = [];

        $scope.message = {
          "comment": ""
        };

        $scope.close = function () {
          $scope.discussions = [];
          $location.path('/');
        };

        $scope.reply = function (discussion) {
          var reply = discussionItemService.makeReply( $scope.message.comment, discussion);
          if( reply ) {
            discussionItemService.saveDiscussion( reply, function( err ){
              if(!err) {
                $scope.message.comment = "";
              }
            });
          }
        };

        /**
         * Start the process of showing a full discussion
         * @param  {Object} discussion Discussion object
         */
        function showDiscussion( discussion, projectUuid ) {
          $scope.discussions.push(discussion);
          //$(".full-dialog-container").hide().fadeIn("slow");  // To be replaced with ngAnimate when it becomes standard
          $location.path('/discussion/' + discussion.original.id);
          $scope.loadFullDiscussion( discussion.original.id, projectUuid );
        }

        /**
         * Start the process of loading the full discussion
         * @param  {Object} discussion Discussion object
         */
        $scope.loadFullDiscussion = function( discussionId, projectUuid ) {
          discussionItemService.load( discussionId, projectUuid, function( err, results){
            $scope.replies = results.thread;
            if( $scope.discussions.length===0 ) {
              $scope.discussions.push({
                "original": results,
                "latest": results.last_child
              });
            }
          });
        };

        /* Listen when the user requests to see a full discussion */
        $scope.$on('discussion-show', function ( evt, discussion, projectUuid ) {
          showDiscussion( discussion, projectUuid );
          $anchorScroll();
        });

        /* Listen for when new discussion items are added */
        $scope.$on('discussion-new-item', function ( evt, postedData, response ) {
          if( $scope.discussions.length===1 && response.parent_id && response.parent_id === $scope.discussions[0].original.id ) {
            $scope.replies.push(response);
          }
        });

        /* While controllers are sperated: i.e. not using ngRoutes @@ngRoutes */

        if( $location.path().indexOf("/discussion/")>=0 ) {
          var paths = $location.path().split("/");
          var discussionId = paths[paths.length-1];
          $scope.loadFullDiscussion( discussionId );
        }
      }
    };
  }
]);