/**
 * @description Wraps a modal header and footer around a crispy form then invokes Angular.ui dialog 
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 3 Sept 2013
 */
angular.module('lawpal').factory( "lawPalDialog", [ "$q", "$http", "$dialog", function( $q, $http, $dialog )
	{
		return {
			/**
			 * Opens an Angular UI dialog, retrieves a HTML form using XHR, inserts the title and wraps a header and footer around the form
			 * @param  {String} title Title of dialog/form
			 * @param  {String} url   URL of HTML form to retrieve
			 * @return {Function}       promise for completion either save or cancel
			 */
			"open": function( title, url, itemScope ) {
				var deferred = $q.defer();
				var template = '';
				var modalId = 'modal-' + new Date().getTime(); // ModalID is a class, but is also unique. A class is used because there is no method available to set the ID of the modal dialo div

				// Setup header and footer
				var templateHeader = '<div class="modal-dialog"><div class="modal-content">'+
				  '<div class="modal-header">'+
				  '<button ng-click="close(null)" class="close" aria-hidden="true">&times;</button>'+
				  '<h4>{{title}}</h4>'+
				  '</div>'+
				  '<form ng-submit="save(\'.{modalId}\')">'+
				  '<div class="modal-body">';
			   	var templateFooter = '</div>'+
				  '<div class="modal-footer">'+
				  '<input type="button" ng-click="close()" class="btn" value="Cancel" />'+
				  '<input type="submit" value="Save" class="btn btn-primary" />'+
				  '</div>'+
				  '</form>'+
				  '</div></div>';

				 // Configure modal dialog
				var dialogOptions = {
					dialogClass: "modal modal-show " + modalId,
					backdrop: true,
					keyboard: true,
					dialogFade: true,
					backdropClick: true,
					scope: itemScope,
					controller: dialogController
				};

				title = title || "";

				// Retrieve HTML form
				$http.get( url ).success( function( html ) {
					html = html.replace("form>","span>");
					//html = html.replace(/ id=\"id_/g," ng-model=\"");
					//html = html.replace(/ value=\"(.*?)\"/g," ng-init=\"name='{1}'\"");
					
					// Wrap the HTML inside the header and footer
					template = templateHeader + html + templateFooter;
					// Insert title
					dialogOptions.template = template.replace("{{title}}", title);
					dialogOptions.template = dialogOptions.template.replace("{modalId}", modalId);
					dialogOptions.template = dialogOptions.template.replace("data-required=\"true\"", "required data-required");

					// Open dialog
					var d = $dialog.dialog( dialogOptions );
					d.open().then( function(result){ /* Success */
						deferred.resolve( result );
					});

				}).error( function( response ) {
					/* Error unable to load form */
					deferred.reject( response );
				});

				return deferred.promise;
			}
		};
	}
]);