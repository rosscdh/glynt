function Pusher( key ) {

}

Pusher.prototype.subscribe = function( channelName ) {
	window.mock_Pusher = new bindIt();
	return mock_Pusher;
}

function bindIt() {
	this._callback = null;
}

bindIt.prototype.bind_all = function( callback ) {
	this._callback = callback;
}

bindIt.prototype.send_message = function( eventName, data ) {
	this._callback( eventName, data );
}