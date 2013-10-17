/**
 * This project is a filter for Angularjs to truncate text strings to a set number of characters or words and add ellipses when needed.
 * @author : sparkalow
 * source: https://github.com/sparkalow/angular-truncate
 * Date: Oct 17 2013
 */
/*
 Usage: 
    <p>
        {{ text | characters:25 }} or {{ text | words:5 }}
    </p>
 */
lawPalApp.filter('characters', function () {
        'use strict';
        return function (input, chars, breakOnWord) {
            if (isNaN(chars)) return input;
            if (chars <= 0) return '';
            if (input && input.length >= chars) {
                input = input.substring(0, chars);

                if (!breakOnWord) {
                    var lastspace = input.lastIndexOf(' ');
                    //get last space
                    if (lastspace !== -1) {
                        input = input.substr(0, lastspace);
                    }
                }else{
                    while(input.charAt(input.length-1) == ' '){
                        input = input.substr(0, input.length -1);
                    }
                }
                return input + '...';
            }
            return input;
        };
    })
    .filter('words', function () {
        'use strict';
        return function (input, words) {
            if (isNaN(words)) return input;
            if (words <= 0) return '';
            if (input) {
                var inputWords = input.split(/\s+/);
                if (inputWords.length > words) {
                    input = inputWords.slice(0, words).join(' ') + '...';
                }
            }
            return input;
        };
    });