/**
 * @description LawPal checklist item GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').controller( 'attachmentCtrl', [
	'$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', 'toaster', '$modal',
	function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location, toaster, $modal ) {
		'use strict';
		$scope.attachModel = {
			'loading': true,
			'deleting': false,
			'feedback': [],
			'feedbackItem': {},
			'has_feedback': false
		};

		$scope.close = function() {
			$scope.model.selectedAttachments=[];
		};

		$scope.delete = function( attachment ) {
			$scope.attachModel.deleting = true;
			lawPalService.deleteAttachment( attachment ).then(
				function() {
					toaster.pop('success', 'attachment deleted');
					$scope.close();
					$scope.attachment.is_deleted = true;
					$scope.attachModel.deleting = false;
				},
				function error(/*err*/) {
					toaster.pop('error', 'unable to delete attachment');
					$scope.attachModel.deleting = false;
				}
			);
		};

		$scope.getFeedback = function( attachment, isResponse ) {
			var feedbackItem = $scope.attachment.feedbackItem;
			var modalInstance = $modal.open({
				"windowClass": "modal modal-show",
				"templateUrl": "template/lawpal/attachment/feedback.html",
				"controller": "feedbackRequestCtrl",
				"animate": false,
				"resolve": {
					"attachment": function(){
						return attachment;
					},
					'feedbackItem': function(){
						return feedbackItem;
					}
				}
			});

			modalInstance.result.then(
				function( data ) {
					$scope.getFeedbackAction( attachment, data, isResponse );
				}
			);
		};

		$scope.getFeedbackAction = function( attachment, feedbackData, isResponse ) {
			var feedbackItem = isResponse?$scope.attachment.feedbackItem:null;
			var comment = feedbackData.comment;
			var status = 0; /*isResponse?3:0;*/ // Set status to 3 is this is a reply
			status = feedbackData.complete?4:status; // if completed set status to 4

			lawPalService.feedbackRequest( attachment, comment, feedbackItem, status ).then(
				function success( /*response*/ ) {
					//console.log( 'response', response );
					toaster.pop("success", "Feedback sent");
				},
				function error( /*err*/ ) {
					//console.log( 'error', err );
					toaster.pop("error", "Unable to send feedback");
				}
			);
		};

		$scope.cancelRequest = function( attachment, comment ) {
			var feedbackItem = $scope.attachment.feedbackItem;
			lawPalService.feedbackRequest( attachment, comment, feedbackItem, 4 ).then(
				function success( /*response*/ ) {
					//console.log( 'response', response );
					toaster.pop("success", "Feedback sent");
				},
				function error( /*err*/ ) {
					//console.log( 'error', err );
					toaster.pop("error", "Unable to send feedback");
				}
			);
		};

		$scope.getFeedbackStatus = function( attachment ) {
			lawPalService.feedbackStatus( attachment ).then(
				function success( response ) {
					console.log( 'response', response );
					if( response.results && response.results.length>0 ) {
						var currentFeedbackItem = response.results[0];
						if(currentFeedbackItem.status<4) {
							$scope.attachment.has_feedback = true;
							$scope.attachment.feedbackItem = currentFeedbackItem;
						}
					}
				},
				function error( err ) {
					console.log( 'error', err );
				}
			);
		};

		//$scope.getFeedbackStatus( $scope.attachment );

		
}]);