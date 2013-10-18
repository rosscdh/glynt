/**
 * Displays a full page dialog containing an entire discussion exchange
 * 1. requries a tag on the page somewhere
 *   <div class="discussion-viewer-container"></div>
 * 2. Recieves a broadcast message to display a specific discussion item (most likely a parent)
 */
angular.module('lawpal').directive('discussionViewerContainer', ['$compile', '$timeout', 'discussionItemService', '$anchorScroll',
  function ($compile, $timeout, discussionItemService, $anchorScroll) {
    'use strict';
    return {
      'replace': true,
      'restrict': 'EAC',
      'link': function (scope /*, elm, attrs*/ ) {

        function showDiscussion(discussion) {
          scope.discussions.push(discussion);
        }

        scope.discussions = [];

        scope.$on('discussion-show', function ( evt, discussion ) {
          showDiscussion(/*discussionItemService.*/discussion);
          $anchorScroll();
        });
      },
      'controller': function ($scope /*, $element, $attrs*/ ) {

        $scope.close = function () {
          $scope.discussions = [];
        };

        $scope.reply = function (discussion) {
          discussionItemService.reply(discussion);
        };
      },
      'template': '<div class="full-dialog-container">' +
        '<div ng-animate="\'animateToaster\'" ng-repeat="discussion in discussions">\n' +
        '<div class="full-dialog-underlay"></div>' +
      // Start: Dialog
      '<div class="full-dialog">' +
        '<div class="container full-dialog-content">\n' +
        '  <div class="clearfix"><button class="close" ng-click="close()">&times</button></div>\n' +
        '  <div class="row clearfix">\n' +
      // Start: avatar column
      '    <div class="col-lg-2 col-offset-1">\n' +
        '       <div class="fn fn-lg clearfix" user-mini-widget user="discussion.latest.meta.user" data-show-props="photo,name"></div>\n' +
        '       <div class="time text-muted">\n' +
        '          <i class="icon icon-time"></i>\n' +
        '          <small ng-bind="discussion.latest.meta.timestamp | timeAgo"></small>\n' +
        '       </div>\n' +
        '    </div>\n' +
      // End: avatar column
      '    <div class="col-lg-6">\n' +
        '       <div class="comment" ng-bind="discussion.latest.comment"></div>\n' +
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