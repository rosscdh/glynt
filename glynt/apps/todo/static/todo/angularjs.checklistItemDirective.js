/**
 * 
 */

lawPalApp.directive('checklistItemActions', function () {
	return {
		"restrict": 'C',
		"link": function (scope, elem, attrs) {
			console.log( attrs );
			
			var url = attrs["url"];
			url = url.replace(":project_uuid", scope.model.project.uuid).replace(":slug", scope.item.slug );

			scope.url = url;
		},
		"controller": [ '$scope', '$resource' , function( $scope, $resource ) {
			var options = { 'project_uuid': $scope.model.project.uuid , 'slug': $scope.slug };
			/*
			var options ={ 'project_uuid': $scope.model.project.uuid, 'slug': $scope.slug };
			*/
		}
		],
		"template": '<button href="{[{url}]}" data-toggle="modal" data-target="#modal-checklist-item" data-is_ajax="true" data-target_toggle_object="#item-name-{[{item.slug}]}" title="Edit" data-tooltip="Edit" class="btn btn-small btn-link item-edit"><i class="glyphicon glyphicon-pencil"></i></button>'+
					'<button data-tooltip="Delete Item" class="btn btn-small btn-link text-danger" ng-click="deleteItem(item)"><i class="glyphicon glyphicon-remove text-danger"></i></button>'
	};
});