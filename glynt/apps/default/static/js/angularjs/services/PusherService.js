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

AngularPusher = function( $q, $rootScope, key, channelName ) {
	this._q = $q;
	this._rootscope = $rootScope;
	this._initial = true;

	this._key = key;
	this._channel = channelName;
	this._pusher = new Pusher(key);
    this._channel = this._pusher.subscribe(channelName);
    this._channel.bind_all(function (event_name, data) {
            console.log( "Pusher event", event_name, data );
            if ( typeof (data) === 'object' ) {
            	console.log("broadcasting", event_name );
            	// Convert pusher data into standard data
            	if( data.instance && data.instance.project && data.instance.project.pk )
            		data.instance.project = data.instance.project.pk;

            	if( data.instance && data.instance.pk ) {
            		data.instance.id = data.instance.pk;
            		delete data.instance.pk;
            	}

            	$rootScope.$broadcast( event_name, data );
            }

    });
};