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
      'link': function ( /*scope , elm, attrs*/ ) {
      },
      'controller': function ($scope /*, $element, $attrs*/ ) {
        // Contains the original discussion, it's an array so the we can take advantage of ngAnimate later
        $scope.discussions = [];
        // An array of replies for the current discussion
        $scope.replies = [];

        $scope.close = function () {
          $(".full-dialog-container").fadeOut("slow",
            function() { $scope.discussions = []; }
          );  // To be replaced with ngAnimate when it becomes standard
          $location.path('/');
        };

        $scope.reply = function (discussion) {
          discussionItemService.reply(discussion);
        };

        /**
         * Start the process of showing a full discussion
         * @param  {Object} discussion Discussion object
         */
        function showDiscussion(discussion) {
          $scope.discussions.push(discussion);
          $(".full-dialog-container").hide().fadeIn("slow");  // To be replaced with ngAnimate when it becomes standard
          $location.path('/discussion/' + discussion.original.id);
          $scope.loadFullDiscussion( discussion.original.id );
        }

        /**
         * Start the process of loading the full discussion
         * @param  {Object} discussion Discussion object
         */
        $scope.loadFullDiscussion = function( discussionId ) {
          discussionItemService.load( discussionId, function( err, results){
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
        $scope.$on('discussion-show', function ( evt, discussion ) {
          showDiscussion( discussion );
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
      },
      'template': '<div class="full-dialog-container">' +
        '<div ng-animate="\'animateToaster\'" ng-repeat="discussion in discussions">\n' +
        '<div class="full-dialog-underlay"></div>' +
        // Start: Dialog
        '<div class="full-dialog">' +
        '<div class="container full-dialog-content">\n' +
        '  <div class="clearfix"><button class="close" ng-click="close()">&times</button></div>\n' +
        '  <div class="row" ng-show="discussion.original.title"><div class="col-lg-5 col-offset-3"><h3 ng-bind="discussion.original.title"></h3></div></div>'+
        '  <div class="row clearfix" ng-repeat="reply in replies | orderBy:\'meta.timestamp\':true">\n'+
        // Start: avatar column
        '    <div class="col-lg-2 col-offset-1">\n' +
        '       <div class="fn fn-lg clearfix" user-mini-widget user="reply.meta.user" data-show-props="photo,name"></div>\n' +
        '       <div class="time text-muted">\n' +
        /*'          <i class="icon icon-time"></i>\n' +*/
        '          <small ng-bind="reply.meta.timestamp | timeAgo"></small>\n' +
        '       </div>\n' +
        '    </div>\n' +
        // End: avatar column
        '    <div class="col-lg-6">\n' +
        '       <div class="comment" ng-bind="reply.comment"></div>\n' +
        '    </div>\n' +
        // End: comment column
        '  </div>\n'+
        '  <div class="row clearfix">\n' +
        // Start: avatar column
        '    <div class="col-lg-2 col-offset-1">\n' +
        '       <div class="fn fn-lg clearfix" user-mini-widget user="discussion.original.meta.user" data-show-props="photo,name"></div>\n' +
        '       <div class="time text-muted">\n' +
        /*'          <i class="icon icon-time"></i>\n' +*/
        '          <small ng-bind="discussion.original.meta.timestamp | timeAgo"></small>\n' +
        '       </div>\n' +
        '    </div>\n' +
        // End: avatar column
        '    <div class="col-lg-6">\n' +
        '       <div class="comment" ng-bind="discussion.original.comment"></div>\n' +
        '    </div>\n' +
        // End: comment column
        '  </div>\n' + // .row
        '</div>\n' + // .full-dialog-container
        '</div>' + // .full-dialog
      // End: Dialog
        '<div class="full-dialog-toolbar">\n' +
        '   <div class="container">\n' +
        '       <div class="col-lg-9">\n' +
        '         <button class="btn btn-primary pull-right" ng-click="close()">Close</button>\n' +
        '         <button class="btn btn-info pull-right" ng-click="reply(discussion.original)"><i class="icon icon-reply"></i> Respond</button>\n' +
        '       </div>\n' +
        '   </div>\n' +
        '</div>\n' +
        '</div>' +
        '</div>'
    };
  }
]);