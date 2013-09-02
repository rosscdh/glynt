/**
 * @description LawPal API interface
 * @author <a href="mailtolee.j.sinclair@gmail.com">Lee Sinclair</a>
 * Date: 2 Sept 2013
 */
angular.module('lawpal').factory( "lawPalService", [ '$q', '$timeout', '$resource' , function( $q, $timeout, $resource )
	{
		/* Load the LawPal local interface */
		var lawPalInterface = LawPal;
		var userType = "is_customer";
		var checklist = [];

		/* Define API interfaces for check list items */
		var checkListItem = {
			"remove": $resource("/api/v1/todo/:id", {}, { "save": {"method": "PATCH", headers: {'Content-Type': 'application/json'} } } )
		};
		var checkList = { };

		return {
			/**
			 * Returns the list of check list items, ordered by the sort by parameter
			 * @param  {String} 	sortByProperty used to dermine which attribute to sort the data by
			 * @return {Function}   Promise
			 */
			"getChecklist": function( sortByProperty ) {
				// Set up a promise, because this method might retrieve information from the API directly in the future
				var deferred = $q.defer();

				$timeout( function() 
					{
						var checklist = lawPalInterface.checklist_data();
						if(sortByProperty)
							{
								// Sort list
								checklist = checklist.sort( function( item1, item2) {
									return item1[sortByProperty] - item2[sortByProperty];
								});
							}

						if( angular.isArray(checklist) && checklist.length > 0 )
							{
								deferred.resolve(checklist);
							}
						else
							{
								deferred.reject(checklist);
							}
					}, 
					100
				);

				return deferred.promise;
			},

			/**
			 * Get current users profile type
			 * @return {String} "is_lawyer" or "_is_customer"
			 */
			"getUserType": function() {
				if( lawPalInterface.is_lawyer )
					return "is_lawyer";
				else
					return userType;
			},

			/**
			 * Deletes item from checklist
			 * @param  {Object} 	item JSON object representing the check list item to remove
			 * @return {Function}   promise to delete item
			 */
			"deleteItem": function( item ) {
				var deferred = $q.defer();
				var options = { "id": item.id };

				var actionDetails = { "is_deleted":  true };


				checkListItem.remove.save( options, actionDetails, 
					function( results ){
						/* Success */
						deferred.resolve( results );
					}, 
					function( results ){
						/* Error */
						deferred.reject( results );
					}
				);

				return deferred.promise;
			}
		};
	}
]);