/**
 * @description LawPal API interface
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').factory( "lawPalUrls", [ function()
	{
		/* Load the LawPal local interface */
		var lawPalInterface = LawPal;
		var getUrl = (lawPalInterface.getEndpoint?lawPalInterface.getEndpoint():null);

		return {
			"checklistItemDetailUrl": function( projectUuid, item ) {
				if( typeof(getUrl)==="undefined" || !getUrl) return null;

				var url = getUrl( ["checklist", "item", "view"] );
				if( url ) {
					url = url.replace(":project_uuid", projectUuid).replace(":slug", item.slug );

					return url;
				}

				return null;
			},

			"checklistItemCreateFormUrl": function( projectUuid, category ) {
				if( typeof(getUrl)==="undefined" || !getUrl) return null;

				var url = getUrl( ["checklist", "item", "create"] );
				if( url ) {
					category = category.escapeHTML().escapeURL(true);
					url = url.replace(":project_uuid", projectUuid).replace(":categoryLabel", category );

					return url;
				}

				return null;
			},

			"checklistItemFormUrl": function( projectUuid, item ) {
				if( typeof(getUrl)==="undefined" || !getUrl) return null;

				var url = getUrl( ["checklist", "item", "form"] );
				if( url ) {
					url = url.replace(":project_uuid", projectUuid).replace(":slug", item.slug );

					return url;
				}

				return null;
			}
		};
	}
]);