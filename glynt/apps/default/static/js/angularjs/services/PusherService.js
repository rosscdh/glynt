/**
 * @author Lee Sinclair <lee.j.sinclair@gmail.com>
 * @createdDate: 11 Sept 2013
 * @description Service wrapper for the Pusher.com javaSCript API
 */

"use strict";

var AngularPusher;

/* Define 'pusher'
*  Module
*
* Description
*/
angular.module("Pusher", []);

angular.module("Pusher").factory("angularPusher", [ "$q", "$rootScope", 
	function( $q, $rootScope ){
		/**
		 * Returns a new instance of AngularPusher object
		 * @param  {String} key     Pusher KEY
		 * @param  {String} channel Pusher channel name
		 * @param  {Object} scope   The scope to bound data changes to
		 * @param  {String} name    Name of the model
		 * @return {Function}         New instance of Angular Pusher
		 */
		return function( key, channelName, scope, name ) {
			var ap = new AngularPusher( $q, $rootScope, key, channelName );
			return ap;
		}
	}
]);

/**
 * Handles incomming data from remove Pusher service and broadcasts it through the rootScope
 * @param {Function} $q          deferred function (angular function)
 * @param {Function} $rootScope  access to angular root scope
 * @param {String} key         Pusher.com key
 * @param {String} channelName Pusher.com channel ID
 */
AngularPusher = function( $q, $rootScope, key, channelName ) {
	this._pusher = new Pusher(key);
    this._channel = this._pusher.subscribe(channelName);
    this._channel.bind_all(
    	/**
    	 * Catch all pusher events
    	 * @param  {String} event_name Name of the event being sent
    	 * @param  {Object} data       JSON object being transmitted
    	 */
    	function (event_name, data) {
            if ( typeof (data) === 'object' ) {
            	// Convert pusher data into standard data
            	// 1. Fix for project ID
            	if( data.instance && data.instance.project && data.instance.project.pk )
            		data.instance.project = data.instance.project.pk;

            	// 2. Fix for checklist item ID
            	if( data.instance && data.instance.pk ) {
            		data.instance.id = data.instance.pk;
            		delete data.instance.pk;
            	}

            	// Send message to all controllers
            	$rootScope.$broadcast( event_name, data );
            }
        }
    );
};