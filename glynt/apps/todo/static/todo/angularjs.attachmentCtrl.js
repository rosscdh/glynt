/**
 * @description LawPal checklist item GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').controller( 'attachmentCtrl', [ 
	'$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', 'toaster', 'multiProgressService',
	function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location, toaster, multiProgressService ) {
		$scope.deleting = false;

		$scope.close = function() {
			$scope.model.selectedAttachments=[];
		};

		$scope.delete = function( attachment ) {
			$scope.deleting = true;
			lawPalService.deleteAttachment( attachment ).then(
				function() {
					toaster.pop('success', 'attachment deleted');
					$scope.close();
					$scope.attachment.is_deleted = true;
					debugger;
					$scope.deleting = false;
				},
				function error(err) {
					toaster.pop('error', 'unable to delete attachment');
					$scope.deleting = false;
				}
			);
		};
		
}]);