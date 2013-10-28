/*
 * Discussion Item Service
 *   This service is used to share code across project, discussion list widgets and is used to open dialogs, 
 *   and request saves from the API
 * 1. Display a specific discussion in full
 * 2. Respond to a specific discussion
 *
 * Author: Lee Sinclair
 */
 
angular.module('lawpal')
.service('discussionItemService', [ '$rootScope', '$modal', 'lawPalService', 'toaster', function ($rootScope, $modal, lawPalService , toaster) {
  'use strict';
  /**
   * Send a request to display a specific discussion
   * @param  {Object} discussion Discussion object
   */
		this.show = function ( discussion ) {
				this.discussion = discussion;
				$rootScope.$broadcast('discussion-show', discussion);
		};

    this.load = function( discussionId, callback ) {
      lawPalService.fullDiscussion( discussionId ).then(
        function( results ) {
          callback( null, results );
        }
      );
    };

    /**
     * Open a dialog to add a new discussion
     */
    this.add = function() {
      this.reply( null );
    };

    /**
     * Open a dialog to reply to a discussion
     * @param  {Object} discussion Parent discussion object
     */
    this.reply = function( discussion ) {
      var modal = this.openDialog( discussion );
      var _this = this;

      modal.result.then(
          function ok( message ) {
            _this.saveDiscussion( message );
          },
          function cancel() {
          }
        );
    };

    /**
     * Given a parent discussion item open a dialog
     * @param  {Object} parent Parent discussion (can be null if no parent)
     * @return {Object}        Object containing modal functions including result.then
     */
    this.openDialog = function( parent ) {
      var modalInstance = $modal.open({
          "windowClass": "modal modal-show",
          "templateUrl": "template/lawpal/discussion/newDiscussion.html",
          "controller": "newDiscussionDialogCtrl",
          "animate": false,
          "resolve": {
            "parent": function(){
              return parent;
            }
          }
        });

        return modalInstance;
    };

    this.makeReply = function( comment, parentDiscussion ) {
      return {
        "comment": comment,
        "parent_id": parentDiscussion.id,
        "subject": ""
      };
    };

    /**
     * Requests that the API service saves the discussion item
     * @param  {Object} message Message data
     */
    this.saveDiscussion = function( message, callback ) {
        toaster.pop( "info", "Saving" );
        var userPk = lawPalService.getCurrentUser().pk;
        
        var messageDetails = {
          "object_pk": lawPalService.getProjectUuid(),
          "title": message.subject||"",
          "comment": message.comment,
          "user": userPk,
          "content_type_id": lawPalService.projectContentTypeId(),
          "parent_id": message.parent_id
        };

        lawPalService.addDiscussion( messageDetails ).then(
          function success( response ) {
            $rootScope.$broadcast('discussion-new-item', message, response );
            toaster.pop( "success", "Discussion item saved" );
            if( typeof(callback)==="function" ) {
              callback(null, response);
            }
          },
          function error( /*err*/ ) {
            toaster.pop( "warning", "Error", "Unable to post discussion item" );
          }
        );
      };
}]);