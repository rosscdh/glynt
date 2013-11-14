/**
 * @description LawPal checklist item GUI directives
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */

/**
 * Displays edit and delete buttons
 * @param  {Factory} lawPalUrls Enables access to determine which forms to display
 * @return {Object}            AngularJS directive
 */
lawPalApp.directive('checklistItemActions', [ 'lawPalUrls', function ( lawPalUrls ) {
	'use strict';
	return {
		"restrict": 'A',
		"link": function (scope /*, elem, attrs*/) {
			//var url = attrs["url"];
			var url = lawPalUrls.checklistItemFormUrl( scope.model.project.uuid, scope.item );
			//url = url.replace(":project_uuid", scope.model.project.uuid).replace(":slug", scope.item.slug );

			scope.editUrl = url;
		},/*
		"controller": [ '$scope', '$resource' , 
			function( $scope, $resource ) {

			}
		]*/
		"template": '<span class="on-file-drop-hide"><a tooltip="Delete Item" class="btn btn-small btn-link text-danger item-delete" ng-click="deleteItem(item)"><i class="glyphicon glyphicon-remove text-danger"></i></a>'+
					/*'<a class="btn btn-link item-move"><i class="icon icon-move"></i></a>'+*/
					'<a xhref="{[{editUrl}]}" ng-click="editItem()" title="Edit" data-tooltip="Edit" class="btn btn-small btn-link item-edit"><i class="glyphicon glyphicon-pencil"></i></a></span>'+
					'<button class="on-file-drop-show btn btn-link">Drop file</button>'
	};
}]);

/**
 * Displays checklist item heading
 * @param  {Factory} lawPalUrls Enables access to determine which forms to display
 * @return {Object}            AngularJS directive
 */
lawPalApp.directive('checklistItemLink', [ 'lawPalUrls', function ( lawPalUrls ) {
	'use strict';
	return {
		"restrict": 'A',
		'transclude': true,
		"link": function (scope /*, elem, attrs*/) {
			var url = lawPalUrls.checklistItemDetailUrl( scope.model.project.uuid, scope.item );
			//url = url.replace(":project_uuid", scope.model.project.uuid).replace(":slug", scope.item.slug );

			scope.viewUrl = url;
		},/*
		"controller": [ '$scope' , function( $scope ) {
			$scope.test = alert;
		}
		],*/
		"template": '<h4><a href="{[{viewUrl}]}" ng-bind="item.name"></a></h4>'
	};
}]);

/**
 * Displays associated details about the checklist item such as attachment count
 * @param  {Factory} lawPalUrls Enables access to determine which forms to display
 * @return {Object}            AngularJS directive
 */
lawPalApp.directive('checklistItemDetails', [ 'lawPalUrls', function ( ) {
	'use strict';
	return {
		"restrict": 'A',/*
		"link": function (scope, elem, attrs) {		

		},
		"controller": [ '$scope', '$resource' , function( $scope, $resource ) {

		}
		],*/
		"template": '<a tooltip="{[{item.num_attachments}]} Attachments" class="btn btn-small btn-link" ng-show="item.num_attachments" ng-click="viewItem( item )"><i class="glyphicon glyphicon-file"></i><span class="badge" ng-bind="item.num_attachments"></span></a>'
	};
}]);