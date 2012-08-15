
contactObserver = function contactObserver(callbacks, params) {
  var self = this;
  self.q = null;
  self.resultCallback = null;
  self.callBacks = [];
  self.itemSet = [];
  self.itemSetIds = [];
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
  self.recieverCallback = function recieverCallback(results) {
    // console.log('name:' + name)
    // console.log('picture:' + picture)
    // console.log('extra:' + extra)
    console.log(MD5(self.resultCallback))
    for (r in results) {
      item = results[r];

      if (self.itemSetIds.indexOf(self.resultCallback) == -1) {

        self.itemSet.push({
          'name': item.name,
          'picture': item.picture,
          'extra': item.extra
        });

      };

    }

    self.itemSetIds.push(self.resultCallback);
    // callback to the requestor with the resultset as it currently stands
    self.resultCallback(self.itemSet);
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
  * @param resultCallback Object
  * @result void
  */
  self.query = function query(q,resultCallback) {
    // call base
    self.queryBase(q);
    self.resultCallback = resultCallback;

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