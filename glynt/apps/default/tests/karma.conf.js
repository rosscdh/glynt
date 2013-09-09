// Karma configuration
// Generated on Thu Sep 05 2013 09:50:35 GMT+1000 (EST)

module.exports = function(config) {
  config.set({

    // base path, that will be used to resolve files and exclude
    basePath: '../',


    // frameworks to use
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'static/js/jquery.min.js',
      'static/bootstrap-v3/js/bootstrap.min.js',
      'static/js/sugar-1.3.9.min.js',
      'static/js/angularjs/lib/angular.js',
      'static/js/angularjs/lib/angular-resource.js',
      'static/js/angularjs/lib/ui-bootstrap-tpls-0.5.0.min.js',
      'static/js/angularjs/lib/angular-mocks.js', /* Required for testing */
      'static/js/angularjs/lawpal.app.js',
      'static/js/angularjs/services/LawPalService.js',
      'static/js/angularjs/services/LawPalUrls.js',
      'static/js/angularjs/services/LawPalDialog.js',
      '../todo/static/todo/angularjs.checklistCtrl.js',
      '../todo/static/todo/angularjs.checklistItemCtrl.js',
      '../todo/static/todo/angularjs.checklistItemDirective.js',
      'tests/mvc/**/*Data.js',
      'tests/mvc/**/*Spec.js'
    ],

    // list of files to exclude
    exclude: [
      
    ],


    // test results reporter to use
    // possible values: 'dots', 'progress', 'junit', 'growl', 'coverage'
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera
    // - Safari (only Mac)
    // - PhantomJS
    // - IE (only Windows)
    browsers: ['Chrome'],


    // If browser does not capture in given timeout [ms], kill it
    captureTimeout: 60000,


    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: false
  });
};
