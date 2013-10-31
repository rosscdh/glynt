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
    this.projectUuid = null;
		this.show = function ( discussion, projectUuid ) {
				this.discussion = discussion;
        if( projectUuid ) {
          this.projectUuid = projectUuid;
        }
				$rootScope.$broadcast('discussion-show', discussion, projectUuid);
		};

    /**
     * Load full discussion from API
     * @param  {Number}   discussionId discussion ID
     * @param  {String}   projectUuid  project UUID (optional)
     * @param  {Function} callback     Called back once results are retrieved
     */
    this.load = function( discussionId, projectUuid, callback ) {
      lawPalService.fullDiscussion( discussionId, projectUuid ).then(
        function( results ) {
          callback( null, results );
        }
      );
    };

    /**
     * Open a dialog to add a new discussion
     * @param {String} projectUuid Project UUID (optional) required on pages that have no specifically assigned project
     */
    this.add = function( projectUuid ) {
      this.reply( null, projectUuid );
    };

    /**
     * Open a dialog to reply to a discussion
     * @param  {Object} discussion Parent discussion object
     */
    this.reply = function( discussion, projectUuid ) {
      var modal = this.openDialog( discussion );
      var _this = this;

      if( projectUuid ) {
        this.projectUuid = projectUuid;
      }

      modal.result.then(
          function ok( message ) {
            if( projectUuid ) {
              message.project_uuid = projectUuid;
            }
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

    /**
     * Create reply data object
     * @param  {String} comment          Comment made by someone
     * @param  {Object} parentDiscussion The original discussion
     */
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
        var projectUuid = this.projectUuid || lawPalService.getProjectUuid();
        
        var messageDetails = {
          "object_pk": projectUuid,
          "title": message.subject||"",
          "comment": message.comment,
          "user": userPk,
          "content_type_id": lawPalService.projectContentTypeId(),
          "parent_id": message.parent_id
        };

        lawPalService.addDiscussion( messageDetails, projectUuid ).then(
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