/**
* Observer to manage callbacks for widgets
* Register an event_name and a callback with the class 
* and then dispatch the event_name and an object which will be inserted into the callback
* i.e.
* observer = argosPanOptia();
* function myCallbackFunction(callback_object) { console.log(callback_object); };
* observer.registerCallback('invitee.add', myCallbackFunction);
* observer.dispatch('invitee.add', {'profile_picture': 'http://monkies.com/the-biggest-one.jpg', 'name': 'Callback Ross', 'email': 'ross@weareml.com'});
* 
* Observer pattern
*/
argosPanOptia = function argosPanOptia() {
  var self = this;

  // dict of events {'<event_name>': [<event callbackFunction>, <event callbackFunction>]}
  self.events = {};
  self.registeredCallbackList = {};

  self.registerEvent = function registerEvent(event_name) {
    if (self.events[event_name] == undefined) {
      self.events[event_name] = [];
    };
  };
  self.deRegisterEvent = function deRegisterEvent(event_name) {
    if (self.events[event_name] != undefined) {
      self.events[event_name] = [];
    };
  };

  self.registerCallback = function registerCallback(event_name, callback) {
    if (self.events[event_name] == undefined) self.registerEvent(event_name);
    var callbackId = MD5(String(callback));
    // allow only 1 instance of each callback in
    if (self.registeredCallbackList[callbackId] == undefined) {
      self.events[event_name].push(callback);
      self.registeredCallbackList[callbackId] = true;
    };
  };

  self.dispatch = function dispatch(event_name, value) {
    var event_callbacks = self.events[event_name];
    if (event_callbacks != undefined && event_callbacks.length > 0) {
      $.each(event_callbacks, function(index, callback){
        eval(callback(value));
      });
    }
  };

};

/**
* ContactsWidget: Allows for multiple contact types to be hooked up (facebook,linkedin,google)
* and managed according to our particular formatting requirements
* Oberserver pattern
*/
contactsWidget = function contactsWidget(callbacks, params) {
  var self = this;
  self.q = null;
  self.resultCallback = null;
  self.callBacks = [];
  self.itemSet = [];
  self.itemSetCallbackIds = [];
  self.params = {
  } + params;

  /** 
  * Initialize the object based on that passed in
  * @param callbacks Hash of javascript callbacks
  * @param params Hash
  * @result void
  */
  self.init = function init(callbacks, params) {
    for (c in callbacks) {
      self.callBacks[c] = callbacks[c];
    }
    for (p in params) {
      self.params[p] = params[p];
    }
  }

  /** 
  * Perform waiting actions
  * @result void
  */
  self.waiting = function waiting() {
  };

  /** 
  * Primary reciever Callback, which will take the data and append it to our list
  * @param results List a list of objects in format {name, picture, extra}
  * @result void
  */
  self.recieverCallback = function recieverCallback(results,callbackId) {
    // console.log('name:' + name)
    // console.log('picture:' + picture)
    // console.log('extra:' + extra)
    for (r in results) {
      item = results[r];
      self.itemSet.push({
        'name': item.name,
        'picture': item.picture,
        'extra': item.extra
      });
    };

    self.itemSetCallbackIds[callbackId] = true;
    // callback to the requestor with the resultset as it currently stands
    self.resultCallback(self.filterItemSet());
  };

  /** 
  * Method to parse and prepare the query
  * @param q String
  * @result void
  */
  self.queryBase = function queryBase(q) {
    self.q = q.toLowerCase();
  };

  /** 
  * Method to provider a filtered set of the local list of contacts
  * @param itemSet List *optional
  * @result List
  */
  self.filterItemSet = function filterItemSet(itemSet) {
    var filterSet = (itemSet == undefined) ? self.itemSet : itemSet ;
    filterSet = $.grep(filterSet, function (a) {
      return a.name.toLowerCase().indexOf(self.q) >= 0;
    });
    return filterSet;
  }
  /** 
  * Primary query call, accessed externally to start the process
  * @param q String
  * @param resultCallback Object
  * @result void
  */
  self.query = function query(q,resultCallback) {
    // call base
    self.queryBase(q);
    self.resultCallback = resultCallback;

    // callbacks
    for (m in self.callBacks) {
      callbackId = MD5(String(self.callBacks[m]));
      if ( self.itemSetCallbackIds.hasOwnProperty(callbackId) == false ) {
        // record this callback being issued
        self.itemSetCallbackIds[callbackId] = false;
        // call watcher callback and supply our callback
        self.callBacks[m](self.q, callbackId, self.recieverCallback);
      } else {
        // default filter
        self.resultCallback(self.filterItemSet());
      };
    }
    // waiting
    self.waiting();
  };

  // initialize the object
  self.init(callbacks, params);
}