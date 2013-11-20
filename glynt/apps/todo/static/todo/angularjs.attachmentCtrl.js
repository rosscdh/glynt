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
			var modalInstance = $modal.open({
				"windowClass": "modal modal-show",
				"templateUrl": "template/lawpal/attachment/feedback.html",
				"controller": "feedbackRequestCtrl",
				"animate": false,
				"resolve": {
					"attachment": function(){
						return attachment;
					}
				}
			});

			modalInstance.result.then(
				function( data ) {
					$scope.getFeedbackAction( attachment, data.comment, isResponse );
				}
			);
		};

		$scope.getFeedbackAction = function( attachment, comment, isResponse ) {
			var feedbackItem = isResponse?$scope.attachModel.feedbackItem:null;
			var status = isResponse?0:3;
			lawPalService.feedbackRequest( attachment, comment, feedbackItem ).then(
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
			var feedbackItem = $scope.attachModel.feedbackItem;
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
						$scope.attachModel.has_feedback = true;
						$scope.attachModel.feedbackItem = response.results[response.results.length-1];
					}
				},
				function error( err ) {
					console.log( 'error', err );
				}
			);
		};

		$scope.getFeedbackStatus( $scope.attachment );
}]);