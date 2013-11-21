/**
 * @description LawPal checklist item GUI controller
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').controller( 'checklistItemCtrl', [ 
	'$scope', 'lawPalService', 'lawPalUrls', 'lawPalDialog', '$location', 'toaster', 'multiProgressService',
	function( $scope, lawPalService, lawPalUrls, lawPalDialog, $location, toaster, multiProgressService ) {
		/**
		 * Removes an item from the checklist
		 * @param  {Object} item JSON object representing a checklist item
		 */
		$scope.deleteItem = function() {
			var item = $scope.item;
			var promise = lawPalService.deleteChecklistItem( item );
			promise.then(
				function( results ) { /* Success */
					$scope.removeItemFromArray( item );
					//$scope.addAlert( "Item removed", "success" );
				},
				function( details ) { /* Error */
					$scope.addAlert( "Unable to remove item", "error" );
				}
			);
		};

		/**
		 * Determines the checklist item status of an item
		 * @return {String} status name
		 */
		$scope.getItemStatus = function() {
			var item = $scope.item;
			switch( item.status )
			{
				case 0: return "new";
				case 1: return "open";
				case 2: return "pending";
				case 3: return "resolved";
				case 4: return "closed";
			}

			return "unknown";
		};

		$scope.pendingFeedback = function() {
			var item = $scope.item;
			var slug = item.slug;

			return $scope.isChecklistItemAssigned(item)?"pending-feedback":"";
			
		};

		/**
		 * Determines the checklist item display status of an item
		 * @return {String} status name for display
		 */
		$scope.getItemDisplayStatus = function() {
			var item = $scope.item;
			switch( item.status )
			{
				case 0: return "New";
				case 1: return "Open";
				case 2: return "Pending";
				case 3: return "Resolved";
				case 4: return "Closed";
			}

			return "Unknown";
		};

		/**
		 * Determine if checklist item is assigned to the current user
		 * @return {Boolean} true if assigned
		 */
		$scope.getAssignedStatus = function() {
			var item = $scope.item;

			return $scope.isChecklistItemAssigned(item);
		};

		/**
		 * Show detail view of checklist item
		 */
		$scope.viewItem = function() {
			var item = $scope.item;
			var url = lawPalUrls.checklistItemDetailUrl( $scope.model.project.uuid, item, true );
			if( url )
				window.location.href = url;
		};

		/**
		 * Incepts the edit process
		 */
		$scope.editItem = function() {
			var item = $scope.item;
			// Get URL to request edit form HTML
			var url = lawPalUrls.checklistItemFormUrl( $scope.model.project.uuid, item );

			// Open edit form + dialog
			lawPalDialog.open( "Edit item", url, item ).then(
				function(result) { /* Success */
					/* Update model */
					if( result && result.name )  {
						item.name = result.name;

						$scope.saveItem( item );
					}
				},
				function(/*result*/) { /* Error */
					/* Update model */
					//console.error(result);
				}
			);
		};

		$scope.setStatusClosed = function( ) {
			var item = $scope.item;
			lawPalService.closeChecklistItem(item).then(
				function success() {
					//console.log('Closed', response);
				},
				function error() {
					//console.log('Error');
				}
			);
		};

		$scope.uploadSelector = function() {
			var data = {
				"project": lawPalService.getProjectId(),
				"todo": $scope.item.id,
				"uploaded_by": { "pk": lawPalService.getCurrentUser().pk }
			};
			filepicker.setKey('A4Ly2eCpkR72XZVBKwJ06z');
			filepicker.pickMultiple({
				'mimetypes': ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-powerpoint', 'application/vnd.ms-excel'],
				'container': 'modal',
				'services':['BOX','COMPUTER','DROPBOX','GITHUB','GOOGLE_DRIVE','GMAIL','URL','FTP','WEBDAV'],
				'multiple': true
			  },
			  function(InkBlob){
				if( InkBlob && angular.isArray(InkBlob) ) {
					angular.forEach( InkBlob, function( ib ){
						lawPalService.localUpload( ib, data, function(/* err, response*/ ) {
							/*console.log("error", err, response );*/
						});
					});
				}
			  },
			  function(FPError){
				console.log(FPError.toString());
			  }
			);
		};

		$scope.onFileSelect = function( files ) {
			var allowedTypes = [ "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-powerpoint", "application/vnd.ms-excel" ];
			files.each( function( file ){
				var fileType = file.type;
				if( fileType && allowedTypes.indexOf(fileType)>=0 ) {
					//toaster.pop("info", "Starting file upload", file.name );
					lawPalService.attachFileChecklistItem( $scope.item, file ).then(
						function success() {
							/* Wait for Pusher confirmation */
						},
						function error(err) {
							toaster.pop("error", "Unable to upload file", file.name );
						}
					);
				} else {
					toaster.pop("error", "File type not allowed", file.name );
				}
			});
		};

		$scope.viewAttachment = function( attachment ) {
			//$("#crocodoc").attr("src", attachment.crocdoc_url);
			$scope.model.selectedAttachments = [];
			attachment.pageHeight = $(window).height() - 150;
			$scope.model.selectedAttachments.push(attachment);
		};

		/**
		 * Recieves messages that an attachment has been added
		 * @param  {Event} e	Broadcast event
		 * @param  {Object} data Data from the update event
		 */
		$scope.$on("todo.attachment.created", function( e, data ){
			$scope.item.attachments = $scope.item.attachments || [];
			//console.log("data:", data.todo, "item:",$scope.item.name, data.instance.name == $scope.item.name);
			//debugger;
			if( typeof(data)==="object" && data.todo == $scope.item.name && !data.processed ) {
				data.processed = true;
				//console.log("incrementing", $scope.item.slug, data.slug );
				$scope.item.num_attachments = $scope.item.num_attachments?$scope.item.num_attachments+1:1;
				toaster.pop("success", data.todo || "Attachment", "attached: " + data.attachment );
				$scope.$apply();

				$scope.reloadHandle = setTimeout( function(){
					$scope.loadAttachments( $scope.item );
				}, 2000);
			}
		});

		$scope.$on("feedbackrequest.opened", function( e, data ) {
			//data.assigned;
			$scope.updateFeedbackStatus( data );
		});

		$scope.$on("feedbackrequest.cancelled", function( e, data ) {
			//data.assigned;
			$scope.updateFeedbackStatus( data );
		});

		$scope.$on("todo.status_change", function( e, data ) {
			//data.assigned;
			$scope.updateFeedbackStatus( data, true );
		});

		$scope.updateFeedbackStatus = function( data, cancel ) {
			var item = $scope.item;
			var attachments = $scope.item.attachments;
			var attachment;
			var feedbackItem;
			// Is the message for this todo item
			if( data.instance.slug === $scope.item.slug ) {
				// Does the filename  match the event data			

					//console.log( data, $scope.attachment );
					attachment = findAttachment( attachments, data.attachment );
					if( attachment) {
						// Update status
						lawPalService.feedbackStatus( attachment ).then(
							function success( response ) {
								if(response.results) {
									for(var i=0;i<response.results.length;i++) {
										feedbackItem = response.results[i];
							
										if(feedbackItem.status<4 && feedbackItem.assigned_to_current_user ) {
											//attachment = findAttachment(feedbackItem);
											if(attachment) {
												attachment.feedbackRequired = true;
												attachment.has_feedback = true;
												attachment.feedbackItem = feedbackItem;
											}
										} else if (feedbackItem.status<4) {
											if(attachment) {
												attachment.has_feedback = true;
												attachment.feedbackRequired = false;
												attachment.feedbackItem = feedbackItem;
											}
										}
									}
								}
							},
							function error(/*err*/) {

							}
						);

						if( cancel ) {
							attachment.feedbackRequired = false;
							attachment.has_feedback = false;
							attachment.feedbackItem = {};
						}
					}
			}
		};

		function findAttachment( attachments, fileName ) {
			if(attachments) {
				for(var j=0;j<attachments.length;j++) {
					if(attachments[j].filename===fileName) {
						return attachments[j];
					}
				}
			}
			
			return null;
		}

}]);