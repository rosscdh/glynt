wordCount = function WordCount(params) {
    self = this;

    self.STATIC_URL = params.STATIC_URL;
    //document.body.innerText.toLowerCase().trim().replace(/[,;.]/g,'').split(/[\s\/]+/g).sort()
    self.sWords = (params.doc == undefined) ? false : params.doc;
    self.iWordsCount = self.sWords.length; // count w/ duplicates
    self.stopWords = [];
    self.result = [];

    // array of words to ignore
    $.getScript(self.STATIC_URL + 'author/js/stopwords.js', function() {
      self.stopWords = (function(){
          var o = {}; // object prop checking > in array checking
          var iCount = stopwords.length;
          for (var i=0;i<iCount;i++){
              o[stopwords[i]] = true;
          }
          return o;
      }());

      self.result = (self.sWords === false) ? false : self.evaluateWords();
    });

    self.prepareDoc = function prepareDoc(data) {
        return data.toLowerCase().trim().replace(/(<([^>]+)>)/gi,'').replace(/(\{\{([\/{1}])?(.+)\}\})/gi,'').replace(/[\,\;\.\[\]\(\)]/ig,'').split(/[\s\/]+/ig).sort();
    };

    self.parseDoc = function parseDoc(doc) {
        self.sWords = self.prepareDoc(doc);
        self.iWordsCount = self.sWords.length;
        self.result = self.evaluateWords();
        return self.result;
    };

    self.evaluateWords = function evaluateWords() {
        var ignore = self.stopWords;

        if (typeof self.sWords != 'object') {
            self.sWords = self.prepareDoc(self.sWords);
        }

        var counts = {}; // object for math
        var arr = []; // an array of objects to return

        for (var i=0; i < self.iWordsCount; i++) {
            var sWord = self.sWords[i];
            if (!ignore[sWord]) {
                counts[sWord] = counts[sWord] || 0;
                counts[sWord]++;
            }
        }
        for (sWord in counts) {
            arr.push({
                text: sWord,
                frequency: counts[sWord]
            });
        };
        return self.sortResult(arr);
    };

    self.sortResult = function sortResult(arr) {
        // sort array by descending frequency | http://stackoverflow.com/a/8837505
        return arr.sort(function(a,b){
            return (a.frequency > b.frequency) ? -1 : ((a.frequency < b.frequency) ? 1 : 0);
        }); 
    };

    self.mostFrequent = function mostFrequent(max) {
        max = (max === undefined) ? self.result.length: max;
        return self.result.slice(0, max)
    };

    self.leastFrequent = function leastFrequent(max) {
        from = (max <= self.result.length) ? (self.result.length - max) : 0;
        return self.result.slice(from, self.result.length)
    };
};