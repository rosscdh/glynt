contactObserver = function contactObserver(callbacks, params) {
  var self = this;
  self.q = null;
  self.callBacks = [];
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
  * @param name String
  * @param picture Url
  * @param extra Hash
  * @result void
  */
  self.recieverCallback = function recieverCallback(name, picture, extra) {
    console.log('name:' + name)
    console.log('picture:' + picture)
    console.log('extra:' + extra)
  };

  /** 
  * Method to parse and prepare the query
  * @param q String
  * @result void
  */
  self.queryBase = function queryBase(q) {
    self.q = q;
  };

  /** 
  * Primary query call, accessed externally to start the process
  * @param q String
  * @result void
  */
  self.query = function query(q) {
    // call base
    self.queryBase(q);

    // callbacks
    for (m in self.callBacks) {
      // call watcher callback and supply our callback
      self.callBacks[m](self.q, self.recieverCallback);
    }
    // waiting
    self.waiting();
  };

  // initialize the object
  self.init(callbacks, params);
}